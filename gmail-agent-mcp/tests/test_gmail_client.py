"""
Test module for Gmail client functionality.
Run with: pytest tests/test_gmail_client.py -v
"""

import logging
import pytest
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from gmail_agent.gmail_client import GmailClient
from config.settings import settings


class TestGmailClient:
    """Test cases for Gmail client."""
    
    def setup_method(self):
        """Setup for each test method."""
        self.gmail_client = GmailClient()
    
    def test_credentials_file_exists(self):
        """Test that credentials file exists."""
        assert settings.credentials_file_path.exists(), (
            f"Credentials file not found: {settings.credentials_file_path}\n"
            "Please download credentials.json from Google Cloud Console and place it in the credentials folder"
        )
    
    def test_gmail_authentication(self):
        """Test Gmail API authentication."""
        # This test requires manual intervention for OAuth flow
        # Skip if running in CI or automated environment
        import os
        if os.getenv('CI') or os.getenv('AUTOMATED_TESTING'):
            pytest.skip("Skipping authentication test in automated environment")
        
        assert self.gmail_client.authenticate(), "Gmail authentication failed"
        assert self.gmail_client.service is not None, "Gmail service not initialized"
        assert self.gmail_client.credentials is not None, "Gmail credentials not set"
    
    def test_gmail_profile(self):
        """Test getting Gmail profile information."""
        # Skip if not authenticated
        if not self.gmail_client.service:
            if not self.gmail_client.authenticate():
                pytest.skip("Cannot test profile without authentication")
        
        profile = self.gmail_client.get_profile()
        assert profile is not None, "Failed to get Gmail profile"
        assert 'emailAddress' in profile, "Profile missing email address"
        assert 'messagesTotal' in profile, "Profile missing messages total"
        assert 'threadsTotal' in profile, "Profile missing threads total"
    
    def test_recent_emails(self):
        """Test fetching recent emails."""
        # Skip if not authenticated
        if not self.gmail_client.service:
            if not self.gmail_client.authenticate():
                pytest.skip("Cannot test emails without authentication")
        
        recent_emails = self.gmail_client.get_recent_emails(count=5)
        assert isinstance(recent_emails, list), "Recent emails should return a list"
        
        if recent_emails:  # Only test if emails exist
            email = recent_emails[0]
            assert 'id' in email, "Email missing ID"
            assert 'snippet' in email, "Email missing snippet"


def test_gmail_connection_integration():
    """
    Integration test that mimics the original test_gmail_connection function.
    This can be run manually to verify full Gmail functionality.
    """
    logger = logging.getLogger(__name__)
    
    logger.info("Starting Gmail Agent integration test...")
    
    # Initialize Gmail client
    gmail_client = GmailClient()
    
    # Authenticate
    logger.info("Authenticating with Gmail API...")
    auth_success = gmail_client.authenticate()
    assert auth_success, "Authentication failed!"
    
    # Get profile information
    logger.info("Getting profile information...")
    profile = gmail_client.get_profile()
    assert profile is not None, "Failed to get profile information"
    
    print(f"\n✅ Connected to Gmail!")
    print(f"📧 Email: {profile.get('emailAddress')}")
    print(f"📊 Total messages: {profile.get('messagesTotal', 'Unknown')}")
    print(f"🧵 Total threads: {profile.get('threadsTotal', 'Unknown')}")
    
    # Get recent emails
    logger.info("Fetching recent emails...")
    recent_emails = gmail_client.get_recent_emails(count=5)
    assert recent_emails is not None, "No emails found or error occurred"
    
    if recent_emails:
        print(f"\n📬 Recent {len(recent_emails)} emails:")
        print("-" * 80)
        
        for i, email in enumerate(recent_emails, 1):
            print(f"\n{i}. 📧 Email ID: {email.get('id', 'N/A')}")
            print(f"   📤 From: {email.get('from', 'N/A')}")
            print(f"   📋 Subject: {email.get('subject', 'N/A')}")
            print(f"   📅 Date: {email.get('date', 'N/A')}")
            print(f"   📄 Snippet: {email.get('snippet', 'N/A')[:100]}...")
    
    logger.info("Gmail Agent integration test completed successfully!")


if __name__ == "__main__":
    """
    Run the integration test directly.
    """
    logging.basicConfig(
        level=logging.INFO,
        format='%(name)s - %(levelname)s - %(message)s'
    )
    
    try:
        test_gmail_connection_integration()
        print("\n🎉 Gmail Agent is working correctly!")
    except Exception as e:
        print(f"\n❌ Gmail Agent test failed: {e}")
        sys.exit(1)