![n8n Creator Hub](https://img.shields.io/badge/n8n-Creator%20Hub-FF6D5B?style=flat-square&logo=n8n)
![Maintenance](https://img.shields.io/badge/Maintained-Yes-green?style=flat-square)

# TeloSignal Workflow Vault

n8n workflow templates with the part most templates skip written down: every workflow ships with its own README, canvas screenshot, prerequisites and step-by-step setup. All three are published on the [n8n Creator Hub](https://n8n.io/creators/patrickn8n/).

**Start here: [Benchmark Content Safety Guardrails](workflows/ai-safety/benchmark-content-safety-guardrails/).** It runs 36 labelled test prompts (PII, NSFW, jailbreak attempts, secret keys, unsafe URLs) through the n8n Guardrails node and emails accuracy, precision, recall and F1 per category. Run it before you trust a guardrail in production.

⭐ If a workflow here saves you a build, a star helps other n8n users find the vault.

---

## Workflows

| Workflow | Category | What it does | Creator Hub |
|----------|----------|--------------|-------------|
| [Benchmark Content Safety Guardrails](workflows/ai-safety/benchmark-content-safety-guardrails/) | AI Safety | 36 labelled prompts through the Guardrails node, metrics report by email | [#10729](https://n8n.io/workflows/10729-benchmark-content-safety-guardrails-with-automated-test-suite-and-reports/) |
| [Google Sheets Batch Enrichment](workflows/data-enrichment/google-sheets-batch-enrichment/) | Data Enrichment | Calls a REST API per sheet row in rate-limited batches and writes the result back | [#14205](https://n8n.io/workflows/14205-enrich-google-sheets-rows-via-any-rest-api-in-rate-limited-batches/) |
| [Smart Sales Invoice Processor](workflows/data-processing/smart-sales-invoice-processor/) | Data Processing | Turns a sales CSV into validated invoices in n8n Data tables, with 200/400/409 responses | [#10274](https://n8n.io/workflows/10274-process-sales-csvs-into-invoices-with-data-tables-and-email-notifications/) |

## How each workflow is documented

Every workflow README answers the same four questions in the same order, so you can compare them at a glance:

* **Metric:** which number shows that the workflow works.
* **Pattern:** the data flow in one sentence.
* **Principle:** why it is built this way and which failure it prevents.
* **Question:** one prompt for adapting it to your own case.

## Where the ideas come from

[TeloSignal](https://www.telosignal.com/data/n8n-use-case-demand-index) indexes 13,500+ public n8n templates every week. New workflows in this vault target categories where that index shows demand but few well-documented templates.

---

## 🛠️ Quick Start

1.  **Download:** Pick a workflow from the table above and copy its `workflow.json`.
2.  **Import:** In your n8n instance, click **Import from File** or paste the JSON into the canvas.
3.  **Configure & run:** Add the credentials and variables listed in the workflow's README and sticky notes, then run it once.

---

## 🧠 MCP Experts
This vault includes AI Experts hosted on Vercel.

### Hormozi Expert

- **Location:** [mcps/hormozi-mcp](mcps/hormozi-mcp/)
- **MCP Endpoint (Streamable HTTP):** `https://<your-vercel-project>.vercel.app/mcp`
- **Tool:** `analyze_vault_workflow`
- **Usage:** Critique workflows using the $100M Offer framework.

---

## 📝 License

Distributed under the MIT License. See [LICENSE](https://github.com/patrick-creates/telosignal-workflow-vault/blob/main/LICENSE)  for more information.
