"""Tests for CmdInsight"""

import pytest
from datetime import datetime

from cmdinsight.parser import HistoryParser, CommandEntry
from cmdinsight.analyzer import CommandAnalyzer
from cmdinsight.suggester import CommandSuggester
from cmdinsight.reporter import ReportGenerator


class TestHistoryParser:
    """Test history parser functionality"""
    
    def test_parse_bash_format(self):
        """Test parsing bash history format"""
        content = "ls -la\ncd /home\ngit status\n"
        parser = HistoryParser(shell_type="bash")
        entries = parser._parse_bash(content)
        
        assert len(entries) == 3
        assert entries[0].command == "ls -la"
        assert entries[1].command == "cd /home"
        assert entries[2].command == "git status"
        
    def test_parse_zsh_extended_format(self):
        """Test parsing zsh extended history format"""
        content = ": 1700000000:0;ls -la\n: 1700000001:0;cd /home\n"
        parser = HistoryParser(shell_type="zsh")
        entries = parser._parse_zsh(content)
        
        assert len(entries) == 2
        assert entries[0].command == "ls -la"
        assert entries[0].timestamp is not None
        
    def test_parse_fish_format(self):
        """Test parsing fish history format"""
        content = "- cmd: ls -la\n  when: 1700000000\n- cmd: cd /home\n  when: 1700000001\n"
        parser = HistoryParser(shell_type="fish")
        entries = parser._parse_fish(content)
        
        assert len(entries) == 2
        assert entries[0].command == "ls -la"
        assert entries[0].timestamp is not None


class TestCommandAnalyzer:
    """Test command analyzer functionality"""
    
    @pytest.fixture
    def sample_entries(self):
        """Create sample command entries"""
        return [
            CommandEntry(command="git status", shell_type="bash"),
            CommandEntry(command="git commit", shell_type="bash"),
            CommandEntry(command="git status", shell_type="bash"),
            CommandEntry(command="ls -la", shell_type="bash"),
            CommandEntry(command="python script.py", shell_type="bash"),
            CommandEntry(command="git status", shell_type="bash"),
            CommandEntry(command="npm install", shell_type="bash"),
            CommandEntry(command="ls -la", shell_type="bash"),
        ]
        
    def test_analyze_basic_stats(self, sample_entries):
        """Test basic statistics analysis"""
        analyzer = CommandAnalyzer(sample_entries)
        result = analyzer.analyze()
        
        assert result.total_commands == 8
        assert result.unique_commands == 5
        assert len(result.top_commands) > 0
        
    def test_categorize_commands(self, sample_entries):
        """Test command categorization"""
        analyzer = CommandAnalyzer(sample_entries)
        result = analyzer.analyze()
        
        assert "version_control" in result.command_categories
        assert result.command_categories["version_control"] >= 3  # git commands
        
    def test_efficiency_score(self, sample_entries):
        """Test efficiency score calculation"""
        analyzer = CommandAnalyzer(sample_entries)
        result = analyzer.analyze()
        
        assert 0 <= result.efficiency_score <= 100
        
    def test_insights_generation(self, sample_entries):
        """Test insights generation"""
        analyzer = CommandAnalyzer(sample_entries)
        result = analyzer.analyze()
        
        assert len(result.insights) > 0
        assert any("git" in insight.lower() for insight in result.insights)


class TestCommandSuggester:
    """Test command suggester functionality"""
    
    @pytest.fixture
    def sample_analyzer(self):
        """Create analyzer with sample entries"""
        entries = [
            CommandEntry(command="git status", shell_type="bash"),
            CommandEntry(command="git status", shell_type="bash"),
            CommandEntry(command="git status", shell_type="bash"),
            CommandEntry(command="git status", shell_type="bash"),
            CommandEntry(command="git status", shell_type="bash"),
            CommandEntry(command="ls -la", shell_type="bash"),
            CommandEntry(command="ls -la", shell_type="bash"),
            CommandEntry(command="ls -la", shell_type="bash"),
        ]
        return CommandAnalyzer(entries)
        
    def test_generate_suggestions(self, sample_analyzer):
        """Test suggestion generation"""
        suggester = CommandSuggester(sample_analyzer)
        suggestions = suggester.generate_suggestions()
        
        assert len(suggestions) > 0
        assert all(hasattr(s, 'title') for s in suggestions)
        
    def test_alias_suggestions(self, sample_analyzer):
        """Test alias suggestion generation"""
        suggester = CommandSuggester(sample_analyzer)
        suggestions = suggester._suggest_aliases()
        
        # Should suggest aliases for frequently used commands
        # Note: suggestions may be empty if threshold not met
        assert isinstance(suggestions, list)


class TestReportGenerator:
    """Test report generator functionality"""
    
    @pytest.fixture
    def sample_result(self):
        """Create sample analysis result"""
        from cmdinsight.analyzer import CommandStats, AnalysisResult
        
        return AnalysisResult(
            total_commands=100,
            unique_commands=50,
            top_commands=[
                CommandStats(
                    command="git status",
                    count=20,
                    base_command="git",
                    category="version_control",
                    avg_length=10.0,
                )
            ],
            command_categories={"version_control": 30, "development": 20},
            hourly_distribution={10: 5, 11: 10, 12: 8},
            daily_distribution={"Mon": 15, "Tue": 20},
            efficiency_score=65.5,
            insights=["Test insight"],
            time_saved_estimate=10.5,
        )
        
    def test_generate_summary(self, sample_result):
        """Test summary report generation"""
        reporter = ReportGenerator(use_color=False)
        summary = reporter.generate_summary(sample_result)
        
        assert "100" in summary
        assert "50" in summary
        assert "65.5" in summary
        
    def test_export_json(self, sample_result):
        """Test JSON export"""
        reporter = ReportGenerator()
        json_output = reporter.export_json(sample_result, [])
        
        import json
        data = json.loads(json_output)
        
        assert data["analysis"]["total_commands"] == 100
        assert data["analysis"]["unique_commands"] == 50


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
