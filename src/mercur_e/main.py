"""
MERCUR-E GitHub Bot - Main Application
FastAPI server with webhook handling and AI integration
"""
from fastapi import FastAPI, Request, HTTPException, Header, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import Any
import json
from loguru import logger
import sys

from .config import settings
from .security import verify_webhook_signature, verify_webhook_signature_sha1
from .github_auth import github_auth
from .commands import CommandHandler, CommandParser

# Configure logging
logger.remove()
logger.add(
    sys.stderr,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
    level=settings.log_level
)
logger.add(
    settings.log_file,
    rotation="10 MB",
    retention="30 days",
    level=settings.log_level
)

# Initialize FastAPI app
app = FastAPI(
    title="MERCUR-E GitHub Bot",
    description="AI-powered GitHub App for repository automation",
    version="1.0.0"
)

# Configure CORS
origins = settings.allowed_origins.split(',') if settings.allowed_origins != '*' else ['*']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "app": "MERCUR-E GitHub Bot",
        "version": "1.0.0"
    }


@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "github_app_id": settings.github_app_id,
        "fastmcp_enabled": settings.fastmcp_enabled,
        "pam_enabled": settings.pam_enabled
    }


async def process_webhook_event(event_type: str, payload: Dict[str, Any]):
    """
    Process GitHub webhook events
    
    Args:
        event_type: Type of GitHub event
        payload: Event payload
    """
    try:
        logger.info(f"Processing {event_type} event")
        
        # Extract common information
        repository = payload.get('repository', {})
        repo_name = repository.get('full_name', 'unknown')
        installation_id = payload.get('installation', {}).get('id')
        
        if not installation_id:
            logger.warning(f"No installation ID found in {event_type} event")
            return
        
        # Get GitHub client
        gh = github_auth.get_github_client(installation_id)
        repo = gh.get_repo(repo_name)
        
        # Handle different event types
        if event_type == 'issue_comment':
            await handle_issue_comment(payload, gh, repo)
        elif event_type == 'pull_request':
            await handle_pull_request(payload, gh, repo)
        elif event_type == 'push':
            await handle_push(payload, gh, repo)
        else:
            logger.info(f"Event type {event_type} not handled")
            
    except Exception as e:
        logger.error(f"Error processing webhook event: {e}", exc_info=True)


async def handle_issue_comment(payload: Dict[str, Any], gh, repo):
    """Handle issue_comment events"""
    action = payload.get('action')
    comment = payload.get('comment', {})
    issue = payload.get('issue', {})
    
    # Only process created comments
    if action != 'created':
        return
    
    comment_body = comment.get('body', '')
    comment_author = comment.get('user', {}).get('login', 'unknown')
    
    logger.info(f"Processing comment from {comment_author}: {comment_body[:50]}...")
    
    # Parse commands
    commands = CommandParser.parse_commands(comment_body)
    
    if not commands:
        logger.info("No commands found in comment")
        return
    
    logger.info(f"Found {len(commands)} command(s): {[c['command'] for c in commands]}")
    
    # Get PR or issue object
    issue_number = issue.get('number')
    is_pull_request = 'pull_request' in issue
    
    if is_pull_request:
        pr = repo.get_pull(issue_number)
        issue_obj = None
    else:
        pr = None
        issue_obj = repo.get_issue(issue_number)
    
    # Create command handler
    handler = CommandHandler(gh, repo)
    
    # Execute commands
    results = []
    for cmd in commands:
        command = cmd['command']
        args = cmd['args']
        
        logger.info(f"Executing command: /{command} {args}")
        
        if command == 'test':
            result = await handler.handle_test_command(pr, issue_obj, args)
        elif command == 'merge':
            if not pr:
                result = {'success': False, 'message': '❌ /merge can only be used on pull requests'}
            else:
                result = await handler.handle_merge_command(pr, args)
        elif command == 'report':
            result = await handler.handle_report_command(pr, issue_obj, args)
        else:
            result = {'success': False, 'message': f'❌ Unknown command: /{command}'}
        
        results.append(result)
        
        # Post result as comment
        if pr:
            pr.create_comment(result['message'])
        elif issue_obj:
            issue_obj.create_comment(result['message'])
    
    logger.info(f"Executed {len(results)} command(s)")


