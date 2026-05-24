"""
Utility functions for CmdInsight
工具函数模块
"""

import os
import sys
from pathlib import Path
from typing import Optional


def get_terminal_width() -> int:
    """Get terminal width with fallback"""
    try:
        return os.get_terminal_size().columns
    except OSError:
        return 80


def truncate_text(text: str, max_length: int, suffix: str = "...") -> str:
    """Truncate text to max length with suffix"""
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def format_duration(seconds: float) -> str:
    """Format duration in human-readable format"""
    if seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.1f}min"
    else:
        hours = seconds / 3600
        return f"{hours:.1f}h"


def format_number(num: int) -> str:
    """Format number with thousands separator"""
    return f"{num:,}"


def ensure_directory(path: Path) -> None:
    """Ensure directory exists, create if not"""
    path.mkdir(parents=True, exist_ok=True)


def is_valid_shell(shell: str) -> bool:
    """Check if shell type is supported"""
    valid_shells = {"bash", "zsh", "fish", "powershell"}
    return shell.lower() in valid_shells


def detect_shell_from_env() -> str:
    """Detect shell type from environment variables"""
    shell = os.environ.get("SHELL", "").lower()
    
    if "zsh" in shell:
        return "zsh"
    elif "bash" in shell:
        return "bash"
    elif "fish" in shell:
        return "fish"
    
    # Check for PowerShell
    if sys.platform == "win32":
        return "powershell"
        
    return "bash"  # Default fallback


def get_config_dir() -> Path:
    """Get configuration directory path"""
    if sys.platform == "win32":
        base = Path(os.environ.get("APPDATA", "~"))
    else:
        base = Path.home() / ".config"
        
    return base / "cmdinsight"


def get_cache_dir() -> Path:
    """Get cache directory path"""
    if sys.platform == "win32":
        base = Path(os.environ.get("LOCALAPPDATA", "~"))
    else:
        base = Path.home() / ".cache"
        
    return base / "cmdinsight"
