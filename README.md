# 🧹 repo-clean

**Professional repository cleanup utility for developers and teams**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

Clean up messy repositories with confidence. Remove backup files, fix naming conventions, and establish professional hygiene standards across your codebase.

## 🎯 Why repo-clean?

Every developer has encountered repositories cluttered with:
- `.backup`, `.bak`, `.old` files scattered everywhere
- Files named `ENHANCED_`, `WORKING_`, `FIXED_`, `FINAL_`
- Inconsistent git configurations across team members
- Missing or inadequate `.gitignore` patterns

**repo-clean solves these problems safely and educationally.**

## ✨ Features

### 🔍 **Complete Repository Health Toolkit**
repo-clean is the **only tool** that combines file hygiene, bloat detection, AND comprehensive code quality linting in one unified interface.

### 🔍 **Smart Detection**
- **File Hygiene**: Backup files, naming conventions, git config issues
- **Bloat Detection**: `node_modules`, build artifacts, oversized directories
- **Repository Structure**: Nested repos, directories that should be separate projects
- **Large Files**: Assets that should use Git LFS or external storage
- **Code Quality**: Multi-ecosystem linting (Python, JavaScript, Go, Rust, Java)

### 🧪 **Comprehensive Code Quality Linting**
- **5 Ecosystems**: Python, JavaScript/TypeScript, Go, Rust, Java
- **15+ Linters**: eslint, pylint, prettier, black, mypy, clippy, and more
- **Safe Auto-fixing**: ONLY formatting fixes (prettier, black, gofmt) - NEVER logic changes
- **Custom Analysis**: Complexity, security patterns, documentation quality

### 🛡️ **Safety First**
- **Preview mode**: See exactly what will change before committing
- **Automatic backups**: Creates rollback points before any changes
- **Incremental operations**: Clean one issue type at a time
- **Detailed logging**: Full audit trail of all operations

### 📚 **Educational**
- Explains **why** each issue matters
- Suggests **best practices** for prevention
- Provides **learning resources** for repository hygiene
- Shows **before/after metrics** to demonstrate impact

### 🚀 **Professional Grade**
- Handles large repositories efficiently
- Supports multi-repository operations
- Integrates with CI/CD workflows
- Comprehensive error handling with helpful messages

## 🚀 Quick Start

```bash
# Install
pip install repo-clean

# Scan for issues (safe, read-only)
repo-clean scan

# Preview cleanup (shows what would change)
repo-clean clean --preview

# Clean backup files safely
repo-clean clean --backup-files

# Fix naming conventions
repo-clean rename --interactive

# Run comprehensive code quality linting
repo-clean lint

# Preview what could be safely fixed (recommended first)
repo-clean lint --preview-fixes

# Fix ONLY safe formatting issues (prettier, black, gofmt)
repo-clean lint --fix

# Full health check with recommendations
repo-clean report
```

## 📋 Example Output

```
🔍 Scanning repository for hygiene issues...

✅ Repository: /home/user/my-project
📊 Found 23 issues across 4 categories:

🗂️  Backup Files (15 found)
   ├── src/main.py.backup          [Why: Clutters workspace, confuses IDEs]
   ├── config.json.bak             [Why: Security risk if contains secrets]
   └── workflow.yml.old            [Why: Outdated code can mislead]

🏷️  Naming Issues (5 found)
   ├── ENHANCED_user_service.py    [Why: Non-descriptive, unprofessional]
   ├── WORKING_api_handler.py      [Why: Suggests experimental code]
   └── FIXED_database_utils.py     [Why: Temporary naming became permanent]

💾 Bloat Directories (3 found)
   ├── node_modules/ (847.2MB)     [Why: Should be in .gitignore, slows clones]
   ├── __pycache__/ (23.1MB)       [Why: Generated files, environment-specific]
   └── .pytest_cache/ (5.8MB)      [Why: Test artifacts, should be temporary]

📁 Non-repo Directories (2 found)
   ├── legacy-project/             [Why: Nested .git found, should be submodule]
   └── data-warehouse/             [Why: 2.1GB directory, consider separate repo]

📊 Large Files (4 found)
   ├── assets/demo.mp4 (45.2MB)    [Why: Use Git LFS for media files]
   ├── data/export.zip (12.8MB)    [Why: Archives should use external storage]
   └── models/trained.pkl (156MB)  [Why: ML models should use Git LFS]

🧪 Code Quality (3 ecosystems)
   ├── Python: pylint (23 issues - manual), black (8 issues - 🔧 fixable), mypy ✅
   ├── JavaScript: eslint (15 issues - manual), prettier (12 issues - 🔧 fixable)
   └── Custom: complexity (3 - manual), security patterns ✅

⚙️  Git Config (2 issues)
   ├── user.name: "root"           [Why: Poor attribution, not descriptive]
   └── user.email: missing         [Why: Required for proper attribution]

📄 Gitignore (1 gap)
   └── Missing *.backup* pattern   [Why: Future backup files will be tracked]

💡 Run 'repo-clean clean --preview' to see proposed fixes
🧪 Run 'repo-clean lint --preview-fixes' to see safe formatting fixes available
🔧 Run 'repo-clean lint --fix' for SAFE formatting only (never logic changes)
📚 Run 'repo-clean explain backup-files' to learn more
```

## 📖 Documentation

- [Installation Guide](docs/installation.md)
- [Usage Examples](docs/usage.md)
- [Code Quality Linting](docs/linting.md)
- [Safety Features](docs/safety.md)
- [Error Handling](docs/error-handling.md)
- [Best Practices](docs/best-practices.md)

## 🤝 Contributing

Born from real-world experience cleaning 1,500+ problematic files across 42 production repositories.

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

---

**Built with ❤️ for the developer community**