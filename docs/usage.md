# Usage Examples

## Basic Commands

### Scan (Read-only)
Get an overview of repository hygiene issues:

```bash
# Scan current directory
repo-clean scan

# Scan specific directory
repo-clean scan /path/to/repo

# Scan with specific issue types only
repo-clean scan --issue-types backup_files,naming_conventions
```

### Clean (Modify files)
Clean up issues safely with backups:

```bash
# Preview what would be cleaned (safe, no changes)
repo-clean clean --preview

# Clean backup files only
repo-clean clean --backup-files

# Clean with user confirmation for each file
repo-clean clean --interactive

# Clean everything with automatic backups
repo-clean clean --backup-files --force
```

### Report
Generate comprehensive hygiene reports:

```bash
# Text report
repo-clean report

# JSON report for automation
repo-clean report --format json

# HTML report for sharing
repo-clean report --format html --output report.html
```

### Fix Naming
Rename files to follow conventions:

```bash
# Interactive renaming with suggestions
repo-clean rename --interactive

# Fix specific patterns
repo-clean rename --patterns "ENHANCED_*,WORKING_*,FIXED_*"

# Preview renames without making changes
repo-clean rename --preview
```

## Real-world Examples

### Daily Repository Hygiene
```bash
# Quick health check
repo-clean scan

# Clean backup files safely
repo-clean clean --backup-files --interactive

# Generate weekly team report
repo-clean report --format html --output weekly-hygiene-report.html
```

### CI/CD Integration
```bash
# Fail CI if hygiene issues found
repo-clean scan --exit-code

# Generate metrics for dashboard
repo-clean report --format json > hygiene-metrics.json

# Auto-clean in development branch
if [[ $BRANCH == "development" ]]; then
  repo-clean clean --backup-files --force
fi
```

### Team Onboarding
```bash
# New team member setup
repo-clean scan --explain-all

# Learn about each issue type
repo-clean explain backup-files
repo-clean explain naming-conventions
repo-clean explain git-config
```

### Large Repository Management
```bash
# Multi-repository scanning
for repo in ~/projects/*/; do
  echo "Scanning $repo"
  repo-clean scan "$repo" --format json >> hygiene-summary.json
done

# Batch cleaning with logging
repo-clean clean --backup-files --log-file cleanup-$(date +%Y%m%d).log
```

## Advanced Usage

### Custom Patterns
```bash
# Define custom backup patterns
repo-clean scan --backup-patterns "*.tmp,*.cache,*~"

# Custom naming issue patterns
repo-clean scan --naming-patterns "OLD_*,TEMP_*,DEBUG_*"
```

### Selective Operations
```bash
# Only scan specific file types
repo-clean scan --file-types "*.py,*.js,*.md"

# Exclude directories
repo-clean scan --exclude-dirs "node_modules,venv,.git"

# Include hidden files
repo-clean scan --include-hidden
```

### Output Customization
```bash
# Minimal output
repo-clean scan --quiet

# Verbose output with explanations
repo-clean scan --verbose --explain-all

# Machine-readable output
repo-clean scan --format json --no-color
```

## Safety Features

### Preview Mode
Always preview changes before applying:
```bash
repo-clean clean --preview
```

### Backup Creation
Automatic backups before any destructive operation:
```bash
repo-clean clean --backup-files  # Creates .repo-clean-backup/
```

### Rollback
Undo recent changes:
```bash
repo-clean rollback --last  # Undo last operation
repo-clean rollback --id abc123  # Undo specific operation
```

### Interactive Mode
Confirm each change individually:
```bash
repo-clean clean --interactive
# For each file: (y)es, (n)o, (a)ll, (q)uit
```

## Tips and Best Practices

1. **Always scan first**: `repo-clean scan` before any cleanup
2. **Use preview mode**: `--preview` to see what will change
3. **Start interactive**: `--interactive` for fine-grained control
4. **Regular scanning**: Add to git pre-commit hooks
5. **Team reports**: Generate weekly HTML reports for team review

## Common Workflows

### Personal Development
```bash
# Daily routine
repo-clean scan
repo-clean clean --backup-files --interactive

# Before committing
repo-clean scan --exit-code
```

### Team Maintenance
```bash
# Weekly team review
repo-clean report --format html --output team-hygiene-$(date +%Y%m%d).html

# New project setup
repo-clean scan --explain-all > HYGIENE_GUIDELINES.md
```

### Production Preparation
```bash
# Pre-release cleanup
repo-clean scan --strict
repo-clean clean --backup-files --force
repo-clean report --format json > release-hygiene-report.json
```