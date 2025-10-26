"""
Tests for configuration management
"""
import pytest
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))


class TestConfiguration:
    """Test configuration loading and validation"""
    
    def test_settings_default_values(self, test_env):
        """Test default configuration values"""
        from mercur_e.config import Settings
        
        settings = Settings()
        
        assert settings.host == "0.0.0.0"
        assert settings.port == 8000
        assert settings.debug is False
        assert settings.log_level == "INFO"
    
    def test_settings_from_env(self, test_env):
        """Test loading settings from environment"""
        from mercur_e.config import Settings
        
        os.environ["PORT"] = "9000"
        os.environ["DEBUG"] = "True"
        os.environ["LOG_LEVEL"] = "DEBUG"
        
        settings = Settings()
        
        assert settings.port == 9000
        assert settings.debug is True
        assert settings.log_level == "DEBUG"
        
        # Cleanup
        del os.environ["PORT"]
        del os.environ["DEBUG"]
        del os.environ["LOG_LEVEL"]
    
    def test_github_app_id_required(self):
        """Test that GitHub App ID is required"""
        from mercur_e.config import Settings
        from pydantic import ValidationError
        
        # Clear environment
        os.environ.pop("GITHUB_APP_ID", None)
        
        with pytest.raises(ValidationError):
            Settings()
    
    def test_webhook_secret_required(self):
        """Test that webhook secret is required"""
        from mercur_e.config import Settings
        from pydantic import ValidationError
        
        os.environ["GITHUB_APP_ID"] = "123456"
        os.environ.pop("GITHUB_WEBHOOK_SECRET", None)
        
        with pytest.raises(ValidationError):
            Settings()
        
        # Cleanup
        del os.environ["GITHUB_APP_ID"]
