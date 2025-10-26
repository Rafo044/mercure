"""
FastMCP Server for AI Integration - MERCUR-E
Exposes GitHub bot functionality to AI assistants
"""
from fastmcp import FastMCP
from typing import Any
from loguru import logger
from .github_auth import github_auth
from .commands import CommandHandler, CommandParser
import json


# Initialize FastMCP server
mcp = FastMCP("MERCUR-E GitHub Bot")


def main():
    """Main entry point for MCP server"""
    logger.info("Starting FastMCP server for MERCUR-E GitHub Bot")
    mcp.run()


@mcp.tool()
async def parse_github_comment(comment_text: str) -> dict[str, Any]:
    """
    Parse GitHub comment for bot commands
    
    Args:
        comment_text: The text of the GitHub comment
    
    Returns:
        Dictionary containing parsed commands
    """
    try:
        commands = CommandParser.parse_commands(comment_text)
        return {
            "success": True,
            "commands": commands,
            "count": len(commands)
        }
    except Exception as e:
        logger.error(f"Error parsing comment: {e}")
        return {
            "success": False,
            "error": str(e)
        }


@mcp.tool()
async def analyze_pull_request(
    owner: str,
    repo: str,
    pr_number: int
) -> dict[str, Any]:
    """
    Analyze a pull request and provide insights
    
    Args:
        owner: Repository owner
        repo: Repository name
        pr_number: Pull request number
    
    Returns:
        Dictionary containing PR analysis
    """
    try:
        installation_id = github_auth.get_installation_id_for_repo(owner, repo)
        if not installation_id:
            return {"success": False, "error": "Installation not found"}
        
        gh = github_auth.get_github_client(installation_id)
        repository = gh.get_repo(f"{owner}/{repo}")
        pr = repository.get_pull(pr_number)
        
        # Gather PR information
        commit = pr.get_commits().reversed[0]
        statuses = commit.get_combined_status()
        
        files_changed = []
        for file in pr.get_files():
            files_changed.append({
                "filename": file.filename,
                "status": file.status,
                "additions": file.additions,
                "deletions": file.deletions,
                "changes": file.changes
            })
        
        analysis = {
            "success": True,
            "pr": {
                "number": pr.number,
                "title": pr.title,
                "state": pr.state,
                "author": pr.user.login,
                "mergeable": pr.mergeable,
                "merged": pr.merged,
                "draft": pr.draft,
                "additions": pr.additions,
                "deletions": pr.deletions,
                "changed_files": pr.changed_files,
                "commits": pr.commits,
                "comments": pr.comments,
                "review_comments": pr.review_comments
            },
            "ci_status": {
                "state": statuses.state,
                "total_count": statuses.total_count
            },
            "files": files_changed[:10],  # Limit to first 10 files
            "labels": [label.name for label in pr.labels]
        }
        
        return analysis
        
    except Exception as e:
        logger.error(f"Error analyzing PR: {e}")
        return {
            "success": False,
            "error": str(e)
        }


@mcp.tool()
async def get_repository_info(owner: str, repo: str) -> dict[str, Any]:
    """
    Get repository information and metadata
    
    Args:
        owner: Repository owner
        repo: Repository name
    
    Returns:
        Dictionary containing repository information
    """
    try:
        installation_id = github_auth.get_installation_id_for_repo(owner, repo)
        if not installation_id:
            return {"success": False, "error": "Installation not found"}
        
        gh = github_auth.get_github_client(installation_id)
        repository = gh.get_repo(f"{owner}/{repo}")
        
        info = {
            "success": True,
            "repository": {
                "name": repository.name,
                "full_name": repository.full_name,
                "description": repository.description,
                "private": repository.private,
                "default_branch": repository.default_branch,
                "language": repository.language,
                "stars": repository.stargazers_count,
                "forks": repository.forks_count,
                "open_issues": repository.open_issues_count,
                "has_issues": repository.has_issues,
                "has_projects": repository.has_projects,
                "has_wiki": repository.has_wiki,
                "archived": repository.archived
            }
        }
        
        return info
        
    except Exception as e:
        logger.error(f"Error getting repository info: {e}")
        return {
            "success": False,
            "error": str(e)
        }


@mcp.tool()
async def suggest_command(
    context: str,
    pr_state: str | None = None,
    ci_status: str | None = None
) -> dict[str, Any]:
    """
    Suggest appropriate bot command based on context
    
    Args:
        context: Description of the current situation
        pr_state: Current PR state (open, closed, merged)
        ci_status: Current CI status (success, failure, pending)
    
    Returns:
        Dictionary containing suggested command
    """
    try:
        suggestions = []
        
        # Analyze context and suggest commands
        context_lower = context.lower()
        
        if "test" in context_lower or "ci" in context_lower:
            suggestions.append({
                "command": "/test",
                "description": "Trigger GitHub Actions workflow",
                "usage": "/test [workflow_name]"
            })
        
        if "merge" in context_lower and pr_state == "open" and ci_status == "success":
            suggestions.append({
                "command": "/merge",
                "description": "Merge the pull request",
                "usage": "/merge [squash|merge|rebase]"
            })
        
        if "report" in context_lower or "status" in context_lower:
            suggestions.append({
                "command": "/report",
                "description": "Generate status report",
                "usage": "/report"
            })
        
        return {
            "success": True,
            "suggestions": suggestions,
            "count": len(suggestions)
        }
        
    except Exception as e:
        logger.error(f"Error suggesting command: {e}")
        return {
            "success": False,
            "error": str(e)
        }


@mcp.tool()
async def get_workflow_runs(
    owner: str,
    repo: str,
    limit: int = 10
) -> dict[str, Any]:
    """
    Get recent workflow runs for a repository
    
    Args:
        owner: Repository owner
        repo: Repository name
        limit: Maximum number of runs to return
    
    Returns:
        Dictionary containing workflow run information
    """
    try:
        installation_id = github_auth.get_installation_id_for_repo(owner, repo)
        if not installation_id:
            return {"success": False, "error": "Installation not found"}
        
        gh = github_auth.get_github_client(installation_id)
        repository = gh.get_repo(f"{owner}/{repo}")
        
        runs = []
        for run in repository.get_workflow_runs()[:limit]:
            runs.append({
                "id": run.id,
                "name": run.name,
                "status": run.status,
                "conclusion": run.conclusion,
                "created_at": run.created_at.isoformat(),
                "updated_at": run.updated_at.isoformat(),
                "head_branch": run.head_branch,
                "head_sha": run.head_sha[:7]
            })
        
        return {
            "success": True,
            "runs": runs,
            "count": len(runs)
        }
        
    except Exception as e:
        logger.error(f"Error getting workflow runs: {e}")
        return {
            "success": False,
            "error": str(e)
        }


@mcp.resource("github://events")
async def get_recent_events() -> str:
    """
    Get recent GitHub events processed by the bot
    
    Returns:
        JSON string containing recent events
    """
    # This would be connected to an event store in production
    return json.dumps({
        "message": "Event history not yet implemented",
        "events": []
    })


if __name__ == "__main__":
    main()
