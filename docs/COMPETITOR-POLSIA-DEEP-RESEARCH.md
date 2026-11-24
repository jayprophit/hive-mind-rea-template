# Polsia — consolidated competitive research (supplied 11 and 24 November 2026)

Two independent research assessments were supplied by the user and are filed
here as source material for the REA loop. They describe the **commercial**
`polsia.com` platform and adjacent systems; they are not instructions to copy
its implementation, and nothing here is legal, tax or financial advice.

**Provenance and limits.** Claims are attributed to their published sources
(Polsia public docs/terms, its GitHub README, a Mixergy interview of 27 May
2026, a Trustpilot snapshot of 3.5/5 across 482 reviews, vendor comparison
pages and public architecture docs). They were not independently audited for
this project. Polsia is our initial reference product, not our architectural
limit. Section 17 of the second assessment is explicit: studying functional
behaviour is acceptable, reproducing proprietary implementation is not.
Polsia's published acceptable-use policy restricts copying and derivative
works, subject to applicable law and permission.

## A. Business assessment (11 Nov 2026)

### Reported platform economics
| Item | Reported figure |
|---|---|
| Payment fee | 3% of customer payments (older reviews still say 20%) |
| Advertising fee | 20% of ad budget |
| Customer settlement | 31 days, no reported payout cap |
| Listed plans | $0 / $20 / $50 / $100–200 per month, with credits |

**Our position:** no credits, no revenue share, no payout hold, no paid or
feature gates. Funds and keys remain the user's. This is a deliberate
difference, not an oversight.

### Founder-reported earnings evidence (unaudited)
From the Mixergy interview: 10% of businesses earning at least $1 (figure
ambiguous in the source), highest observed business revenue $3k–$4k (period
unclear), ~50% first-month churn for Polsia's own customers, and no
independently verified millionaires found. Polsia's own multi-million ARR does
not imply its users' businesses were similarly successful. **No independently
audited current maximum for a customer business was established.**

Honest framing adopted here: £1k–£5k/month is a plausible small-business
target, £10k–£100k/month needs proven demand and retention, £1m+/year is an
exceptional result rather than a reasonable expectation. No probability is
attached and no return is promised.

### Recommended vertical (reference only)
B2B contract intelligence: discover and qualify public procurement
opportunities for smaller suppliers. Initial segment proposed: facilities
management and commercial cleaning. Data supply cited: ~800,000 EU notices a
year worth >€815bn, plus UK Find a Tender. At a hypothetical £99/month, ~842
paying customers gives £1m annualised revenue and ~4,210 gives £1m operating
profit at a 20% margin. Demand and price are **unvalidated**.

Launch gate proposed: 20–30 discovery contacts and three businesses willing
to commit to a paid pilot before major engineering or paid advertising.
Operating rule: never present AI eligibility output as a verified legal
conclusion; keep official source links and flag uncertainty.

## B. Full gap and architecture research (24 Nov 2026)

### Core thesis
The opportunity is not "more agents" but a more **reliable, accountable,
economical and recoverable** autonomous system. Combine Polsia's onboarding
simplicity with Paperclip-style organisational governance, durable workflow
execution, interchangeable agent harnesses, traditional business systems and
optional decentralised infrastructure.

### Customer-feedback problem categories and our local answers
| Reported problem | Local answer already present |
|---|---|
| Same bug fixed repeatedly | independent tests + regression detection |
| Credits spent on agent mistakes | no credits; repairs recorded as free fixes |
| "Fixed" but still broken | evidence-based completion criteria |
| Stalled onboarding | resumable local onboarding |
| Delayed projects | deadlines, escalation, alternate owner |
| Variable output quality | quality gates + human review |
| Hard to get support | diagnostics export + human escalation |
| Uncertain commercial results | validate demand; never invent metrics |
| Too much founder intervention | one-time remembered authorisation, sensitive actions re-ask |
| Generated apps hard to extend | portable repo + documented architecture |

Categories are deduplicated from self-selected reviews; frequency and severity
were not measured.

