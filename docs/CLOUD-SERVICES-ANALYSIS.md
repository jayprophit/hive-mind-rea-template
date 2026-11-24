# Cloud workbenches and media services — 2026-11-24

Fetched live where possible. None is a hard dependency; all use the person's own
account and free quotas. Paid tiers are never required to finish a task.

## Kaggle — `https://www.kaggle.com/`
- The page is JS-rendered; the live title is "The World's AI Proving Ground".
- Known offering: free notebook runtimes with weekly GPU/TPU quotas, public
  datasets, competitions and model/dataset hosting.
- **Benefit to the build:** dataset research, evaluation of small open models,
  batch REA/measurement jobs. Not needed for the static app itself.
- **Verdict:** useful optional workbench; add as an optional runtime entry, not
  a dependency.

## Google Colab — `https://colab.research.google.com/`
- JS-rendered sign-in page; free notebook runtime with limited GPU/TPU.
- **Benefit:** run the same REA/byte-accounting scripts and small-model tests in
  the cloud without using the laptop's 8 GB RAM.
- **Verdict:** useful optional workbench; same status as Kaggle.

## Higgsfield — `https://higgsfield.ai/`
- Live page confirms an AI-native creative suite: image, video and voice
  generation, editing room (change angle/light/camera), **cloud computer with
  GPU** running Blender and LoRAs through MCP, 35+ frontier models, an agentic
  production engine, and a **Higgsfield MCP for Claude**.
- Currently running a paid-plan sale (69% off) — it is a commercial product,
  with limited trial credits rather than a durable free tier.
- **Benefit:** if you choose to use it, it can supply high-quality image/video
  beyond our local Pillow/ffmpeg placeholders, and its GPU computer can host
  creative workloads. `higgsfield mcp` was already marked "pending / needs API
  key identification" in `INTEGRATIONS.md`.
- **Verdict:** optional paid integration with your own key; never required.
  Local generation (Pillow, SVG, ffmpeg, edge-tts, faster-whisper) remains the
  free default.

## Hugging Face Spaces — `https://huggingface.co/spaces`
- Live catalogue shows free CPU Spaces and many ZeroGPU demos: image/video
  generation, voice isolation, TTS, OCR, face swap, 3D generation, agent-memory
  leaderboards and MCP-tagged spaces.
- **Benefit:** free hosted endpoints for image/video/audio models that our
  8 GB machine cannot run; ZeroGPU is a PRO feature.
- **Verdict:** strong free/optional source of model demos and API endpoints;
  useful for media generation without local GPU.

## Oracle Always Free — `https://www.oracle.com/cloud/free/`
- Direct fetch returned 403, so no live quote here. The documented Always Free
  tier is 4 ARM OCPUs / 24 GB RAM, permanently free.
- **Benefit:** the always-on team VM in `DEPLOYMENT-ARCHITECTURE.md` — one VM for
  the team, containers per bot, running Ollama and the bridge 24/7.
- **Verdict:** best free answer to "own cloud computer per bot"; verify current
  terms at signup.

## Others worth noting
- **Cloudflare Workers AI**: free daily allowance across ~76 models (Llama 3.2
  3B, Gemma, Qwen, Whisper, FLUX, embeddings) — already in `app/src/models.js`.
- **GitHub**: repo + Actions (CI/cron), Pages (static site), Codespaces (60 h/mo),
  GitHub Models free tier — already in `models.js` `GITHUB_RUNTIMES`.
- **Replicate / fal.ai**: paid per-use model APIs; useful only with your own key,
  never required.

## Decision
Add Kaggle, Colab, HF Spaces, Higgsfield and Oracle as **optional** entries in
the model/cloud registry (`CLOUD_SERVICES` in `app/src/models.js`). Keep local
generation and free tiers as defaults. Do not add any paid gate to the app.
