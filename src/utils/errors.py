"""
Comprehensive error handling framework for repo-clean

Provides detailed, helpful error messages with suggested solutions
and educational context for all failure scenarios.
"""

import os
import sys
import traceback
from typing import Optional, Dict, List, Any
from enum import Enum
from dataclasses import dataclass


class ErrorCategory(Enum):
    """Categories of errors for better organization and handling"""
    PERMISSION = "permission"
    FILESYSTEM = "filesystem"
    GIT = "git"
    CONFIGURATION = "configuration"
    USER_INPUT = "user_input"
    NETWORK = "network"
    DEPENDENCY = "dependency"
    INTERNAL = "internal"


class ErrorSeverity(Enum):
    """Error severity levels for appropriate user communication"""
    CRITICAL = "critical"     # Cannot continue, immediate attention needed
    HIGH = "high"            # Major issue, significant impact
    MEDIUM = "medium"        # Moderate issue, workaround possible
    LOW = "low"             # Minor issue, informational
    INFO = "info"           # Not an error, just information


@dataclass
class ErrorContext:
    """Rich context information for error handling"""
    operation: str
    file_path: Optional[str] = None
    command: Optional[str] = None
    expected: Optional[str] = None
    actual: Optional[str] = None
    suggestions: List[str] = None
    related_docs: List[str] = None
    safe_to_continue: bool = False


class RepoCleanError(Exception):
    """Base exception for all repo-clean errors with rich context"""

    def __init__(
        self,
        message: str,
        category: ErrorCategory,
        severity: ErrorSeverity,
        context: Optional[ErrorContext] = None,
        cause: Optional[Exception] = None,
        suggestions: Optional[List[str]] = None
    ):
        super().__init__(message)
        self.message = message
        self.category = category
        self.severity = severity
        self.context = context or ErrorContext(operation="unknown")
        self.cause = cause
        self.suggestions = suggestions or []

        # Auto-generate suggestions based on error type
        if not self.suggestions:
            self.suggestions = self._generate_suggestions()

    def _generate_suggestions(self) -> List[str]:
        """Generate helpful suggestions based on error category"""
        suggestions = []

        if self.category == ErrorCategory.PERMISSION:
            suggestions.extend([
                "Check file/directory permissions with 'ls -la'",
                "Ensure you have write access to the repository",
                "Consider running with appropriate user privileges",
                "Verify the repository is not read-only"
            ])

        elif self.category == ErrorCategory.GIT:
            suggestions.extend([
                "Verify you're in a git repository with 'git status'",
                "Check if git is properly installed with 'git --version'",
                "Ensure the repository is not corrupted",
                "Try running 'git fsck' to check repository integrity"
            ])

        elif self.category == ErrorCategory.FILESYSTEM:
            suggestions.extend([
                "Check available disk space with 'df -h'",
                "Verify the path exists and is accessible",
                "Ensure no other processes are locking the files",
                "Check filesystem permissions and mount status"
            ])

        elif self.category == ErrorCategory.CONFIGURATION:
            suggestions.extend([
                "Review your git configuration with 'git config --list'",
                "Check repo-clean configuration file syntax",
                "Verify environment variables are set correctly",
                "Try running with default configuration first"
            ])

        elif self.category == ErrorCategory.USER_INPUT:
            suggestions.extend([
                "Check command syntax with 'repo-clean --help'",
                "Verify file paths are correct and accessible",
                "Ensure required arguments are provided",
                "Try using absolute paths instead of relative"
            ])

        return suggestions


