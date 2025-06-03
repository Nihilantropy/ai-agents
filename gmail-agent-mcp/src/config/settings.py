"""
Configuration settings for Gmail Agent MCP server.
Handles all environment variables and API configuration.
"""

import os
from pathlib import Path
from typing import List

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Project paths
    project_root: Path = Field(default_factory=lambda: Path(__file__).parent.parent.parent)
    credentials_path: Path = Field(default_factory=lambda: Path(__file__).parent.parent.parent / "credentials")
    
    # Gmail API settings
    gmail_credentials_file: str = Field(default="credentials.json", description="OAuth2 credentials file")
    gmail_token_file: str = Field(default="token.json", description="OAuth2 token file")
    gmail_scopes: List[str] = Field(
        default=[
            'https://www.googleapis.com/auth/gmail.readonly'
        ],
        description="Gmail API scopes"
    )
    
    # Application settings
    log_level: str = Field(default="INFO", description="Logging level")
    max_emails: int = Field(default=50, description="Maximum emails to fetch in one request")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
    
    @property
    def credentials_file_path(self) -> Path:
        """Full path to the credentials file."""
        return self.credentials_path / self.gmail_credentials_file
    
    @property
    def token_file_path(self) -> Path:
        """Full path to the token file."""
        return self.credentials_path / self.gmail_token_file


# Global settings instance
settings = Settings()