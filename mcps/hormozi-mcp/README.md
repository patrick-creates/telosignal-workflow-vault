# Hormozi MCP Expert

> MCP Expert by [TeloSignal](https://telosignal.com)

An MCP server that critiques n8n workflows using Alex Hormozi's $100M Offer framework. Deployed on Vercel as a Server-Sent Events (SSE) endpoint.

---

## What it does

Fetches any workflow from this vault and returns a structured critique based on the Hormozi value equation: does the workflow deliver a dream outcome, reduce time delay, and minimize effort for the end user?

---

## Tool

### `analyze_vault_workflow(workflow_name: str)`

Fetches `workflows/<workflow_name>.md` from the GitHub repo and runs it through the Hormozi knowledge base.

**Example:**
```
analyze_vault_workflow("data-enrichment/google-sheets-batch-enrichment")
```

---

## Setup

### 1. Deploy to Vercel

```bash
cd mcps/hormozi-mcp
vercel deploy
```

### 2. Connect to your MCP client

Add the SSE endpoint to your MCP client config:

```json
{
  "mcpServers": {
    "hormozi": {
      "url": "https://<your-vercel-project>.vercel.app/sse"
    }
  }
}
```

### 3. Run locally

```bash
pip install -r requirements.txt
python api/index.py
```

Local SSE endpoint: `http://localhost:8000/sse`

---

## Knowledge Base

`hormozi_kb.md` — contains the $100M Offer and $100M Leads frameworks used for critiques. Edit this file to update the expert's reasoning without changing any code.

---

## Adding a New Expert

1. Duplicate this folder: `cp -r mcps/hormozi-mcp mcps/<expert-name>-mcp`
2. Replace `hormozi_kb.md` with the new expert's knowledge base
3. Update the `FastMCP` name in `api/index.py`
4. Deploy as a new standalone Vercel project

---

## Stack

| Component | Detail |
|-----------|--------|
| Framework | MCP Python SDK (`mcp>=1.23.0`) |
| Transport | SSE via `mcp.sse_app()` |
| Deployment | Vercel (Python serverless) |
| Host validation | Disabled via `TransportSecuritySettings` — required for non-localhost Vercel deployment |
