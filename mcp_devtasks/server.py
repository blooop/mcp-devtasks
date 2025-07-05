from fastmcp import FastMCP
import yaml
import subprocess
from typing import Dict
import os

# Default commands if YAML config is missing
DEFAULT_COMMANDS = {
    "install": "install",
    "build": "build",
    "lint": "lint",
    "test": "test",
    "ci": "ci",
}

# Load commands from YAML (development version uses mcp_devtasks.yaml)
CONFIG_FILE = os.path.join(os.path.dirname(__file__), "mcp_devtasks.yaml")
if not os.path.exists(CONFIG_FILE):
    CONFIG_FILE = "/workspaces/mcp-devtasks/mcp_devtasks.yaml"

if os.path.exists(CONFIG_FILE):
    with open(CONFIG_FILE, encoding="utf-8") as f:
        COMMANDS: Dict[str, str] = yaml.safe_load(f)
else:
    COMMANDS: Dict[str, str] = DEFAULT_COMMANDS.copy()

mcp = FastMCP("Dev MCP Server")


def run_shell_command(cmd: str) -> str:
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, timeout=120, check=False
        )
        return result.stdout + ("\n" + result.stderr if result.stderr else "")
    except Exception as e:
        return f"Error: {e}"


@mcp.tool
def list_commands() -> str:
    """
    List all available dev commands with descriptions for when to use them.
    """
    descriptions = {
        "install": "Install all dependencies required for the project. Use this when setting up the project for the first time or when dependencies change.",
        "build": "Build the project. Use this after making changes to source code that require compilation or packaging.",
        "lint": "Lint the codebase. Use this to check for code style and quality issues before committing or pushing changes.",
        "test": "Run all tests. Use this to verify that your code works as expected and nothing is broken.",
        "ci": "Run the full CI pipeline. Use this to perform all checks (formatting, linting, tests) as done in continuous integration.",
    }
    lines = []
    for cmd in COMMANDS:
        desc = descriptions.get(cmd, "No description available.")
        lines.append(f"{cmd}: {desc}")
    return "\n".join(lines)


@mcp.tool
def list_command_names() -> str:
    """
    List just the available command names, one per line.
    """
    return "\n".join(COMMANDS.keys())


@mcp.tool(
    description="Run a dev command by name. Returns the output of the command. Use this to execute project tasks such as build, test, lint, etc."
)
def run_command(command: str) -> str:
    """
    Run a dev command by name. Returns the output of the command. Use this to execute project tasks such as build, test, lint, etc.
    """
    if command not in COMMANDS:
        return f"Unknown command: {command}"
    return run_shell_command(COMMANDS[command])


if __name__ == "__main__":
    mcp.run()
