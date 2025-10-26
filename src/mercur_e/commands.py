"""
Command handlers for GitHub bot slash commands
"""
import re
from typing import Any
from github import Github
from github.Repository import Repository
from github.PullRequest import PullRequest
from github.Issue import Issue
from loguru import logger


class CommandParser:
    """Parse slash commands from comments"""
    
    COMMAND_PATTERN = r'/(\w+)(?:\s+(.+))?'
    
    @staticmethod
    def parse_commands(text: str) -> list[dict[str, Any]]:
        """
        Parse slash commands from comment text
        
        Args:
            text: Comment text to parse
        
        Returns:
            List of command dictionaries with 'command' and 'args' keys
        """
        commands = []
        matches = re.finditer(CommandParser.COMMAND_PATTERN, text, re.MULTILINE)
        
        for match in matches:
            command = match.group(1).lower()
            args = match.group(2).strip() if match.group(2) else ""
            commands.append({
                'command': command,
                'args': args
            })
        
        return commands


class CommandHandler:
    """Handle bot commands"""
    
    def __init__(self, github_client: Github, repo: Repository):
        self.github = github_client
        self.repo = repo
    
    async def handle_test_command(
        self,
        pr: PullRequest | None = None,
        issue: Issue | None = None,
        args: str = ""
    ) -> dict[str, Any]:
        """
        Handle /test command - trigger GitHub Actions workflow
        
        Args:
            pr: Pull request object (if applicable)
            issue: Issue object (if applicable)
            args: Command arguments (workflow name, branch, etc.)
        
        Returns:
            Result dictionary with status and message
        """
        try:
            # Parse arguments
            workflow_name = args if args else "ci.yml"
            ref = pr.head.ref if pr else self.repo.default_branch
            
            logger.info(f"Triggering workflow '{workflow_name}' on ref '{ref}'")
            
            # Get workflow
            workflows = self.repo.get_workflows()
            target_workflow = None
            
            for workflow in workflows:
                if workflow.path.endswith(workflow_name) or workflow.name == workflow_name:
                    target_workflow = workflow
                    break
            
            if not target_workflow:
                return {
                    'success': False,
                    'message': f"❌ Workflow '{workflow_name}' not found"
                }
            
            # Trigger workflow
            success = target_workflow.create_dispatch(ref=ref)
            
            if success:
                message = f"✅ Triggered workflow '{workflow_name}' on branch '{ref}'"
                logger.info(message)
                return {'success': True, 'message': message}
            else:
                message = f"❌ Failed to trigger workflow '{workflow_name}'"
                logger.error(message)
                return {'success': False, 'message': message}
                
        except Exception as e:
            error_msg = f"❌ Error triggering workflow: {str(e)}"
            logger.error(error_msg)
            return {'success': False, 'message': error_msg}
    
    async def handle_merge_command(
        self,
        pr: PullRequest,
        args: str = ""
    ) -> dict[str, Any]:
        """
        Handle /merge command - merge pull request
        
        Args:
            pr: Pull request object
            args: Merge method (squash, merge, rebase)
        
        Returns:
            Result dictionary with status and message
        """
        try:
            # Parse merge method
            merge_method = args.lower() if args in ['squash', 'merge', 'rebase'] else 'squash'
            
            logger.info(f"Attempting to merge PR #{pr.number} using {merge_method} method")
            
            # Check if PR is mergeable
            if pr.mergeable is False:
                return {
                    'success': False,
                    'message': "❌ Pull request has merge conflicts and cannot be merged"
                }
            
            # Check if PR is approved (optional - can be configured)
            # reviews = pr.get_reviews()
            # approved = any(review.state == 'APPROVED' for review in reviews)
            
            # Check CI status
            commit = pr.get_commits().reversed[0]
            statuses = commit.get_combined_status()
            
            if statuses.state not in ['success', 'pending']:
                return {
                    'success': False,
                    'message': f"❌ Cannot merge: CI checks are {statuses.state}"
                }
            
            # Perform merge
            merge_result = pr.merge(
                merge_method=merge_method,
                commit_title=f"Merge PR #{pr.number}: {pr.title}",
                commit_message=f"Merged via GitHub Bot using {merge_method} method"
            )
            
            if merge_result.merged:
                message = f"✅ Successfully merged PR #{pr.number} using {merge_method} method"
                logger.info(message)
                return {'success': True, 'message': message}
            else:
                message = f"❌ Failed to merge PR #{pr.number}"
                logger.error(message)
                return {'success': False, 'message': message}
                
        except Exception as e:
            error_msg = f"❌ Error merging PR: {str(e)}"
            logger.error(error_msg)
            return {'success': False, 'message': error_msg}
    
    async def handle_report_command(
        self,
        pr: PullRequest | None = None,
        issue: Issue | None = None,
        args: str = ""
    ) -> dict[str, Any]:
        """
        Handle /report command - post status report
        
        Args:
            pr: Pull request object (if applicable)
            issue: Issue object (if applicable)
            args: Report type or custom message
        
        Returns:
            Result dictionary with status and message
        """
        try:
            target = pr or issue
            if not target:
                return {
                    'success': False,
                    'message': "❌ No PR or issue context for report"
                }
            
            logger.info(f"Generating report for {'PR' if pr else 'issue'} #{target.number}")
            
            # Generate report based on type
            if pr:
                report = self._generate_pr_report(pr, args)
            else:
                report = self._generate_issue_report(issue, args)
            
            # Post comment
            target.create_comment(report)
            
            message = f"✅ Posted report on {'PR' if pr else 'issue'} #{target.number}"
            logger.info(message)
            return {'success': True, 'message': message}
            
        except Exception as e:
            error_msg = f"❌ Error generating report: {str(e)}"
            logger.error(error_msg)
            return {'success': False, 'message': error_msg}
    
    def _generate_pr_report(self, pr: PullRequest, report_type: str) -> str:
        """Generate PR status report"""
        report = f"## 📊 Pull Request Report\n\n"
        report += f"**PR:** #{pr.number} - {pr.title}\n"
        report += f"**Author:** @{pr.user.login}\n"
        report += f"**Status:** {pr.state}\n"
        report += f"**Mergeable:** {'✅ Yes' if pr.mergeable else '❌ No'}\n\n"
        
        # CI Status
        commit = pr.get_commits().reversed[0]
        statuses = commit.get_combined_status()
        report += f"**CI Status:** {statuses.state}\n\n"
        
        # Check details
        if statuses.statuses:
            report += "### Check Details\n"
            for status in statuses.statuses:
                emoji = "✅" if status.state == "success" else "❌" if status.state == "failure" else "⏳"
                report += f"- {emoji} **{status.context}**: {status.state}\n"
        
        # Files changed
        report += f"\n**Files Changed:** {pr.changed_files}\n"
        report += f"**Additions:** +{pr.additions} | **Deletions:** -{pr.deletions}\n"
        
        return report
    
    def _generate_issue_report(self, issue: Issue, report_type: str) -> str:
        """Generate issue status report"""
        report = f"## 📋 Issue Report\n\n"
        report += f"**Issue:** #{issue.number} - {issue.title}\n"
        report += f"**Author:** @{issue.user.login}\n"
        report += f"**Status:** {issue.state}\n"
        report += f"**Labels:** {', '.join([label.name for label in issue.labels])}\n"
        report += f"**Comments:** {issue.comments}\n"
        
        return report
