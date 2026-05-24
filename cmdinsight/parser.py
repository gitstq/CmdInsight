"""
History Parser - Multi-shell command history file parser
支持多种Shell的历史文件解析器
"""

import os
import re
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from datetime import datetime
from dataclasses import dataclass, field


@dataclass
class CommandEntry:
    """Command history entry representation"""
    command: str
    timestamp: Optional[datetime] = None
    shell_type: str = "unknown"
    session_id: Optional[str] = None
    exit_code: Optional[int] = None
    
    def to_dict(self) -> Dict:
        return {
            "command": self.command,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
            "shell_type": self.shell_type,
            "session_id": self.session_id,
            "exit_code": self.exit_code,
        }


class HistoryParser:
    """
    Multi-shell command history parser
    
    Supports:
    - Bash (.bash_history)
    - Zsh (.zsh_history)
    - Fish (fish_history)
    - PowerShell (ConsoleHost_history.txt)
    """
    
    # Shell history file patterns
    SHELL_HISTORY_PATHS = {
        "bash": ".bash_history",
        "zsh": ".zsh_history", 
        "fish": ".local/share/fish/fish_history",
        "powershell": ".local/share/powershell/PSReadline/ConsoleHost_history.txt",
    }
    
    # Zsh extended history pattern: `: timestamp:duration;command`
    ZSH_EXTENDED_PATTERN = re.compile(r"^: (\d+):(\d+);(.+)$")
    
    # Fish history pattern: `- cmd: command` followed by `- when: timestamp`
    FISH_CMD_PATTERN = re.compile(r"^- cmd: (.+)$")
    FISH_TIME_PATTERN = re.compile(r"^\s+when: (\d+)$")
    
    def __init__(self, history_path: Optional[str] = None, shell_type: Optional[str] = None):
        """
        Initialize history parser
        
        Args:
            history_path: Custom path to history file
            shell_type: Shell type (bash, zsh, fish, powershell)
        """
        self.history_path = history_path
        self.shell_type = shell_type or self._detect_shell_type()
        
    def _detect_shell_type(self) -> str:
        """Detect current shell type from environment"""
        shell = os.environ.get("SHELL", "").lower()
        if "zsh" in shell:
            return "zsh"
        elif "bash" in shell:
            return "bash"
        elif "fish" in shell:
            return "fish"
        elif "powershell" in shell.lower() or "pwsh" in shell:
            return "powershell"
        return "bash"  # Default fallback
        
    def _get_history_path(self) -> Path:
        """Get the path to history file"""
        if self.history_path:
            return Path(self.history_path).expanduser()
            
        home = Path.home()
        history_file = self.SHELL_HISTORY_PATHS.get(self.shell_type)
        
        if history_file:
            return home / history_file
            
        # Fallback: try to find any history file
        for shell, path in self.SHELL_HISTORY_PATHS.items():
            full_path = home / path
            if full_path.exists():
                return full_path
                
        raise FileNotFoundError(f"No history file found for shell: {self.shell_type}")
        
    def parse(self, limit: Optional[int] = None) -> List[CommandEntry]:
        """
        Parse command history file
        
        Args:
            limit: Maximum number of entries to parse
            
        Returns:
            List of CommandEntry objects
        """
        try:
            history_path = self._get_history_path()
        except FileNotFoundError:
            return []
            
        if not history_path.exists():
            return []
            
        with open(history_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
            
        if self.shell_type == "zsh":
            entries = self._parse_zsh(content)
        elif self.shell_type == "fish":
            entries = self._parse_fish(content)
        elif self.shell_type == "powershell":
            entries = self._parse_powershell(content)
        else:
            entries = self._parse_bash(content)
            
        if limit and limit > 0:
            entries = entries[-limit:]
            
        return entries
        
    def _parse_bash(self, content: str) -> List[CommandEntry]:
        """Parse Bash history format"""
        entries = []
        lines = content.strip().split("\n")
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            entries.append(CommandEntry(
                command=line,
                shell_type="bash"
            ))
            
        return entries
        
    def _parse_zsh(self, content: str) -> List[CommandEntry]:
        """Parse Zsh history format (supports extended format)"""
        entries = []
        lines = content.strip().split("\n")
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Check for extended format
            match = self.ZSH_EXTENDED_PATTERN.match(line)
            if match:
                timestamp_str, _, command = match.groups()
                try:
                    timestamp = datetime.fromtimestamp(int(timestamp_str))
                except (ValueError, OSError):
                    timestamp = None
                entries.append(CommandEntry(
                    command=command,
                    timestamp=timestamp,
                    shell_type="zsh"
                ))
            else:
                entries.append(CommandEntry(
                    command=line,
                    shell_type="zsh"
                ))
                
        return entries
        
    def _parse_fish(self, content: str) -> List[CommandEntry]:
        """Parse Fish shell history format"""
        entries = []
        lines = content.strip().split("\n")
        
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            
            cmd_match = self.FISH_CMD_PATTERN.match(line)
            if cmd_match:
                command = cmd_match.group(1)
                timestamp = None
                
                # Look for timestamp on next line
                if i + 1 < len(lines):
                    time_match = self.FISH_TIME_PATTERN.match(lines[i + 1])
                    if time_match:
                        try:
                            timestamp = datetime.fromtimestamp(int(time_match.group(1)))
                            i += 1
                        except (ValueError, OSError):
                            pass
                            
                entries.append(CommandEntry(
                    command=command,
                    timestamp=timestamp,
                    shell_type="fish"
                ))
            i += 1
            
        return entries
        
    def _parse_powershell(self, content: str) -> List[CommandEntry]:
        """Parse PowerShell history format"""
        entries = []
        lines = content.strip().split("\n")
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            entries.append(CommandEntry(
                command=line,
                shell_type="powershell"
            ))
            
        return entries
        
    def get_history_stats(self) -> Dict:
        """Get basic statistics about history file"""
        try:
            history_path = self._get_history_path()
            stat = history_path.stat()
            entries = self.parse()
            
            return {
                "path": str(history_path),
                "shell_type": self.shell_type,
                "total_commands": len(entries),
                "file_size_bytes": stat.st_size,
                "last_modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
            }
        except (FileNotFoundError, OSError):
            return {
                "path": None,
                "shell_type": self.shell_type,
                "total_commands": 0,
                "file_size_bytes": 0,
                "last_modified": None,
            }
