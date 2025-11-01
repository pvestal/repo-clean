# Error Handling

repo-clean implements comprehensive error handling designed to be educational and helpful rather than cryptic.

## Error Categories

### 1. Permission Errors
**When**: Insufficient permissions to read/write files

```bash
❌ Permission Error: Cannot modify protected file

📁 File: /project/system/config.backup
🔧 Reason: File owned by root, current user lacks write permission
💡 Solution: Run with sudo or change file ownership
📋 Command: sudo chown $(whoami) /project/system/config.backup

🔄 Safe to retry: Yes, after fixing permissions
```

### 2. File System Errors
**When**: Disk space, corrupted files, network drives

```bash
❌ File System Error: Insufficient disk space

📊 Required: 150MB for backup creation
📊 Available: 45MB on /home partition
🔧 Solution: Free up disk space or choose different backup location
💡 Suggestion: Run 'repo-clean clean --no-backup' to skip backup creation

🔄 Recovery: Operation aborted, no files modified
```

### 3. Git Repository Errors
**When**: Invalid git repos, corrupted git state

```bash
❌ Git Error: Not a valid git repository

📁 Directory: /path/to/project
🔧 Reason: No .git directory found
💡 Options:
   1. Initialize git repo: git init
   2. Scan as regular directory: repo-clean scan --no-git
   3. Navigate to correct repository root

🔄 Safe to continue: Yes, with --no-git flag
```

### 4. Configuration Errors
**When**: Invalid config files, missing dependencies

```bash
❌ Configuration Error: Invalid pattern syntax

📄 Config: .repo-clean.yml
🔧 Issue: Invalid regex pattern '*.backup['
💡 Fix: Escape special characters or use glob patterns
📋 Valid: '*.backup' or '.*\.backup$'

🔄 Using defaults: Yes, invalid patterns ignored
```

## Error Recovery

### Automatic Recovery
repo-clean attempts automatic recovery when safe:

```bash
🔄 Auto-recovery: Backup verification failed
📁 Original: /tmp/backup-abc123/file.py
🔧 Action: Re-creating backup with fresh hash
✅ Success: Backup verified, operation proceeding
```

### Manual Recovery
When automatic recovery isn't possible:

```bash
❌ Manual intervention required

🚨 Issue: Conflicting file modifications detected
📁 Files: src/main.py (modified during operation)
🔧 Options:
   1. Abort and review changes: repo-clean abort
   2. Force continue (risk data loss): repo-clean continue --force
   3. Restart operation: repo-clean retry --fresh

💡 Recommendation: Option 1 (abort and review)
```

### Rollback Capability
Every operation can be undone:

```bash
🔄 Operation failed, initiating rollback

📋 Restoring: 5 files from backup abc123
✅ Restored: src/main.py.backup
✅ Restored: config.json.bak
✅ Restored: data/temp.old
✅ Restored: scripts/work.backup
✅ Restored: logs/debug.tmp

🎉 Rollback complete: Repository restored to original state
```

## Error Context

### Rich Error Details
Every error includes comprehensive context:

```json
{
  "error": {
    "type": "PermissionError",
    "category": "file_system",
    "severity": "high",
    "message": "Cannot write to protected directory",
    "context": {
      "file_path": "/protected/config.backup",
      "operation": "backup_creation",
      "user": "patrick",
      "required_permission": "write",
      "current_permission": "read"
    },
    "suggestions": [
      "Run with sudo privileges",
      "Change file ownership",
      "Use --no-backup flag"
    ],
    "recovery_options": [
      "abort_safe",
      "retry_with_sudo",
      "skip_file"
    ]
  }
}
```

### Progressive Disclosure
Errors show appropriate detail levels:

```bash
# Basic user
❌ Cannot clean backup files: Permission denied

# Verbose mode (-v)
❌ Permission Error: Cannot clean backup files
📁 Affected: 3 files in /protected/
🔧 Fix: Run with sudo or change permissions

# Debug mode (-vv)
❌ PermissionError in backup_cleaner.py:45
📁 Files: /protected/file1.backup, /protected/file2.bak, /protected/file3.old
🔍 Details: User 'patrick' (uid=1000) lacks write permission
🔍 Directory: /protected/ (mode=755, owner=root:root)
💡 Solutions: [sudo, chown, chmod, skip]
🔄 Recovery: abort_safe, retry_with_sudo, skip_protected
```

## Error Prevention

### Pre-flight Checks
repo-clean validates conditions before operations:

