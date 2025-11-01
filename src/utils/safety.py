"""
Safety-first file operations for repo-clean

Ensures all operations are reversible, logged, and performed with
maximum safety to prevent data loss or repository corruption.
"""

import os
import shutil
import hashlib
import json
import tempfile
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from datetime import datetime
from dataclasses import dataclass, asdict
from .errors import RepoCleanError, ErrorCategory, ErrorSeverity, ErrorContext


@dataclass
class SafetyOperation:
    """Record of a safety operation for rollback purposes"""
    operation_id: str
    operation_type: str  # 'delete', 'rename', 'modify'
    timestamp: str
    source_path: str
    backup_path: Optional[str] = None
    destination_path: Optional[str] = None
    file_hash: Optional[str] = None
    metadata: Dict = None

    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization"""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict) -> 'SafetyOperation':
        """Create from dictionary for JSON deserialization"""
        return cls(**data)


class SafetyManager:
    """Manages safe file operations with backup and rollback capabilities"""

    def __init__(self, repository_path: str, backup_dir: Optional[str] = None):
        self.repository_path = Path(repository_path).resolve()
        self.backup_dir = Path(backup_dir) if backup_dir else self.repository_path / ".repo-clean-backups"
        self.session_id = self._generate_session_id()
        self.operations: List[SafetyOperation] = []
        self.operation_log_path = self.backup_dir / f"session-{self.session_id}.log"

        # Ensure backup directory exists
        self.backup_dir.mkdir(parents=True, exist_ok=True)

        # Initialize operation log
        self._initialize_operation_log()

    def _generate_session_id(self) -> str:
        """Generate unique session ID for this cleanup session"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{timestamp}_{hash(str(self.repository_path)) % 10000:04d}"

    def _initialize_operation_log(self):
        """Initialize the operation log file"""
        log_data = {
            "session_id": self.session_id,
            "repository_path": str(self.repository_path),
            "started_at": datetime.now().isoformat(),
            "operations": []
        }

        try:
            with open(self.operation_log_path, 'w', encoding='utf-8') as f:
                json.dump(log_data, f, indent=2)
        except Exception as e:
            raise RepoCleanError(
                f"Failed to initialize operation log: {e}",
                ErrorCategory.FILESYSTEM,
                ErrorSeverity.CRITICAL,
                ErrorContext(
                    operation="initialize_log",
                    file_path=str(self.operation_log_path)
                ),
                cause=e
            )

    def _calculate_file_hash(self, file_path: Path) -> str:
        """Calculate SHA-256 hash of file for integrity verification"""
        try:
            hash_sha256 = hashlib.sha256()
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_sha256.update(chunk)
            return hash_sha256.hexdigest()
        except Exception as e:
            raise RepoCleanError(
                f"Failed to calculate hash for {file_path}: {e}",
                ErrorCategory.FILESYSTEM,
                ErrorSeverity.MEDIUM,
                ErrorContext(
                    operation="calculate_hash",
                    file_path=str(file_path)
                ),
                cause=e
            )

    def _create_backup(self, source_path: Path) -> Path:
        """Create a backup of a file before modifying it"""
        if not source_path.exists():
            raise RepoCleanError(
                f"Cannot backup non-existent file: {source_path}",
                ErrorCategory.FILESYSTEM,
                ErrorSeverity.HIGH,
                ErrorContext(
                    operation="backup_creation",
                    file_path=str(source_path)
                )
            )

        # Create unique backup filename
        relative_path = source_path.relative_to(self.repository_path)
        backup_filename = f"{self.session_id}_{str(relative_path).replace(os.sep, '_')}"
        backup_path = self.backup_dir / backup_filename

        try:
            # Ensure backup directory structure exists
            backup_path.parent.mkdir(parents=True, exist_ok=True)

            # Copy file to backup location
            shutil.copy2(source_path, backup_path)

            # Verify backup integrity
            original_hash = self._calculate_file_hash(source_path)
            backup_hash = self._calculate_file_hash(backup_path)

            if original_hash != backup_hash:
                raise RepoCleanError(
                    f"Backup verification failed: hash mismatch for {source_path}",
                    ErrorCategory.INTERNAL,
                    ErrorSeverity.CRITICAL,
                    ErrorContext(
                        operation="backup_verification",
                        file_path=str(source_path),
                        expected=original_hash,
                        actual=backup_hash
                    )
                )

            return backup_path

        except Exception as e:
            if isinstance(e, RepoCleanError):
                raise
            raise RepoCleanError(
                f"Failed to create backup for {source_path}: {e}",
                ErrorCategory.FILESYSTEM,
                ErrorSeverity.HIGH,
                ErrorContext(
                    operation="backup_creation",
                    file_path=str(source_path)
                ),
                cause=e
            )

    def _log_operation(self, operation: SafetyOperation):
        """Log an operation to the session log"""
        self.operations.append(operation)

        try:
            # Read current log
            with open(self.operation_log_path, 'r', encoding='utf-8') as f:
                log_data = json.load(f)

            # Add new operation
            log_data["operations"].append(operation.to_dict())
            log_data["last_updated"] = datetime.now().isoformat()

            # Write updated log
            with open(self.operation_log_path, 'w', encoding='utf-8') as f:
                json.dump(log_data, f, indent=2)

        except Exception as e:
            # Don't fail the operation if logging fails, but warn
            print(f"Warning: Failed to log operation: {e}")

    def safe_delete(self, file_path: Path, reason: str = "") -> bool:
        """Safely delete a file with backup and logging"""
        if not file_path.exists():
            return True  # Already deleted

        try:
            # Create backup first
            backup_path = self._create_backup(file_path)
            file_hash = self._calculate_file_hash(file_path)

            # Create operation record
            operation = SafetyOperation(
                operation_id=f"{self.session_id}_{len(self.operations):04d}",
                operation_type="delete",
                timestamp=datetime.now().isoformat(),
                source_path=str(file_path),
                backup_path=str(backup_path),
                file_hash=file_hash,
                metadata={"reason": reason}
            )

            # Perform the deletion
            file_path.unlink()

            # Log the operation
            self._log_operation(operation)

            return True

        except Exception as e:
            if isinstance(e, RepoCleanError):
                raise
            raise RepoCleanError(
                f"Failed to safely delete {file_path}: {e}",
                ErrorCategory.FILESYSTEM,
                ErrorSeverity.HIGH,
                ErrorContext(
                    operation="safe_delete",
                    file_path=str(file_path)
                ),
                cause=e
            )

    def safe_rename(self, source_path: Path, destination_path: Path, reason: str = "") -> bool:
        """Safely rename a file with backup and logging"""
        if not source_path.exists():
            raise RepoCleanError(
                f"Cannot rename non-existent file: {source_path}",
                ErrorCategory.FILESYSTEM,
                ErrorSeverity.HIGH,
                ErrorContext(
                    operation="safe_rename",
                    file_path=str(source_path)
                )
            )

        if destination_path.exists():
            raise RepoCleanError(
                f"Destination already exists: {destination_path}",
                ErrorCategory.FILESYSTEM,
                ErrorSeverity.HIGH,
                ErrorContext(
                    operation="safe_rename",
                    file_path=str(destination_path),
                    suggestions=[
                        "Choose a different destination name",
                        "Remove or rename the existing destination file first",
                        "Use a backup suffix to avoid conflicts"
                    ]
                )
            )

        try:
            # Create backup first
            backup_path = self._create_backup(source_path)
            file_hash = self._calculate_file_hash(source_path)

            # Create operation record
            operation = SafetyOperation(
                operation_id=f"{self.session_id}_{len(self.operations):04d}",
                operation_type="rename",
                timestamp=datetime.now().isoformat(),
                source_path=str(source_path),
                destination_path=str(destination_path),
                backup_path=str(backup_path),
                file_hash=file_hash,
                metadata={"reason": reason}
            )

            # Perform the rename
            source_path.rename(destination_path)

            # Verify the operation
            if not destination_path.exists():
                raise RepoCleanError(
                    f"Rename verification failed: {destination_path} does not exist after rename",
                    ErrorCategory.INTERNAL,
                    ErrorSeverity.CRITICAL,
                    ErrorContext(
                        operation="rename_verification",
                        file_path=str(destination_path)
                    )
                )

            # Log the operation
            self._log_operation(operation)

            return True

        except Exception as e:
            if isinstance(e, RepoCleanError):
                raise
            raise RepoCleanError(
                f"Failed to safely rename {source_path} to {destination_path}: {e}",
                ErrorCategory.FILESYSTEM,
                ErrorSeverity.HIGH,
                ErrorContext(
                    operation="safe_rename",
                    file_path=str(source_path)
                ),
                cause=e
            )

    def rollback_operation(self, operation_id: str) -> bool:
        """Rollback a specific operation"""
        operation = None
        for op in self.operations:
            if op.operation_id == operation_id:
                operation = op
                break

        if not operation:
            raise RepoCleanError(
                f"Operation not found: {operation_id}",
                ErrorCategory.USER_INPUT,
                ErrorSeverity.MEDIUM,
                ErrorContext(
                    operation="rollback",
                    suggestions=[
                        "Check the operation ID is correct",
                        "Use 'repo-clean status' to see available operations",
                        "Ensure you're in the same repository"
                    ]
                )
            )

        try:
            if operation.operation_type == "delete":
                return self._rollback_delete(operation)
            elif operation.operation_type == "rename":
                return self._rollback_rename(operation)
            else:
                raise RepoCleanError(
                    f"Cannot rollback operation type: {operation.operation_type}",
                    ErrorCategory.INTERNAL,
                    ErrorSeverity.MEDIUM,
                    ErrorContext(operation="rollback")
                )

        except Exception as e:
            if isinstance(e, RepoCleanError):
                raise
            raise RepoCleanError(
                f"Failed to rollback operation {operation_id}: {e}",
                ErrorCategory.INTERNAL,
                ErrorSeverity.HIGH,
                ErrorContext(
                    operation="rollback",
                    file_path=operation.source_path
                ),
                cause=e
            )

    def _rollback_delete(self, operation: SafetyOperation) -> bool:
        """Rollback a delete operation by restoring from backup"""
        if not operation.backup_path:
            raise RepoCleanError(
                "No backup available for delete operation rollback",
                ErrorCategory.INTERNAL,
                ErrorSeverity.HIGH,
                ErrorContext(operation="rollback_delete")
            )

        backup_path = Path(operation.backup_path)
        source_path = Path(operation.source_path)

        if not backup_path.exists():
            raise RepoCleanError(
                f"Backup file missing: {backup_path}",
                ErrorCategory.FILESYSTEM,
                ErrorSeverity.HIGH,
                ErrorContext(
                    operation="rollback_delete",
                    file_path=str(backup_path)
                )
            )

        # Restore file from backup
        shutil.copy2(backup_path, source_path)

        # Verify restoration
        if operation.file_hash:
            restored_hash = self._calculate_file_hash(source_path)
            if restored_hash != operation.file_hash:
                raise RepoCleanError(
                    "Rollback verification failed: hash mismatch",
                    ErrorCategory.INTERNAL,
                    ErrorSeverity.CRITICAL,
                    ErrorContext(
                        operation="rollback_verification",
                        expected=operation.file_hash,
                        actual=restored_hash
                    )
                )

        return True

    def _rollback_rename(self, operation: SafetyOperation) -> bool:
        """Rollback a rename operation"""
        if not operation.destination_path:
            raise RepoCleanError(
                "No destination path available for rename rollback",
                ErrorCategory.INTERNAL,
                ErrorSeverity.HIGH,
                ErrorContext(operation="rollback_rename")
            )

        source_path = Path(operation.source_path)
        destination_path = Path(operation.destination_path)

        if not destination_path.exists():
            raise RepoCleanError(
                f"Renamed file missing: {destination_path}",
                ErrorCategory.FILESYSTEM,
                ErrorSeverity.HIGH,
                ErrorContext(
                    operation="rollback_rename",
                    file_path=str(destination_path)
                )
            )

        # Rename back to original
        destination_path.rename(source_path)

        return True

    def rollback_session(self) -> int:
        """Rollback all operations in the current session"""
        rollback_count = 0
        errors = []

        # Rollback in reverse order
        for operation in reversed(self.operations):
            try:
                self.rollback_operation(operation.operation_id)
                rollback_count += 1
            except Exception as e:
                errors.append(f"Failed to rollback {operation.operation_id}: {e}")

        if errors:
            raise RepoCleanError(
                f"Session rollback partially failed. {rollback_count} operations rolled back, {len(errors)} failed",
                ErrorCategory.INTERNAL,
                ErrorSeverity.HIGH,
                ErrorContext(
                    operation="session_rollback",
                    suggestions=[
                        "Check individual operation status",
                        "Manual recovery may be needed for failed operations",
                        "Review backup directory for manual restoration"
                    ]
                )
            )

        return rollback_count

    def get_session_summary(self) -> Dict:
        """Get summary of the current session"""
        return {
            "session_id": self.session_id,
            "repository_path": str(self.repository_path),
            "backup_directory": str(self.backup_dir),
            "operations_count": len(self.operations),
            "operations": [op.to_dict() for op in self.operations],
            "log_file": str(self.operation_log_path)
        }

    def cleanup_old_backups(self, days_old: int = 30) -> int:
        """Clean up backup files older than specified days"""
        if not self.backup_dir.exists():
            return 0

        cleanup_count = 0
        cutoff_time = datetime.now().timestamp() - (days_old * 24 * 60 * 60)

        try:
            for backup_file in self.backup_dir.iterdir():
                if backup_file.is_file() and backup_file.stat().st_mtime < cutoff_time:
                    backup_file.unlink()
                    cleanup_count += 1

        except Exception as e:
            raise RepoCleanError(
                f"Failed to cleanup old backups: {e}",
                ErrorCategory.FILESYSTEM,
                ErrorSeverity.MEDIUM,
                ErrorContext(
                    operation="cleanup_backups",
                    file_path=str(self.backup_dir)
                ),
                cause=e
            )

        return cleanup_count