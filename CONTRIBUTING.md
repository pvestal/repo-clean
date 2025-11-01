# Contributing to repo-clean

Thank you for your interest in contributing to repo-clean! This utility was born from real-world experience cleaning 1,500+ problematic files across 42 production repositories, and we welcome community improvements.

## 🚀 Quick Start

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/your-username/repo-clean.git
   cd repo-clean
   ```
3. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # or
   venv\Scripts\activate     # Windows
   ```
4. **Install in development mode**:
   ```bash
   pip install -e .
   ```

## 🛠️ Development Guidelines

### Code Style
- Follow PEP 8 Python style guidelines
- Use type hints for all functions and methods
- Include comprehensive docstrings with examples
- Maintain the educational and safety-first philosophy

### Architecture Principles
- **Safety First**: All operations must be reversible or have backup mechanisms
- **Educational**: Explain why issues matter, not just what they are
- **Modular Design**: Keep components independent and testable
- **Rich Error Context**: Provide helpful error messages with suggestions

### Key Components
- `src/core/scanner.py` - Issue detection logic
- `src/core/cleaner.py` - Safe cleanup operations
- `src/core/reporter.py` - User-friendly reporting
- `src/utils/safety.py` - Backup and rollback mechanisms
- `src/utils/errors.py` - Error handling framework
- `src/utils/explanations.py` - Educational content

## 🧪 Testing

Run the test suite before submitting changes:

```bash
# Run basic functionality tests
python -m src.main scan --help
python -m src.main clean --help
python -m src.main report --help

# Test on a sample repository
mkdir test-repo && cd test-repo
git init
echo "test" > file.backup
echo "test" > ENHANCED_script.py
cd ..
python -m src.main scan test-repo
```

## 📝 Submitting Changes

1. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-improvement
   ```

2. **Make your changes** following the guidelines above

3. **Test thoroughly** with various repository scenarios

4. **Commit with clear messages**:
   ```bash
   git commit -m "Add support for detecting .tmp backup files"
   ```

5. **Push and create a Pull Request**:
   ```bash
   git push origin feature/your-improvement
   ```

## 🎯 Contribution Ideas

### High Priority
- **New Issue Types**: Additional problematic patterns to detect
- **Language Support**: Extend beyond Python to other ecosystems
- **CI/CD Integration**: GitHub Actions, GitLab CI templates
- **Performance**: Optimize scanning for very large repositories

### Medium Priority
- **Interactive Mode**: Better user experience for selective cleanup
- **Configuration Files**: `.repo-clean.yml` for project-specific rules
- **Metrics Dashboard**: Visual reports of cleanup impact
- **Plugin System**: Allow custom issue detectors

### Documentation
- **Video Tutorials**: Show repo-clean in action
- **Best Practices Guide**: Repository hygiene recommendations
- **Case Studies**: Real-world cleanup examples
- **Integration Examples**: CI/CD workflow configurations

## 🐛 Bug Reports

When reporting bugs, please include:

1. **Environment Details**:
   - Operating system and version
   - Python version
   - repo-clean version (`repo-clean --version`)

2. **Repository Context**:
   - Repository size and structure
   - Git configuration
   - Any special characteristics

3. **Steps to Reproduce**:
   - Exact commands run
   - Expected vs actual behavior
   - Any error messages (full output)

4. **Sample Data** (if possible):
   - Minimal repository structure that reproduces the issue
   - Anonymized file examples

## 💬 Questions and Discussions

- **Issues**: Bug reports and feature requests
- **Discussions**: Architecture questions and ideas
- **Security**: Email security issues privately

## 📜 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Happy Contributing! 🧹✨**

Together we can make repositories cleaner and developers more productive.