"""
Educational explanation system for repo-clean

Provides detailed explanations for why issues matter and how to prevent them,
turning cleanup operations into learning opportunities.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum


class ExplanationLevel(Enum):
    """Different levels of explanation detail"""
    BRIEF = "brief"           # One-line explanation
    STANDARD = "standard"     # Paragraph with context
    DETAILED = "detailed"     # Full explanation with examples
    EDUCATIONAL = "educational"  # Learning-focused with best practices


@dataclass
class Explanation:
    """Rich explanation with multiple detail levels"""
    issue_type: str
    brief: str
    standard: str
    detailed: str
    educational: str
    examples: List[str]
    best_practices: List[str]
    related_concepts: List[str]
    prevention_tips: List[str]


class ExplanationEngine:
    """Engine for providing educational explanations about repository hygiene"""

    def __init__(self):
        self.explanations = self._load_explanations()

    def explain(self, issue_type: str, level: ExplanationLevel = ExplanationLevel.STANDARD) -> str:
        """Get explanation for a specific issue type at the requested detail level"""
        if issue_type not in self.explanations:
            return f"No explanation available for issue type: {issue_type}"

        explanation = self.explanations[issue_type]

        if level == ExplanationLevel.BRIEF:
            return f"💡 {explanation.brief}"
        elif level == ExplanationLevel.STANDARD:
            return self._format_standard_explanation(explanation)
        elif level == ExplanationLevel.DETAILED:
            return self._format_detailed_explanation(explanation)
        elif level == ExplanationLevel.EDUCATIONAL:
            return self._format_educational_explanation(explanation)

    def _format_standard_explanation(self, explanation: Explanation) -> str:
        """Format a standard explanation"""
        return f"""
📚 Why this matters: {explanation.standard}

💡 Quick examples:
{chr(10).join(f"   • {example}" for example in explanation.examples[:2])}

