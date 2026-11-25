# Extracted research: Aetherius/Genesis — best parts for Polsia Free v1

Source files (supplied by the user, 8 and 24 Nov 2026):
`Aetherius_Cloud_Fabric_Conversation_FULL.txt` and
`Aetherius_Genesis_Research_Conversation_FULL.txt`. The transcripts are
best-effort exports with explicitly partial sections; claims are attributed,
not independently verified. Nothing from those projects' code was copied.

## 1. Transferable mechanisms worth having locally

| Mechanism | Source idea | Local implementation here |
|---|---|---|
| Cost preference ladder | LEVEL 0 local/self-hosted → LEVEL 1 forever-free → LEVEL 2 renewable free → LEVEL 3/4 paid only with explicit authorisation; TRIAL_ONLY excluded | `app/src/cloud-fabric.js COST_LEVELS`, `FREE_TIER_CLASSES`, `DEFAULT_PAID_POLICY` |
| Zero-surprise billing | `paid_usage_allowed: false`; warn/reduce/failover at 70/80/90/95/100% of a free quota; FREE→PAID needs an approval event | `quotaController()` in the same module |
| Service classes | Storage ≠ object ≠ Git ≠ DB ≠ cache ≠ queue ≠ compute ≠ inference ≠ email ≠ identity | `SERVICE_CLASSES` |
| Provider registry schema | Machine-readable fields, last-verified dates and provenance; **never credentials in the file** | `PROVIDER_REGISTRY` entries with no secrets |
| Logical directory tree | One user-facing path tree over many physical backends | `VIRTUAL_TREE`, `routeObject()` |
| Object provenance | object_id, logical_path, content_hash, classification, backends, sync state | `OBJECT_REGISTRY_FIELDS` |
| Data classes and routing | Secrets only in a vault; code/docs in Git; DB in a DB; large media in cheap storage | `DATA_CLASS_ROUTES` |
| Deduplication | Content hash → object identity, never across access-control boundaries | `DEDUP_RULE` |
| Replication tiers | PRIMARY / MIRROR / BACKUP / ARCHIVE are not interchangeable | `REPLICATION_ROLES`, `TIERED_DATA` |
| Sync engine | Stable IDs, change journal, outbox, checkpoints, idempotency, tombstones, explicit conflict model, offline queue | `SYNC_ENGINE_FIELDS`, `CONFLICT_MODELS` (reference) |
| Credential broker | KeePass-style vault; scoped, time-limited tokens; secrets never in repos, YAML, chat or logs | `CREDENTIAL_BROKER_RULES` (guardrails only) |
| Provisioning agent | Idempotent, checkpointed steps; genuine human gates for registration, MFA, KYC, legal and payment | `PROVISIONING_GATES` |
| Evidence states | PROPOSED → DESIGNED → PARTIAL → IMPLEMENTED → TESTED → VERIFIED → BLOCKED | `EVIDENCE_STATES` |
| AI-to-AI messaging | Typed envelope, schemas, signing, scoped permissions, durable bus, translation, human-auditable consequences | Already present via `PROTOCOLS`, bus and A2A envelope; `AGENT_MESSAGE_RULES` records the guardrails |

## 2. Griffin / continuous interaction — useful architecture, not a dependency

From the Griffin research the valuable idea is a **time-synchronised
interaction layer**: perception → reasoning → turn-taking → speech → rendering,
with interruption handling, rather than a chatbot bolted onto an avatar.
Reported vendor figures (48% human-belief after one minute, 720p generation,
VideoFDB 3.83 vs human 3.92) are Tavus/NVIDIA-reported benchmarks, **not**
evidence of consciousness or emotion. Griffin-Lite is research-preview only.

Hardware reality noted in the research: a ~3 GB GTX 1050 cannot do Griffin-class
720p real-time diffusion; local text, microphone, webcam, lightweight vision,
offline STT/TTS and a 2D/lightweight-3D avatar are feasible. This is why our
local implementation uses browser APIs, SVG/canvas rendering and the existing
optional bridge, with no paid avatar service and no model-training claims.

## 3. Free open-source candidates (research/reference only, licences checked separately)

whisper.cpp (MIT) offline STT · Kokoro-82M (Apache 2.0) local voice ·
MediaPipe (Apache 2.0) face/body tracking · OpenFaceFX (MIT) phoneme animation
study · Linly-Talker-Stream (Apache 2.0) full-duplex study · MuseTalk 1.5
(MIT code) neural face study · StreamAvatar and whisper.cpp as references ·
MiniCPM-o 4.5 as a research reference (~12 GB GPU, not for this machine).

These are **candidates**, not installed dependencies. Licences for code, model
weights, voices, datasets and bundled assets must be audited individually.

## 4. Boundaries adopted

-Local-first and £0 by default; no subscriptions, credits or Tavus dependency.
-Disclose that the human is AI; do not present deception as success.
-No claims of emotion, consciousness or a first-party trained model where none
 exists; optional Ollama models are labelled temporary test backends.
-Human gates for sensitive or irreversible actions; all actions audited.
-Simulations and registries are never presented as implemented systems.
