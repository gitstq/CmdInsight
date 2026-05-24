"""
CmdInsight - Terminal Command History Intelligent Analysis Engine
终端命令历史智能分析引擎

A lightweight CLI tool for analyzing command history patterns,
discovering efficiency bottlenecks, and providing intelligent suggestions.
"""

__version__ = "1.0.0"
__author__ = "CmdInsight Team"
__description__ = "Terminal Command History Intelligent Analysis Engine"

from .analyzer import CommandAnalyzer
from .parser import HistoryParser
from .suggester import CommandSuggester
from .reporter import ReportGenerator

__all__ = [
    "CommandAnalyzer",
    "HistoryParser", 
    "CommandSuggester",
    "ReportGenerator",
]
