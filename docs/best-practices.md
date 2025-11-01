# Best Practices

## Repository Hygiene Philosophy

### Prevention Over Cleanup
The best hygiene issues are the ones that never occur:

```bash
# Set up your development environment right
echo "*.backup" >> .gitignore
echo "*.bak" >> .gitignore
echo "*.old" >> .gitignore
echo "*~" >> .gitignore

# Configure your IDE to avoid problematic naming
# VS Code: settings.json
{
  "files.autoSave": "off",
  "files.hotExit": "off"
}
```

### Regular Maintenance
Include hygiene checks in your workflow:

```bash
# Weekly hygiene check
repo-clean scan > weekly-hygiene-report.txt

# Pre-commit hygiene
git config hooks.pre-commit "repo-clean scan --exit-code"

# CI/CD integration
repo-clean scan --format json > hygiene-metrics.json
```

## Development Workflow Integration

### Daily Development
```bash
# Morning routine
repo-clean scan --quick

# Before committing
repo-clean scan --exit-code
git add .
git commit -m "Your commit message"

# End of day cleanup
repo-clean clean --backup-files --interactive
```

### Code Review Process
```bash
# Before creating PR
repo-clean report --format html --output pr-hygiene-report.html

# Add to PR template
# ## Hygiene Check
# - [ ] No backup files committed
# - [ ] No problematic naming conventions
# - [ ] Large files use Git LFS
# - [ ] Bloat directories in .gitignore
```

### Team Collaboration
```bash
# Team hygiene standards
repo-clean config --team-mode
repo-clean scan --strict > team-standards.md

# Share configuration
cp .repo-clean.yml .repo-clean-team.yml
git add .repo-clean-team.yml
```

## Git Integration Best Practices

### .gitignore Optimization
```bash
# Generate comprehensive .gitignore
repo-clean gitignore --generate

# Update existing .gitignore
repo-clean gitignore --update --merge

# Validate .gitignore coverage
repo-clean scan --gitignore-gaps
```

### Pre-commit Hooks
```bash
#!/bin/sh
# .git/hooks/pre-commit

echo "Running repository hygiene check..."
if ! repo-clean scan --exit-code --quiet; then
    echo "❌ Hygiene issues found. Run 'repo-clean scan' for details."
    echo "💡 Auto-fix with: repo-clean clean --interactive"
    exit 1
fi

echo "✅ Repository hygiene: Clean"
```

### Git LFS Integration
```bash
# Configure Git LFS for large files
repo-clean lfs-setup

# Migrate existing large files
repo-clean lfs-migrate --files "*.zip,*.tar.gz,*.mp4"

# Monitor LFS usage
repo-clean lfs-report
```

## Project Structure Best Practices

### Directory Organization
```
project/
├── src/                 # Source code
├── tests/              # Test files
├── docs/               # Documentation
├── tools/              # Development tools
├── scripts/            # Utility scripts
├── temp/               # Temporary files (gitignored)
├── archive/            # Old files (separate repo)
└── .repo-clean.yml     # Hygiene configuration
```

### File Naming Conventions
```bash
# Good naming
user_service.py         # Clear, descriptive
api_client_v2.py       # Version indicated properly
data_processor.py      # Purpose obvious

# Avoid these patterns
ENHANCED_user_service.py
WORKING_api_client.py
user_service_FIXED.py
api_client_FINAL.py
```

### Size Management
```bash
# Keep repositories focused
# Single responsibility per repo
# Use submodules for related projects
# Git LFS for large assets

# Monitor size regularly
repo-clean size-report
du -sh .git/
```

## CI/CD Integration

### GitHub Actions
```yaml
name: Repository Hygiene
on: [push, pull_request]

jobs:
  hygiene:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2

    - name: Setup Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.9'

    - name: Install repo-clean
      run: pip install repo-clean

    - name: Hygiene Check
      run: |
        repo-clean scan --exit-code
        repo-clean report --format json > hygiene-report.json

    - name: Upload Report
      uses: actions/upload-artifact@v2
      with:
        name: hygiene-report
        path: hygiene-report.json
```

### GitLab CI
```yaml
stages:
  - hygiene
  - test
  - deploy

hygiene-check:
  stage: hygiene
  image: python:3.9
  before_script:
    - pip install repo-clean
  script:
    - repo-clean scan --exit-code
    - repo-clean report --format json > hygiene-report.json
  artifacts:
    reports:
      junit: hygiene-report.json
    paths:
      - hygiene-report.json
```

### Jenkins Pipeline
```groovy
pipeline {
    agent any

    stages {
        stage('Hygiene Check') {
            steps {
                sh 'pip install repo-clean'
                sh 'repo-clean scan --exit-code'

                script {
                    def report = sh(
                        script: 'repo-clean report --format json',
                        returnStdout: true
                    ).trim()

                    publishHTML([
                        allowMissing: false,
                        alwaysLinkToLastBuild: true,
                        keepAll: true,
                        reportDir: '.',
                        reportFiles: 'hygiene-report.html',
                        reportName: 'Repository Hygiene Report'
                    ])
                }
            }
        }
    }
}
```

