#!/usr/bin/env python3
"""
Direct Server Starter for MCP Server
Startet den Server direkt ohne -m src
"""
import sys
import os

# Add src to path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, 'src')
sys.path.insert(0, src_dir)

# Import and run the server
from mcp_server.server import main

if __name__ == '__main__':
    print("="*70)
    print("Microsoft Sentinel MCP Server")
    print("="*70)
    print(f"Python: {sys.version}")
    print(f"Working Directory: {os.getcwd()}")
    print(f"Source Directory: {src_dir}")
    print("="*70)
    print()
    
    main()
