"""
Configuration management for MERCUR-E GitHub Bot
"""
from pydantic_settings import BaseSettings
from pydantic import Field
import os


class Settings(BaseSettings):
    """Application settings"""
    
    # GitHub App Configuration
    github_app_id: int | None = Field(default=None, env="GITHUB_APP_ID")
    github_app_private_key_path: str = Field(
        default="./private-key.pem",
        env="GITHUB_APP_PRIVATE_KEY_PATH"
    )
    github_webhook_secret: str | None = Field(default=None, env="GITHUB_WEBHOOK_SECRET")
    
    # Server Configuration
    host: str = Field(default="0.0.0.0", env="HOST")
    port: int = Field(default=8000, env="PORT")
    debug: bool = Field(default=False, env="DEBUG")
    
    # PAM Authentication
    pam_service: str = Field(default="login", env="PAM_SERVICE")
    pam_enabled: bool = Field(default=False, env="PAM_ENABLED")
    
    # AI Integration
    fastmcp_enabled: bool = Field(default=True, env="FASTMCP_ENABLED")
    fastmcp_port: int = Field(default=8001, env="FASTMCP_PORT")
    
    # Logging
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    log_file: str = Field(default="./logs/githubbot.log", env="LOG_FILE")
    
    # Security
    allowed_origins: str = Field(default="*", env="ALLOWED_ORIGINS")
    tls_cert_path: str | None = Field(default=None, env="TLS_CERT_PATH")
    tls_key_path: str | None = Field(default=None, env="TLS_KEY_PATH")
    
    model_config = {
        "env_file": ".env",
        "case_sensitive": False,
        "extra": "ignore"
    }
    
    def get_private_key(self) -> str:
        """Read and return the GitHub App private key"""
        if not os.path.exists(self.github_app_private_key_path):
            raise FileNotFoundError(
                f"Private key not found at {self.github_app_private_key_path}"
            )
        
        with open(self.github_app_private_key_path, 'r') as f:
            return f.read()


# Global settings instance
settings = Settings()
