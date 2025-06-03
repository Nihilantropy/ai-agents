# Gmail Agent MCP Server

A simple Gmail API client that will evolve into a Model Context Protocol (MCP) server for email management.

## 🚀 Quick Start

### 1. Setup Project
```bash
# Clone/create project directory
mkdir gmail-agent-mcp
cd gmail-agent-mcp

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Gmail API Setup

#### Step 2.1: Create Credentials Directory
```bash
# Create credentials directory at project root
mkdir credentials
```

#### Step 2.2: Google Cloud Console Setup
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Gmail API:
   - Go to "APIs & Services" > "Library"
   - Search for "Gmail API"
   - Click "Enable"

#### Step 2.3: Create OAuth2 Credentials
1. Go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "OAuth client ID"
3. Choose "Desktop application"
4. Name it (e.g., "Gmail Agent")
5. Click "Create"
6. Download the JSON file
7. Rename it to `credentials.json`
8. Place it in the `credentials/` folder: `credentials/credentials.json`

#### Step 2.4: Configure OAuth Consent Screen
1. Go to "APIs & Services" > "OAuth consent screen"
2. Choose "External" (unless you have Google Workspace)
3. Fill required fields:
   - App name: "Gmail Agent"
   - User support email: your email
   - Developer contact: your email
4. Add scopes:
   - `https://www.googleapis.com/auth/gmail.readonly`
   - `https://www.googleapis.com/auth/gmail.metadata`
5. Add test users (your email address)

### 3. Run the Application
```bash
# Option A: Use the run script (recommended)
python3 run.py

# Option B: Set PYTHONPATH manually
PYTHONPATH=src python3 src/gmail_agent/main.py
```

### 4. First Time OAuth Flow
- The browser will open automatically
- Sign in with your Google account
- Grant permissions to the app
- Return to the terminal

## 📁 Project Structure

```
gmail-agent-mcp/
├── src/
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py              # Configuration
│   └── gmail_agent/
│       ├── __init__.py
│       ├── gmail_client.py          # Gmail API client
│       └── main.py                  # Application logic
├── credentials/
│   ├── credentials.json             # OAuth2 credentials (you add this)
│   └── token.json                  # Auto-generated token
├── tests/
├── run.py                          # Main entry point
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

## 🔧 Configuration

Edit `.env` file to customize settings:

```env
# Gmail API
GMAIL_CREDENTIALS_FILE=credentials.json
GMAIL_TOKEN_FILE=token.json

# Application
LOG_LEVEL=INFO
MAX_EMAILS=50
```

## 🎯 What This Does

Currently, the application:
- ✅ Authenticates with Gmail API
- ✅ Reads your Gmail profile
- ✅ Fetches recent emails
- ✅ Displays email metadata (subject, sender, date, snippet)

## 🔒 Security Notes

- `credentials.json` contains your OAuth2 client secrets
- `token.json` contains your access tokens
- Both are excluded from git via `.gitignore`
- Never commit these files to version control

## 🚧 Next Steps

This is the foundation. We'll build on this to create:
- MCP server functionality
- Email filtering and search tools
- Integration with LlamaIndex
- Local AI agent capabilities

## 🐛 Troubleshooting

### "Credentials file not found"
- Make sure `credentials.json` is in the `credentials/` folder
- Check the file name is exactly `credentials.json`

### "Authentication failed"
- Check your OAuth consent screen is configured
- Make sure you added your email as a test user
- Try deleting `token.json` and re-authenticating

### "Gmail API not enabled"
- Go to Google Cloud Console
- Enable Gmail API for your project

### Permission Errors
- Check the OAuth scopes in your credentials
- Make sure you granted all requested permissions

## 📝 Logging

Logs are written to:
- Console (stdout)
- `gmail_agent.log` file

Adjust log level in `.env` file (`DEBUG`, `INFO`, `WARNING`, `ERROR`).

## 🧪 Testing

The project now has a proper test structure separated from the core functionality.

### Running Tests

```bash
# Run all tests
pytest

# Run tests with verbose output
pytest -v

# Run specific test file
pytest tests/test_gmail_client.py -v

# Run integration test manually (requires OAuth)
python tests/test_gmail_client.py
```

### Test Structure

```
tests/
├── __init__.py                     # Test package
├── conftest.py                     # Pytest configuration
└── test_gmail_client.py            # Gmail client tests
```

**Note**: Some tests require manual OAuth authentication and will be skipped in automated environments. Use the integration test for full functionality verification.

## 📁 Updated Project Structure

```
gmail-agent-mcp/
├── src/
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py              # Configuration
│   ├── gmail_agent/
│   │   ├── __init__.py
│   │   └── gmail_client.py          # Gmail API client
│   └── main.py                      # Core application logic
├── tests/
│   ├── __init__.py
│   ├── conftest.py                  # Pytest configuration
│   └── test_gmail_client.py         # Tests
├── credentials/
│   ├── credentials.json             # OAuth2 credentials (you add this)
│   └── token.json                  # Auto-generated token
├── pytest.ini                      # Pytest configuration
├── run.py                          # Main entry point
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

## 🎯 What This Does

The refactored application:
- ✅ Separates core functionality from test logic
- ✅ Provides proper test structure with pytest
- ✅ Maintains all original functionality
- ✅ Allows automated and manual testing
- ✅ Sets up foundation for MCP server development