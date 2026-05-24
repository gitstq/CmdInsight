"""
Report Generator - Generate beautiful terminal reports
报告生成器 - 生成美观的终端报告
"""

import json
from typing import List, Dict, Optional
from datetime import datetime

from .analyzer import AnalysisResult, CommandStats
from .suggester import Suggestion


class ReportGenerator:
    """
    Generate beautiful terminal reports for command analysis
    
    Features:
    - Summary reports
    - Detailed statistics
    - Visual charts (ASCII)
    - JSON export
    """
    
    # Box drawing characters
    BOX = {
        "tl": "┌", "tr": "┐", "bl": "└", "br": "┘",
        "h": "─", "v": "│",
        "lt": "├", "rt": "┤", "tt": "┬", "bt": "┴", "cr": "┼",
    }
    
    # Chart characters
    CHART_CHARS = ["▁", "▂", "▃", "▄", "▅", "▆", "▇", "█"]
    
    def __init__(self, use_color: bool = True):
        """
        Initialize report generator
        
        Args:
            use_color: Whether to use ANSI colors in output
        """
        self.use_color = use_color
        
    def _color(self, text: str, color: str) -> str:
        """Apply ANSI color to text"""
        if not self.use_color:
            return text
            
        colors = {
            "red": "\033[91m",
            "green": "\033[92m",
            "yellow": "\033[93m",
            "blue": "\033[94m",
            "magenta": "\033[95m",
            "cyan": "\033[96m",
            "white": "\033[97m",
            "bold": "\033[1m",
            "dim": "\033[2m",
            "reset": "\033[0m",
        }
        
        return f"{colors.get(color, '')}{text}{colors['reset']}"
        
    def generate_summary(self, result: AnalysisResult) -> str:
        """Generate a summary report"""
        lines = []
        
        # Header
        lines.append(self._color("\n📊 CmdInsight Analysis Report", "bold"))
        lines.append(self._color("=" * 50, "cyan"))
        lines.append("")
        
        # Basic stats
        lines.append(self._color("📈 Overview", "bold"))
        lines.append(f"  Total Commands:    {self._color(str(result.total_commands), 'green')}")
        lines.append(f"  Unique Commands:   {self._color(str(result.unique_commands), 'green')}")
        lines.append(f"  Efficiency Score:  {self._color(f'{result.efficiency_score}%', 'yellow')}")
        lines.append(f"  Time Saved:        {self._color(f'{result.time_saved_estimate} min', 'cyan')}")
        lines.append("")
        
        # Top commands
        if result.top_commands:
            lines.append(self._color("🔝 Top Commands", "bold"))
            for i, cmd in enumerate(result.top_commands[:10], 1):
                count_str = self._color(f"({cmd.count})", "dim")
                lines.append(f"  {i:2}. {cmd.base_command:<15} {count_str}")
            lines.append("")
            
        # Categories
        if result.command_categories:
            lines.append(self._color("📁 Command Categories", "bold"))
            for category, count in list(result.command_categories.items())[:8]:
                bar = self._generate_bar(count, max(result.command_categories.values()))
                lines.append(f"  {category:<20} {bar} {count}")
            lines.append("")
            
        # Insights
        if result.insights:
            lines.append(self._color("💡 Insights", "bold"))
            for insight in result.insights:
                lines.append(f"  {insight}")
            lines.append("")
            
        return "\n".join(lines)
        
    def generate_detailed(self, result: AnalysisResult) -> str:
        """Generate a detailed report with charts"""
        lines = [self.generate_summary(result)]
        
        # Hourly distribution chart
        if result.hourly_distribution:
            lines.append(self._color("⏰ Hourly Distribution", "bold"))
            lines.append(self._generate_hourly_chart(result.hourly_distribution))
            lines.append("")
            
        # Daily distribution
        if result.daily_distribution:
            lines.append(self._color("📅 Daily Distribution", "bold"))
            lines.append(self._generate_daily_chart(result.daily_distribution))
            lines.append("")
            
        return "\n".join(lines)
        
    def generate_suggestions_report(self, suggestions: List[Suggestion]) -> str:
        """Generate a suggestions report"""
        lines = []
        
        lines.append(self._color("\n💡 Command Suggestions", "bold"))
        lines.append(self._color("=" * 50, "cyan"))
        lines.append("")
        
        current_category = None
        for suggestion in suggestions:
            if suggestion.category != current_category:
                current_category = suggestion.category
                lines.append(self._color(f"\n[{current_category.upper()}]", "yellow"))
                
            lines.append(f"  {self._color('•', 'cyan')} {suggestion.title}")
            lines.append(f"    {self._color(suggestion.description, 'dim')}")
            lines.append(f"    {self._color('$ ', 'green')}{suggestion.command}")
            lines.append("")
            
        return "\n".join(lines)
        
    def _generate_bar(self, value: int, max_value: int, width: int = 20) -> str:
        """Generate an ASCII bar chart"""
        if max_value == 0:
            return "░" * width
            
        filled = int((value / max_value) * width)
        return self._color("█" * filled, "cyan") + "░" * (width - filled)
        
    def _generate_hourly_chart(self, hourly: Dict[int, int]) -> str:
        """Generate hourly distribution chart"""
        lines = []
        max_val = max(hourly.values()) if hourly else 1
        
        # Create chart rows
        for hour in range(0, 24, 4):
            row = []
            for h in range(hour, min(hour + 4, 24)):
                val = hourly.get(h, 0)
                if max_val > 0:
                    idx = min(len(self.CHART_CHARS) - 1, int((val / max_val) * (len(self.CHART_CHARS) - 1)))
                    row.append(self.CHART_CHARS[idx])
                else:
                    row.append(" ")
                    
            time_label = f"{hour:02d}:00"
            lines.append(f"  {time_label}  {''.join(row)}")
            
        return "\n".join(lines)
        
    def _generate_daily_chart(self, daily: Dict[str, int]) -> str:
        """Generate daily distribution chart"""
        lines = []
        max_val = max(daily.values()) if daily else 1
        
        for day, count in daily.items():
            bar = self._generate_bar(count, max_val, width=10)
            lines.append(f"  {day}  {bar} {count}")
            
        return "\n".join(lines)
        
    def export_json(self, result: AnalysisResult, suggestions: List[Suggestion]) -> str:
        """Export analysis result as JSON"""
        data = {
            "analysis": result.to_dict(),
            "suggestions": [s.to_dict() for s in suggestions],
            "generated_at": datetime.now().isoformat(),
        }
        return json.dumps(data, indent=2)
        
    def export_markdown(self, result: AnalysisResult, suggestions: List[Suggestion]) -> str:
        """Export analysis result as Markdown"""
        lines = [
            "# CmdInsight Analysis Report",
            "",
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "## 📈 Overview",
            "",
            f"- **Total Commands:** {result.total_commands}",
            f"- **Unique Commands:** {result.unique_commands}",
            f"- **Efficiency Score:** {result.efficiency_score}%",
            f"- **Estimated Time Saved:** {result.time_saved_estimate} minutes",
            "",
            "## 🔝 Top Commands",
            "",
            "| Rank | Command | Count | Category |",
            "|------|---------|-------|----------|",
        ]
        
        for i, cmd in enumerate(result.top_commands[:10], 1):
            lines.append(f"| {i} | `{cmd.base_command}` | {cmd.count} | {cmd.category} |")
            
        lines.extend([
            "",
            "## 📁 Categories",
            "",
        ])
        
        for category, count in result.command_categories.items():
            lines.append(f"- **{category}:** {count} commands")
            
        lines.extend([
            "",
            "## 💡 Insights",
            "",
        ])
        
        for insight in result.insights:
            lines.append(f"- {insight}")
            
        lines.extend([
            "",
            "## 🚀 Suggestions",
            "",
        ])
        
        for suggestion in suggestions:
            lines.append(f"### {suggestion.title}")
            lines.append(f"{suggestion.description}")
            lines.append(f"```bash")
            lines.append(suggestion.command)
            lines.append(f"```")
            lines.append("")
            
        return "\n".join(lines)