async def handle_pull_request(payload: Dict[str, Any], gh, repo):
    """Handle pull_request events"""
    action = payload.get('action')
    pr_data = payload.get('pull_request', {})
    pr_number = pr_data.get('number')
    
    logger.info(f"Pull request #{pr_number} action: {action}")
    
    # Handle specific PR actions
    if action == 'opened':
        pr = repo.get_pull(pr_number)
        welcome_message = (
            f"👋 Thanks for opening this pull request!\n\n"
            f"Available commands:\n"
            f"- `/test [workflow]` - Trigger CI workflow\n"
            f"- `/merge [method]` - Merge this PR (squash/merge/rebase)\n"
            f"- `/report` - Generate status report\n"
        )
        pr.create_comment(welcome_message)
    
    elif action == 'synchronize':
        # PR was updated with new commits
        logger.info(f"PR #{pr_number} synchronized with new commits")


async def handle_push(payload: Dict[str, Any], gh, repo):
    """Handle push events"""
    ref = payload.get('ref', '')
    pusher = payload.get('pusher', {}).get('name', 'unknown')
    commits = payload.get('commits', [])
    
    logger.info(f"Push to {ref} by {pusher} with {len(commits)} commit(s)")
    
    # You can add custom logic here, e.g., auto-deploy on push to main
    if ref == f"refs/heads/{repo.default_branch}":
        logger.info(f"Push to default branch {repo.default_branch}")


@app.post("/webhook")
async def webhook(
    request: Request,
    background_tasks: BackgroundTasks,
    x_hub_signature_256: Optional[str] = Header(None),
    x_hub_signature: Optional[str] = Header(None),
    x_github_event: Optional[str] = Header(None)
):
    """
    GitHub webhook endpoint
    
    Handles incoming webhook events from GitHub
    """
    # Read raw body for signature verification
    body = await request.body()
    
    # Verify webhook signature
    signature_valid = False
    if x_hub_signature_256:
        signature_valid = verify_webhook_signature(body, x_hub_signature_256)
    elif x_hub_signature:
        signature_valid = verify_webhook_signature_sha1(body, x_hub_signature)
    
    if not signature_valid:
        logger.warning("Invalid webhook signature")
        raise HTTPException(status_code=401, detail="Invalid signature")
    
    # Parse JSON payload
    try:
        payload = json.loads(body)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON")
    
    # Log event
    logger.info(f"Received {x_github_event} event")
    
    # Process event in background
    background_tasks.add_task(process_webhook_event, x_github_event, payload)
    
    return JSONResponse(
        status_code=200,
        content={"status": "accepted", "event": x_github_event}
    )


@app.post("/api/parse-comment")
async def parse_comment_api(request: Request):
    """
    API endpoint to parse comments for commands
    Used by AI integration
    """
    data = await request.json()
    comment_text = data.get('comment', '')
    
    commands = CommandParser.parse_commands(comment_text)
    
    return {
        "success": True,
        "commands": commands,
        "count": len(commands)
    }


@app.get("/api/status")
async def get_status():
    """Get bot status and statistics"""
    return {
        "status": "operational",
        "app_id": settings.github_app_id,
        "features": {
            "commands": ["test", "merge", "report"],
            "events": ["issue_comment", "pull_request", "push"],
            "ai_integration": settings.fastmcp_enabled,
            "pam_auth": settings.pam_enabled
        }
    }


def main():
    """Main entry point for the application"""
    import uvicorn
    
    logger.info("Starting MERCUR-E GitHub Bot")
    logger.info(f"GitHub App ID: {settings.github_app_id}")
    logger.info(f"FastMCP enabled: {settings.fastmcp_enabled}")
    logger.info(f"PAM authentication enabled: {settings.pam_enabled}")
    
    # Run server
    uvicorn.run(
        "mercur_e.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    )


if __name__ == "__main__":
    main()
