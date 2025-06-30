import yaml
import subprocess
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from typing import Dict

# Load commands from YAML
with open("/workspaces/mcp-devtasks/dev_commands.yaml", encoding="utf-8") as f:
    COMMANDS: Dict[str, str] = yaml.safe_load(f)

app = FastAPI(title="Dev MCP Server")


def run_shell_command(cmd: str) -> str:
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=120, check=False)
        return result.stdout + ("\n" + result.stderr if result.stderr else "")
    except Exception as e:
        return f"Error: {e}"


@app.get("/commands", response_class=PlainTextResponse)
def list_commands():
    return "\n".join(COMMANDS.keys())


@app.get("/run/{command}", response_class=PlainTextResponse)
def run_command(command: str):
    if command not in COMMANDS:
        return f"Unknown command: {command}"
    output = run_shell_command(COMMANDS[command])
    return output

# For local dev: uvicorn main:app --reload
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