class ErrorHandler:
    """Central error handling with educational explanations"""

    def __init__(self, verbose: bool = False, log_file: Optional[str] = None):
        self.verbose = verbose
        self.log_file = log_file
        self.error_count = 0
        self.warning_count = 0

    def handle_error(self, error: RepoCleanError) -> bool:
        """
        Handle an error with appropriate user communication

        Returns:
            bool: True if operation can continue safely, False if should abort
        """
        self.error_count += 1

        # Format error message for user
        formatted_message = self._format_error_message(error)

        # Display to user based on severity
        if error.severity in [ErrorSeverity.CRITICAL, ErrorSeverity.HIGH]:
            print(f"❌ {formatted_message}", file=sys.stderr)
        else:
            print(f"⚠️  {formatted_message}")

        # Log detailed information if verbose or to log file
        if self.verbose or self.log_file:
            detailed_info = self._get_detailed_error_info(error)
            if self.verbose:
                print(detailed_info)
            if self.log_file:
                self._log_to_file(detailed_info)

        return error.context.safe_to_continue

    def _format_error_message(self, error: RepoCleanError) -> str:
        """Format error message for user-friendly display"""
        lines = [f"Error: {error.message}"]

        # Add context if available
        if error.context.file_path:
            lines.append(f"File: {error.context.file_path}")

        if error.context.operation:
            lines.append(f"Operation: {error.context.operation}")

        # Add suggestions
        if error.suggestions:
            lines.append("\n💡 Suggestions:")
            for suggestion in error.suggestions[:3]:  # Limit to top 3
                lines.append(f"   • {suggestion}")

        # Add helpful hint based on severity
        if error.severity == ErrorSeverity.CRITICAL:
            lines.append("\n🚨 This error prevents repo-clean from continuing safely.")
        elif error.context.safe_to_continue:
            lines.append("\n✅ This issue can be skipped. Continue? (y/n)")

        return "\n".join(lines)

    def _get_detailed_error_info(self, error: RepoCleanError) -> str:
        """Get detailed error information for logging/verbose output"""
        info = [
            f"=== DETAILED ERROR INFORMATION ===",
            f"Category: {error.category.value}",
            f"Severity: {error.severity.value}",
            f"Message: {error.message}",
            f"Operation: {error.context.operation}",
        ]

        if error.context.file_path:
            info.append(f"File Path: {error.context.file_path}")

        if error.context.command:
            info.append(f"Command: {error.context.command}")

        if error.context.expected:
            info.append(f"Expected: {error.context.expected}")

        if error.context.actual:
            info.append(f"Actual: {error.context.actual}")

        if error.cause:
            info.append(f"Underlying Cause: {error.cause}")
            info.append(f"Traceback: {traceback.format_exception(type(error.cause), error.cause, error.cause.__traceback__)}")

        info.append(f"All Suggestions:")
        for i, suggestion in enumerate(error.suggestions, 1):
            info.append(f"  {i}. {suggestion}")

        if error.context.related_docs:
            info.append(f"Related Documentation:")
            for doc in error.context.related_docs:
                info.append(f"  - {doc}")

        return "\n".join(info)

    def _log_to_file(self, message: str):
        """Log detailed error information to file"""
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(f"\n[{self._get_timestamp()}] {message}\n")
        except Exception as e:
            print(f"Warning: Could not write to log file {self.log_file}: {e}")

    def _get_timestamp(self) -> str:
        """Get formatted timestamp for logging"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def get_summary(self) -> str:
        """Get summary of errors encountered"""
        if self.error_count == 0 and self.warning_count == 0:
            return "✅ No errors encountered"

        summary = []
        if self.error_count > 0:
            summary.append(f"❌ {self.error_count} error(s)")
        if self.warning_count > 0:
            summary.append(f"⚠️ {self.warning_count} warning(s)")

        return " | ".join(summary)


# Specific error types for common scenarios
class PermissionError(RepoCleanError):
    """Permission-related errors"""
    def __init__(self, file_path: str, operation: str, cause: Optional[Exception] = None):
        context = ErrorContext(
            operation=operation,
            file_path=file_path,
            suggestions=[
                f"Check permissions: chmod u+w {file_path}",
                "Ensure you own the file or have appropriate access",
                "Verify the file is not being used by another process"
            ]
        )
        super().__init__(
            f"Permission denied accessing {file_path}",
            ErrorCategory.PERMISSION,
            ErrorSeverity.HIGH,
            context,
            cause
        )


class GitRepositoryError(RepoCleanError):
    """Git repository related errors"""
    def __init__(self, path: str, cause: Optional[Exception] = None):
        context = ErrorContext(
            operation="git_detection",
            file_path=path,
            suggestions=[
                "Ensure you're in a git repository",
                "Initialize git with 'git init' if needed",
                "Check if .git directory exists and is readable"
            ]
        )
        super().__init__(
            f"Not a valid git repository: {path}",
            ErrorCategory.GIT,
            ErrorSeverity.CRITICAL,
            context,
            cause
        )


class SafetyCheckError(RepoCleanError):
    """Safety check failures"""
    def __init__(self, check_name: str, details: str):
        context = ErrorContext(
            operation="safety_check",
            expected="safety check to pass",
            actual=f"safety check failed: {details}",
            safe_to_continue=False
        )
        super().__init__(
            f"Safety check '{check_name}' failed: {details}",
            ErrorCategory.INTERNAL,
            ErrorSeverity.CRITICAL,
            context
        )


# Error factory functions for common scenarios
def create_file_not_found_error(file_path: str, operation: str) -> RepoCleanError:
    """Create a file not found error with helpful context"""
    return RepoCleanError(
        f"File not found: {file_path}",
        ErrorCategory.FILESYSTEM,
        ErrorSeverity.MEDIUM,
        ErrorContext(
            operation=operation,
            file_path=file_path,
            suggestions=[
                "Verify the file path is correct",
                "Check if the file was moved or deleted",
                "Use absolute path to avoid confusion",
                "Run 'repo-clean scan' to refresh file list"
            ],
            safe_to_continue=True
        )
    )


def create_backup_creation_error(target_path: str, cause: Exception) -> RepoCleanError:
    """Create a backup creation error"""
    return RepoCleanError(
        f"Failed to create backup for {target_path}",
        ErrorCategory.FILESYSTEM,
        ErrorSeverity.HIGH,
        ErrorContext(
            operation="backup_creation",
            file_path=target_path,
            suggestions=[
                "Check available disk space",
                "Verify write permissions to backup directory",
                "Ensure target file is not locked by another process",
                "Try specifying a different backup location"
            ],
            safe_to_continue=False  # Can't proceed without backup
        ),
        cause
    )