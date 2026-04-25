"""Hormozi MCP server — analyze n8n workflows using the Hormozi value framework."""

import os

import requests
import openai
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings

load_dotenv()

MODEL = os.environ["API_MODEL"]
RAW_BASE = os.environ["WORKFLOW_GITHUB_RAW_BASE"]
WORKFLOW_EXT = os.environ["WORKFLOW_EXTENSION"]

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
    """Fetch raw workflow JSON from the TeloSignal Vault on GitHub."""
    url = f"{RAW_BASE}/{name}{WORKFLOW_EXT}"
    try:
        r = requests.get(url, timeout=20)
        return r.text if r.status_code == 200 else "Workflow not found."
    except requests.RequestException:
        return "Connection to Vault failed."

@mcp.tool()
def analyze_vault_workflow(workflow_name: str) -> str:
    """Fetches a workflow from Telosignal Vault and gives a Hormozi-style critique."""
    workflow_content = fetch_vault_workflow(workflow_name)

    kb_path = os.path.join(os.path.dirname(__file__), "hormozi_kb.md")
    try:
        with open(kb_path, "r", encoding="utf-16") as f:
            kb = f.read()
    except FileNotFoundError:
        kb = "Knowledge base file not found."

    client = openai.OpenAI(
        api_key=os.environ["API_ANTHROPIC_KEY"],
        base_url="https://openrouter.ai/api/v1",
    )

    prompt = (
        f"Analyze this n8n workflow through the Hormozi $100M Offer value equation.\n\n"
        f"WORKFLOW:\n{workflow_content}\n\n"
        "Evaluate each variable:\n"
        "- Dream Outcome: What concrete result does this deliver?\n"
        "- Perceived Likelihood of Success: How confident will the user be it works?\n"
        "- Time Delay: How fast do they see results?\n"
        "- Effort & Sacrifice: How hard is setup and ongoing use?\n\n"
        "Format your response exactly like this:\n"
        "Dream Outcome: [✓/⚠] [one line]\n"
        "Perceived Likelihood: [✓/⚠] [one line]\n"
        "Time Delay: [✓/⚠] [one line]\n"
        "Effort/Sacrifice: [✓/⚠] [one line]\n\n"
        "Verdict: [one actionable sentence — what to fix, or 'ship it' if cleared]"
    )

    response = client.chat.completions.create(
        model=MODEL,
        max_tokens=1024,
        messages=[
            {"role": "system", "content": kb},
            {"role": "user", "content": prompt},
        ],
    )

    return f"Hormozi Analysis for {workflow_name}:\n\n{response.choices[0].message.content}"

app = mcp.streamable_http_app()
