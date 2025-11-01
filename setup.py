#!/usr/bin/env python3
"""
Setup script for repo-clean
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

# Read version from __init__.py
version = {}
with open("src/__init__.py") as fp:
    exec(fp.read(), version)

setup(
    name="repo-clean",
    version=version["__version__"],
    author=version["__author__"],
    author_email="patrick.vestal@gmail.com",
    description=version["__description__"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pvestal/repo-clean",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Version Control :: Git",
        "Topic :: Software Development :: Quality Assurance",
        "Topic :: System :: Systems Administration",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Environment :: Console",
    ],
    python_requires=">=3.8",
    install_requires=[
        # Core dependencies - keeping minimal for broad compatibility
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.8",
            "mypy>=0.800",
        ],
        "test": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "pytest-mock>=3.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "repo-clean=main:main",
        ],
    },
    keywords=[
        "git",
        "repository",
        "cleanup",
        "hygiene",
        "backup-files",
        "naming-conventions",
        "development-tools",
        "code-quality",
        "professional-development",
    ],
    project_urls={
        "Bug Reports": "https://github.com/pvestal/repo-clean/issues",
        "Source": "https://github.com/pvestal/repo-clean",
        "Documentation": "https://github.com/pvestal/repo-clean#readme",
    },
    zip_safe=False,
    include_package_data=True,
)