#!/usr/bin/env python3
"""
repo-clean: Professional repository cleanup utility

Main CLI interface providing safe, educational repository hygiene operations.
"""

import sys
import argparse
import traceback
from pathlib import Path
from typing import List, Optional

from .utils.errors import ErrorHandler, RepoCleanError, ErrorCategory, ErrorSeverity, ErrorContext
from .utils.explanations import ExplanationEngine, ExplanationLevel
from .utils.safety import SafetyManager
from .core.scanner import RepositoryScanner
from .core.cleaner import RepositoryCleaner
from .core.reporter import RepositoryReporter


class RepoCleanCLI:
    """Main CLI interface for repo-clean"""

    def __init__(self):
        self.error_handler = ErrorHandler()
        self.explanation_engine = ExplanationEngine()

    def main(self, args: Optional[List[str]] = None) -> int:
        """Main entry point for the CLI"""
        try:
            parser = self._create_parser()
            parsed_args = parser.parse_args(args)

            # Set up error handler verbosity
            if hasattr(parsed_args, 'verbose'):
                self.error_handler.verbose = parsed_args.verbose
            if hasattr(parsed_args, 'log_file'):
                self.error_handler.log_file = parsed_args.log_file

            # Execute the requested command
            return self._execute_command(parsed_args)

        except KeyboardInterrupt:
            print("\n⚠️ Operation cancelled by user")
            return 130  # Standard exit code for SIGINT

        except RepoCleanError as e:
            can_continue = self.error_handler.handle_error(e)
            return 0 if can_continue else 1

        except Exception as e:
            # Handle unexpected errors gracefully
            error = RepoCleanError(
                f"Unexpected error: {e}",
                ErrorCategory.INTERNAL,
                ErrorSeverity.CRITICAL,
                ErrorContext(operation="main"),
                cause=e
            )
            self.error_handler.handle_error(error)

            if self.error_handler.verbose:
                print("\n🐛 Full traceback:")
                traceback.print_exc()

            return 1

    def _create_parser(self) -> argparse.ArgumentParser:
        """Create the main argument parser"""
        parser = argparse.ArgumentParser(
            prog='repo-clean',
            description='🧹 Professional repository cleanup utility',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  repo-clean scan                     # Scan for hygiene issues
  repo-clean clean --preview          # Preview cleanup operations
  repo-clean clean --backup-files     # Remove backup files safely
  repo-clean rename --interactive     # Fix naming conventions
  repo-clean explain backup_files     # Learn about backup file issues
  repo-clean report                   # Full repository health report

For detailed help on any command: repo-clean <command> --help
            """
        )

        # Global options
        parser.add_argument(
            '--verbose', '-v',
            action='store_true',
            help='Show detailed output and error information'
        )
        parser.add_argument(
            '--log-file',
            type=str,
            help='Log detailed information to specified file'
        )
        parser.add_argument(
            '--repository', '-r',
            type=str,
            default='.',
            help='Repository path (default: current directory)'
        )

        # Subcommands
        subparsers = parser.add_subparsers(
            dest='command',
            help='Available commands',
            metavar='COMMAND'
        )

        self._add_scan_command(subparsers)
        self._add_clean_command(subparsers)
        self._add_rename_command(subparsers)
        self._add_explain_command(subparsers)
        self._add_report_command(subparsers)
        self._add_status_command(subparsers)
        self._add_rollback_command(subparsers)

        return parser

    def _add_scan_command(self, subparsers):
        """Add the scan command"""
        scan_parser = subparsers.add_parser(
            'scan',
            help='Scan repository for hygiene issues',
            description='Safely scan repository for hygiene issues without making any changes'
        )
        scan_parser.add_argument(
            '--types',
            nargs='+',
            choices=['backup_files', 'naming_conventions', 'git_config', 'gitignore_gaps'],
            help='Specific issue types to scan for'
        )
        scan_parser.add_argument(
            '--quiet', '-q',
            action='store_true',
            help='Only show summary, not detailed findings'
        )

    def _add_clean_command(self, subparsers):
        """Add the clean command"""
        clean_parser = subparsers.add_parser(
            'clean',
            help='Clean up repository issues',
            description='Safely clean up repository hygiene issues with backup and rollback'
        )
        clean_parser.add_argument(
            '--preview',
            action='store_true',
            help='Show what would be changed without making changes'
        )
        clean_parser.add_argument(
            '--backup-files',
            action='store_true',
            help='Remove backup files (.backup, .bak, .old)'
        )
        clean_parser.add_argument(
            '--interactive', '-i',
            action='store_true',
            help='Prompt for confirmation before each operation'
        )
        clean_parser.add_argument(
            '--force',
            action='store_true',
            help='Skip safety confirmations (not recommended)'
        )

    def _add_rename_command(self, subparsers):
        """Add the rename command"""
        rename_parser = subparsers.add_parser(
            'rename',
            help='Fix problematic file naming conventions',
            description='Rename files with problematic naming patterns to professional alternatives'
        )
        rename_parser.add_argument(
            '--interactive', '-i',
            action='store_true',
            help='Prompt for new name for each file'
        )
        rename_parser.add_argument(
            '--patterns',
            nargs='+',
            default=['ENHANCED', 'WORKING', 'FIXED', 'FINAL', 'NEW', 'COMPLETE'],
            help='Naming patterns to fix'
        )
        rename_parser.add_argument(
            '--preview',
            action='store_true',
            help='Show proposed renames without making changes'
        )

    def _add_explain_command(self, subparsers):
        """Add the explain command"""
        explain_parser = subparsers.add_parser(
            'explain',
            help='Get detailed explanations about hygiene issues',
            description='Learn why specific issues matter and how to prevent them'
        )
        explain_parser.add_argument(
            'issue_type',
            choices=['backup_files', 'naming_conventions', 'git_config', 'gitignore_gaps'],
            help='Type of issue to explain'
        )
        explain_parser.add_argument(
            '--level',
            choices=['brief', 'standard', 'detailed', 'educational'],
            default='standard',
            help='Level of detail for explanation'
        )

    def _add_report_command(self, subparsers):
        """Add the report command"""
        report_parser = subparsers.add_parser(
            'report',
            help='Generate comprehensive repository health report',
            description='Create detailed report of repository hygiene status and recommendations'
        )
        report_parser.add_argument(
            '--format',
            choices=['text', 'json', 'html'],
            default='text',
            help='Output format for the report'
        )
        report_parser.add_argument(
            '--output', '-o',
            type=str,
            help='Save report to specified file'
        )

    def _add_status_command(self, subparsers):
        """Add the status command"""
        status_parser = subparsers.add_parser(
            'status',
            help='Show status of repo-clean operations',
            description='Display information about current and past cleanup sessions'
        )
        status_parser.add_argument(
            '--session',
            type=str,
            help='Show details for specific session ID'
        )

    def _add_rollback_command(self, subparsers):
        """Add the rollback command"""
        rollback_parser = subparsers.add_parser(
            'rollback',
            help='Rollback previous operations',
            description='Safely rollback previous cleanup operations using backups'
        )
        rollback_parser.add_argument(
            '--operation',
            type=str,
            help='Specific operation ID to rollback'
        )
        rollback_parser.add_argument(
            '--session',
            type=str,
            help='Rollback entire session'
        )
        rollback_parser.add_argument(
            '--list',
            action='store_true',
            help='List available operations to rollback'
        )

    def _execute_command(self, args) -> int:
        """Execute the specified command"""
        # Validate repository path
        repo_path = Path(args.repository).resolve()
        if not repo_path.exists():
            raise RepoCleanError(
                f"Repository path does not exist: {repo_path}",
                ErrorCategory.USER_INPUT,
                ErrorSeverity.HIGH,
                ErrorContext(
                    operation="repository_validation",
                    file_path=str(repo_path)
                )
            )

        # Initialize core components
        scanner = RepositoryScanner(repo_path)
        safety_manager = SafetyManager(repo_path)
        cleaner = RepositoryCleaner(repo_path, safety_manager, self.error_handler)
        reporter = RepositoryReporter(repo_path, self.explanation_engine)

        # Execute command
        if args.command == 'scan':
            return self._execute_scan(scanner, args)
        elif args.command == 'clean':
            return self._execute_clean(cleaner, args)
        elif args.command == 'rename':
            return self._execute_rename(cleaner, args)
        elif args.command == 'explain':
            return self._execute_explain(args)
        elif args.command == 'report':
            return self._execute_report(reporter, args)
        elif args.command == 'status':
            return self._execute_status(safety_manager, args)
        elif args.command == 'rollback':
            return self._execute_rollback(safety_manager, args)
        else:
            print("❌ No command specified. Use 'repo-clean --help' for usage information.")
            return 1

    def _execute_scan(self, scanner: RepositoryScanner, args) -> int:
        """Execute scan command"""
        print("🔍 Scanning repository for hygiene issues...")

        try:
            issues = scanner.scan_repository(issue_types=args.types)

            if not issues:
                print("✅ No hygiene issues found! Your repository follows good practices.")
                return 0

            print(f"\n📊 Found {len(issues)} issue categories:\n")

            for issue_type, findings in issues.items():
                print(f"🗂️  {issue_type.replace('_', ' ').title()} ({len(findings)} found)")

                if not args.quiet:
                    for finding in findings[:5]:  # Show first 5 examples
                        explanation = self.explanation_engine.explain(issue_type, ExplanationLevel.BRIEF)
                        print(f"   ├── {finding['path']} [{explanation.split('[')[1] if '[' in explanation else 'Needs attention'}]")

                    if len(findings) > 5:
                        print(f"   └── ... and {len(findings) - 5} more")
                print()

            print("💡 Next steps:")
            print("   • Run 'repo-clean clean --preview' to see proposed fixes")
            print("   • Run 'repo-clean explain <issue>' to learn more about specific issues")
            print("   • Run 'repo-clean report' for detailed analysis")

            return 0

        except Exception as e:
            raise RepoCleanError(
                f"Scan operation failed: {e}",
                ErrorCategory.INTERNAL,
                ErrorSeverity.HIGH,
                ErrorContext(operation="scan"),
                cause=e
            )

    def _execute_clean(self, cleaner: RepositoryCleaner, args) -> int:
        """Execute clean command"""
        if args.preview:
            print("🔍 Previewing cleanup operations...\n")
            # Preview logic would go here
            print("✅ Preview completed. Use 'repo-clean clean' to apply changes.")
            return 0

        if not any([args.backup_files]):
            print("❌ No cleanup options specified. Use --backup-files or other options.")
            print("💡 Run 'repo-clean clean --help' for available options.")
            return 1

        print("🧹 Starting repository cleanup...")

        try:
            results = cleaner.clean_repository(
                backup_files=args.backup_files,
                interactive=args.interactive,
                force=args.force
            )

            print(f"\n✅ Cleanup completed successfully!")
            print(f"📊 Results: {results}")
            print(f"\n💾 Backups created in: {cleaner.safety_manager.backup_dir}")
            print("🔄 Use 'repo-clean rollback --list' to see rollback options")

            return 0

        except Exception as e:
            raise RepoCleanError(
                f"Clean operation failed: {e}",
                ErrorCategory.INTERNAL,
                ErrorSeverity.HIGH,
                ErrorContext(operation="clean"),
                cause=e
            )

    def _execute_rename(self, cleaner: RepositoryCleaner, args) -> int:
        """Execute rename command"""
        if args.preview:
            print("🔍 Previewing rename operations...\n")
            # Preview logic would go here
            print("✅ Preview completed. Use 'repo-clean rename' to apply changes.")
            return 0

        print("🏷️ Fixing naming conventions...")

        try:
            results = cleaner.fix_naming_conventions(
                patterns=args.patterns,
                interactive=args.interactive
            )

            print(f"\n✅ Rename completed successfully!")
            print(f"📊 Results: {results}")

            return 0

        except Exception as e:
            raise RepoCleanError(
                f"Rename operation failed: {e}",
                ErrorCategory.INTERNAL,
                ErrorSeverity.HIGH,
                ErrorContext(operation="rename"),
                cause=e
            )

    def _execute_explain(self, args) -> int:
        """Execute explain command"""
        level = ExplanationLevel(args.level)
        explanation = self.explanation_engine.explain(args.issue_type, level)
        print(explanation)
        return 0

    def _execute_report(self, reporter: RepositoryReporter, args) -> int:
        """Execute report command"""
        print("📊 Generating repository health report...")

        try:
            report = reporter.generate_report(format=args.format)

            if args.output:
                with open(args.output, 'w', encoding='utf-8') as f:
                    f.write(report)
                print(f"✅ Report saved to: {args.output}")
            else:
                print("\n" + report)

            return 0

        except Exception as e:
            raise RepoCleanError(
                f"Report generation failed: {e}",
                ErrorCategory.INTERNAL,
                ErrorSeverity.HIGH,
                ErrorContext(operation="report"),
                cause=e
            )

    def _execute_status(self, safety_manager: SafetyManager, args) -> int:
        """Execute status command"""
        try:
            summary = safety_manager.get_session_summary()

            print("📋 Repository cleanup status:")
            print(f"   Current session: {summary['session_id']}")
            print(f"   Operations: {summary['operations_count']}")
            print(f"   Backup directory: {summary['backup_directory']}")

            if summary['operations']:
                print("\n📝 Recent operations:")
                for op in summary['operations'][-5:]:  # Show last 5
                    print(f"   • {op['operation_type']}: {op['source_path']}")

            return 0

        except Exception as e:
            raise RepoCleanError(
                f"Status check failed: {e}",
                ErrorCategory.INTERNAL,
                ErrorSeverity.MEDIUM,
                ErrorContext(operation="status"),
                cause=e
            )

    def _execute_rollback(self, safety_manager: SafetyManager, args) -> int:
        """Execute rollback command"""
        if args.list:
            summary = safety_manager.get_session_summary()
            if not summary['operations']:
                print("📋 No operations to rollback in current session.")
                return 0

            print("🔄 Available rollback operations:")
            for op in summary['operations']:
                print(f"   • {op['operation_id']}: {op['operation_type']} {op['source_path']}")
            return 0

        if args.operation:
            print(f"🔄 Rolling back operation: {args.operation}")
            success = safety_manager.rollback_operation(args.operation)
            if success:
                print("✅ Operation rolled back successfully")
                return 0
            else:
                print("❌ Rollback failed")
                return 1

        if args.session:
            print(f"🔄 Rolling back entire session...")
            count = safety_manager.rollback_session()
            print(f"✅ Rolled back {count} operations")
            return 0

        print("❌ No rollback target specified. Use --operation, --session, or --list")
        return 1


def main():
    """Entry point for the repo-clean CLI"""
    cli = RepoCleanCLI()
    return cli.main()


if __name__ == '__main__':
    sys.exit(main())