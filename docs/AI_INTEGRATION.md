# 🤖 AI Integration Guide - MERCUR-E GitHub Bot

Complete guide for integrating AI assistants with your GitHub bot using FastMCP.

## 📋 Overview

The MERCUR-E GitHub Bot exposes a FastMCP server that allows AI assistants (like Claude, GPT, or custom models) to:

- Parse GitHub comments and extract commands
- Analyze pull requests and provide insights
- Suggest appropriate bot commands based on context
- Generate comprehensive reports
- Monitor workflow runs

## 🚀 Quick Start

### 1. Start the MCP Server

```bash
# In a separate terminal from the main bot
./run_mcp.sh
```

The MCP server will start on port 8001 (configurable in `.env`).

### 2. Configure Your AI Assistant

Point your AI assistant to the MCP server:

```
MCP Server URL: http://localhost:8001
```

For remote access:
```
MCP Server URL: https://bot.yourdomain.com:8001
```

## 🔧 Available MCP Tools

### 1. parse_github_comment

Parse GitHub comments to extract bot commands.

**Input:**
```json
{
  "comment_text": "/test ci.yml\n/merge squash\n/report"
}
```

**Output:**
```json
{
  "success": true,
  "commands": [
    {"command": "test", "args": "ci.yml"},
    {"command": "merge", "args": "squash"},
    {"command": "report", "args": ""}
  ],
  "count": 3
}
```

**AI Use Case:**
- Extract actionable commands from natural language
- Validate command syntax
- Count commands in a comment

### 2. analyze_pull_request

Get comprehensive analysis of a pull request.

**Input:**
```json
{
  "owner": "username",
  "repo": "repository",
  "pr_number": 123
}
```

**Output:**
```json
{
  "success": true,
  "pr": {
    "number": 123,
    "title": "Add new feature",
    "state": "open",
    "author": "developer",
    "mergeable": true,
    "merged": false,
    "draft": false,
    "additions": 150,
    "deletions": 30,
    "changed_files": 5,
    "commits": 3,
    "comments": 2,
    "review_comments": 1
  },
  "ci_status": {
    "state": "success",
    "total_count": 3
  },
  "files": [...],
  "labels": ["feature", "ready-for-review"]
}
```

**AI Use Case:**
- Assess PR readiness for merge
- Identify potential issues
- Generate summary reports
- Recommend next actions

### 3. get_repository_info

Fetch repository metadata and settings.

**Input:**
```json
{
  "owner": "username",
  "repo": "repository"
}
```

**Output:**
```json
{
  "success": true,
  "repository": {
    "name": "repository",
    "full_name": "username/repository",
    "description": "Project description",
    "private": false,
    "default_branch": "main",
    "language": "Python",
    "stars": 42,
    "forks": 7,
    "open_issues": 3,
    "has_issues": true,
    "has_projects": true,
    "has_wiki": true,
    "archived": false
  }
}
```

**AI Use Case:**
- Understand repository context
- Check repository settings
- Gather statistics

### 4. suggest_command

Get AI-powered command suggestions based on context.

**Input:**
```json
{
  "context": "PR has passing CI and is approved",
  "pr_state": "open",
  "ci_status": "success"
}
```

**Output:**
```json
{
  "success": true,
  "suggestions": [
    {
      "command": "/merge",
      "description": "Merge the pull request",
      "usage": "/merge [squash|merge|rebase]"
    }
  ],
  "count": 1
}
```

**AI Use Case:**
- Recommend appropriate actions
- Help users discover commands
- Context-aware suggestions

### 5. get_workflow_runs

Retrieve recent workflow run history.

**Input:**
```json
{
  "owner": "username",
  "repo": "repository",
  "limit": 10
}
```

**Output:**
```json
{
  "success": true,
  "runs": [
    {
      "id": 123456,
      "name": "CI",
      "status": "completed",
      "conclusion": "success",
      "created_at": "2024-10-26T12:00:00Z",
      "updated_at": "2024-10-26T12:05:00Z",
      "head_branch": "main",
      "head_sha": "abc1234"
    }
  ],
  "count": 10
}
```

**AI Use Case:**
- Monitor CI/CD pipeline
- Identify failing workflows
- Track deployment history

## 🎯 AI Assistant Integration Examples

### Example 1: Claude Desktop

Configure in `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "mercur-e-bot": {
      "command": "python",
      "args": ["/path/to/githubbot/mcp_server.py"],
      "env": {
        "GITHUB_APP_ID": "123456"
      }
    }
  }
}
```

### Example 2: Custom AI Integration

```python
import requests

# Connect to MCP server
MCP_URL = "http://localhost:8001"

# Analyze a PR
response = requests.post(
    f"{MCP_URL}/tools/analyze_pull_request",
    json={
        "owner": "myorg",
        "repo": "myrepo",
        "pr_number": 42
    }
)

pr_data = response.json()

# AI processes the data and suggests action
if pr_data["pr"]["mergeable"] and pr_data["ci_status"]["state"] == "success":
    print("Suggestion: Use /merge squash to merge this PR")
```

### Example 3: Automated PR Review Assistant

