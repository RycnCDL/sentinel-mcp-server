"""
Main entry point for the Microsoft Sentinel MCP Server

Run the server with:
    python -m src
or:
    python src
"""
import sys
import os

# Add src directory to Python path for relative imports
src_dir = os.path.dirname(os.path.abspath(__file__))
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

from mcp_server.server import main

if __name__ == "__main__":
    main()
