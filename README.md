![n8n Creator Hub](https://img.shields.io/badge/n8n-Creator%20Hub-FF6D5B?style=flat-square&logo=n8n)
![Maintenance](https://img.shields.io/badge/Maintained-Yes-green?style=flat-square)

# TeloSignal Workflow Vault

> Production-ready n8n workflow templates — built and maintained by [TeloSignal](https://telosignal.com), The n8n Workflow Intelligence Index.

Most n8n workflows are built to "just work." These are built to scale. This vault contains the core logic used by TeloSignal to manage complex data lineage, automated testing, and high-volume processing.

Published on the [n8n Creator Hub](https://n8n.io/creators/patrickn8n/).

---

## 💎 The TeloSignal Standard

Every workflow in this repository is built using our proprietary **4-Element Formula**. We don't just move data; we build intelligence.

* **Metric:** Defining the success criteria for the automation.
* **Pattern:** Utilizing proven architectural structures for data flow.
* **Principle:** Applying rigorous logic gates and error-handling rules.
* **Question:** Ensuring the workflow answers a specific business hypothesis.

---

## 📊 Market Intelligence Source
This repository is the execution arm of the [TeloSignal n8n Demand Index](https://www.telosignal.com/data/n8n-use-case-demand-index). 

Every workflow here is built to address specific **"High-Value Scarcity"** gaps identified in our weekly index of 9100+ templates. We don't build random automations; we build for the categories where demand is high but reliable solutions are scarce.

---

## 🚀 Workflows

| Workflow | Category | Description |
|----------|----------|-------------|
| [Google Sheets Batch Enrichment](workflows/data-enrichment/google-sheets-batch-enrichment/) | Data Enrichment | API batch enrichment into Google Sheets |
| [Smart Sales Invoice Processor](workflows/data-processing/smart-sales-invoice-processor/) | Data Processing | Invoice processing with Data Tables |
| [Benchmark Content Safety Guardrails](workflows/ai-safety/benchmark-content-safety-guardrails/) | AI Safety | Automated test suite & reports for content safety |

---

## 🛠️ How to Use

1.  **Browse:** Select a workflow from the table above.
2.  **Download:** Copy the `workflow.json` file from the directory.
3.  **Import:** In your n8n instance, click **Import from File** or simply paste the JSON into the canvas.
4.  **Configure:** Add your specific credentials and environment variables as noted in the workflow annotations.

---

## 🧠 MCP Experts
This vault includes AI Experts hosted on Vercel.

### Hormozi Expert

- **Location:** [mcps/hormozi-mcp](mcps/hormozi-mcp/)
- **SSE Endpoint:** `https://<your-vercel-project>.vercel.app/sse`
- **Tool:** `analyze_vault_workflow`
- **Usage:** Critique workflows using the $100M Offer framework.

---

## 📝 License

Distributed under the MIT License. See [LICENSE](https://github.com/patrick-creates/telosignal-workflow-vault/blob/main/LICENSE)  for more information.
