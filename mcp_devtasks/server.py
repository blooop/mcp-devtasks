#!/usr/bin/env python3
"""
Entry point for the MCP Development Tasks Server.
This file allows running the server directly during development.
"""

from .main import mcp


def main():
    mcp.run(transport="http", host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