## Configuration Management

### Project-specific Configuration
```yaml
# .repo-clean.yml
scan:
  include_hidden: false
  max_file_size: 100MB
  exclude_dirs:
    - node_modules
    - .venv
    - build

patterns:
  backup_files:
    - "*.backup"
    - "*.bak"
    - "*~"

  naming_issues:
    - "ENHANCED_*"
    - "WORKING_*"
    - "TEMP_*"

safety:
  backup_retention: 30  # days
  require_confirmation: true
  respect_git: true

reporting:
  format: "text"
  include_suggestions: true
  show_file_sizes: true
```

### Team Configuration
```yaml
# .repo-clean-team.yml
team:
  strict_mode: true
  enforce_standards: true

standards:
  max_backup_files: 0
  max_large_files: 5
  required_gitignore_patterns:
    - "*.backup"
    - "*.log"
    - "node_modules/"

notifications:
  email_reports: true
  slack_webhook: "https://hooks.slack.com/..."
```

## Performance Optimization

### Large Repository Handling
```bash
# Incremental scanning
repo-clean scan --incremental --cache

# Parallel processing
repo-clean scan --workers 4

# Exclude large directories
repo-clean scan --exclude-dirs "node_modules,venv,.git"

# Limit scope
repo-clean scan --max-depth 3
```

### Memory Management
```bash
# Process files in batches
repo-clean clean --batch-size 100

# Stream large files
repo-clean scan --stream-mode

# Conservative memory usage
repo-clean scan --low-memory
```

## Monitoring and Metrics

### Hygiene Metrics
```bash
# Generate regular metrics
repo-clean metrics --weekly > metrics/week-$(date +%Y%W).json

# Track improvements over time
repo-clean trends --since 3months

# Team dashboard data
repo-clean dashboard-data > /var/www/hygiene-dashboard/data.json
```

### Alerting
```bash
# Alert on hygiene degradation
repo-clean scan --alert-threshold 10 --email admin@company.com

# Slack integration
repo-clean scan --slack-webhook https://hooks.slack.com/...

# Custom alerts
repo-clean scan --format json | jq '.total_issues' | \
  while read count; do
    if [ $count -gt 20 ]; then
      echo "High hygiene issues detected: $count" | \
        mail -s "Repo Hygiene Alert" team@company.com
    fi
  done
```

## Security Considerations

### Sensitive Data Protection
```bash
# Avoid scanning sensitive files
repo-clean scan --exclude-patterns "*secret*,*key*,*password*"

# Secure backup handling
repo-clean clean --secure-delete

# Audit trail
repo-clean audit --all-operations
```

### Access Control
```bash
# User-specific configuration
repo-clean config --user-mode

# Project-level permissions
repo-clean config --project-mode --team-lead-only
```

## Troubleshooting

### Common Issues
```bash
# Permission problems
sudo chown -R $(whoami): .
repo-clean scan

# Git repository issues
git fsck
git gc
repo-clean scan --no-git-validation

# Performance issues
repo-clean scan --exclude-dirs "large_dir1,large_dir2"
repo-clean clean --batch-size 50
```

### Debugging
```bash
# Verbose output
repo-clean scan --verbose

# Debug mode
repo-clean scan --debug

# Trace all operations
repo-clean clean --trace
```

## Automation Scripts

### Weekly Maintenance
```bash
#!/bin/bash
# weekly-hygiene.sh

echo "=== Weekly Repository Hygiene ==="
date

# Scan all projects
for project in ~/projects/*/; do
    echo "Scanning $project"
    cd "$project"

    if repo-clean scan --exit-code; then
        echo "✅ $project: Clean"
    else
        echo "⚠️ $project: Issues found"
        repo-clean clean --backup-files --interactive
    fi
done

# Generate summary report
repo-clean report --all-projects --format html > weekly-report.html
echo "Report generated: weekly-report.html"
```

### Pre-release Checklist
```bash
#!/bin/bash
# pre-release-hygiene.sh

echo "=== Pre-release Hygiene Check ==="

# Strict scanning
if ! repo-clean scan --strict --exit-code; then
    echo "❌ Hygiene issues found - release blocked"
    exit 1
fi

# Size check
if ! repo-clean size-check --max-size 100MB; then
    echo "❌ Repository too large - consider Git LFS"
    exit 1
fi

# Security scan
if ! repo-clean security-scan; then
    echo "❌ Security issues found"
    exit 1
fi

echo "✅ Repository ready for release"
```

---

**Remember: Good hygiene practices compound over time. Start small, be consistent, and gradually improve your standards.**