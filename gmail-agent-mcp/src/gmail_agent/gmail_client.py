"""
Gmail API client for reading and managing emails.
Handles authentication, email fetching, and basic email operations.
"""

import logging
import os
from typing import List, Dict, Any, Optional

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from config.settings import settings


logger = logging.getLogger(__name__)


class GmailClient:
    """Gmail API client for email operations."""
    
    def __init__(self):
        """Initialize Gmail client with authentication."""
        self.service = None
        self.credentials = None
        
    def _check_credentials_file(self) -> bool:
        """
        Check if credentials file exists at project root.
        Returns True if found, False otherwise.
        """
        if not settings.credentials_file_path.exists():
            logger.error(f"Credentials file not found: {settings.credentials_file_path}")
            logger.error("Please download credentials.json from Google Cloud Console and place it in the credentials folder")
            return False
        return True
    
    def authenticate(self) -> bool:
        """
        Authenticate with Gmail API using the simplest possible method.
        No local server, no complex setup - just manual code entry.
        Returns True if authentication successful, False otherwise.
        """
        # Step 1: Check if credentials file exists
        if not self._check_credentials_file():
            return False
        
        creds = None
        
        # Step 2: Try to load existing token
        if settings.token_file_path.exists():
            try:
                creds = Credentials.from_authorized_user_file(
                    str(settings.token_file_path), 
                    settings.gmail_scopes
                )
                logger.info("Loaded existing credentials from token file")
            except Exception as e:
                logger.warning(f"Failed to load existing token: {e}")
        
        # Step 3: Refresh token if expired
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
                logger.info("Refreshed expired credentials")
            except Exception as e:
                logger.warning(f"Failed to refresh credentials: {e}")
                creds = None
        
        # Step 4: Authenticate if no valid credentials (SIMPLE METHOD)
        if not creds or not creds.valid:
            try:
                logger.info("Starting simple OAuth2 authentication...")
                
                flow = InstalledAppFlow.from_client_secrets_file(
                    str(settings.credentials_file_path), 
                    settings.gmail_scopes
                )
                
                # Manual OAuth flow - no local server needed!
                print("\n" + "="*60)
                print("🔐 GMAIL AUTHENTICATION")
                print("="*60)
                print("📱 A web page will open in your browser")
                print("🔑 Sign in and grant permissions") 
                print("📋 Copy the authorization code and paste it here")
                print("="*60)
                
                # Generate authorization URL
                flow.redirect_uri = 'urn:ietf:wg:oauth:2.0:oob'  # Special redirect for manual flow
                auth_url, _ = flow.authorization_url(prompt='consent')
                
                print(f"\n🌐 Please visit this URL to authorize the application:")
                print(f"   {auth_url}")
                print()
                
                # Get authorization code from user
                auth_code = input("📋 Enter the authorization code: ").strip()
                
                if not auth_code:
                    logger.error("No authorization code provided")
                    return False
                
                # Exchange code for credentials
                flow.fetch_token(code=auth_code)
                creds = flow.credentials
                logger.info("Authentication successful!")
                
            except Exception as e:
                logger.error(f"Authentication failed: {e}")
                return False
            
            # Step 5: Save credentials for next time
            try:
                with open(settings.token_file_path, "w") as token:
                    token.write(creds.to_json())
                logger.info(f"Saved credentials to {settings.token_file_path}")
            except Exception as e:
                logger.error(f"Failed to save token: {e}")
        
        # Step 6: Build Gmail service
        try:
            self.service = build('gmail', 'v1', credentials=creds)
            self.credentials = creds
            logger.info("Gmail service initialized successfully!")
            return True
        except Exception as e:
            logger.error(f"Failed to build Gmail service: {e}")
            return False
    
    def get_profile(self) -> Optional[Dict[str, Any]]:
        """
        Get Gmail profile information.
        Returns profile data or None if error.
        """
        if not self.service:
            logger.error("Gmail service not initialized. Call authenticate() first.")
            return None
        
        try:
            profile = self.service.users().getProfile(userId='me').execute()
            logger.info(f"Profile retrieved for: {profile.get('emailAddress')}")
            return profile
        except HttpError as e:
            logger.error(f"Failed to get profile: {e}")
            return None
    
    def list_messages(self, query: str = "", max_results: int = None) -> List[Dict[str, Any]]:
        """
        List Gmail messages based on query.
        
        Args:
            query: Gmail search query (e.g., "is:unread", "from:example@gmail.com")
            max_results: Maximum number of messages to return
            
        Returns:
            List of message metadata
        """
        if not self.service:
            logger.error("Gmail service not initialized. Call authenticate() first.")
            return []
        
        if max_results is None:
            max_results = settings.max_emails
        
        try:
            result = self.service.users().messages().list(
                userId='me',
                q=query,
                maxResults=max_results
            ).execute()
            
            messages = result.get('messages', [])
            logger.info(f"Found {len(messages)} messages for query: '{query}'")
            return messages
            
        except HttpError as e:
            logger.error(f"Failed to list messages: {e}")
            return []
    
    def get_message(self, message_id: str) -> Optional[Dict[str, Any]]:
        """
        Get full message content by ID.
        
        Args:
            message_id: Gmail message ID
            
        Returns:
            Full message data or None if error
        """
        if not self.service:
            logger.error("Gmail service not initialized. Call authenticate() first.")
            return None
        
        try:
            message = self.service.users().messages().get(
                userId='me', 
                id=message_id,
                format='full'
            ).execute()
            
            logger.debug(f"Retrieved message: {message_id}")
            return message
            
        except HttpError as e:
            logger.error(f"Failed to get message {message_id}: {e}")
            return None
    
    def get_recent_emails(self, count: int = 10) -> List[Dict[str, Any]]:
        """
        Get recent emails with basic information.
        
        Args:
            count: Number of recent emails to retrieve
            
        Returns:
            List of email summaries
        """
        messages = self.list_messages(max_results=count)
        emails = []
        
        for msg in messages:
            message_id = msg['id']
            full_message = self.get_message(message_id)
            
            if full_message:
                # Extract basic email info
                headers = full_message.get('payload', {}).get('headers', [])
                email_info = {
                    'id': message_id,
                    'threadId': full_message.get('threadId'),
                    'snippet': full_message.get('snippet', ''),
                }
                
                # Extract common headers
                for header in headers:
                    name = header.get('name', '').lower()
                    value = header.get('value', '')
                    
                    if name in ['from', 'to', 'subject', 'date']:
                        email_info[name] = value
                
                emails.append(email_info)
        
        logger.info(f"Retrieved {len(emails)} recent emails")
        return emails