"""
Pytest configuration and fixtures
"""
import pytest
import os
from pathlib import Path


@pytest.fixture
def test_env():
    """Set up test environment variables"""
    os.environ["GITHUB_APP_ID"] = "123456"
    os.environ["GITHUB_WEBHOOK_SECRET"] = "test_secret"
    os.environ["GITHUB_APP_PRIVATE_KEY_PATH"] = "./tests/fixtures/test_key.pem"
    yield
    # Cleanup
    for key in ["GITHUB_APP_ID", "GITHUB_WEBHOOK_SECRET", "GITHUB_APP_PRIVATE_KEY_PATH"]:
        os.environ.pop(key, None)


@pytest.fixture
def sample_webhook_payload():
    """Sample GitHub webhook payload"""
    return {
        "action": "created",
        "issue": {
            "number": 1,
            "title": "Test Issue",
            "user": {"login": "testuser"}
        },
        "comment": {
            "body": "/test ci.yml",
            "user": {"login": "testuser"}
        },
        "repository": {
            "full_name": "testuser/testrepo",
            "name": "testrepo",
            "owner": {"login": "testuser"}
        },
        "installation": {
            "id": 12345
        }
    }


@pytest.fixture
def sample_pr_payload():
    """Sample pull request payload"""
    return {
        "action": "opened",
        "number": 1,
        "pull_request": {
            "number": 1,
            "title": "Test PR",
            "state": "open",
            "user": {"login": "testuser"},
            "head": {"ref": "feature-branch"},
            "mergeable": True,
            "merged": False
        },
        "repository": {
            "full_name": "testuser/testrepo"
        },
        "installation": {
            "id": 12345
        }
    }
