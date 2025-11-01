"""
Repository linter for code quality and standards enforcement
"""

from pathlib import Path
from typing import Dict, List, Optional, Tuple
import json
import subprocess
import re
import ast


class RepositoryLinter:
    """Comprehensive repository linting for code quality and standards"""

    def __init__(self, repository_path: Path):
        self.repository_path = Path(repository_path)

        # Supported linters by ecosystem
        self.linters = {
            'python': {
                'pylint': {'cmd': 'pylint', 'files': '*.py', 'config': '.pylintrc'},
                'flake8': {'cmd': 'flake8', 'files': '*.py', 'config': '.flake8'},
                'black': {'cmd': 'black', 'files': '*.py', 'config': 'pyproject.toml'},
                'mypy': {'cmd': 'mypy', 'files': '*.py', 'config': 'mypy.ini'},
                'isort': {'cmd': 'isort', 'files': '*.py', 'config': '.isort.cfg'},
                'bandit': {'cmd': 'bandit', 'files': '*.py', 'config': '.bandit'},
            },
            'javascript': {
                'eslint': {'cmd': 'eslint', 'files': '*.js,*.jsx,*.ts,*.tsx', 'config': '.eslintrc*'},
                'prettier': {'cmd': 'prettier', 'files': '*.js,*.jsx,*.ts,*.tsx,*.json', 'config': '.prettierrc*'},
                'jshint': {'cmd': 'jshint', 'files': '*.js', 'config': '.jshintrc'},
                'tslint': {'cmd': 'tslint', 'files': '*.ts,*.tsx', 'config': 'tslint.json'},
                'stylelint': {'cmd': 'stylelint', 'files': '*.css,*.scss,*.less', 'config': '.stylelintrc*'},
            },
            'go': {
                'golint': {'cmd': 'golint', 'files': '*.go', 'config': None},
                'gofmt': {'cmd': 'gofmt', 'files': '*.go', 'config': None},
                'go-vet': {'cmd': 'go vet', 'files': '*.go', 'config': None},
                'staticcheck': {'cmd': 'staticcheck', 'files': '*.go', 'config': None},
            },
            'rust': {
                'clippy': {'cmd': 'cargo clippy', 'files': '*.rs', 'config': 'clippy.toml'},
                'rustfmt': {'cmd': 'cargo fmt', 'files': '*.rs', 'config': 'rustfmt.toml'},
            },
            'java': {
                'checkstyle': {'cmd': 'checkstyle', 'files': '*.java', 'config': 'checkstyle.xml'},
                'pmd': {'cmd': 'pmd', 'files': '*.java', 'config': 'pmd.xml'},
                'spotbugs': {'cmd': 'spotbugs', 'files': '*.java', 'config': None},
            }
        }

        # Quality thresholds
        self.quality_thresholds = {
            'python': {'pylint': 8.0, 'complexity': 10, 'line_length': 88},
            'javascript': {'eslint': 0, 'complexity': 15, 'line_length': 100},
            'go': {'golint': 0, 'complexity': 10, 'line_length': 120},
            'rust': {'clippy': 0, 'complexity': 12, 'line_length': 100},
            'java': {'checkstyle': 0, 'complexity': 15, 'line_length': 120}
        }

    def lint_repository(self, ecosystems: Optional[List[str]] = None,
                       linters: Optional[List[str]] = None,
                       fix_mode: bool = False) -> Dict[str, Dict]:
        """Run comprehensive linting across specified ecosystems"""
        results = {}

        # Auto-detect ecosystems if not specified
        if ecosystems is None:
            ecosystems = self._detect_ecosystems()

        for ecosystem in ecosystems:
            if ecosystem not in self.linters:
                continue

            ecosystem_results = {}
            available_linters = self.linters[ecosystem]

            # Filter to specific linters if requested
            if linters:
                available_linters = {k: v for k, v in available_linters.items() if k in linters}

            for linter_name, linter_config in available_linters.items():
                if self._is_linter_available(linter_config['cmd']):
                    linter_result = self._run_linter(
                        ecosystem, linter_name, linter_config, fix_mode
                    )
                    ecosystem_results[linter_name] = linter_result

            if ecosystem_results:
                results[ecosystem] = ecosystem_results

        # Add custom quality checks
        results['custom_quality'] = self._run_custom_quality_checks(ecosystems)

        return results

    def _detect_ecosystems(self) -> List[str]:
        """Auto-detect programming ecosystems in repository"""
        ecosystems = []

        # Check for ecosystem indicators
        indicators = {
            'python': ['*.py', 'requirements.txt', 'setup.py', 'pyproject.toml', 'Pipfile'],
            'javascript': ['*.js', '*.jsx', '*.ts', '*.tsx', 'package.json', 'yarn.lock'],
            'go': ['*.go', 'go.mod', 'go.sum'],
            'rust': ['*.rs', 'Cargo.toml', 'Cargo.lock'],
            'java': ['*.java', 'pom.xml', 'build.gradle', 'gradle.properties']
        }

        for ecosystem, patterns in indicators.items():
            for pattern in patterns:
                if list(self.repository_path.rglob(pattern)):
                    ecosystems.append(ecosystem)
                    break

        return ecosystems

    def _is_linter_available(self, command: str) -> bool:
        """Check if linter is installed and available"""
        try:
            cmd = command.split()[0]  # Get base command
            subprocess.run([cmd, '--version'],
                         capture_output=True,
                         check=True,
                         timeout=5)
            return True
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError):
            return False

    def _run_linter(self, ecosystem: str, linter_name: str,
                   linter_config: Dict, fix_mode: bool) -> Dict:
        """Run individual linter and parse results"""
        result = {
            'available': True,
            'exit_code': 0,
            'issues': [],
            'summary': {},
            'suggestions': []
        }

        try:
            # Build command
            cmd = self._build_linter_command(linter_name, linter_config, fix_mode)

            # Run linter
            process = subprocess.run(
                cmd,
                cwd=self.repository_path,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )

            result['exit_code'] = process.returncode
            result['stdout'] = process.stdout
            result['stderr'] = process.stderr

            # Parse linter output
            issues = self._parse_linter_output(linter_name, process.stdout, process.stderr)
            result['issues'] = issues
            result['summary'] = self._summarize_issues(issues)
            result['suggestions'] = self._generate_suggestions(ecosystem, linter_name, issues)

        except subprocess.TimeoutExpired:
            result['error'] = 'Linter timed out after 5 minutes'
        except Exception as e:
            result['error'] = str(e)

        return result

    def _build_linter_command(self, linter_name: str, linter_config: Dict,
                             fix_mode: bool) -> List[str]:
        """Build linter command with appropriate flags"""
        cmd = linter_config['cmd'].split()

        # Add format flags for machine-readable output
        if linter_name == 'pylint':
            cmd.extend(['--output-format=json'])
        elif linter_name == 'flake8':
            cmd.extend(['--format=json'])
        elif linter_name == 'eslint':
            cmd.extend(['--format=json'])
            if fix_mode:
                cmd.append('--fix')
        elif linter_name == 'prettier':
            if fix_mode:
                cmd.append('--write')
            else:
                cmd.append('--check')

        # Add file patterns
        if linter_config['files']:
            file_patterns = linter_config['files'].split(',')
            for pattern in file_patterns:
                matching_files = list(self.repository_path.rglob(pattern.strip()))
                cmd.extend([str(f) for f in matching_files])

        return cmd

    def _parse_linter_output(self, linter_name: str, stdout: str, stderr: str) -> List[Dict]:
        """Parse linter output into structured issues"""
        issues = []

        try:
            if linter_name in ['pylint', 'eslint'] and stdout:
                # JSON format output
                data = json.loads(stdout)
                if isinstance(data, list):
                    for item in data:
                        issues.append(self._normalize_issue(linter_name, item))
                elif isinstance(data, dict) and 'results' in data:
                    for result in data['results']:
                        issues.append(self._normalize_issue(linter_name, result))

            elif linter_name == 'flake8':
                # Parse flake8 output format
                for line in stdout.splitlines():
                    if ':' in line:
                        issue = self._parse_flake8_line(line)
                        if issue:
                            issues.append(issue)

            else:
                # Generic parsing for other linters
                for line in stdout.splitlines():
                    if line.strip():
                        issues.append({
                            'file': 'unknown',
                            'line': 0,
                            'column': 0,
                            'severity': 'info',
                            'message': line.strip(),
                            'rule': 'generic'
                        })

        except json.JSONDecodeError:
            # Fallback to text parsing
            issues.append({
                'file': 'parse_error',
                'line': 0,
                'column': 0,
                'severity': 'error',
                'message': 'Failed to parse linter output',
                'raw_output': stdout[:500]
            })

        return issues

    def _normalize_issue(self, linter_name: str, raw_issue: Dict) -> Dict:
        """Normalize different linter output formats"""
        if linter_name == 'pylint':
            return {
                'file': raw_issue.get('path', 'unknown'),
                'line': raw_issue.get('line', 0),
                'column': raw_issue.get('column', 0),
                'severity': raw_issue.get('type', 'info'),
                'message': raw_issue.get('message', ''),
                'rule': raw_issue.get('message-id', ''),
                'category': raw_issue.get('category', 'general')
            }
        elif linter_name == 'eslint':
            return {
                'file': raw_issue.get('filePath', 'unknown'),
                'line': raw_issue.get('line', 0),
                'column': raw_issue.get('column', 0),
                'severity': 'error' if raw_issue.get('severity') == 2 else 'warning',
                'message': raw_issue.get('message', ''),
                'rule': raw_issue.get('ruleId', ''),
                'category': 'linting'
            }
        else:
            return raw_issue

    def _parse_flake8_line(self, line: str) -> Optional[Dict]:
        """Parse flake8 output line"""
        # Format: filename:line:column: error_code message
        match = re.match(r'^([^:]+):(\d+):(\d+):\s*(\w+)\s+(.+)$', line)
        if match:
            return {
                'file': match.group(1),
                'line': int(match.group(2)),
                'column': int(match.group(3)),
                'severity': 'error' if match.group(4).startswith('E') else 'warning',
                'message': match.group(5),
                'rule': match.group(4),
                'category': 'style'
            }
        return None

    def _summarize_issues(self, issues: List[Dict]) -> Dict:
        """Create summary statistics from issues"""
        summary = {
            'total_issues': len(issues),
            'by_severity': {},
            'by_file': {},
            'by_rule': {},
            'top_issues': []
        }

        # Count by severity
        for issue in issues:
            severity = issue.get('severity', 'unknown')
            summary['by_severity'][severity] = summary['by_severity'].get(severity, 0) + 1

        # Count by file
        for issue in issues:
            file = issue.get('file', 'unknown')
            summary['by_file'][file] = summary['by_file'].get(file, 0) + 1

        # Count by rule
        for issue in issues:
            rule = issue.get('rule', 'unknown')
            summary['by_rule'][rule] = summary['by_rule'].get(rule, 0) + 1

        # Find top issues
        top_rules = sorted(summary['by_rule'].items(), key=lambda x: x[1], reverse=True)[:5]
        summary['top_issues'] = [{'rule': rule, 'count': count} for rule, count in top_rules]

        return summary

    def _generate_suggestions(self, ecosystem: str, linter_name: str,
                            issues: List[Dict]) -> List[str]:
        """Generate actionable suggestions based on issues found"""
        suggestions = []

        if not issues:
            suggestions.append(f"✅ {linter_name}: No issues found - excellent code quality!")
            return suggestions

        # Ecosystem-specific suggestions
        if ecosystem == 'python':
            if linter_name == 'pylint':
                avg_score = 10 - (len(issues) / 10)  # Rough estimate
                if avg_score < 8:
                    suggestions.append(f"🎯 Focus on improving pylint score (current: ~{avg_score:.1f}/10)")
                    suggestions.append("💡 Run 'pylint --generate-rcfile > .pylintrc' to customize rules")

            elif linter_name == 'black':
                suggestions.append("🎨 Run 'black .' to auto-format all Python files")
                suggestions.append("💡 Add black to pre-commit hooks for consistent formatting")

        elif ecosystem == 'javascript':
            if linter_name == 'eslint':
                suggestions.append("🔧 Run 'eslint --fix .' to auto-fix many issues")
                suggestions.append("💡 Consider adding ESLint to your build process")

            elif linter_name == 'prettier':
                suggestions.append("🎨 Run 'prettier --write .' to format all files")
                suggestions.append("💡 Set up IDE integration for automatic formatting")

        # Generic suggestions based on issue patterns
        error_count = len([i for i in issues if i.get('severity') == 'error'])
        warning_count = len([i for i in issues if i.get('severity') == 'warning'])

        if error_count > 0:
            suggestions.append(f"🚨 Priority: Fix {error_count} error(s) first")

        if warning_count > 10:
            suggestions.append(f"⚠️ Consider addressing {warning_count} warnings gradually")

        # File-specific suggestions
        files_with_issues = len(set(i.get('file', '') for i in issues))
        if files_with_issues > 20:
            suggestions.append("📁 Focus on files with the most issues first")

        return suggestions

    def _run_custom_quality_checks(self, ecosystems: List[str]) -> Dict:
        """Run custom quality checks beyond standard linters"""
        results = {
            'code_complexity': self._check_code_complexity(ecosystems),
            'file_sizes': self._check_file_sizes(),
            'naming_conventions': self._check_naming_conventions(ecosystems),
            'documentation': self._check_documentation_quality(),
            'security_patterns': self._check_basic_security_patterns(ecosystems)
        }

        return results

    def _check_code_complexity(self, ecosystems: List[str]) -> Dict:
        """Check for overly complex code structures"""
        complexity_issues = []

        if 'python' in ecosystems:
            for py_file in self.repository_path.rglob('*.py'):
                complexity = self._analyze_python_complexity(py_file)
                if complexity > 10:  # McCabe complexity threshold
                    complexity_issues.append({
                        'file': str(py_file.relative_to(self.repository_path)),
                        'complexity': complexity,
                        'suggestion': 'Consider breaking down complex functions'
                    })

        return {
            'issues': complexity_issues,
            'threshold': 10,
            'suggestion': 'Refactor functions with complexity > 10'
        }

    def _analyze_python_complexity(self, file_path: Path) -> int:
        """Simple complexity analysis for Python files"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            tree = ast.parse(content)
            complexity = 0

            for node in ast.walk(tree):
                # Count decision points
                if isinstance(node, (ast.If, ast.While, ast.For, ast.With)):
                    complexity += 1
                elif isinstance(node, ast.Try):
                    complexity += len(node.handlers)

            return complexity
        except:
            return 0

    def _check_file_sizes(self) -> Dict:
        """Check for overly large files that should be split"""
        large_files = []

        for file_path in self.repository_path.rglob('*'):
            if file_path.is_file() and not file_path.name.startswith('.'):
                try:
                    line_count = len(file_path.read_text(encoding='utf-8').splitlines())
                    if line_count > 500:  # Threshold for large files
                        large_files.append({
                            'file': str(file_path.relative_to(self.repository_path)),
                            'lines': line_count,
                            'suggestion': 'Consider splitting into smaller modules'
                        })
                except:
                    pass

        return {
            'issues': large_files,
            'threshold': 500,
            'suggestion': 'Split files with >500 lines into smaller modules'
        }

    def _check_naming_conventions(self, ecosystems: List[str]) -> Dict:
        """Check naming convention compliance"""
        naming_issues = []

        if 'python' in ecosystems:
            for py_file in self.repository_path.rglob('*.py'):
                # Check snake_case for Python files
                if not re.match(r'^[a-z_][a-z0-9_]*\.py$', py_file.name):
                    naming_issues.append({
                        'file': str(py_file.relative_to(self.repository_path)),
                        'issue': 'Should use snake_case naming',
                        'current': py_file.name
                    })

        return {
            'issues': naming_issues,
            'suggestion': 'Follow ecosystem naming conventions'
        }

    def _check_documentation_quality(self) -> Dict:
        """Check documentation coverage and quality"""
        doc_issues = []

        # Check for README
        readme_files = list(self.repository_path.glob('README*'))
        if not readme_files:
            doc_issues.append({
                'type': 'missing_readme',
                'message': 'No README file found',
                'suggestion': 'Add README.md with project description'
            })

        # Check for LICENSE
        license_files = list(self.repository_path.glob('LICENSE*'))
        if not license_files:
            doc_issues.append({
                'type': 'missing_license',
                'message': 'No LICENSE file found',
                'suggestion': 'Add LICENSE file for open source projects'
            })

        return {
            'issues': doc_issues,
            'suggestion': 'Maintain good documentation practices'
        }

    def _check_basic_security_patterns(self, ecosystems: List[str]) -> Dict:
        """Check for basic security anti-patterns"""
        security_issues = []

        # Check for potential secrets in code
        secret_patterns = [
            r'password\s*=\s*["\'][^"\']+["\']',
            r'api_key\s*=\s*["\'][^"\']+["\']',
            r'secret\s*=\s*["\'][^"\']+["\']',
            r'token\s*=\s*["\'][^"\']+["\']'
        ]

        for file_path in self.repository_path.rglob('*'):
            if file_path.suffix in ['.py', '.js', '.ts', '.java', '.go', '.rs']:
                try:
                    content = file_path.read_text(encoding='utf-8')
                    for pattern in secret_patterns:
                        matches = re.finditer(pattern, content, re.IGNORECASE)
                        for match in matches:
                            line_num = content[:match.start()].count('\n') + 1
                            security_issues.append({
                                'file': str(file_path.relative_to(self.repository_path)),
                                'line': line_num,
                                'type': 'potential_secret',
                                'message': 'Potential hardcoded secret detected',
                                'suggestion': 'Use environment variables or config files'
                            })
                except:
                    pass

        return {
            'issues': security_issues,
            'suggestion': 'Use proper secret management practices'
        }

    def generate_linting_report(self, results: Dict, format: str = 'text') -> str:
        """Generate comprehensive linting report"""
        if format == 'json':
            return json.dumps(results, indent=2)

        # Text format report
        report_lines = []
        report_lines.append("🔍 Repository Linting Report")
        report_lines.append("=" * 50)
        report_lines.append("")

        total_issues = 0

        for ecosystem, linters in results.items():
            if ecosystem == 'custom_quality':
                continue

            report_lines.append(f"## {ecosystem.title()} Ecosystem")
            report_lines.append("")

            for linter_name, linter_result in linters.items():
                if linter_result.get('available'):
                    issues_count = len(linter_result.get('issues', []))
                    total_issues += issues_count

                    status = "✅" if issues_count == 0 else f"⚠️ {issues_count} issues"
                    report_lines.append(f"  {linter_name}: {status}")

                    # Add top suggestions
                    suggestions = linter_result.get('suggestions', [])[:2]
                    for suggestion in suggestions:
                        report_lines.append(f"    💡 {suggestion}")
                else:
                    report_lines.append(f"  {linter_name}: ❌ Not available")

            report_lines.append("")

        # Custom quality checks
        if 'custom_quality' in results:
            report_lines.append("## Custom Quality Checks")
            report_lines.append("")

            custom = results['custom_quality']
            for check_name, check_result in custom.items():
                issues_count = len(check_result.get('issues', []))
                total_issues += issues_count

                status = "✅" if issues_count == 0 else f"⚠️ {issues_count} issues"
                report_lines.append(f"  {check_name.replace('_', ' ').title()}: {status}")

            report_lines.append("")

        # Summary
        report_lines.append("## Summary")
        report_lines.append("")
        report_lines.append(f"📊 Total Issues Found: {total_issues}")

        if total_issues == 0:
            report_lines.append("🎉 Excellent! Your repository meets all quality standards.")
        elif total_issues < 10:
            report_lines.append("✨ Good code quality with minor improvements needed.")
        elif total_issues < 50:
            report_lines.append("🔧 Moderate issues found - consider addressing systematically.")
        else:
            report_lines.append("🚨 Significant quality issues found - prioritize fixing critical items.")

        return "\n".join(report_lines)