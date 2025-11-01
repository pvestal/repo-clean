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

### 🔍 **Smart Detection**
- Finds backup files using intelligent pattern matching
- Identifies problematic naming conventions
- Detects git configuration inconsistencies
- Analyzes `.gitignore` coverage gaps

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

⚙️  Git Config (2 issues)
   ├── user.name: "root"           [Why: Poor attribution, not descriptive]
   └── user.email: missing         [Why: Required for proper attribution]

📄 Gitignore (1 gap)
   └── Missing *.backup* pattern   [Why: Future backup files will be tracked]

💡 Run 'repo-clean clean --preview' to see proposed fixes
📚 Run 'repo-clean explain backup-files' to learn more
```

## 📖 Documentation

- [Installation Guide](docs/installation.md)
- [Usage Examples](docs/usage.md)
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