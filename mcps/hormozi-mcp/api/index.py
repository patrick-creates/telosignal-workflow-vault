from mcp.server.fastmcp import FastMCP
import requests
import os

# We set warn_on_untrusted_hosts to False to stop the strict Host header check
mcp = FastMCP("Hormozi", warn_on_untrusted_hosts=False)

# Helper: Get latest workflow from your GitHub Vault
def fetch_vault_workflow(name):
    url = f"https://raw.githubusercontent.com/patrick-creates/telosignal-workflow-vault/main/workflows/{name}.md"
    try:
        r = requests.get(url)
        return r.text if r.status_code == 200 else "Workflow not found."
    except:
        return "Connection to Vault failed."

@mcp.tool()
def analyze_vault_workflow(workflow_name: str) -> str:
    """Fetches a workflow from Telosignal Vault and gives a Hormozi-style critique."""
    workflow_content = fetch_vault_workflow(workflow_name)
    
    # Vercel Path Fix: Look for the file relative to this script
    kb_path = os.path.join(os.path.dirname(__file__), "..", "hormozi_kb.md")
    
    try:
        with open(kb_path, "r") as f:
            kb = f.read()
    except FileNotFoundError:
        kb = "Knowledge base file not found."

    return f"Hormozi Analysis for {workflow_name}:\n\nCONTEXT:\n{kb}\n\nWORKFLOW:\n{workflow_content}"

app = mcp.sse_app()
