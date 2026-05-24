"""
Command Analyzer - Analyze command patterns and usage statistics
命令分析器 - 分析命令模式和使用统计
"""

import re
from collections import Counter, defaultdict
from typing import List, Dict, Tuple, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass, field

from .parser import CommandEntry


@dataclass
class CommandStats:
    """Statistics for a single command"""
    command: str
    count: int
    base_command: str
    category: str
    avg_length: float
    last_used: Optional[datetime] = None
    
    def to_dict(self) -> Dict:
        return {
            "command": self.command,
            "count": self.count,
            "base_command": self.base_command,
            "category": self.category,
            "avg_length": self.avg_length,
            "last_used": self.last_used.isoformat() if self.last_used else None,
        }


@dataclass 
class AnalysisResult:
    """Complete analysis result"""
    total_commands: int
    unique_commands: int
    top_commands: List[CommandStats]
    command_categories: Dict[str, int]
    hourly_distribution: Dict[int, int]
    daily_distribution: Dict[str, int]
    efficiency_score: float
    insights: List[str]
    time_saved_estimate: float  # in minutes
    
    def to_dict(self) -> Dict:
        return {
            "total_commands": self.total_commands,
            "unique_commands": self.unique_commands,
            "top_commands": [c.to_dict() for c in self.top_commands],
            "command_categories": self.command_categories,
            "hourly_distribution": self.hourly_distribution,
            "daily_distribution": self.daily_distribution,
            "efficiency_score": self.efficiency_score,
            "insights": self.insights,
            "time_saved_estimate": self.time_saved_estimate,
        }


