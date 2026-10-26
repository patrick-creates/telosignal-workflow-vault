# Changelog

All notable changes to this project are documented here. Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Changed
- README leads with the Guardrails benchmark; marketing paragraphs replaced by a plain description of the four README questions and where workflow ideas come from.
- Workflow table and each workflow README link to its own Creator Hub page.
- Value lines in the workflow READMEs no longer make unmeasured claims (e.g. "80 %").

### Fixed
- Batch Enrichment README listed an Error Trigger and Error Logger that the workflow does not contain; the node table now matches `workflow.json`.
- Invoice Processor README said it sends email notifications; it prepares them, sending is not part of the workflow.
- Removed leftover screenshot placeholder comments.

## [1.0.0] – 2026-10-25

First tagged release.

### Added
- Workflow **Google Sheets Batch Enrichment** (`workflows/data-enrichment/`): rate-limited batch enrichment of sheet rows via a REST API.
- Workflow **Smart Sales Invoice Processor** (`workflows/data-processing/`): CSV upload → validated, enriched invoices in n8n Data tables, with 200/400/409 JSON responses.
- Workflow **Benchmark Content Safety Guardrails** (`workflows/ai-safety/`): 36 test prompts through the n8n Guardrails node, confusion matrix and precision/recall/F1 report by email.
- Per-workflow README following the 4-element formula (Metric, Pattern, Principle, Question) with canvas screenshot.
- **Hormozi MCP Expert** (`mcps/hormozi-mcp/`): MCP server (Streamable HTTP, Vercel) with `analyze_vault_workflow` and `test_server` tools.
- CI: Pylint (Python 3.10–3.12) and CodeQL.
- Issue templates.

### Fixed
- Docs: MCP endpoint is `/mcp` (Streamable HTTP), not `/sse`; Hormozi expert uses an OpenRouter key and needs all four env vars; corrected `analyze_vault_workflow` example path.
