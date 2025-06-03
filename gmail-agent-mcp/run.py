#!/usr/bin/env python3
"""
Entry point script for Gmail Agent MCP.
Sets up the Python path and runs the main application.
"""

import sys
from pathlib import Path

# Add src directory to Python path
src_path = Path(__file__).parent / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

# Import and run main
from main import main

if __name__ == "__main__":
    main()