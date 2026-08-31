# AI Engineer Track — Build 02 · Agentic 3-Way Document Match

An agentic workflow that automates **invoice / purchase-order / receipt (3-way) matching** — the
classic accounts-payable control — built as an **n8n workflow with deterministic LLM extraction,
discrepancy detection, and a human approval path.** Includes a schema-backed Postgres store and a
measured cost / ROI analysis.

This build shows the **agentic-workflow + automation-engineering** side of the portfolio: not just a
model call, but a supervised business process with verification and economics.

---

## What it does

1. **Generate** — `generator.py` creates a synthetic document set (invoice / PO / receipt per row)
   with ~8% of rows **seeded with discrepancies** (amount mismatch).
2. **Extract** — n8n Code nodes (`nodes/extract.js`) enforce a **JSON-schema contract** for the
   structured fields the match logic needs.
3. **Match** — `nodes/match3way.js` runs the deterministic 3-way rule: amounts agree (within EPS)
   and vendor agrees across all three documents.
4. **Classify / Approve / Dead-letter** — matching rows proceed to approval; mismatches are
   classified, routed to an approver, or dead-lettered.
5. **Verify** — `verify_match.py` proves the logic **flags every seeded discrepancy** (recall) with
   no false positives.
6. **Cost it** — `cost_report.py` turns the automation into ROI.

---

## Architecture

```
 generator.py ──▶ documents.json ──▶ n8n workflow (nodes/)
                                        ├─ extract.js      → structured fields (JSON schema)
                                        ├─ classify.js     → match / mismatch / exception
                                        ├─ match3way.js    → deterministic 3-way rule
                                        ├─ approval.js     → human decision
                                        └─ deadletter.js   → quarantine
                                            │
                                            ▼
                                   Postgres (schema.sql)  +  verify_match.py (proof)
```

| Component | File | Role |
|---|---|---|
| Synthetic data | `generator.py` | Documents with seeded discrepancies (seeded `random.seed(7)` for reproducibility) |
| Schema contract | `nodes/extract.js` | Structured extraction shape (`invoice_no`, `total`, `vendor`, `date`) |
| Match logic | `nodes/match3way.js` | Amount + vendor agreement across invoice/PO/receipt |
| Verify (Python) | `verify_match.py` | Same rule, run in CI/tests — proves recall + precision |
| Persistence | `schema.sql` | `documents` table with status, decision, approver, timestamps |
| Economics | `cost_report.py` | Assumptions-based ROI model |
| Runtime | `docker-compose.yml` | n8n + Postgres |

---

## Quick start

### 1. Generate the document set

```bash
python generator.py
# writes documents.json with 40 rows, ~8% seeded mismatches
```

### 2. Prove the match logic catches every discrepancy

```bash
python verify_match.py
# seeded discrepancies: N
# flagged: N
# recall on seeded mismatches: 100%
```

### 3. Run the n8n workflow

```bash
docker compose up -d
# n8n → http://localhost:5678  (admin / admin — change in production)
# Postgres on :5432, database "docs"
```

In n8n, import the node scripts into a workflow and run the extraction → match → classify →
approve / dead-letter sequence. The `nodes/*.js` files are drop-in Code nodes.

### 4. Read the economics

```bash
python cost_report.py
# weekly cost: $X.XX   hours saved: 25.0   weekly saving: $1,250.00   ROI: Nx
```

---

## Design notes

- **Deterministic core, LLM at the edges.** Extraction uses an LLM (with a JSON-schema contract),
  but the *match decision* is a plain deterministic rule. That means the business control is
  guaranteed regardless of model behaviour — the same philosophy as the agent builds in this track.
- **Proven, not assumed.** `verify_match.py` is the CI-style check that the workflow's own logic
  flags every seeded discrepancy. (In production this would be a pytest/golden-set suite.)
- **SQL-schema persistence** means every decision (status, approver, timestamp) is auditable.

---

## Portfolio context

| Build | Repo | Focus |
|---|---|---|
| 01 | [`ai-engineer-track`](https://github.com/koatedevopskpai/ai-engineer-track) | Agent + RAG vertical slice |
| 02 | [`ai-engineer-track-build-01`](https://github.com/koatedevopskpai/ai-engineer-track-build-01) | Guardrails, evals, HITL, Docker |
| **03** | **this repo** | **Agentic workflow (n8n) + cost/ROI + audit trail** |

---

## What this demonstrates
- **Agentic workflow orchestration** (n8n) with a human approval path.
- **Deterministic business rules** over LLM-extracted data — reliability by design.
- **Verification** — the match logic is proven against seeded defects (recall/precision).
- **Cost-awareness** — ROI modeled, not hand-waved.
- **Auditability** — schema-backed decisions with approver + timestamps.

---

## Security note
The n8n basic-auth credentials (`admin`/`admin`) and Postgres password in `docker-compose.yml` are
**local-development defaults** — override them before any shared or production deployment.

---

## License
MIT — free to use, learn from, and build on.

---

*Built as part of a personal AI engineering portfolio. Questions or feedback welcome via issues.*