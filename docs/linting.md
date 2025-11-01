# Code Quality Linting

repo-clean includes comprehensive linting capabilities that integrate with popular code quality tools across multiple programming ecosystems.

## Overview

The linting system provides:
- **Multi-ecosystem support**: Python, JavaScript/TypeScript, Go, Rust, Java
- **Tool integration**: Works with popular linters (eslint, pylint, prettier, etc.)
- **Auto-fixing**: Automatically fix issues where possible
- **Quality analysis**: Custom quality checks beyond standard linters
- **Unified reporting**: Consistent output across all tools

## Quick Start

```bash
# Auto-detect ecosystems and run all available linters
repo-clean lint

# Lint specific ecosystem
repo-clean lint --ecosystems javascript

# Auto-fix issues
repo-clean lint --fix

# Run specific linters only
repo-clean lint --linters eslint prettier

# Save detailed report
repo-clean lint --format json --output quality-report.json
```

## Supported Ecosystems

### 🐍 Python
**Supported Linters:**
- **pylint** - Comprehensive code analysis
- **flake8** - Style guide enforcement
- **black** - Code formatting
- **mypy** - Static type checking
- **isort** - Import sorting
- **bandit** - Security analysis

**Auto-detection:** `*.py`, `requirements.txt`, `setup.py`, `pyproject.toml`

**Example:**
```bash
# Python-specific linting
repo-clean lint --ecosystems python

# Run specific Python tools
repo-clean lint --linters pylint mypy

# Auto-format Python code
repo-clean lint --linters black --fix
```

### 🟨 JavaScript/TypeScript
**Supported Linters:**
- **eslint** - Code quality and style
- **prettier** - Code formatting
- **jshint** - JavaScript quality
- **tslint** - TypeScript linting (legacy)
- **stylelint** - CSS/SCSS linting

**Auto-detection:** `*.js`, `*.jsx`, `*.ts`, `*.tsx`, `package.json`

**Example:**
```bash
# JavaScript ecosystem linting
repo-clean lint --ecosystems javascript

# Auto-fix ESLint and Prettier issues
repo-clean lint --linters eslint prettier --fix

# TypeScript-specific
repo-clean lint --linters eslint prettier --ecosystems javascript
```

### 🔵 Go
**Supported Linters:**
- **golint** - Go style guide
- **gofmt** - Code formatting
- **go vet** - Static analysis
- **staticcheck** - Advanced analysis

**Auto-detection:** `*.go`, `go.mod`, `go.sum`

### ⚡ Rust
**Supported Linters:**
- **clippy** - Lint collection
- **rustfmt** - Code formatting

**Auto-detection:** `*.rs`, `Cargo.toml`, `Cargo.lock`

### ☕ Java
**Supported Linters:**
- **checkstyle** - Style checking
- **pmd** - Static analysis
- **spotbugs** - Bug detection

**Auto-detection:** `*.java`, `pom.xml`, `build.gradle`

## Command Options

### Basic Usage
```bash
# Scan and lint everything
repo-clean lint

# Preview what would be fixed
repo-clean lint --fix --format json | jq '.[] | select(.fixable == true)'
```

### Ecosystem Selection
```bash
# Specific ecosystems
repo-clean lint --ecosystems python javascript

# All supported ecosystems (explicit)
repo-clean lint --ecosystems python javascript go rust java
```

### Linter Selection
```bash
# Specific linters
repo-clean lint --linters eslint pylint

# Python linters only
repo-clean lint --ecosystems python --linters pylint black mypy

# JavaScript formatters only
repo-clean lint --ecosystems javascript --linters prettier
```

### Auto-fixing
```bash
# Fix all auto-fixable issues
repo-clean lint --fix

# Fix specific linter issues
repo-clean lint --linters black prettier --fix

# Preview fixes without applying
repo-clean lint --fix --format json > preview-fixes.json
```

### Output Formats
```bash
# Human-readable text (default)
repo-clean lint

# Machine-readable JSON
repo-clean lint --format json

# Save to file
repo-clean lint --output quality-report.html --format json
```

## Linting Report Example

```
🔍 Repository Linting Report
==================================================

## Python Ecosystem

  pylint: ⚠️ 23 issues
    💡 Focus on improving pylint score (current: ~7.2/10)
    💡 Run 'pylint --generate-rcfile > .pylintrc' to customize rules

  black: ⚠️ 8 issues
    💡 Run 'black .' to auto-format all Python files
    💡 Add black to pre-commit hooks for consistent formatting

  mypy: ✅ No issues

## JavaScript Ecosystem

  eslint: ⚠️ 15 issues
    💡 Run 'eslint --fix .' to auto-fix many issues
    💡 Consider adding ESLint to your build process

  prettier: ⚠️ 12 issues
    💡 Run 'prettier --write .' to format all files
    💡 Set up IDE integration for automatic formatting

## Custom Quality Checks

  Code Complexity: ⚠️ 3 issues
  File Sizes: ⚠️ 2 issues
  Naming Conventions: ✅ No issues
  Documentation: ⚠️ 1 issue
  Security Patterns: ✅ No issues

## Summary

📊 Total Issues Found: 64
🔧 Moderate issues found - consider addressing systematically.
```

## Custom Quality Checks

Beyond standard linters, repo-clean includes custom quality analysis:

