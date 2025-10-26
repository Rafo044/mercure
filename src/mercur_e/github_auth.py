"""
GitHub App Authentication and API Client for MERCUR-E
"""
import time
import jwt
import requests
from github import Github, GithubIntegration
from typing import Any
from loguru import logger
from .config import settings


class GitHubAppAuth:
    """Handle GitHub App authentication and token management"""
    
    def __init__(self):
        self.app_id = settings.github_app_id
        self.private_key = settings.get_private_key()
        self.integration = GithubIntegration(self.app_id, self.private_key)
        self._installation_tokens: dict[int, dict[str, Any]] = {}
    
    def generate_jwt(self) -> str:
        """Generate JWT for GitHub App authentication"""
        now = int(time.time())
        payload = {
            'iat': now,
            'exp': now + (10 * 60),  # JWT expires in 10 minutes
            'iss': self.app_id
        }
        
        token = jwt.encode(
            payload,
            self.private_key,
            algorithm='RS256'
        )
        
        return token
    
    def get_installation_token(self, installation_id: int) -> str:
        """
        Get installation access token for a specific installation.
        Caches tokens and refreshes when expired.
        """
        # Check if we have a cached token that's still valid
        if installation_id in self._installation_tokens:
            cached = self._installation_tokens[installation_id]
            if cached['expires_at'] > time.time() + 60:  # 1 min buffer
                return cached['token']
        
        # Get new token
        try:
            token = self.integration.get_access_token(installation_id).token
            
            # Cache the token (GitHub tokens expire after 1 hour)
            self._installation_tokens[installation_id] = {
                'token': token,
                'expires_at': time.time() + (60 * 60)  # 1 hour
            }
            
            logger.info(f"Generated new installation token for installation {installation_id}")
            return token
            
        except Exception as e:
            logger.error(f"Failed to get installation token: {e}")
            raise
    
    def get_github_client(self, installation_id: int) -> Github:
        """Get authenticated GitHub client for an installation"""
        token = self.get_installation_token(installation_id)
        return Github(token)
    
    def get_installation_id_for_repo(self, owner: str, repo: str) -> Optional[int]:
        """Get installation ID for a specific repository"""
        try:
            jwt_token = self.generate_jwt()
            headers = {
                'Authorization': f'Bearer {jwt_token}',
                'Accept': 'application/vnd.github.v3+json'
            }
            
            url = f'https://api.github.com/repos/{owner}/{repo}/installation'
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                return response.json()['id']
            else:
                logger.error(f"Failed to get installation ID: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Error getting installation ID: {e}")
            return None


# Global auth instance
github_auth = GitHubAppAuth()
