"""
Command Suggester - Generate intelligent command suggestions
命令建议器 - 生成智能命令建议
"""

import re
from typing import List, Dict, Optional
from dataclasses import dataclass

from .parser import CommandEntry
from .analyzer import CommandAnalyzer, CommandStats


@dataclass
class Suggestion:
    """A command suggestion"""
    title: str
    description: str
    command: str
    category: str
    priority: int  # 1-5, 5 being highest
    
    def to_dict(self) -> Dict:
        return {
            "title": self.title,
            "description": self.description,
            "command": self.command,
            "category": self.category,
            "priority": self.priority,
        }


class CommandSuggester:
    """
    Generate intelligent command suggestions based on usage patterns
    
    Features:
    - Alias suggestions for frequently used commands
    - Workflow optimization tips
    - Command combination suggestions
    - Tool recommendations
    """
    
    # Common command improvements
    COMMAND_IMPROVEMENTS = {
        "ls": {
            "suggestion": "ls -lah",
            "reason": "Show hidden files, sizes in human-readable format",
        },
        "grep": {
            "suggestion": "grep -rni",
            "reason": "Recursive, case-insensitive search with line numbers",
        },
        "find": {
            "suggestion": "find . -name '*.ext' -type f",
            "reason": "More specific file search pattern",
        },
        "ps": {
            "suggestion": "ps aux | grep",
            "reason": "Find specific process easily",
        },
        "cat": {
            "suggestion": "bat",
            "reason": "Modern cat with syntax highlighting and Git integration",
        },
        "du": {
            "suggestion": "du -sh * | sort -h",
            "reason": "Show directory sizes sorted by size",
        },
        "df": {
            "suggestion": "df -h",
            "reason": "Show disk usage in human-readable format",
        },
    }
    
    # Tool recommendations based on patterns
    TOOL_RECOMMENDATIONS = {
        "git": [
            Suggestion(
                title="Install Git Aliases",
                description="Common git aliases for faster workflow",
                command="git config --global alias.co checkout && git config --global alias.br branch",
                category="workflow",
                priority=4,
            ),
            Suggestion(
                title="Use Git Status Short",
                description="Shorter git status output",
                command="git status -s",
                category="workflow",
                priority=3,
            ),
        ],
        "docker": [
            Suggestion(
                title="Docker Cleanup Alias",
                description="Remove unused Docker resources",
                command="docker system prune -af --volumes",
                category="maintenance",
                priority=3,
            ),
        ],
        "python": [
            Suggestion(
                title="Use Virtual Environment",
                description="Create isolated Python environment",
                command="python -m venv .venv && source .venv/bin/activate",
                category="development",
                priority=5,
            ),
        ],
        "npm": [
            Suggestion(
                title="Use npm ci for CI",
                description="Faster, reproducible installs",
                command="npm ci",
                category="development",
                priority=3,
            ),
        ],
    }
    
    def __init__(self, analyzer: CommandAnalyzer):
        """
        Initialize suggester with analyzer
        
        Args:
            analyzer: CommandAnalyzer instance with parsed entries
        """
        self.analyzer = analyzer
        self.entries = analyzer.entries
        
    def generate_suggestions(self, limit: int = 10) -> List[Suggestion]:
        """
        Generate all suggestions
        
        Args:
            limit: Maximum number of suggestions to return
            
        Returns:
            List of Suggestion objects sorted by priority
        """
        suggestions = []
        
        # Add alias suggestions
        suggestions.extend(self._suggest_aliases())
        
        # Add command improvement suggestions
        suggestions.extend(self._suggest_improvements())
        
        # Add tool recommendations
        suggestions.extend(self._suggest_tools())
        
        # Add workflow suggestions
        suggestions.extend(self._suggest_workflows())
        
        # Sort by priority and limit
        suggestions.sort(key=lambda s: s.priority, reverse=True)
        
        return suggestions[:limit]
        
    def _suggest_aliases(self) -> List[Suggestion]:
        """Suggest aliases for frequently used commands"""
        suggestions = []
        base_counter = self.analyzer._get_base_command_counter()
        
        for cmd, count in base_counter.most_common(10):
            if count >= 5 and len(cmd) > 3:
                # Generate alias suggestion
                alias_char = cmd[0]
                
                # Avoid common conflicts
                if alias_char in ["c", "l", "g", "d"]:
                    alias_char = cmd[:2]
                    
                suggestions.append(Suggestion(
                    title=f"Alias for '{cmd}'",
                    description=f"Used {count} times. Create a short alias.",
                    command=f"alias {alias_char}='{cmd}'",
                    category="alias",
                    priority=min(5, count // 3),
                ))
                
        return suggestions
        
    def _suggest_improvements(self) -> List[Suggestion]:
        """Suggest improvements for common commands"""
        suggestions = []
        base_counter = self.analyzer._get_base_command_counter()
        
        for cmd, count in base_counter.most_common(20):
            if cmd in self.COMMAND_IMPROVEMENTS:
                improvement = self.COMMAND_IMPROVEMENTS[cmd]
                suggestions.append(Suggestion(
                    title=f"Improve '{cmd}' usage",
                    description=improvement["reason"],
                    command=improvement["suggestion"],
                    category="improvement",
                    priority=3,
                ))
                
        return suggestions
        
    def _suggest_tools(self) -> List[Suggestion]:
        """Suggest tools based on usage patterns"""
        suggestions = []
        base_counter = self.analyzer._get_base_command_counter()
        
        for tool, tool_suggestions in self.TOOL_RECOMMENDATIONS.items():
            if tool in base_counter and base_counter[tool] >= 3:
                suggestions.extend(tool_suggestions)
                
        # Check for modern tool opportunities
        if "cat" in base_counter and base_counter["cat"] >= 5:
            suggestions.append(Suggestion(
                title="Try 'bat' instead of 'cat'",
                description="Modern cat with syntax highlighting",
                command="brew install bat  # or apt install bat",
                category="tool",
                priority=4,
            ))
            
        if "ls" in base_counter and base_counter["ls"] >= 10:
            suggestions.append(Suggestion(
                title="Try 'exa' instead of 'ls'",
                description="Modern ls with colors and Git integration",
                command="brew install exa  # or apt install exa",
                category="tool",
                priority=3,
            ))
            
        if "find" in base_counter and base_counter["find"] >= 5:
            suggestions.append(Suggestion(
                title="Try 'fd' instead of 'find'",
                description="Faster, more intuitive find",
                command="brew install fd  # or apt install fd-find",
                category="tool",
                priority=3,
            ))
            
        if "grep" in base_counter and base_counter["grep"] >= 10:
            suggestions.append(Suggestion(
                title="Try 'ripgrep' (rg) instead of 'grep'",
                description="Much faster grep with better defaults",
                command="brew install ripgrep  # or apt install ripgrep",
                category="tool",
                priority=4,
            ))
            
        return suggestions
        
    def _suggest_workflows(self) -> List[Suggestion]:
        """Suggest workflow improvements"""
        suggestions = []
        
        # Check for repeated patterns
        command_pairs = []
        for i in range(len(self.entries) - 1):
            current = self.entries[i].command.strip().split()[0] if self.entries[i].command.strip() else ""
            next_cmd = self.entries[i + 1].command.strip().split()[0] if self.entries[i + 1].command.strip() else ""
            if current and next_cmd:
                command_pairs.append((current, next_cmd))
                
        pair_counter = {}
        for pair in command_pairs:
            pair_counter[pair] = pair_counter.get(pair, 0) + 1
            
        # Suggest combining frequently paired commands
        for (cmd1, cmd2), count in sorted(pair_counter.items(), key=lambda x: x[1], reverse=True)[:5]:
            if count >= 3:
                suggestions.append(Suggestion(
                    title=f"Combine '{cmd1}' and '{cmd2}'",
                    description=f"These commands are often used together ({count} times)",
                    command=f"{cmd1} && {cmd2}",
                    category="workflow",
                    priority=2,
                ))
                
        return suggestions
        
    def get_alias_script(self) -> str:
        """Generate a shell script with suggested aliases"""
        suggestions = self._suggest_aliases()
        
        lines = [
            "#!/bin/bash",
            "# CmdInsight Suggested Aliases",
            "# Generated based on your command history analysis",
            "",
        ]
        
        for suggestion in suggestions:
            lines.append(f"# {suggestion.description}")
            lines.append(f"{suggestion.command}")
            lines.append("")
            
        return "\n".join(lines)
