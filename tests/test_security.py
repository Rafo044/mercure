"""
Tests for security and webhook validation
"""
import pytest
import hmac
import hashlib
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from mercur_e.security import verify_webhook_signature, verify_webhook_signature_sha1


class TestWebhookSignature:
    """Test webhook signature validation"""
    
    def test_verify_signature_sha256_valid(self):
        """Test valid SHA-256 signature"""
        payload = b'{"action": "created"}'
        secret = "test_secret"
        
        # Calculate signature
        signature = hmac.new(
            secret.encode('utf-8'),
            payload,
            hashlib.sha256
        ).hexdigest()
        
        full_signature = f"sha256={signature}"
        
        assert verify_webhook_signature(payload, full_signature, secret) is True
    
    def test_verify_signature_sha256_invalid(self):
        """Test invalid SHA-256 signature"""
        payload = b'{"action": "created"}'
        signature = "sha256=invalid_signature"
        
        assert verify_webhook_signature(payload, signature, "test_secret") is False
    
    def test_verify_signature_sha256_no_signature(self):
        """Test with no signature provided"""
        payload = b'{"action": "created"}'
        
        assert verify_webhook_signature(payload, None) is False
        assert verify_webhook_signature(payload, "") is False
    
    def test_verify_signature_sha256_wrong_format(self):
        """Test with wrong signature format"""
        payload = b'{"action": "created"}'
        signature = "invalid_format"
        
        assert verify_webhook_signature(payload, signature, "test_secret") is False
    
    def test_verify_signature_sha1_valid(self):
        """Test valid SHA-1 signature"""
        payload = b'{"action": "created"}'
        secret = "test_secret"
        
        # Calculate signature
        signature = hmac.new(
            secret.encode('utf-8'),
            payload,
            hashlib.sha1
        ).hexdigest()
        
        full_signature = f"sha1={signature}"
        
        assert verify_webhook_signature_sha1(payload, full_signature, secret) is True
    
    def test_verify_signature_sha1_invalid(self):
        """Test invalid SHA-1 signature"""
        payload = b'{"action": "created"}'
        secret = "test_secret"
        signature = "sha1=invalid_signature"
        
        assert verify_webhook_signature_sha1(payload, signature, secret) is False
    
    def test_timing_attack_resistance(self):
        """Test that signature comparison is constant-time"""
        payload = b'{"action": "created"}'
        secret = "test_secret"
        
        # Calculate correct signature
        correct_sig = hmac.new(
            secret.encode('utf-8'),
            payload,
            hashlib.sha256
        ).hexdigest()
        
        # Test with slightly different signatures
        wrong_sig1 = correct_sig[:-1] + "a"
        wrong_sig2 = "a" + correct_sig[1:]
        
        # Both should fail
        assert verify_webhook_signature(payload, f"sha256={wrong_sig1}") is False
        assert verify_webhook_signature(payload, f"sha256={wrong_sig2}") is False