🔧 Prevention: {explanation.prevention_tips[0] if explanation.prevention_tips else "Keep repository clean regularly"}
"""

    def _format_detailed_explanation(self, explanation: Explanation) -> str:
        """Format a detailed explanation"""
        sections = [
            f"📚 Detailed Explanation: {explanation.detailed}",
            "",
            "💡 Examples:",
        ]

        for example in explanation.examples:
            sections.append(f"   • {example}")

        sections.extend([
            "",
            "✅ Best Practices:",
        ])

        for practice in explanation.best_practices:
            sections.append(f"   • {practice}")

        if explanation.prevention_tips:
            sections.extend([
                "",
                "🛡️ Prevention Tips:",
            ])
            for tip in explanation.prevention_tips:
                sections.append(f"   • {tip}")

        return "\n".join(sections)

    def _format_educational_explanation(self, explanation: Explanation) -> str:
        """Format an educational explanation with full learning context"""
        sections = [
            f"🎓 Educational Deep Dive: {explanation.issue_type.replace('_', ' ').title()}",
            "=" * 60,
            "",
            f"📖 What it is: {explanation.educational}",
            "",
            "🔍 Real-world Examples:",
        ]

        for example in explanation.examples:
            sections.append(f"   • {example}")

        sections.extend([
            "",
            "🏆 Industry Best Practices:",
        ])

        for practice in explanation.best_practices:
            sections.append(f"   • {practice}")

        if explanation.related_concepts:
            sections.extend([
                "",
                "🔗 Related Concepts to Learn:",
            ])
            for concept in explanation.related_concepts:
                sections.append(f"   • {concept}")

        sections.extend([
            "",
            "🛡️ How to Prevent This Issue:",
        ])

        for tip in explanation.prevention_tips:
            sections.append(f"   • {tip}")

        sections.extend([
            "",
            "📚 Further Reading:",
            "   • Git Best Practices: https://git-scm.com/book",
            "   • Professional Development Workflows",
            "   • Repository Organization Patterns",
        ])

        return "\n".join(sections)

    def get_issue_summary(self, issues: List[str]) -> str:
        """Get a summary explanation for multiple issues"""
        if not issues:
            return "✅ No hygiene issues found! Your repository follows good practices."

        summary = [
            "📊 Repository Hygiene Summary",
            "=" * 40,
            "",
            f"Found {len(issues)} types of issues that impact repository professionalism:",
            ""
        ]

        for issue in issues:
            if issue in self.explanations:
                brief = self.explanations[issue].brief
                summary.append(f"• {issue.replace('_', ' ').title()}: {brief}")
            else:
                summary.append(f"• {issue.replace('_', ' ').title()}: Needs attention")

        summary.extend([
            "",
            "💡 Use 'repo-clean explain <issue>' for detailed information",
            "🔧 Use 'repo-clean clean --preview' to see proposed fixes",
        ])

        return "\n".join(summary)

    def _load_explanations(self) -> Dict[str, Explanation]:
        """Load all explanations for different issue types"""
        return {
            "backup_files": Explanation(
                issue_type="backup_files",
                brief="Backup files clutter workspace and confuse development tools",
                standard="Backup files like .backup, .bak, and .old accumulate over time, making repositories look unprofessional and potentially exposing sensitive information from previous versions.",
                detailed="Backup files are automatically created by text editors, manual copies, or development tools. While useful during active development, they become technical debt when left in repositories. They clutter file browsers, confuse IDE indexing, can contain outdated or sensitive information, and signal poor development practices to collaborators and employers.",
                educational="Backup files represent a common anti-pattern in software development where temporary safety mechanisms become permanent clutter. Professional developers use version control (git) for safety instead of manual backups. The presence of many backup files often indicates lack of confidence with git commands or workflows that need improvement. Learning proper git usage eliminates the need for manual backup files.",
                examples=[
                    "config.php.backup containing old database passwords",
                    "main.py.bak from a failed refactoring attempt last month",
                    "README.md.old from before the documentation rewrite",
                    "package.json~ created by vim during editing",
                    "Dockerfile.backup-20231015 with outdated dependencies"
                ],
                best_practices=[
                    "Use git branches for experimental changes instead of copying files",
                    "Commit frequently with descriptive messages for safety",
                    "Use .gitignore to prevent backup files from being tracked",
                    "Configure editors to not create backup files in project directories",
                    "Use git stash for temporary work storage"
                ],
                related_concepts=[
                    "Version Control Systems (Git)",
                    "Gitignore patterns and file exclusion",
                    "Development environment configuration",
                    "Professional repository organization",
                    "Technical debt management"
                ],
                prevention_tips=[
                    "Add *.backup*, *.bak, *.old to your .gitignore file",
                    "Configure your text editor to save backups elsewhere",
                    "Learn git branching for safe experimentation",
                    "Set up automatic cleanup scripts in your development workflow",
                    "Use 'repo-clean scan' regularly to catch backup files early"
                ]
            ),

            "naming_conventions": Explanation(
                issue_type="naming_conventions",
                brief="Unprofessional naming patterns suggest experimental or temporary code",
                standard="Files named with prefixes like ENHANCED_, WORKING_, FIXED_, or FINAL_ indicate temporary naming that became permanent, suggesting poor development discipline and making code harder to navigate.",
                detailed="Naming convention violations typically occur when developers create temporary variations of files during debugging, refactoring, or experimentation. Names like 'WORKING_api.py' or 'ENHANCED_user_service.py' were likely intended as short-term experiments but became permanent parts of the codebase. This creates several problems: it makes the codebase harder to navigate, suggests the code might be experimental or unreliable, makes automated tooling more difficult, and signals unprofessional development practices to reviewers.",
                educational="File naming conventions are a fundamental aspect of software engineering professionalism. Good naming should be descriptive, consistent, and permanent. Temporary naming patterns like 'WORKING_' or 'FIXED_' violate the principle that code should be self-documenting. They also suggest that the developer lacks confidence in version control systems or proper development workflows. Professional codebases use meaningful, stable names that describe the file's purpose or functionality, not its development history or current state.",
                examples=[
                    "ENHANCED_user_authentication.py (unclear what was enhanced)",
                    "WORKING_database_connector.py (implies other versions don't work)",
                    "FIXED_payment_processor.py (what was broken? is it still broken?)",
                    "FINAL_report_generator.py (suggests multiple versions exist)",
                    "NEW_email_service.py (how new? will it always be new?)"
                ],
                best_practices=[
                    "Use descriptive names that explain purpose: 'user_authentication.py'",
                    "Keep naming consistent across the project",
                    "Use version control for tracking changes, not filenames",
                    "Choose names that will make sense to other developers",
                    "Refactor old files rather than creating 'NEW_' versions"
                ],
                related_concepts=[
                    "Code documentation and self-documenting code",
                    "Refactoring techniques and safe code evolution",
                    "Team collaboration and code readability",
                    "Software maintenance and long-term thinking",
                    "Professional development standards"
                ],
                prevention_tips=[
                    "Plan file names before creating files",
                    "Use git branches for experimental versions",
                    "Rename files immediately after experimentation ends",
                    "Set up code review processes to catch naming issues",
                    "Establish team naming conventions and enforce them"
                ]
            ),

            "git_config": Explanation(
                issue_type="git_config",
                brief="Inconsistent git configuration affects attribution and collaboration",
                standard="Git configuration inconsistencies like missing user names, generic emails, or varying formats across commits make it difficult to track contributions and maintain professional development practices.",
                detailed="Git configuration problems typically manifest as commits with incorrect or missing author information, inconsistent email formats, or generic usernames like 'root' or 'user'. This creates several issues: difficulty tracking who made specific changes, problems with automated tools that rely on author information, unprofessional appearance in commit logs, potential legal/compliance issues around code attribution, and confusion in team environments where multiple people share systems.",
                educational="Proper git configuration is essential for professional software development. The user.name and user.email settings are not just metadata—they're legal attribution that may be required for licensing, intellectual property, and compliance purposes. Many automated tools, deployment systems, and code analysis platforms rely on consistent author information. In team environments, proper attribution helps with code review, debugging, and understanding project history. Learning to maintain consistent git configuration across all development environments is a mark of professional development practices.",
                examples=[
                    "Commits showing author as 'root' instead of developer name",
                    "Mixed email addresses (personal vs work) in same repository",
                    "Missing email addresses causing git warnings",
                    "Generic usernames like 'user' or 'developer' in commits",
                    "Inconsistent name formats ('John' vs 'John Smith' vs 'J. Smith')"
                ],
                best_practices=[
                    "Set global git config: git config --global user.name 'Your Name'",
                    "Use consistent email: git config --global user.email 'you@company.com'",
                    "Use work email for work projects, personal email for personal projects",
                    "Set up git configuration templates for new repositories",
                    "Regularly audit git configuration across development environments"
                ],
                related_concepts=[
                    "Version control best practices",
                    "Professional development identity",
                    "Code attribution and intellectual property",
                    "Team collaboration workflows",
                    "Automated tooling and CI/CD integration"
                ],
                prevention_tips=[
                    "Set up global git configuration on all development machines",
                    "Use git hooks to verify author information before commits",
                    "Create setup scripts that configure git for new team members",
                    "Document team standards for git configuration",
                    "Use 'repo-clean report' to check configuration consistency"
                ]
            ),

            "gitignore_gaps": Explanation(
                issue_type="gitignore_gaps",
                brief="Incomplete .gitignore allows unwanted files to be tracked",
                standard="Missing patterns in .gitignore files allow temporary files, build artifacts, credentials, and other unwanted content to be accidentally committed to version control.",
                detailed="Gitignore gaps occur when .gitignore files don't cover all the types of files that should be excluded from version control. Common gaps include: missing backup file patterns, incomplete coverage of build artifacts, missing temporary file patterns, lack of IDE-specific exclusions, and missing patterns for credentials or configuration files. These gaps lead to repository pollution, security risks from committed credentials, larger repository sizes, and confusion about which files are important.",
                educational="The .gitignore file is a critical component of repository hygiene that defines what should and shouldn't be tracked by version control. A well-maintained .gitignore file reflects deep understanding of the development ecosystem, including build tools, editors, operating systems, and deployment processes. It's not a one-time setup but requires ongoing maintenance as projects evolve. Professional developers proactively maintain comprehensive .gitignore files and understand that excluding the right files is as important as including the right ones.",
                examples=[
                    "Missing *.log pattern allowing debug logs to be committed",
                    "No .env pattern risking exposure of API keys",
                    "Missing node_modules/ causing huge repository size",
                    "No *.backup* pattern allowing backup files to accumulate",
                    "Missing IDE files like .vscode/ or .idea/ cluttering repository"
                ],
                best_practices=[
                    "Use comprehensive .gitignore templates for your technology stack",
                    "Review and update .gitignore as project dependencies change",
                    "Include patterns for all development tools used by team members",
                    "Document why specific patterns are included",
                    "Test .gitignore effectiveness regularly"
                ],
                related_concepts=[
                    "Security best practices and credential management",
                    "Repository organization and cleanliness",
                    "Development environment standardization",
                    "Build and deployment artifact management",
                    "Team development workflow coordination"
                ],
                prevention_tips=[
                    "Start with comprehensive .gitignore templates",
                    "Add new patterns immediately when new tools are introduced",
                    "Use global gitignore for personal development preferences",
                    "Set up pre-commit hooks to check for common exclusion patterns",
                    "Regularly audit tracked files for items that should be ignored"
                ]
            )
        }