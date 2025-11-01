# Installation Guide

## Requirements

- **Python 3.8+** (3.9+ recommended)
- **Git** (for repository operations)
- **Unix-like system** (Linux, macOS, WSL on Windows)

## Quick Install

### From PyPI (Recommended)
```bash
pip install repo-clean
```

### From Source (Development)
```bash
git clone https://github.com/pvestal/repo-clean.git
cd repo-clean
pip install -e .
```

## Verify Installation

```bash
repo-clean --version
repo-clean --help
```

## Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv repo-clean-env

# Activate (Linux/Mac)
source repo-clean-env/bin/activate

# Activate (Windows)
repo-clean-env\Scripts\activate

# Install
pip install repo-clean
```

## System-wide Installation

For system administrators who want repo-clean available to all users:

```bash
sudo pip install repo-clean
```

## Docker Installation

```bash
docker run --rm -v $(pwd):/workspace pvestal/repo-clean scan /workspace
```

## Troubleshooting

### Permission Errors
If you encounter permission errors:
```bash
pip install --user repo-clean
```

### Python Version Issues
Check your Python version:
```bash
python --version
# Should be 3.8 or higher
```

### Path Issues
If `repo-clean` command not found:
```bash
# Add to your shell profile (.bashrc, .zshrc)
export PATH="$HOME/.local/bin:$PATH"
```

## Uninstallation

```bash
pip uninstall repo-clean
```