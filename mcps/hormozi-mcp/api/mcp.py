import os
import requests
import anthropic

from starlette.applications import Starlette
from starlette.routing import Mount
from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings

mcp = FastMCP(
    "Hormozi",
    transport_security=TransportSecuritySettings(
        enable_dns_rebinding_protection=False
    ),
)

@mcp.tool()
def test_server() -> str:
    """Test tool to verify the MCP server is working."""
    return "✅ Hormozi MCP server is running on Vercel!"

def fetch_vault_workflow(name: str) -> str:
    url = f"https://raw.githubusercontent.com/patrick-creates/telosignal-workflow-vault/main/workflows/{name}.md"
    try:
        r = requests.get(url, timeout=20)
        return r.text if r.status_code == 200 else "Workflow not found."
    except Exception:
        return "Connection to Vault failed."

@mcp.tool()
def analyze_vault_workflow(workflow_name: str) -> str:
    """Fetches a workflow from Telosignal Vault and gives a Hormozi-style critique."""
    workflow_content = fetch_vault_workflow(workflow_name)

    # Load KB from mcps/hormozi-mcp/hormozi_kb.md relative to this file
    kb_path = os.path.join(os.path.dirname(__file__), "hormozi_kb.md")
    try:
        with open(kb_path, "r", encoding="utf-8") as f:
            kb = f.read()
    except FileNotFoundError:
        kb = "Knowledge base file not found."

    client = anthropic.Anthropic(api_key=os.environ.get("API_ANTHROPIC_KEY"))

    response = client.messages.create(
        model="claude-opus-4-7",
        max_tokens=1024,
        system=kb,
        messages=[
            {
                "role": "user",
                "content": f"""Analyze this n8n workflow through the Hormozi $100M Offer value equation.

WORKFLOW:
{workflow_content}

Evaluate each variable:
- Dream Outcome: What concrete result does this deliver?
- Perceived Likelihood of Success: How confident will the user be it works for them?
- Time Delay: How fast do they see results?
- Effort & Sacrifice: How hard is setup and ongoing use?

Format your response exactly like this:
Dream Outcome: [✓/⚠] [one line]
Perceived Likelihood: [✓/⚠] [one line]
Time Delay: [✓/⚠] [one line]
Effort/Sacrifice: [✓/⚠] [one line]

Verdict: [one actionable sentence — what to fix before publishing, or "ship it" if cleared]""",
            }
        ],
    )

    return f"Hormozi Analysis for {workflow_name}:\n\n{response.content[0].text}"

app = Starlette(routes=[Mount("/", app=mcp.streamable_http_app())])
