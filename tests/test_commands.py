"""
Tests for command parsing and handling
"""
import pytest
from unittest.mock import Mock, AsyncMock, patch
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from mercur_e.commands import CommandParser, CommandHandler


class TestCommandParser:
    """Test command parsing functionality"""
    
    def test_parse_single_command(self):
        """Test parsing a single command"""
        text = "/test ci.yml"
        commands = CommandParser.parse_commands(text)
        
        assert len(commands) == 1
        assert commands[0]['command'] == 'test'
        assert commands[0]['args'] == 'ci.yml'
    
    def test_parse_multiple_commands(self):
        """Test parsing multiple commands"""
        text = "/test\n/merge squash\n/report"
        commands = CommandParser.parse_commands(text)
        
        assert len(commands) == 3
        assert commands[0]['command'] == 'test'
        assert commands[1]['command'] == 'merge'
        assert commands[1]['args'] == 'squash'
        assert commands[2]['command'] == 'report'
    
    def test_parse_command_without_args(self):
        """Test parsing command without arguments"""
        text = "/report"
        commands = CommandParser.parse_commands(text)
        
        assert len(commands) == 1
        assert commands[0]['command'] == 'report'
        assert commands[0]['args'] == ''
    
    def test_parse_no_commands(self):
        """Test parsing text with no commands"""
        text = "This is just a regular comment"
        commands = CommandParser.parse_commands(text)
        
        assert len(commands) == 0
    
    def test_parse_mixed_content(self):
        """Test parsing text with commands and regular text"""
        text = "Here's my review:\n/test\nLooks good!\n/merge squash"
        commands = CommandParser.parse_commands(text)
        
        assert len(commands) == 2
        assert commands[0]['command'] == 'test'
        assert commands[1]['command'] == 'merge'


class TestCommandHandler:
    """Test command handler functionality"""
    
    @pytest.fixture
    def mock_github(self):
        """Mock GitHub client"""
        return Mock()
    
    @pytest.fixture
    def mock_repo(self):
        """Mock repository"""
        repo = Mock()
        repo.default_branch = "main"
        return repo
    
    @pytest.fixture
    def handler(self, mock_github, mock_repo):
        """Create command handler instance"""
        return CommandHandler(mock_github, mock_repo)
    
    @pytest.mark.asyncio
    async def test_handle_test_command_success(self, handler, mock_repo):
        """Test successful test command execution"""
        # Mock workflow
        mock_workflow = Mock()
        mock_workflow.path = "ci.yml"
        mock_workflow.create_dispatch = Mock(return_value=True)
        
        mock_workflows = Mock()
        mock_workflows.__iter__ = Mock(return_value=iter([mock_workflow]))
        mock_repo.get_workflows = Mock(return_value=mock_workflows)
        
        result = await handler.handle_test_command(args="ci.yml")
        
        assert result['success'] is True
        assert 'Triggered workflow' in result['message']
    
    @pytest.mark.asyncio
    async def test_handle_test_command_workflow_not_found(self, handler, mock_repo):
        """Test test command with non-existent workflow"""
        mock_workflows = Mock()
        mock_workflows.__iter__ = Mock(return_value=iter([]))
        mock_repo.get_workflows = Mock(return_value=mock_workflows)
        
        result = await handler.handle_test_command(args="nonexistent.yml")
        
        assert result['success'] is False
        assert 'not found' in result['message']
    
    @pytest.mark.asyncio
    async def test_handle_merge_command_success(self, handler):
        """Test successful merge command"""
        mock_pr = Mock()
        mock_pr.number = 123
        mock_pr.mergeable = True
        mock_pr.title = "Test PR"
        
        # Mock commit and status
        mock_commit = Mock()
        mock_status = Mock()
        mock_status.state = "success"
        mock_commit.get_combined_status = Mock(return_value=mock_status)
        
        mock_commits = Mock()
        mock_commits.reversed = [mock_commit]
        mock_pr.get_commits = Mock(return_value=mock_commits)
        
        # Mock merge result
        mock_merge_result = Mock()
        mock_merge_result.merged = True
        mock_pr.merge = Mock(return_value=mock_merge_result)
        
        result = await handler.handle_merge_command(mock_pr, "squash")
        
        assert result['success'] is True
        assert 'Successfully merged' in result['message']
    
    @pytest.mark.asyncio
    async def test_handle_merge_command_not_mergeable(self, handler):
        """Test merge command on non-mergeable PR"""
        mock_pr = Mock()
        mock_pr.mergeable = False
        
        result = await handler.handle_merge_command(mock_pr, "squash")
        
        assert result['success'] is False
        assert 'merge conflicts' in result['message']
    
    @pytest.mark.asyncio
    async def test_handle_report_command_pr(self, handler):
        """Test report command on PR"""
        mock_pr = Mock()
        mock_pr.number = 123
        mock_pr.title = "Test PR"
        mock_pr.state = "open"
        mock_pr.user = Mock(login="testuser")
        mock_pr.mergeable = True
        mock_pr.changed_files = 5
        mock_pr.additions = 100
        mock_pr.deletions = 50
        
        # Mock commit and status
        mock_commit = Mock()
        mock_status = Mock()
        mock_status.state = "success"
        mock_status.statuses = []
        mock_commit.get_combined_status = Mock(return_value=mock_status)
        
        mock_commits = Mock()
        mock_commits.reversed = [mock_commit]
        mock_pr.get_commits = Mock(return_value=mock_commits)
        
        mock_pr.create_comment = Mock()
        
        result = await handler.handle_report_command(pr=mock_pr)
        
        assert result['success'] is True
        assert 'Posted report' in result['message']
        mock_pr.create_comment.assert_called_once()
