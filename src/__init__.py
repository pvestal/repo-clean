"""
repo-clean: Professional repository cleanup utility

A safety-first tool for cleaning up messy repositories with comprehensive
error handling and educational explanations.
"""

__version__ = "1.0.0"
__author__ = "Patrick Vestal"
__description__ = "Professional repository cleanup utility with safety-first operations"

from .core.scanner import RepositoryScanner
from .core.cleaner import RepositoryCleaner
from .core.reporter import RepositoryReporter
from .utils.safety import SafetyManager
from .utils.explanations import ExplanationEngine

__all__ = [
    "RepositoryScanner",
    "RepositoryCleaner",
    "RepositoryReporter",
    "SafetyManager",
    "ExplanationEngine"
]