### Competitor landscape to keep watching
- **Autonomous company platforms:** Paperclip, NanoCorp, Cofounder, Atoms, Soleur, Marblism, Sintra AI, Lindy, Relevance AI, Manus. Paperclip is the strongest control-plane reference (hierarchy, adapters, budgets, heartbeats, duplicate-task prevention, multi-company isolation, approvals).
- **Agent harnesses:** OpenClaw, Hermes Agent, Claude Code, Codex, OpenCode, OpenHands, Cline, Roo Code, Aider, Goose. Use a standard adapter interface rather than permanently selecting one.
- **Orchestration:** LangGraph, CrewAI, Microsoft Agent Framework, AutoGen, Google ADK, OpenAI Agents SDK, MetaGPT, CAMEL, Semantic Kernel, Pydantic AI. LangGraph's persistent stateful execution is the notable pattern.
- **Workflow / ERP:** n8n, Make, Zapier, Activepieces, Node-RED, Temporal, Airflow, Prefect, Odoo, ERPNext, Twenty, Mautic, Appsmith, Metabase. Deterministic workflows should handle predictable work; not everything needs an LLM.
- **Knowledge / models:** Obsidian, Graphify, GraphRAG, Neo4j, Mem0, Letta, Qdrant, pgvector, Ollama, LM Studio, llama.cpp, vLLM, LiteLLM, OpenRouter, DSPy. These overlap with engines we already run.
- **Decentralised:** Olas, Fetch.ai/ASI, SingularityNET, Bittensor, Akash, Golem, Nosana, io.net, IPFS, Filecoin, libp2p, Matrix, Hyperledger Fabric, Ethereum, Safe, Aragon, W3C DID, Verifiable Credentials, CometBFT, Automerge/Yjs. No blockchain requirement for routine work; private data stays off-chain.

### Deployment modes from one core
Centralised cloud, self-hosted, local/offline, decentralised, hybrid/federated.
Configure compute, governance and settlement independently — distributed
infrastructure does not automatically mean decentralised governance.

### Proposed 100-area checklist and audit classifications
100 proposed assessment areas (not 100 confirmed defects). Classify each as
Verified, Implemented, Partial, Unverified, Missing, Defective, Placeholder,
Proposed or Redundant, with requirement IDs, evidence, file locations,
severity, dependencies and acceptance tests. A dashboard showing agents,
revenue or blockchain nodes is **not** evidence those systems work; frontend
display and operational backend must be assessed separately.

### Proposed performance targets
Zero unauthorised financial actions, zero cross-company leakage, zero duplicate
payments, 100% recovery in defined failure scenarios, ≥95% routine task
completion, no unresolved critical vulnerabilities, 100% external-action
logging, 100% budget enforcement, tested rollback, measured idle consumption,
defined offline core, successful export/restore, interchangeable providers.
OWASP Top 10 for Agentic Applications 2026 is suggested as an independent
security frame. Targets are proposals, not certifications.

### Self-healing rule
No agent marks its own work complete solely because it believes it succeeded.
Acceptance criteria, tests and evidence are required; retries are bounded then
escalated. Temporal's durable execution is the reference for surviving crashes.

## C. What changed in this project

- Filed as `docs/COMPETITOR-POLSIA-DEEP-RESEARCH.md` and mirrored into the app
  registry `app/src/competitive-intel.js` (`window.PFV1_INTEL`), imported by
  `main.js`. It is knowledge and guardrails only: no integration, no gates.
- Added client-owned data layer `app/src/data-ownership.js` (`window.PFV1_DATA`):
  local-first, user-chosen GitHub/cloud/Obsidian backup targets, GDPR-aligned
  rights (access, rectification, erasure, portability, objection, restriction),
  no silent upload, secrets only in bridge env, no legal certification claimed.
- Connector routes wired so user-chosen services stay optional and env-held.
- Status of each area is tracked honestly as LIVE / REFERENCE / HUMAN / MISSING
  in `docs/COVERAGE-AND-GAPS.md`.

## D. Not adopted

Paid gates, credits, revenue share, payout holds, invented metrics or
testimonials, guaranteed returns, blockchain as a requirement, bulk
unsolicited messaging, paid advertising without authorisation, copying
proprietary code/assets/prompts. Regulated activity stays human and
jurisdiction-specific.