```python
# AI-powered PR review workflow

def ai_review_pr(owner, repo, pr_number):
    # 1. Analyze PR
    pr_analysis = analyze_pull_request(owner, repo, pr_number)
    
    # 2. Check CI status
    if pr_analysis["ci_status"]["state"] != "success":
        return "Wait for CI to pass before merging"
    
    # 3. Check file changes
    if pr_analysis["pr"]["changed_files"] > 50:
        return "Large PR - consider breaking into smaller changes"
    
    # 4. Suggest command
    if pr_analysis["pr"]["mergeable"]:
        return "Ready to merge! Use: /merge squash"
    else:
        return "Resolve merge conflicts first"
```

## 🔐 Security Considerations

### 1. Authentication

For production, secure your MCP server:

```python
# Add authentication to MCP server
from fastapi import Header, HTTPException

@mcp.tool()
async def secure_tool(api_key: str = Header(...)):
    if api_key != "your-secret-key":
        raise HTTPException(status_code=401)
    # Tool logic here
```

### 2. Rate Limiting

Implement rate limiting for AI requests:

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@mcp.tool()
@limiter.limit("10/minute")
async def rate_limited_tool():
    # Tool logic here
```

### 3. Network Security

For remote access:
- Use HTTPS/TLS
- Implement IP whitelisting
- Use VPN or SSH tunneling

## 📊 Advanced Use Cases

### Use Case 1: Intelligent PR Triage

AI analyzes PRs and automatically:
- Labels based on content
- Assigns reviewers
- Suggests merge strategy
- Identifies potential issues

```python
def intelligent_triage(pr_data):
    # AI analyzes code changes
    if "test" in pr_data["files"]:
        return {"label": "tests", "priority": "high"}
    
    if pr_data["pr"]["additions"] > 500:
        return {"label": "large-pr", "reviewers": ["senior-dev"]}
    
    return {"label": "standard", "priority": "normal"}
```

### Use Case 2: Automated Release Notes

AI generates release notes from merged PRs:

```python
def generate_release_notes(merged_prs):
    notes = []
    for pr in merged_prs:
        # AI categorizes changes
        category = categorize_pr(pr)
        notes.append(f"- [{category}] {pr['title']} (#{pr['number']})")
    
    return "\n".join(notes)
```

### Use Case 3: Code Quality Insights

AI provides code quality feedback:

```python
def quality_insights(pr_data):
    insights = []
    
    # Check test coverage
    test_files = [f for f in pr_data["files"] if "test" in f["filename"]]
    if not test_files:
        insights.append("⚠️ No test files added")
    
    # Check documentation
    doc_files = [f for f in pr_data["files"] if f["filename"].endswith(".md")]
    if not doc_files and pr_data["pr"]["changed_files"] > 5:
        insights.append("📝 Consider adding documentation")
    
    return insights
```

## 🛠️ Custom MCP Tools

### Adding Your Own Tools

Edit `mcp_server.py`:

```python
@mcp.tool()
async def custom_analysis(
    owner: str,
    repo: str,
    analysis_type: str
) -> Dict[str, Any]:
    """
    Custom analysis tool
    
    Args:
        owner: Repository owner
        repo: Repository name
        analysis_type: Type of analysis to perform
    
    Returns:
        Analysis results
    """
    # Your custom logic here
    return {
        "success": True,
        "analysis": "results"
    }
```

### Adding Resources

```python
@mcp.resource("github://custom-resource")
async def custom_resource() -> str:
    """Custom resource endpoint"""
    return json.dumps({
        "data": "custom resource data"
    })
```

## 📈 Monitoring AI Integration

### Track MCP Usage

```python
# Add logging to MCP tools
import time

@mcp.tool()
async def monitored_tool():
    start_time = time.time()
    
    # Tool logic
    result = perform_analysis()
    
    duration = time.time() - start_time
    logger.info(f"Tool executed in {duration:.2f}s")
    
    return result
```

### Metrics to Track

- Tool call frequency
- Response times
- Success/failure rates
- AI assistant usage patterns

## 🔄 Best Practices

1. **Error Handling**: Always return structured error responses
2. **Validation**: Validate all inputs before processing
3. **Caching**: Cache expensive operations (PR analysis, etc.)
4. **Logging**: Log all AI interactions for debugging
5. **Documentation**: Keep tool descriptions up-to-date
6. **Testing**: Test tools independently before AI integration

## 🆘 Troubleshooting

### MCP Server Not Starting

```bash
# Check logs
tail -f logs/githubbot.log

# Verify port is available
lsof -i :8001

# Test manually
curl http://localhost:8001/health
```

### AI Can't Connect

- Verify MCP server is running
- Check firewall rules
- Ensure correct URL/port
- Test with curl first

### Tool Errors

- Check GitHub App permissions
- Verify installation on repository
- Review error logs
- Test with API directly

## 📚 Additional Resources

- [FastMCP Documentation](https://github.com/jlowin/fastmcp)
- [GitHub API Documentation](https://docs.github.com/en/rest)
- [MCP Protocol Specification](https://modelcontextprotocol.io/)

---

Build intelligent GitHub automation with AI! 🤖✨
