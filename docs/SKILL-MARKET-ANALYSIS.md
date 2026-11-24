# Skill / marketplace discovery — 2026-11-24

Sources supplied by the person. Each entry records what the site actually is,
what it offers, licence/posture where stated, and what is relevant to Polsia
Free v1. Findings are observations from the fetched pages, not endorsements.
No code was copied into `app/`.

## 1. Claude Code Marketplaces — `https://www.claudemarketplace.net/`
- Independent directory: **4,570+ skills, 1,075+ MCP servers**, 150k monthly visitors, updated daily.
- Browse by skill category, marketplace and MCP category. Popular skills include `find-skills`, `vercel-react-best-practices`, `frontend-design`, `web-design-guidelines`, `agent-browser`.
- Popular MCP servers: Fetch, Sequential Thinking, Everything, Git, Memory, Time (mostly `modelcontextprotocol/servers`).
- Some listings are paid datasets ($4.99) or one-time tools; most are free.
- **Relevant:** source of skill names to mirror in our `SKILLS` registry; no dependency required.

## 2. SkillsMP — `https://skillsmp.com/`
- Largest aggregator: **~4,000,000 open-source agent skills**, 12 domains, 50+ categories, 9 languages.
- **Free REST API** and **MCP server**. Anonymous REST: 50 request attempts/UTC day, 10/min. Account keys free tier: 50 successful searches/day; Standard 5,000; Professional 25,000 per month. MCP needs browser OAuth sign-in or an API key. A2A agent card at `/.well-known/agent-card.json`.
- Creator search (`?creator=<github-login>`) is exact, case-insensitive.
- **Relevant:** a real, free, standards-based skill-discovery endpoint we could add as an optional `MCP_SERVERS` entry / capability. No key needed for low-volume anonymous use.

## 3. Claude Marketplaces — `https://claudemarketplaces.com/`
- Independent directory ranked by real installs; **18,175 skills, 4,090 MCP servers, 11,156 plugins**.
- Notable plugins: `rea` (reverse engineer anything), `superpowers`, `ecc` (72 agents, 328 skills), `mattpocock-skills`, `n8n`.
- Notable MCP: Context7, Supabase, Browser Use, GitHub, PubMed, Repowise.
- **Relevant:** `rea` aligns with our REA loop; Context7/Browser Use align with our discover/browser capabilities. All are optional external tooling.

## 4. alirezarezvani/claude-skills — GitHub
- Public, MIT, **30.4k stars, 4.2k forks**. 434 production-ready skills for Claude Code, Codex, Gemini, OpenClaw, Hermes, Cursor, OpenCode and more.
- Folders by domain: engineering, product, marketing, finance, c-level, compliance, research, video, etc. 824 stdlib-only Python tools, 931 reference docs.
- Standout: `human-gate`, `skill-retro`, `agent-run-forensics`, `mcp-server-builder`, `skill-security-auditor` (scans for command injection/exfiltration).
- Windows note: clone with `-c core.symlinks=true`, set `PYTHONUTF8=1`.
- **Relevant:** strong match for our role team and human-gate design. `skill-security-auditor` is worth adding as an install gate. MIT licence permits use; still no code copied into `app/`.

## 5. AI Templates — `https://www.aitmpl.com/skills/`
- **946 Claude skills**, plus agents, commands, settings, hooks, MCPs and plugins; backed by `davila7/claude-code-templates` (30.8k stars). Stack Builder for composing installs.
- **Relevant:** large catalogue for optional skill discovery; no dependency.

## 6. Collective Brain — `https://collectivebrain.de/en/skills/`
- **111 vetted skills**, 8 categories (Design & UX, Branding, Product, Visual, AI & Automation, Development, Content & Marketing, Office & Data), all free; up to two new per day after a security check.
- Includes `Defuddle` (clean article → Markdown), `Accessibility Review (WCAG 2.1 AA)`, `Schema Markup Generator`, `Find Skills`, `Obsidian Markdown`, `MCP Builder`.
- **Relevant:** `Defuddle` and `Obsidian Markdown` complement our Obsidian export; accessibility and schema skills complement our page rebuild checks.

## 7. Marketing Skills — `https://marketing-skills.com/skills`
- **53 open-source marketing skills** for Claude Code, Codex, Cursor (`coreyhaines31/marketingskills`), v2.14.28. Domains: SEO (8), Copy (7), CRO (7), Ads (6), Lifecycle (6), Growth (7), Strategy (5), Research (7).
- Includes `reverse-engineer-marketing`, `competitors`, `pricing`, `onboarding`, `paywalls`.
- **Relevant:** `pricing` and `onboarding` inform the payments/invoice work; `reverse-engineer-marketing` aligns with our REA discovery phase.

## 8. MCP Servers — `https://mcpservers.org/agent-skills`
- Large agent-skills library with official author indexes: Anthropic 575, OpenAI 450, GitHub 515, Microsoft 869, Cloudflare 107, Vercel 341, Google Workspace 99.
- Categories include document, browser automation, database, research, video, image, productivity, data analysis.
- Notable: `agent-browser` (Vercel), `firecrawl-*` (deep research, QA, competitive intel), `remotion-best-practices`, Anthropic docx/xlsx/pptx/pdf (some proprietary licences).
- **Relevant:** `agent-browser` and Firecrawl tools match our BROWSER_AUTOMATION capability; note proprietary licences on some Anthropic document skills.

## Synthesis for Polsia Free v1

1. **No new hard dependency is justified.** All eight are directories or skill packs; our app already has its own registries and free defaults.
2. **Optional integrations worth adding to registries** (all free/standard):
   - SkillsMP REST/MCP for skill discovery (anonymous quota available)
   - Context7 for up-to-date docs
   - Browser Use / Vercel Agent Browser for browser automation
   - `skill-security-auditor` as an install gate (MIT repo)
   - `Defuddle` + Obsidian Markdown for second-brain export
3. **Licence caution:** Anthropic document skills and some PPTX entries are marked proprietary; do not vendored them into `app/`. Prefer MIT/open-source packs.
4. **Pattern match:** the `human-gate`, `skill-retro` and REA plugins validate the design already chosen in `docs/TEAM-BRIEF.md` — we are aligned with the ecosystem rather than missing a standard.

This analysis closes the "identify these sites" ask. Installing any of them is optional and gated by the person's choice; none is required for a feature.
