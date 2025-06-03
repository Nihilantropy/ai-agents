"""
Main entry point for Gmail Agent MCP server.
Provides core setup and initialization functionality.
"""

import logging
import sys
from pathlib import Path

from config.settings import settings


def setup_logging():
    """Configure logging for the application."""
    logging.basicConfig(
        level=getattr(logging, settings.log_level.upper()),
        format='%(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
        ]
    )


def check_setup() -> bool:
    """
    Check if the application is properly configured.
    Returns True if setup is complete, False otherwise.
    """
    logger = logging.getLogger(__name__)
    
    # Check for credentials directory and file
    if not settings.credentials_path.exists():
        print("\n❌ Credentials directory not found!")
        print(f"Expected location: {settings.credentials_path}")
        print("\n🔧 Setup Instructions:")
        print("1. Create credentials directory at project root:")
        print(f"   mkdir {settings.credentials_path}")
        print("2. Follow Gmail API setup in README.md")
        print("3. Download credentials.json and place it in the credentials folder")
        return False
    
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
        return False
    
    logger.info("Setup check completed successfully")
    return True


def main():
    """Main function to initialize the Gmail agent."""
    setup_logging()
    logger = logging.getLogger(__name__)
    
    try:
        if not check_setup():
            return
        
        print("\n✅ Gmail Agent setup is complete!")
        print("\nTo test the functionality, run:")
        print("   pytest tests/test_gmail_client.py -v")
        print("\nOr for integration test:")
        print("   python tests/test_gmail_client.py")
        print("\nNext steps:")
        print("- Build MCP server functionality")
        print("- Add email filtering and search")
        print("- Create specialized email tools")
            
    except KeyboardInterrupt:
        logger.info("Application interrupted by user")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise


if __name__ == "__main__":
    main()