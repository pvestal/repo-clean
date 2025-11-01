# Safety Features

repo-clean prioritizes safety above all else. Every operation is designed to be reversible and transparent.

## Core Safety Principles

### 1. Preview Before Action
**Never modify files without showing you what will change first.**

```bash
# Always see what will happen
repo-clean clean --preview

# Example output:
# 📋 PREVIEW MODE - No files will be modified
#
# Would delete:
#   ✗ src/main.py.backup (143 bytes) - Backup file clutter
#   ✗ config.json.bak (1.2KB) - Contains outdated configuration
#
# Would rename:
#   📝 ENHANCED_service.py → service_enhanced.py
#   📝 WORKING_api.py → api_draft.py
```

### 2. Automatic Backups
**Every destructive operation creates a recovery point.**

```bash
# Backup location
.repo-clean-backup/
├── 2024-01-15_14-30-25/
│   ├── metadata.json         # Operation details
│   ├── file_list.txt        # What was changed
│   └── files/               # Original file contents
│       ├── src/main.py.backup
│       └── config.json.bak
```

### 3. Incremental Operations
**Clean one issue type at a time for maximum control.**

```bash
# Clean only backup files
repo-clean clean --backup-files

# Then clean naming issues separately
repo-clean clean --naming-conventions

# Rather than cleaning everything at once
```

### 4. Interactive Confirmation
**Review and approve each change individually.**

```bash
repo-clean clean --interactive

# Example interaction:
# Delete src/main.py.backup? [y/n/a/q]
#   y = yes, delete this file
#   n = no, skip this file
#   a = yes to all remaining
#   q = quit without further changes
```

## Safety Mechanisms

### Hash Verification
Files are verified using SHA-256 hashes before and after operations:

```python
# Before deletion
original_hash = calculate_sha256(file_path)
create_backup(file_path, original_hash)

# After operation
if backup_exists:
    verify_backup_integrity(backup_path, original_hash)
```

### Atomic Operations
Operations either complete fully or are automatically rolled back:

```bash
# If any file in a batch operation fails:
# 1. Stop immediately
# 2. Restore all previously modified files
# 3. Report exact failure point
# 4. Leave repository in original state
```

### Permission Checking
Verify permissions before attempting any changes:

```python
def safe_delete(file_path):
    if not os.access(file_path, os.W_OK):
        raise PermissionError(f"Cannot write to {file_path}")

    if not os.access(os.path.dirname(file_path), os.W_OK):
        raise PermissionError(f"Cannot modify directory {dirname}")
```

### Git Integration
Respect git status and provide git-aware safety:

```bash
# Check git status before operations
repo-clean clean --respect-git

# Warns about:
# - Uncommitted changes that might be lost
# - Files that would be deleted are staged
# - Operations that might affect git history
```

## Recovery Features

### Rollback Operations
Undo recent changes with full restoration:

```bash
# List recent operations
repo-clean rollback --list

# Rollback last operation
repo-clean rollback --last

# Rollback specific operation by ID
repo-clean rollback --id 2024-01-15_14-30-25

# Rollback with verification
repo-clean rollback --verify --id abc123
```

### Backup Management
Control backup retention and storage:

```bash
# List all backups
repo-clean backup --list

# Clean old backups (keep last 10)
repo-clean backup --clean --keep 10

# Export backup for external storage
repo-clean backup --export --id abc123 --output backup.tar.gz

# Verify backup integrity
repo-clean backup --verify --all
```

### Emergency Recovery
If something goes wrong, emergency recovery options:

```bash
# Restore everything from last backup
repo-clean emergency-restore

# Restore specific files
repo-clean emergency-restore --files "src/main.py,config.json"

# Restore to specific timestamp
repo-clean emergency-restore --timestamp "2024-01-15 14:30"
```

## Safety Configuration

### Safety Levels
Configure safety behavior per project:

```yaml
# .repo-clean.yml
safety:
  level: strict          # strict, normal, minimal
  backup_retention: 30   # days
  require_confirmation: true
  verify_hashes: true
  respect_git: true
```

### Dangerous Operations
Some operations require explicit confirmation:

```bash
# These require --force flag
repo-clean clean --all --force

# These show extra warnings
repo-clean clean --naming-conventions --force
# ⚠️  WARNING: This will rename files, potentially breaking imports
# ⚠️  Ensure your IDE can handle file renames
# ⚠️  Run tests after this operation
```

## Best Practices

### 1. Test in Safe Environment
```bash
# Clone to test directory
git clone /path/to/repo /tmp/repo-test
cd /tmp/repo-test

# Test repo-clean operations
repo-clean scan
repo-clean clean --preview
repo-clean clean --backup-files

# Only then apply to real repository
```

### 2. Use Version Control
```bash
# Commit before major cleanup
git add .
git commit -m "Pre-cleanup snapshot"

# Then clean
repo-clean clean --backup-files

# Review changes
git diff
git status
```

### 3. Regular Backups
```bash
# Weekly backup verification
repo-clean backup --verify --all

# Monthly backup cleanup
repo-clean backup --clean --keep 20

# Before major operations
repo-clean backup --create-checkpoint
```

### 4. Team Safety
```bash
# Generate safety report for team
repo-clean safety-report --output team-safety-guidelines.md

# Team configuration
repo-clean config --team-mode --strict-safety
```

## Error Handling

### Graceful Failures
Operations fail safely with detailed error messages:

```bash
# Example error output:
# ❌ Operation failed: Permission denied
#
# 📁 Affected: /project/protected-file.backup
# 🔧 Suggestion: Run with sudo or change file permissions
# 📋 Recovery: No files were modified, repository unchanged
# 🔄 Retry: Fix permissions and run: repo-clean retry-last
```

### Partial Failures
When batch operations partially fail:

```bash
# 5 files processed successfully
# 1 file failed (permission denied)
#
# ✅ Completed: Files 1-5 cleaned and backed up
# ❌ Failed: File 6 - insufficient permissions
# 🔄 Resume: repo-clean resume --from-failure
```

### Safety Logs
Detailed logging of all safety-related events:

```bash
# Safety log location
~/.repo-clean/safety.log

# Example entries:
# 2024-01-15 14:30:25 [BACKUP] Created backup: abc123
# 2024-01-15 14:30:26 [VERIFY] Hash verified: src/main.py.backup
# 2024-01-15 14:30:27 [DELETE] Safe deletion: src/main.py.backup
# 2024-01-15 14:30:28 [SUCCESS] Operation completed safely
```

## Security Considerations

### File Content Privacy
```bash
# Backups respect sensitive files
repo-clean clean --exclude-sensitive

# Skip files containing credentials
repo-clean clean --skip-patterns "*secret*,*key*,*password*"
```

### Permission Preservation
```bash
# Maintain file permissions
chmod 755 script.py.backup
repo-clean clean --backup-files
# Backup preserves 755 permissions
```

### Secure Deletion
```bash
# Secure deletion of sensitive backups
repo-clean clean --secure-delete --backup-files

# Uses multiple overwrite passes for sensitive files
```

---

**Remember: repo-clean never modifies files without explicit permission and always provides a way back.**