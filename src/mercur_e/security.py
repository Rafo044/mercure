"""
Security utilities for webhook validation and PAM authentication for MERCUR-E
"""
import hmac
import hashlib
from loguru import logger

try:
    import pamela
    PAM_AVAILABLE = True
except ImportError:
    PAM_AVAILABLE = False
    logger.warning("PAM module not available. PAM authentication disabled.")


def verify_webhook_signature(payload: bytes, signature: str, secret: str | None = None) -> bool:
    """
    Verify GitHub webhook signature using HMAC-SHA256
    
    Args:
        payload: Raw request body bytes
        signature: X-Hub-Signature-256 header value
        secret: Webhook secret (if None, loads from settings)
    
    Returns:
        True if signature is valid, False otherwise
    """
    if not signature:
        logger.warning("No signature provided in webhook request")
        return False
    
    # GitHub sends signature as "sha256=<hash>"
    if not signature.startswith('sha256='):
        logger.warning("Invalid signature format")
        return False
    
    expected_signature = signature.split('=')[1]
    
    # Get secret from settings if not provided
    if secret is None:
        from .config import settings
        secret = settings.github_webhook_secret
        if secret is None:
            logger.error("Webhook secret not configured")
            return False
    
    # Calculate HMAC
    secret_bytes = secret.encode('utf-8')
    calculated_signature = hmac.new(
        secret_bytes,
        payload,
        hashlib.sha256
    ).hexdigest()
    
    # Constant-time comparison to prevent timing attacks
    is_valid = hmac.compare_digest(calculated_signature, expected_signature)
    
    if not is_valid:
        logger.warning("Webhook signature verification failed")
    
    return is_valid


def verify_webhook_signature_sha1(payload: bytes, signature: str, secret: str | None = None) -> bool:
    """
    Verify GitHub webhook signature using HMAC-SHA1 (legacy)
    
    Args:
        payload: Raw request body bytes
        signature: X-Hub-Signature header value
        secret: Webhook secret (if None, loads from settings)
    
    Returns:
        True if signature is valid, False otherwise
    """
    if not signature:
        return False
    
    if not signature.startswith('sha1='):
        return False
    
    expected_signature = signature.split('=')[1]
    
    # Get secret from settings if not provided
    if secret is None:
        from .config import settings
        secret = settings.github_webhook_secret
        if secret is None:
            return False
    
    secret_bytes = secret.encode('utf-8')
    calculated_signature = hmac.new(
        secret_bytes,
        payload,
        hashlib.sha1
    ).hexdigest()
    
    return hmac.compare_digest(calculated_signature, expected_signature)


class PAMAuthenticator:
    """PAM-based authentication for privileged operations"""
    
    def __init__(self):
        from .config import settings
        self.enabled = settings.pam_enabled and PAM_AVAILABLE
        self.service = settings.pam_service
        
        if settings.pam_enabled and not PAM_AVAILABLE:
            logger.error("PAM authentication requested but pamela module not available")
    
    def authenticate(self, username: str, password: str) -> bool:
        """
        Authenticate user via PAM
        
        Args:
            username: Username to authenticate
            password: Password for authentication
        
        Returns:
            True if authentication successful, False otherwise
        """
        if not self.enabled:
            logger.warning("PAM authentication is disabled")
            return False
        
        try:
            pamela.authenticate(username, password, service=self.service)
            logger.info(f"PAM authentication successful for user: {username}")
            return True
        except pamela.PAMError as e:
            logger.warning(f"PAM authentication failed for user {username}: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error during PAM authentication: {e}")
            return False
    
    def check_account(self, username: str) -> bool:
        """
        Check if PAM account is valid
        
        Args:
            username: Username to check
        
        Returns:
            True if account is valid, False otherwise
        """
        if not self.enabled:
            return False
        
        try:
            pamela.check_account(username, service=self.service)
            return True
        except pamela.PAMError:
            return False
        except Exception as e:
            logger.error(f"Error checking PAM account: {e}")
            return False


# Global PAM authenticator instance
pam_auth = PAMAuthenticator()