```bash
🔍 Pre-flight checks...

✅ Git repository: Valid
✅ Disk space: 2.3GB available (need 45MB)
✅ Permissions: Write access confirmed
⚠️  Uncommitted changes: 3 files
❌ Active rebase: Operation would conflict

🛑 Recommendation: Commit changes before cleaning
💡 Override: Use --force-with-uncommitted-changes
```

### Predictive Warnings
Identify potential issues early:

```bash
⚠️  Potential Issues Detected:

📁 Large directory: node_modules/ (1.2GB)
💡 Suggestion: Ensure this is in .gitignore before cleanup

🔗 Symlinks: 3 symbolic links found
💡 Note: Symlink targets will be preserved

🔄 Binary files: 15 executables detected
💡 Warning: Binary files cannot be easily recovered if deleted

Continue? [y/N]
```

## User Experience

### Friendly Error Messages
Technical errors translated to user-friendly language:

```bash
# Technical
errno.ENOSPC: [Errno 28] No space left on device

# User-friendly
❌ Disk Full: Not enough space to create backups

💾 Need: 150MB for safe operation
💾 Available: 12MB on disk
🔧 Quick fix: Delete some files or use external backup location
💡 Alternative: Run without backups (less safe): --no-backup
```

### Interactive Error Resolution
For recoverable errors:

```bash
❌ Permission denied: /system/config.backup

🔧 How would you like to proceed?
1. [S]kip this file and continue
2. [R]etry with sudo privileges
3. [C]hange file permissions
4. [A]bort operation
5. [H]elp - explain options

Choice [S/R/C/A/H]:
```

### Error Learning
repo-clean learns from common errors:

```bash
💡 Tip: This is the 3rd permission error

🎓 Common cause: Running repo-clean on system directories
🔧 Better practice:
   1. Use dedicated user directories
   2. Set up proper file ownership
   3. Consider using Docker for system-wide cleaning

📚 More help: repo-clean docs --permissions
```

## Debugging Support

### Debug Mode
Comprehensive debugging information:

```bash
repo-clean scan --debug

🔍 Debug: Scanner initialized
🔍 Debug: Scanning /home/user/project
🔍 Debug: Found .git directory at /home/user/project/.git
🔍 Debug: Backup patterns: ['*.backup', '*.bak', ...]
🔍 Debug: Checking pattern *.backup
🔍 Debug: glob('*.backup') -> 3 matches
🔍 Debug: Processing file: src/main.py.backup
🔍 Debug: File size: 1,234 bytes
🔍 Debug: Adding to results: backup_files
```

### Trace Mode
Complete operation tracing:

```bash
repo-clean clean --trace

📋 TRACE: Operation started at 2024-01-15 14:30:25
📋 TRACE: Command: clean --backup-files
📋 TRACE: Working directory: /home/user/project
📋 TRACE: User: patrick (uid=1000)
📋 TRACE: Python: 3.9.7, repo-clean: 1.0.0

🔍 TRACE: scanner.scan_backup_files() called
🔍 TRACE: Found 5 backup files
🔍 TRACE: safety_manager.create_backup() called
🔍 TRACE: Backup created: /tmp/repo-clean-backup-abc123
🔍 TRACE: cleaner.delete_file(src/main.py.backup) called
✅ TRACE: File deleted successfully
🔍 TRACE: Operation completed successfully

📋 TRACE: Total time: 0.234 seconds
📋 TRACE: Files processed: 5
📋 TRACE: Errors: 0
```

### Error Reporting
Built-in error reporting for bug reports:

```bash
repo-clean error-report --last

📋 Error Report Generated
📁 Report: /tmp/repo-clean-error-report-20240115.zip
📋 Contains:
   - Error logs and stack traces
   - System information
   - Repository structure (anonymized)
   - Configuration files
   - Operation history

🔒 Privacy: Personal file contents excluded
📧 Submit: Send to github.com/pvestal/repo-clean/issues
```

## Best Practices

### Error Handling in Scripts
```bash
#!/bin/bash

# Check exit codes
if ! repo-clean scan --exit-code; then
    echo "Repository hygiene issues found"
    repo-clean scan --format json > issues.json
    # Handle issues...
fi

# Graceful cleanup
if ! repo-clean clean --backup-files; then
    echo "Cleanup failed, checking for partial completion"
    repo-clean status --last-operation
fi
```

### Automated Error Handling
```yaml
# .repo-clean.yml
error_handling:
  on_permission_error: skip_file
  on_disk_full: abort_safe
  on_git_conflict: abort_with_warning
  backup_location: /external/backup
  max_retries: 3
  retry_delay: 1.0
```

---

**Remember: Every error is an opportunity to learn and improve your repository hygiene practices.**