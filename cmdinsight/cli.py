"""
CmdInsight CLI - Command Line Interface
命令行接口
"""

import sys
import json
from pathlib import Path
from typing import Optional

try:
    import typer
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.progress import Progress, SpinnerColumn, TextColumn
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False
    # Fallback for minimal dependencies
    def typer_command_decorator(f):
        return f
    class typer:
        @staticmethod
        def Typer():
            class FakeTyper:
                def command(self):
                    return lambda f: f
                def callback(self):
                    return lambda f: f
            return FakeTyper()
        @staticmethod
        def Option(default, **kwargs):
            return default
        @staticmethod
        def Argument(default, **kwargs):
            return default
        @staticmethod
        def Exit(code):
            sys.exit(code)

from .parser import HistoryParser
from .analyzer import CommandAnalyzer
from .suggester import CommandSuggester
from .reporter import ReportGenerator


# Initialize Typer app
app = typer.Typer(
    name="cmdinsight",
    help="🔍 Terminal Command History Intelligent Analysis Engine | 终端命令历史智能分析引擎",
    add_completion=False,
)

# Console for rich output
console = Console() if RICH_AVAILABLE else None


def _print_fallback(message: str):
    """Fallback print when Rich is not available"""
    print(message)


def _error_exit(message: str, code: int = 1):
    """Print error and exit"""
    if console:
        console.print(f"[red]Error:[/red] {message}")
    else:
        print(f"Error: {message}")
    raise typer.Exit(code)


@app.command()
def analyze(
    history_path: Optional[str] = typer.Option(
        None,
        "--history", "-h",
        help="Path to history file (auto-detected if not specified)"
    ),
    shell_type: Optional[str] = typer.Option(
        None,
        "--shell", "-s", 
        help="Shell type: bash, zsh, fish, powershell"
    ),
    limit: int = typer.Option(
        10000,
        "--limit", "-l",
        help="Maximum number of history entries to analyze"
    ),
    output_format: str = typer.Option(
        "text",
        "--format", "-f",
        help="Output format: text, json, markdown"
    ),
    output_file: Optional[str] = typer.Option(
        None,
        "--output", "-o",
        help="Output file path (prints to stdout if not specified)"
    ),
    detailed: bool = typer.Option(
        False,
        "--detailed", "-d",
        help="Show detailed report with charts"
    ),
):
    """
    🔍 Analyze command history and generate insights
    
    分析命令历史并生成洞察报告
    """
    # Parse history
    parser = HistoryParser(history_path=history_path, shell_type=shell_type)
    
    if console:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Parsing command history...", total=None)
            entries = parser.parse(limit=limit)
    else:
        print("Parsing command history...")
        entries = parser.parse(limit=limit)
        
    if not entries:
        _error_exit("No command history found. Check your history file path.")
        
    # Analyze
    if console:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Analyzing patterns...", total=None)
            analyzer = CommandAnalyzer(entries)
            result = analyzer.analyze()
    else:
        print("Analyzing patterns...")
        analyzer = CommandAnalyzer(entries)
        result = analyzer.analyze()
        
    # Generate suggestions
    suggester = CommandSuggester(analyzer)
    suggestions = suggester.generate_suggestions()
    
    # Generate report
    reporter = ReportGenerator(use_color=True)
    
    if output_format == "json":
        output = reporter.export_json(result, suggestions)
    elif output_format == "markdown":
        output = reporter.export_markdown(result, suggestions)
    else:
        if detailed:
            output = reporter.generate_detailed(result)
        else:
            output = reporter.generate_summary(result)
        output += "\n" + reporter.generate_suggestions_report(suggestions[:5])
        
    # Output
    if output_file:
        Path(output_file).write_text(output, encoding="utf-8")
        if console:
            console.print(f"[green]✓[/green] Report saved to {output_file}")
        else:
            print(f"Report saved to {output_file}")
    else:
        if console:
            console.print(output)
        else:
            print(output)


@app.command()
def suggest(
    history_path: Optional[str] = typer.Option(
        None,
        "--history", "-h",
        help="Path to history file"
    ),
    shell_type: Optional[str] = typer.Option(
        None,
        "--shell", "-s",
        help="Shell type: bash, zsh, fish, powershell"
    ),
    limit: int = typer.Option(
        5000,
        "--limit", "-l",
        help="Maximum history entries to analyze"
    ),
    export_aliases: bool = typer.Option(
        False,
        "--export-aliases", "-e",
        help="Export suggested aliases as shell script"
    ),
):
    """
    💡 Generate command suggestions and aliases
    
    生成命令建议和别名
    """
    parser = HistoryParser(history_path=history_path, shell_type=shell_type)
    entries = parser.parse(limit=limit)
    
    if not entries:
        _error_exit("No command history found.")
        
    analyzer = CommandAnalyzer(entries)
    suggester = CommandSuggester(analyzer)
    
    if export_aliases:
        script = suggester.get_alias_script()
        print(script)
    else:
        suggestions = suggester.generate_suggestions(limit=10)
        reporter = ReportGenerator(use_color=True)
        
        output = reporter.generate_suggestions_report(suggestions)
        
        if console:
            console.print(output)
        else:
            print(output)


@app.command()
def stats(
    history_path: Optional[str] = typer.Option(
        None,
        "--history", "-h",
        help="Path to history file"
    ),
    shell_type: Optional[str] = typer.Option(
        None,
        "--shell", "-s",
        help="Shell type"
    ),
):
    """
    📊 Show basic statistics about history file
    
    显示历史文件的基本统计信息
    """
    parser = HistoryParser(history_path=history_path, shell_type=shell_type)
    stats_data = parser.get_history_stats()
    
    if console:
        table = Table(title="History File Statistics")
        table.add_column("Property", style="cyan")
        table.add_column("Value", style="green")
        
        for key, value in stats_data.items():
            table.add_row(key.replace("_", " ").title(), str(value) if value else "N/A")
            
        console.print(table)
    else:
        print("\nHistory File Statistics")
        print("=" * 40)
        for key, value in stats_data.items():
            print(f"{key.replace('_', ' ').title()}: {value if value else 'N/A'}")


@app.command()
def version():
    """
    📦 Show version information
    
    显示版本信息
    """
    from . import __version__, __description__
    
    if console:
        console.print(Panel(
            f"[bold]CmdInsight[/bold] v{__version__}\n{__description__}",
            title="📦 Version",
            border_style="cyan",
        ))
    else:
        print(f"CmdInsight v{__version__}")
        print(__description__)


@app.callback()
def main(
    ctx: typer.Context,
):
    """
    🔍 CmdInsight - Terminal Command History Intelligent Analysis Engine
    
    终端命令历史智能分析引擎
    
    Analyze your command history to discover patterns, 
    improve efficiency, and get intelligent suggestions.
    """
    pass


def cli_entry():
    """CLI entry point"""
    app()


if __name__ == "__main__":
    cli_entry()
