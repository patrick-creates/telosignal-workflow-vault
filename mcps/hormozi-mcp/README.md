# Hormozi MCP Expert

> MCP Expert by [TeloSignal](https://telosignal.com)

---

## Why use this

n8n workflows can run correctly and still deliver no real value. This expert catches that gap.

It fetches any workflow from this vault and critiques it through Alex Hormozi's $100M Offer value equation: Dream Outcome, Perceived Likelihood of Success, Time Delay, and Effort/Sacrifice. The output tells you exactly which variable is weak and what to fix before you publish.

**Who it's for**: n8n workflow authors preparing to publish on the Creator Hub, or automation builders reviewing workflows before handing them to clients.

---

## Tool

### `analyze_vault_workflow(workflow_name: str)`

Fetches `workflows/<workflow_name>.md` from the GitHub repo and runs it through the Hormozi knowledge base.

**Example:**

```text
analyze_vault_workflow("data-enrichment/google-sheets-batch-enrichment")
```

### `test_server()`

Confirms the server is reachable. Returns `✅ Hormozi MCP server is running on Vercel!`

---

## Example Output

```text
Hormozi Analysis for data-enrichment/google-sheets-batch-enrichment:

Dream Outcome:        ✓ Clear — enriched sheet with company data, no manual lookup
Perceived Likelihood: ⚠ Weak — no visible success/failure count returned to user
Time Delay:           ✓ Batch loop keeps rate-limit errors from stalling the run
Effort/Sacrifice:     ⚠ Setup friction — API credential config not documented

Verdict: Ship after adding a visible "X rows enriched" output to the webhook response.
```

---

## Prerequisites

- Python 3.10+
- [Vercel CLI](https://vercel.com/docs/cli) (`npm i -g vercel`)
- This vault's GitHub repo set to **public** (workflows fetched via `raw.githubusercontent.com`)

---

## Setup

### 1. Deploy to Vercel

```bash
cd mcps/hormozi-mcp
vercel login        # first time only
vercel deploy --prod
```

Note the production URL from the output, e.g. `https://<your-vercel-project>.vercel.app`.

Set the `API_ANTHROPIC_KEY` environment variable in your Vercel project settings before using `analyze_vault_workflow`.

Your MCP endpoint: `https://<your-vercel-project>.vercel.app/mcp`

### 2. Connect to your MCP client

**Claude Desktop**

Config file location:
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%AppData%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "hormozi": {
      "type": "http",
      "url": "https://<your-vercel-project>.vercel.app/mcp"
    }
  }
}
```

**Cursor**: Settings → MCP → Add Server → paste the `/mcp` URL → select type `Streamable HTTP`.

Restart your client after saving. Verify that `analyze_vault_workflow` appears in the tool list.

### 3. Run locally

```bash
cd mcps/hormozi-mcp
pip install -r requirements.txt
uvicorn api.index:app --host 127.0.0.1 --port 8787
```

Local MCP endpoint: `http://127.0.0.1:8787/mcp`

---

## Test

MCP uses a session handshake. Three steps: initialize → get session ID → call tool.

**PowerShell (Windows)**

```powershell
# Step 1 — Initialize and capture session ID
$r = Invoke-WebRequest `
  -Uri "https://<your-vercel-project>.vercel.app/mcp" `
  -Method POST `
  -Headers @{"Content-Type"="application/json"; "Accept"="application/json, text/event-stream"} `
  -Body '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"test","version":"1.0"}}}'
$sid = $r.Headers["mcp-session-id"]

# Step 2 — List tools
Invoke-RestMethod `
  -Uri "https://<your-vercel-project>.vercel.app/mcp" `
  -Method POST `
  -Headers @{"Content-Type"="application/json"; "Accept"="application/json, text/event-stream"; "Mcp-Session-Id"=$sid} `
  -Body '{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}'

# Step 3 — Call test_server
Invoke-RestMethod `
  -Uri "https://<your-vercel-project>.vercel.app/mcp" `
  -Method POST `
  -Headers @{"Content-Type"="application/json"; "Accept"="application/json, text/event-stream"; "Mcp-Session-Id"=$sid} `
  -Body '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"test_server","arguments":{}}}'
```

**curl (macOS / Linux)**

```bash
# Step 1 — Initialize
curl -s -X POST https://<your-vercel-project>.vercel.app/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -D - \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"test","version":"1.0"}}}'
# Copy mcp-session-id from response headers

# Step 2 — List tools
curl -s -X POST https://<your-vercel-project>.vercel.app/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "Mcp-Session-Id: <session-id>" \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}'

# Step 3 — Call test_server
curl -s -X POST https://<your-vercel-project>.vercel.app/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "Mcp-Session-Id: <session-id>" \
  -d '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"test_server","arguments":{}}}'
```

Expected response on Step 3:

```json
{"result": {"content": [{"type": "text", "text": "✅ Hormozi MCP server is running on Vercel!"}]}}
```

---

## Knowledge Base

`hormozi_kb.md` — contains the $100M Offer and $100M Leads frameworks used for critiques. Edit this file to update the expert's reasoning without touching any code.

---

## Adding a New Expert

1. Duplicate this folder: `cp -r mcps/hormozi-mcp mcps/<expert-name>-mcp`
2. Replace `hormozi_kb.md` with the new expert's knowledge base
3. Update the `FastMCP` name in `api/index.py`
4. Deploy as a new standalone Vercel project

---

## Stack

| Component       | Detail                                                                              |
| --------------- | ----------------------------------------------------------------------------------- |
| Framework       | MCP Python SDK (`mcp[cli]>=1.23.0`)                                                 |
| Transport       | Streamable HTTP via `mcp.streamable_http_app()`                                     |
| Deployment      | Vercel (Python serverless, entrypoint `api/index.py`)                               |
| Host validation | Disabled via `TransportSecuritySettings` — required for Vercel deployment            |
