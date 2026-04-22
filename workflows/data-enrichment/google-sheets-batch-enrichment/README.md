# Google Sheets Batch Enrichment

> Published on [n8n Creator Hub](https://n8n.io/creators/patrickn8n/) · [TeloSignal](https://telosignal.com)

**The Hormozi Value Claim:** "Eliminate 90% of manual data enrichment costs while increasing lead-conversion likelihood by providing real-time intelligence directly in your CRM"

## What this workflow does

Reads every row from a Google Sheet, calls a configurable REST API once per row in rate-limited batches, then writes enriched data back to the sheet or logs errors.

## Metric

Full sheet enriched without hitting API rate limits — configurable batch size and wait time keep requests within any API's threshold.

## Pattern

Rate-limited batch loop: split rows → call API per row → wait between batches → write successes back → log failures → repeat until done.

## Principle

Batching with enforced waits prevents rate-limit errors. Routing success and failure to separate branches keeps the sheet clean and makes errors traceable without stopping the run.

## Question

Which other data source would you enrich this way — a CRM export, a lead list, or a product catalog?

---

## Setup

1. Import `workflow.json` into n8n
2. Configure credentials:
   - Google Sheets OAuth2 (connect to both Sheet nodes)
   - Header Auth credential for your external API
3. Set variables:
   - Sheet ID and tab name in the **Read Rows** node
   - API endpoint URL in the **Call API** node
   - Batch size and wait duration via sticky notes inside the workflow
   - Column(s) to write back in the **Update Row** node
4. Activate

## Nodes used

| Node                       | Purpose                                                          |
|----------------------------|------------------------------------------------------------------|
| Google Sheets (Read Rows)  | Reads all rows from the source sheet                             |
| Split In Batches           | Splits rows into configurable-size batches                       |
| HTTP Request               | Calls external REST API once per row (GET or POST, Header Auth)  |
| Wait                       | Pauses 1 second between batches to respect rate limits           |
| Google Sheets (Update Row) | Writes enriched data back to the sheet on success                |
| Error Logger               | Captures and logs failed API calls separately                    |