class CommandAnalyzer:
    """
    Analyze command history patterns and generate insights
    
    Features:
    - Command frequency analysis
    - Category classification
    - Time-based distribution
    - Efficiency scoring
    - Insight generation
    """
    
    # Command categories with patterns
    COMMAND_CATEGORIES = {
        "version_control": [
            r"^git\s", r"^svn\s", r"^hg\s", r"^gh\s",
        ],
        "file_operations": [
            r"^ls\b", r"^cd\b", r"^cp\b", r"^mv\b", r"^rm\b",
            r"^mkdir\b", r"^touch\b", r"^cat\b", r"^find\b",
            r"^grep\b", r"^chmod\b", r"^chown\b",
        ],
        "development": [
            r"^python\b", r"^pip\b", r"^npm\b", r"^yarn\b",
            r"^node\b", r"^cargo\b", r"^go\b", r"^make\b",
            r"^gcc\b", r"^javac\b", r"^mvn\b", r"^gradle\b",
        ],
        "docker": [
            r"^docker\s", r"^docker-compose\s", r"^kubectl\s",
            r"^helm\s", r"^podman\s",
        ],
        "network": [
            r"^curl\b", r"^wget\b", r"^ssh\b", r"^scp\b",
            r"^ping\b", r"^netstat\b", r"^ifconfig\b", r"^ip\b",
        ],
        "text_editors": [
            r"^vim\b", r"^nano\b", r"^emacs\b", r"^code\b",
            r"^subl\b", r"^nvim\b",
        ],
        "system": [
            r"^sudo\b", r"^systemctl\b", r"^service\b",
            r"^ps\b", r"^kill\b", r"^top\b", r"^htop\b",
            r"^df\b", r"^du\b", r"^free\b",
        ],
        "package_management": [
            r"^apt\b", r"^apt-get\b", r"^yum\b", r"^dnf\b",
            r"^pacman\b", r"^brew\b", r"^snap\b",
        ],
    }
    
    # Commands that indicate high efficiency
    EFFICIENCY_PATTERNS = {
        "aliases": r"^alias\s",
        "functions": r"^\w+\(\)",
        "pipes": r"\|",
        "redirects": r"[<>]",
        "background": r"&\s*$",
        "xargs": r"\bxargs\b",
        "substitution": r"\$\([^)]+\)",
    }
    
    def __init__(self, entries: List[CommandEntry]):
        """
        Initialize analyzer with command entries
        
        Args:
            entries: List of CommandEntry objects to analyze
        """
        self.entries = entries
        self._command_counter: Optional[Counter] = None
        self._base_command_counter: Optional[Counter] = None
        
    def analyze(self) -> AnalysisResult:
        """
        Perform complete analysis on command history
        
        Returns:
            AnalysisResult with all statistics and insights
        """
        if not self.entries:
            return AnalysisResult(
                total_commands=0,
                unique_commands=0,
                top_commands=[],
                command_categories={},
                hourly_distribution={},
                daily_distribution={},
                efficiency_score=0.0,
                insights=["No command history found to analyze."],
                time_saved_estimate=0.0,
            )
            
        # Calculate basic stats
        total = len(self.entries)
        unique = len(set(e.command for e in self.entries))
        
        # Get top commands
        top_commands = self._get_top_commands(20)
        
        # Categorize commands
        categories = self._categorize_commands()
        
        # Time distribution
        hourly = self._get_hourly_distribution()
        daily = self._get_daily_distribution()
        
        # Calculate efficiency score
        efficiency = self._calculate_efficiency_score()
        
        # Generate insights
        insights = self._generate_insights(top_commands, categories, efficiency)
        
        # Estimate time saved
        time_saved = self._estimate_time_saved(top_commands)
        
        return AnalysisResult(
            total_commands=total,
            unique_commands=unique,
            top_commands=top_commands,
            command_categories=categories,
            hourly_distribution=hourly,
            daily_distribution=daily,
            efficiency_score=efficiency,
            insights=insights,
            time_saved_estimate=time_saved,
        )
        
    def _get_command_counter(self) -> Counter:
        """Get counter for full commands"""
        if self._command_counter is None:
            self._command_counter = Counter(e.command for e in self.entries)
        return self._command_counter
        
    def _get_base_command_counter(self) -> Counter:
        """Get counter for base commands (first word)"""
        if self._base_command_counter is None:
            counter = Counter()
            for entry in self.entries:
                parts = entry.command.strip().split()
                if parts:
                    counter[parts[0]] += 1
            self._base_command_counter = counter
        return self._base_command_counter
        
    def _extract_base_command(self, command: str) -> str:
        """Extract base command (first word) from full command"""
        parts = command.strip().split()
        return parts[0] if parts else ""
        
    def _categorize_command(self, command: str) -> str:
        """Categorize a command based on patterns"""
        base = self._extract_base_command(command)
        
        for category, patterns in self.COMMAND_CATEGORIES.items():
            for pattern in patterns:
                if re.search(pattern, command, re.IGNORECASE):
                    return category
                    
        return "other"
        
    def _get_top_commands(self, limit: int = 20) -> List[CommandStats]:
        """Get most frequently used commands"""
        counter = self._get_command_counter()
        base_counter = self._get_base_command_counter()
        
        top = counter.most_common(limit)
        results = []
        
        for command, count in top:
            base = self._extract_base_command(command)
            category = self._categorize_command(command)
            
            # Find last used timestamp
            last_used = None
            for entry in reversed(self.entries):
                if entry.command == command and entry.timestamp:
                    last_used = entry.timestamp
                    break
                    
            results.append(CommandStats(
                command=command,
                count=count,
                base_command=base,
                category=category,
                avg_length=len(command),
                last_used=last_used,
            ))
            
        return results
        
    def _categorize_commands(self) -> Dict[str, int]:
        """Get command counts by category"""
        categories = defaultdict(int)
        
        for entry in self.entries:
            category = self._categorize_command(entry.command)
            categories[category] += 1
            
        return dict(sorted(categories.items(), key=lambda x: x[1], reverse=True))
        
    def _get_hourly_distribution(self) -> Dict[int, int]:
        """Get command distribution by hour"""
        hourly = defaultdict(int)
        
        for entry in self.entries:
            if entry.timestamp:
                hourly[entry.timestamp.hour] += 1
                
        # Fill missing hours with 0
        for hour in range(24):
            if hour not in hourly:
                hourly[hour] = 0
                
        return dict(sorted(hourly.items()))
        
    def _get_daily_distribution(self) -> Dict[str, int]:
        """Get command distribution by day of week"""
        daily = defaultdict(int)
        day_names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        
        for entry in self.entries:
            if entry.timestamp:
                day_name = day_names[entry.timestamp.weekday()]
                daily[day_name] += 1
                
        # Ensure all days are present
        for day in day_names:
            if day not in daily:
                daily[day] = 0
                
        return {day: daily[day] for day in day_names}
        
    def _calculate_efficiency_score(self) -> float:
        """
        Calculate efficiency score (0-100)
        
        Based on:
        - Use of pipes and redirects
        - Use of aliases
        - Command diversity
        - Use of advanced features
        """
        if not self.entries:
            return 0.0
            
        score = 0.0
        total = len(self.entries)
        
        # Check for efficiency patterns
        for entry in self.entries:
            cmd = entry.command
            
            # Pipes indicate command chaining
            if "|" in cmd:
                score += 2
                
            # Redirects show output management
            if re.search(r"[<>]", cmd):
                score += 1.5
                
            # Background execution
            if cmd.rstrip().endswith("&"):
                score += 1
                
            # Command substitution
            if re.search(r"\$\([^)]+\)", cmd):
                score += 2
                
            # xargs for batch processing
            if "xargs" in cmd:
                score += 2
                
            # Aliases
            if cmd.startswith("alias "):
                score += 3
                
        # Normalize to 0-100
        max_possible = total * 5
        normalized = min(100, (score / max_possible) * 100) if max_possible > 0 else 0
        
        return round(normalized, 1)
        
    def _generate_insights(
        self, 
        top_commands: List[CommandStats],
        categories: Dict[str, int],
        efficiency: float
    ) -> List[str]:
        """Generate actionable insights"""
        insights = []
        
        if not top_commands:
            return ["No commands to analyze."]
            
        # Top command insight
        top = top_commands[0]
        insights.append(
            f"🎯 Most used command: '{top.base_command}' ({top.count} times)"
        )
        
        # Category insights
        if categories:
            top_category = max(categories.items(), key=lambda x: x[1])
            insights.append(
                f"📊 Primary workflow: {top_category[0]} ({top_category[1]} commands)"
            )
            
        # Efficiency insights
        if efficiency >= 70:
            insights.append("🚀 Excellent efficiency! You're a power user.")
        elif efficiency >= 40:
            insights.append("⚡ Good efficiency. Consider using more pipes and aliases.")
        else:
            insights.append("💡 Tip: Use pipes (|) and aliases to boost productivity.")
            
        # Repetition detection
        counter = self._get_command_counter()
        repeated = sum(1 for c in counter.values() if c >= 5)
        if repeated >= 10:
            insights.append(
                f"🔄 Found {repeated} frequently repeated commands. "
                "Consider creating aliases for them."
            )
            
        # Git usage
        git_commands = sum(1 for e in self.entries if e.command.startswith("git "))
        if git_commands > 0:
            insights.append(
                f"🌿 Git usage: {git_commands} commands. "
                "Consider git aliases for common operations."
            )
            
        return insights
        
    def _estimate_time_saved(self, top_commands: List[CommandStats]) -> float:
        """
        Estimate time saved through efficient command usage
        
        Returns time in minutes
        """
        # Assume each repeated command saves ~2 seconds
        # compared to typing from scratch
        time_saved = 0.0
        
        for cmd_stat in top_commands:
            if cmd_stat.count > 1:
                # Estimate: 2 seconds saved per repeat
                time_saved += (cmd_stat.count - 1) * 2 / 60
                
        return round(time_saved, 1)
        
    def get_command_suggestions(self) -> List[str]:
        """Generate command suggestions based on patterns"""
        suggestions = []
        base_counter = self._get_base_command_counter()
        
        # Suggest aliases for frequently used commands
        for cmd, count in base_counter.most_common(5):
            if count >= 10 and len(cmd) > 3:
                suggestions.append(
                    f"alias {cmd[0]}='{cmd}'  # Used {count} times"
                )
                
        return suggestions
