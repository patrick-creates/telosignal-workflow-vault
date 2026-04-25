# CLAUDE.md — TeloSignal Workflow Vault

Agent-native environment. Every AI agent working in this repo must follow these rules without exception.

---

## Project Context

Production-ready n8n workflow templates published on the [n8n Creator Hub](https://n8n.io/creators/patrickn8n/) by TeloSignal. Workflows are deployed by real users in production environments. Quality, stability, and clarity are non-negotiable.

---

## Project Standards — Step 4: Stability (MANDATORY)

Every workflow produced or modified in this repo must implement the following stability patterns before it is considered complete.

### Global Error Handler

Every workflow must include a dedicated error-handling path. This is not optional.

- Attach an **Error Trigger** node (or equivalent catch branch) that activates on workflow failure.
- The error path must: capture the error message, the node that failed, and the timestamp.
- Route failures to at minimum one output: a log entry, a notification node (email/Slack/webhook), or a Data table insert.
- Never let a workflow fail silently.

```text
Pattern: Error Trigger → Code (format error payload) → Notify/Log
```

### Retry Logic

Any node that calls an external service (HTTP Request, API node, LLM node) must have retry behavior configured.

- Set **Max Tries** to at minimum 3 on all HTTP Request nodes.
- Use **Wait Between Retries** of at least 1000ms (1 second).
- For rate-limited APIs: use exponential-style waits (1s, 2s, 4s) or a Wait node between batches.
- If n8n's built-in retry is unavailable on a node type, wrap it in a loop with a counter and a Wait node.

### Structured HTTP Responses

Workflows triggered by webhooks must return structured JSON responses for all outcomes:

- `200` — success, include processed count or result summary
- `400` — validation failure, include field-level error details
- `409` — conflict (e.g. duplicate), include conflicting identifier
- Never return raw n8n error objects to callers.

---

## Naming Conventions (MANDATORY)

These rules apply to all `.json` workflow files and any Code nodes within them.

### Variables (camelCase)

All JavaScript/expression variables inside Code nodes and `{{ }}` expressions use camelCase.

```js
// Correct
const invoiceId = item.invoice_id;
const batchSize = 5;
const errorMessage = error.message;

// Wrong
const InvoiceId = ...
const batch_size = ...
const ErrorMessage = ...
```

### Node Names (Title Case)

All n8n node names use Title Case. Names must be descriptive — describe what the node does, not what type it is.

```text
// Correct
"Read Sheet Rows"
"Call Enrichment API"
"Parse CSV Input"
"Send Error Notification"
"Check For Duplicate"

// Wrong
"HTTP Request"         ← too generic
"code"                 ← lowercase
"If1"                  ← meaningless
"node3"                ← auto-generated default
```

### Environment Variables (Prefixed)

All credentials, API keys, and configuration values injected via n8n environment variables or credentials must follow this prefix scheme:

| Prefix | Use for |
|--------|---------|
| `N8N_` | n8n instance configuration |
| `API_` | External API keys and endpoints |
| `DB_` | Database connection strings |
| `NOTIFY_` | Notification service targets (email, Slack webhook URLs) |
| `WORKFLOW_` | Workflow-specific configuration constants |

```text
// Correct
API_OPENAI_KEY
API_GOOGLE_SHEETS_ID
NOTIFY_ERROR_EMAIL
WORKFLOW_BATCH_SIZE

// Wrong
openaikey
mySheetId
email
BATCHSIZE
```

### Sticky Notes

Sticky notes are part of the workflow documentation. Use them. Every workflow must include at minimum:

- One overview sticky note at the start of the canvas describing what the workflow does and who it is for.
- One sticky note per configurable parameter block (batch size, wait time, API endpoint, etc.).

---

## Expert Veto — Pre-Completion Review (MANDATORY)

Before marking any task complete, the agent must simulate a two-expert veto review. Do not skip this step. Do not abbreviate it.

Run the following internal check and include the result in your completion summary.

### Expert 1 — Alex Hormozi (Value Lens)

Hormozi asks: *Does this deliver disproportionate value? Is the outcome obvious and immediate to the user?*

Ask yourself:

- What concrete result does this workflow/change produce for the end user?
- Is the value obvious without explanation, or does it require justification?
- Would a non-technical business owner immediately understand what they gain?
- Is there a measurable output (invoices created, leads enriched, tests passed, errors caught)?
- If the answer to any of these is "no" or "unclear" — the task is not complete. Add the missing value signal before finishing.

### Expert 2 — Warren Buffett (Moat Lens)

Buffett asks: *Does this compound? Is the value durable?*

Ask yourself:

- Does this workflow produce increasing returns the more it is used? (Data accumulates, accuracy improves, time saved scales.)
- Does it avoid brittle dependencies — external APIs that could disappear, credentials hardcoded in nodes, undocumented magic values?
- Would someone running this in 12 months be able to maintain it without asking the original author?
- Is there a moat here — does this template do something that generic n8n templates cannot easily replicate?
- If the answer is "this is disposable / one-shot / fragile" — the task is not complete. Harden it before finishing.

### Veto Output Format

Include this block in your completion message:

```text
## Expert Veto Review

**Hormozi (Value):** [One sentence: what concrete value does this deliver and to whom.]
**Buffett (Moat):** [One sentence: why this is durable and maintainable long-term.]
**Veto status:** CLEARED / BLOCKED — [reason if blocked]
```

If either expert would veto, status is BLOCKED. Fix the issue. Re-run the review. Only proceed when CLEARED.

---

## Workflow Metadata — 4-Element Formula (MANDATORY)

Every workflow in this repo must be in its own folder. No `.json` file exists at the root of a category without an accompanying folder structure.

### Required Folder Structure

```text
workflows/
└── <category>/
    └── <workflow-slug>/
        ├── workflow.json
        └── README.md        ← REQUIRED
```

### README.md — Required Sections

Every `README.md` must follow the 4-element formula in this exact order:

#### 1. Header

```markdown
# <Workflow Name>

> Published on [n8n Creator Hub](<url>) · [TeloSignal](https://telosignal.com)

![n8n version](https://img.shields.io/badge/n8n-%3E%3D<version>-orange) ![n8n 2.x](https://img.shields.io/badge/2.x-compatible-brightgreen) ![License](https://img.shields.io/badge/license-MIT-blue.svg)

> <Hormozi Value Claim — one sentence: what disproportionate outcome does this deliver and for whom?>

## What this workflow does

[2–3 sentences. Plain language. What it does, what triggers it, what it produces.]
```

Replace `<version>` with the minimum n8n version required (check node typeVersions in workflow.json). Add `· 2.x compatible` badge only when verified.

#### 1b. Workflow Overview

```markdown
## Workflow Overview

![Workflow canvas](./screenshot.png)
```

Static screenshot of the n8n canvas. File must be named `screenshot.png` and placed in the workflow folder. If not yet captured: `<!-- screenshot.png — export canvas from n8n UI and place in this folder -->`.

#### 2. Metric

```markdown
## Metric

[The quantifiable success measure. What number moves when this works correctly?
Examples: "Rows enriched per run without rate-limit errors", "Invoices created per CSV upload",
"Accuracy score across N test cases".]
```

#### 3. Pattern

```markdown
## Pattern

[The architectural pattern name + one-sentence description of the data flow.
Examples: "Rate-limited batch loop", "ETL + validation pipeline", "Benchmark harness".]
```

#### 4. Principle

```markdown
## Principle

[The underlying engineering or business reasoning. Why this pattern was chosen.
What failure mode it prevents. What tradeoff it accepts.]
```

#### 5. Question

```markdown
## Question

[One open-ended question that helps the user extend or apply the workflow to their context.
This is the use-case exploration prompt.]
```

#### 5b. Prerequisites (Required)

```markdown
## Prerequisites

| Requirement | Detail |
|---|---|
| n8n version | ≥ x.x · 2.x compatible |
| Credentials | List each required credential type |
| n8n features | Data tables / Community nodes / LangChain (delete as appropriate) |
```

If no external credentials needed: state "No external credentials required — fully native n8n."

#### 6. Setup (Required)

A numbered setup section. Must include: import instructions, credential configuration steps, any variables that need to be changed, and a test command or method.

#### 7. Nodes Used (Required)

A markdown table with columns `Node` and `Purpose`. Every non-trivial node must be listed.

#### 8. Related (Required)

```markdown
## Related

- [Workflow Name](../sibling-folder/) — one-line description
- [n8n docs: Node Name](https://docs.n8n.io/...) — what it covers
```

Minimum: 1 internal vault link + 1 external n8n docs link.

### Enforcement

- A PR or commit that adds a `workflow.json` without a corresponding `README.md` is incomplete.
- A `README.md` missing any of the 4 formula elements (Metric, Pattern, Principle, Question) is incomplete.
- The `README.md` for a workflow is part of the workflow deliverable, not optional documentation.

---

## Repository Structure

```text
workflows/
├── ai-safety/
├── data-enrichment/
└── data-processing/
```

New workflows go into the most relevant category folder. If no category fits, propose a new one before creating it — do not dump files at the root of `workflows/`.

---

## What "Complete" Means in This Repo

A task is complete only when ALL of the following are true:

- [ ] Workflow implements Global Error Handler (Step 4: Stability)
- [ ] Workflow implements Retry Logic on all external service nodes
- [ ] All node names use Title Case and are descriptive
- [ ] All variables in Code nodes use camelCase
- [ ] All environment variables follow the prefix scheme
- [ ] `README.md` exists in the workflow folder
- [ ] `README.md` contains all 4 formula elements (Metric, Pattern, Principle, Question)
- [ ] `README.md` contains Hormozi Value Claim in header block (no label prefix)
- [ ] `README.md` contains badges (n8n min version + MIT license)
- [ ] `README.md` contains Workflow Overview section (screenshot.png or placeholder comment)
- [ ] `README.md` contains Prerequisites section
- [ ] `README.md` contains Related section (≥1 internal vault link + ≥1 external n8n docs link)
- [ ] Expert Veto review completed and status is CLEARED

## MCP Infrastructure

- To run the Hormozi Expert locally: `python mcps/hormozi-mcp/api/index.py`
- Deployment: Hosted on Vercel.
- Frameworks: MCP Python SDK (`mcp>=1.23.0`). DNS rebinding protection disabled via `TransportSecuritySettings(enable_dns_rebinding_protection=False)` — required for Vercel deployment.
- Live SSE endpoint: `https://<your-vercel-project>.vercel.app/sse`

## Workflow Commands

- Use `analyze_vault_workflow(name)` to critique any file in the `/workflows` directory.
- Refer to `mcps/hormozi-mcp/hormozi_kb.md` for Alex Hormozi's business logic.

### MCP Expert Guidelines

- **Expert Path:** All experts live in `/mcps/[expert-name]`
- **Deployment:** Each expert is a standalone Vercel Project.
- **Workflow Access:** Experts fetch raw data from `https://raw.githubusercontent.com/patrick-creates/telosignal-workflow-vault/main/workflows/`.
- **README required:** Every expert folder must contain a `README.md` with: what the expert does, available tools, setup instructions (deploy + local), and stack details.
- **Adding Experts:** To add a new expert, duplicate `hormozi-mcp`, update `mcp.py`, the KB, and `README.md`, then deploy to a new Vercel project.
