"""
Repository scanner for detecting hygiene issues
"""

from pathlib import Path
from typing import Dict, List, Optional, Set
import re
import os
import stat


class RepositoryScanner:
    """Scans repositories for hygiene issues"""

    def __init__(self, repository_path: Path):
        self.repository_path = Path(repository_path)

        # Common bloat patterns
        self.bloat_patterns = [
            "node_modules",
            "__pycache__",
            ".pytest_cache",
            ".mypy_cache",
            ".coverage",
            "*.egg-info",
            "dist",
            "build",
            ".tox",
            ".venv",
            "venv",
            "env",
            ".DS_Store",
            "Thumbs.db",
            "*.log",
            "*.tmp",
            "*.cache"
        ]

        # Backup file patterns
        self.backup_patterns = [
            "*.backup",
            "*.bak",
            "*.old",
            "*~",
            "*.orig",
            "*.save",
            "#*#",
            ".#*"
        ]

        # Problematic naming patterns
        self.naming_patterns = [
            "ENHANCED_*",
            "WORKING_*",
            "FIXED_*",
            "FINAL_*",
            "NEW_*",
            "OLD_*",
            "TEMP_*",
            "TEST_*",
            "COPY_*",
            "*_COPY",
            "*_OLD",
            "*_NEW"
        ]

    def scan_repository(self, issue_types: Optional[List[str]] = None) -> Dict[str, List[Dict]]:
        """Scan repository for hygiene issues"""
        results = {}

        # Default to all issue types if none specified
        if issue_types is None:
            issue_types = ["backup_files", "naming_conventions", "bloat_directories", "non_repo_directories", "large_files"]

        if "backup_files" in issue_types:
            results["backup_files"] = self._scan_backup_files()

        if "naming_conventions" in issue_types:
            results["naming_conventions"] = self._scan_naming_issues()

        if "bloat_directories" in issue_types:
            results["bloat_directories"] = self._scan_bloat_directories()

        if "non_repo_directories" in issue_types:
            results["non_repo_directories"] = self._scan_non_repo_directories()

        if "large_files" in issue_types:
            results["large_files"] = self._scan_large_files()

        return results

    def _scan_backup_files(self) -> List[Dict]:
        """Find backup files using pattern matching"""
        backup_files = []

        for pattern in self.backup_patterns:
            for file_path in self.repository_path.rglob(pattern):
                if file_path.is_file():
                    backup_files.append({
                        "path": str(file_path.relative_to(self.repository_path)),
                        "reason": "Backup file clutter",
                        "size": file_path.stat().st_size,
                        "pattern": pattern
                    })

        return backup_files

    def _scan_naming_issues(self) -> List[Dict]:
        """Find files with problematic naming conventions"""
        naming_issues = []

        for pattern in self.naming_patterns:
            for file_path in self.repository_path.rglob(pattern):
                if file_path.is_file():
                    naming_issues.append({
                        "path": str(file_path.relative_to(self.repository_path)),
                        "reason": "Non-descriptive or temporary naming convention",
                        "pattern": pattern,
                        "suggestion": self._suggest_better_name(file_path.name)
                    })

        return naming_issues

    def _scan_bloat_directories(self) -> List[Dict]:
        """Find bloat directories that shouldn't be in repo"""
        bloat_dirs = []

        for pattern in self.bloat_patterns:
            for dir_path in self.repository_path.rglob(pattern):
                if dir_path.is_dir():
                    size = self._get_directory_size(dir_path)
                    bloat_dirs.append({
                        "path": str(dir_path.relative_to(self.repository_path)),
                        "reason": "Bloat directory - should be in .gitignore",
                        "size": size,
                        "size_human": self._format_size(size),
                        "pattern": pattern,
                        "suggestion": "Add to .gitignore and remove from repo"
                    })

        return bloat_dirs

    def _scan_non_repo_directories(self) -> List[Dict]:
        """Find directories that might not belong in a repository"""
        non_repo_dirs = []

        # Check for directories that look like they should be separate repos
        for item in self.repository_path.iterdir():
            if item.is_dir() and item.name not in ['.git', '.github', '.gitlab']:
                # Check if directory has its own .git
                if (item / '.git').exists():
                    non_repo_dirs.append({
                        "path": str(item.relative_to(self.repository_path)),
                        "reason": "Nested git repository - should be separate repo or submodule",
                        "type": "nested_repo",
                        "suggestion": "Move to separate repository or configure as git submodule"
                    })

                # Check for very large directories that might be separate projects
                size = self._get_directory_size(item)
                if size > 100 * 1024 * 1024:  # 100MB
                    file_count = len(list(item.rglob('*')))
                    if file_count > 1000:  # Many files
                        non_repo_dirs.append({
                            "path": str(item.relative_to(self.repository_path)),
                            "reason": "Very large directory - might be separate project",
                            "type": "large_project",
                            "size": size,
                            "size_human": self._format_size(size),
                            "file_count": file_count,
                            "suggestion": "Consider moving to separate repository"
                        })

        return non_repo_dirs

    def _scan_large_files(self) -> List[Dict]:
        """Find unusually large files that might not belong in repo"""
        large_files = []

        for file_path in self.repository_path.rglob('*'):
            if file_path.is_file():
                size = file_path.stat().st_size
                # Flag files over 10MB
                if size > 10 * 1024 * 1024:
                    file_type = self._classify_file_type(file_path)
                    large_files.append({
                        "path": str(file_path.relative_to(self.repository_path)),
                        "reason": f"Large {file_type} file - consider Git LFS or external storage",
                        "size": size,
                        "size_human": self._format_size(size),
                        "type": file_type,
                        "suggestion": self._suggest_large_file_solution(file_path, size)
                    })

        return large_files

    def _get_directory_size(self, directory: Path) -> int:
        """Calculate total size of directory"""
        total_size = 0
        try:
            for file_path in directory.rglob('*'):
                if file_path.is_file():
                    total_size += file_path.stat().st_size
        except (PermissionError, OSError):
            pass
        return total_size

    def _format_size(self, size: int) -> str:
        """Format size in human readable format"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.1f}{unit}"
            size /= 1024
        return f"{size:.1f}TB"

    def _classify_file_type(self, file_path: Path) -> str:
        """Classify file type based on extension"""
        suffix = file_path.suffix.lower()

        if suffix in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg']:
            return 'image'
        elif suffix in ['.mp4', '.avi', '.mov', '.mkv', '.mp3', '.wav']:
            return 'media'
        elif suffix in ['.zip', '.tar', '.gz', '.rar', '.7z']:
            return 'archive'
        elif suffix in ['.pdf', '.doc', '.docx', '.ppt', '.pptx']:
            return 'document'
        elif suffix in ['.bin', '.exe', '.dll', '.so']:
            return 'binary'
        else:
            return 'data'

    def _suggest_large_file_solution(self, file_path: Path, size: int) -> str:
        """Suggest solution for large files"""
        file_type = self._classify_file_type(file_path)

        if file_type in ['image', 'media', 'document']:
            return "Use Git LFS for large media files"
        elif file_type == 'archive':
            return "Extract or move to external storage"
        elif file_type == 'binary':
            return "Use package manager or separate binary repository"
        else:
            return "Consider external storage or Git LFS"

    def _suggest_better_name(self, filename: str) -> str:
        """Suggest better naming for problematic files"""
        # Remove problematic prefixes and suggest alternatives
        for prefix in ['ENHANCED_', 'WORKING_', 'FIXED_', 'FINAL_', 'NEW_', 'OLD_', 'TEMP_', 'TEST_']:
            if filename.startswith(prefix):
                base_name = filename[len(prefix):]
                if prefix in ['ENHANCED_', 'WORKING_']:
                    return f"{base_name} (or add descriptive suffix like _v2, _draft)"
                elif prefix in ['FIXED_', 'FINAL_']:
                    return f"{base_name} (remove temporary prefix)"
                elif prefix in ['NEW_', 'OLD_']:
                    return f"{base_name} (use version control instead)"
                elif prefix in ['TEMP_', 'TEST_']:
                    return f"{base_name} (move to temp/ or tests/ directory)"

        return "Use descriptive, professional naming"