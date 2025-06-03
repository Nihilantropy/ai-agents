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
    
    def _authenticate_with_credentials(self) -> Optional[Credentials]:
        """
        Authenticate using the credentials file.
        Returns credentials if successful, None otherwise.
        """
        try:
            logger.info("Starting OAuth2 authentication...")
            flow = InstalledAppFlow.from_client_secrets_file(
                str(settings.credentials_file_path), 
                settings.gmail_scopes
            )
            credentials = flow.run_local_server(port=0)
            logger.info("OAuth2 authentication successful")
            return credentials
            
        except Exception as e:
            logger.error(f"OAuth2 authentication failed: {e}")
            return None
    
    def authenticate(self) -> bool:
        """
        Authenticate with Gmail API using OAuth2.
        Returns True if authentication successful, False otherwise.
        """
        # Step 1: Check if credentials file exists
        if not self._check_credentials_file():
            return False
        
        # Step 2: Try to authenticate with credentials
        credentials = self._authenticate_with_credentials()
        if not credentials:
            return False
        
        # Step 3: Build Gmail service
        try:
            self.service = build('gmail', 'v1', credentials=credentials)
            self.credentials = credentials
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