### Code Complexity Analysis
- **Python**: McCabe complexity analysis
- **Threshold**: Functions with complexity > 10
- **Suggestion**: Break down complex functions

### File Size Analysis
- **Threshold**: Files with > 500 lines
- **Suggestion**: Split large files into modules
- **Detection**: All text files (language-aware)

### Naming Convention Compliance
- **Python**: snake_case validation
- **JavaScript**: camelCase validation
- **Detection**: File and variable naming patterns

### Documentation Quality
- **Missing README**: Project documentation
- **Missing LICENSE**: Open source compliance
- **API Documentation**: Code comment coverage

### Basic Security Patterns
- **Hardcoded Secrets**: Password/key detection
- **Patterns**: Common anti-patterns
- **Suggestion**: Environment variable usage

## CI/CD Integration

### GitHub Actions
```yaml
name: Code Quality Linting
on: [push, pull_request]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2

    - name: Setup Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.9'

    - name: Setup Node.js
      uses: actions/setup-node@v2
      with:
        node-version: '16'

    - name: Install repo-clean
      run: pip install repo-clean

    - name: Install linters
      run: |
        pip install pylint black mypy
        npm install -g eslint prettier

    - name: Run linting
      run: |
        repo-clean lint --format json --output quality-report.json

    - name: Upload quality report
      uses: actions/upload-artifact@v2
      with:
        name: quality-report
        path: quality-report.json
```

### Pre-commit Hooks
```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: repo-clean-lint
        name: Repository quality linting
        entry: repo-clean lint --fix
        language: system
        pass_filenames: false
        always_run: true
```

### GitLab CI
```yaml
lint:
  stage: quality
  image: python:3.9
  before_script:
    - pip install repo-clean pylint black
    - apt-get update && apt-get install -y nodejs npm
    - npm install -g eslint prettier
  script:
    - repo-clean lint --format json > quality-report.json
  artifacts:
    reports:
      junit: quality-report.json
    paths:
      - quality-report.json
```

## Configuration

### Project Configuration
```yaml
# .repo-clean.yml
linting:
  ecosystems:
    python:
      enabled: true
      linters: [pylint, black, mypy]
      thresholds:
        pylint_score: 8.0
        complexity: 10

    javascript:
      enabled: true
      linters: [eslint, prettier]
      fix_on_lint: true

  custom_quality:
    max_file_lines: 500
    check_security: true
    check_documentation: true

  output:
    format: text
    show_suggestions: true
    include_custom_checks: true
```

### Global Configuration
```bash
# Set default linting preferences
repo-clean config --global linting.auto_fix true
repo-clean config --global linting.format json
repo-clean config --global linting.ecosystems python,javascript
```

## Linter Installation

### Python Linters
```bash
pip install pylint black mypy flake8 isort bandit
```

### JavaScript Linters
```bash
npm install -g eslint prettier jshint stylelint
# or for TypeScript
npm install -g @typescript-eslint/parser @typescript-eslint/eslint-plugin
```

### Go Linters
```bash
go install golang.org/x/lint/golint@latest
go install honnef.co/go/tools/cmd/staticcheck@latest
```

### Rust Linters
```bash
rustup component add clippy rustfmt
```

### Java Linters
```bash
# Download and configure:
# - Checkstyle: https://checkstyle.sourceforge.io/
# - PMD: https://pmd.github.io/
# - SpotBugs: https://spotbugs.github.io/
```

## Performance Optimization

### Large Repositories
```bash
# Limit scope to changed files
repo-clean lint --files-changed

# Parallel linting
repo-clean lint --workers 4

# Exclude large directories
repo-clean lint --exclude node_modules,dist,build
```

### Incremental Linting
```bash
# Cache results for faster subsequent runs
repo-clean lint --cache

# Lint only modified files (git-aware)
repo-clean lint --git-diff

# Lint specific directories
repo-clean lint src/ tests/
```

## Troubleshooting

### Common Issues

#### Linter Not Found
```bash
❌ Error: eslint not found
💡 Solution: npm install -g eslint
```

#### Configuration Conflicts
```bash
❌ Error: conflicting eslint configurations
💡 Solution: consolidate .eslintrc files or use --config flag
```

#### Performance Issues
```bash
# Skip slow linters
repo-clean lint --exclude-linters mypy

# Limit file scope
repo-clean lint --max-files 100

# Reduce parallel workers
repo-clean lint --workers 1
```

### Debug Mode
```bash
# Verbose linting output
repo-clean lint --verbose

# Debug linter execution
repo-clean lint --debug

# Show exact commands run
repo-clean lint --trace
```

## Best Practices

### 1. Start Small
```bash
# Begin with one ecosystem
repo-clean lint --ecosystems python

# Add more gradually
repo-clean lint --ecosystems python javascript
```

### 2. Use Auto-fix Wisely
```bash
# Preview fixes first
repo-clean lint --format json | grep '"fixable": true'

# Auto-fix safe changes only
repo-clean lint --linters black prettier --fix
```

### 3. Integrate with Development
```bash
# Pre-commit linting
repo-clean lint --fix

# Pre-push validation
repo-clean lint --strict
```

### 4. Team Standards
```bash
# Generate team linting config
repo-clean lint --generate-config > .repo-clean-lint.yml

# Enforce consistent standards
repo-clean lint --config .repo-clean-lint.yml --strict
```

---

**Linting makes repo-clean a complete code quality toolkit - from file hygiene to code standards in one unified tool.**