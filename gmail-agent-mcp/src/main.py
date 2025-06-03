"""
Main entry point for Gmail Agent MCP server.
Demonstrates basic Gmail API functionality and email reading.
"""

import logging
import sys
from pathlib import Path

from gmail_agent.gmail_client import GmailClient
from config.settings import settings


def setup_logging():
    """Configure logging for the application."""
    logging.basicConfig(
        level=getattr(logging, settings.log_level.upper()),
        format='%(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('gmail_agent.log')
        ]
    )


def test_gmail_connection():
    """Test Gmail API connection and basic operations."""
    logger = logging.getLogger(__name__)
    
    logger.info("Starting Gmail Agent test...")
    
    # Initialize Gmail client
    gmail_client = GmailClient()
    
    # Authenticate
    logger.info("Authenticating with Gmail API...")
    if not gmail_client.authenticate():
        logger.error("Authentication failed!")
        return False
    
    # Get profile information
    logger.info("Getting profile information...")
    profile = gmail_client.get_profile()
    if profile:
        print(f"\n✅ Connected to Gmail!")
        print(f"📧 Email: {profile.get('emailAddress')}")
        print(f"📊 Total messages: {profile.get('messagesTotal', 'Unknown')}")
        print(f"🧵 Total threads: {profile.get('threadsTotal', 'Unknown')}")
    else:
        logger.error("Failed to get profile information")
        return False
    
    # Get recent emails
    logger.info("Fetching recent emails...")
    recent_emails = gmail_client.get_recent_emails(count=5)
    
    if recent_emails:
        print(f"\n📬 Recent {len(recent_emails)} emails:")
        print("-" * 80)
        
        for i, email in enumerate(recent_emails, 1):
            print(f"\n{i}. 📧 Email ID: {email.get('id', 'N/A')}")
            print(f"   📤 From: {email.get('from', 'N/A')}")
            print(f"   📋 Subject: {email.get('subject', 'N/A')}")
            print(f"   📅 Date: {email.get('date', 'N/A')}")
            print(f"   📄 Snippet: {email.get('snippet', 'N/A')[:100]}...")
    else:
        print("\n❌ No emails found or error occurred")
        return False
    
    logger.info("Gmail Agent test completed successfully!")
    return True


def main():
    """Main function to run the Gmail agent."""
    setup_logging()
    logger = logging.getLogger(__name__)
    
    try:
        # Check for credentials directory and file
        if not settings.credentials_path.exists():
            print("\n❌ Credentials directory not found!")
            print(f"Expected location: {settings.credentials_path}")
            print("\n🔧 Setup Instructions:")
            print("1. Create credentials directory at project root:")
            print(f"   mkdir {settings.credentials_path}")
            print("2. Follow Gmail API setup in README.md")
            print("3. Download credentials.json and place it in the credentials folder")
            return
        
        if not settings.credentials_file_path.exists():
            print("\n❌ Gmail credentials.json not found!")
            print(f"Expected location: {settings.credentials_file_path}")
            print("\n🔧 Setup Instructions:")
            print("1. Go to Google Cloud Console: https://console.cloud.google.com/")
            print("2. Create a new project or select existing one")
            print("3. Enable Gmail API")
            print("4. Create OAuth2 credentials (Desktop application)")
            print("5. Download credentials.json")
            print(f"6. Place it in: {settings.credentials_file_path}")
            print("\nThen run this script again!")
            return
        
        # Test Gmail connection
        success = test_gmail_connection()
        
        if success:
            print("\n🎉 Gmail Agent is working correctly!")
            print("\nNext steps:")
            print("- Build MCP server functionality")
            print("- Add email filtering and search")
            print("- Create specialized email tools")
        else:
            print("\n❌ Gmail Agent test failed!")
            
    except KeyboardInterrupt:
        logger.info("Application interrupted by user")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise


if __name__ == "__main__":
    main()