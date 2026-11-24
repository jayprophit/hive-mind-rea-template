#!/usr/bin/env python3
"""Generate the formal 100-area requirement audit for Polsia Free v1.

Each area has a permanent ID, an honest classification, a file location,
severity and an acceptance test. Classification vocabulary follows the
research supplied on 24 Nov 2026: Verified, Implemented, Partial, Unverified,
Missing, Defective, Placeholder, Proposed, Redundant. A dashboard showing a
capability is not evidence that the capability works.
"""
from __future__ import annotations

from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
OUT = REPO / "docs" / "REQUIREMENT-AUDIT-100.md"

# (id, category, area, classification, evidence, severity, acceptance test)
AREAS: list[tuple[str, str, str, str, str, str, str]] = [
    # UI and UX (12)
    ("U01", "UI/UX", "Five public pages pixel likeness", "Verified", "craft.json checks round 25, 99.9%", "low", "rebuild_check >=99% at 1440/768/390"),
    ("U02", "UI/UX", "Authenticated dashboard 4 columns", "Implemented", "app/src/dashhome.js", "low", "browser check: 4 columns"),
    ("U03", "UI/UX", "Dashboard 19 panels", "Implemented", "app/src/dashhome.js", "low", "browser check: 19 panels"),
    ("U04", "UI/UX", "Dashboard 59 controls", "Implemented", "app/src/dashhome.js", "low", "browser check: 59 controls"),
    ("U05", "UI/UX", "Dashboard typography fidelity", "Partial", "checks/dash-diff.png ~90.7%", "high", "pixel similarity >=95% vs picture-1.png"),
    ("U06", "UI/UX", "Onboarding asks type and name", "Verified", "app/src/onboarding.js, tests", "low", "end-to-end /new provisioning"),
    ("U07", "UI/UX", "Burger and cascading menus", "Implemented", "app/src/nav.js", "low", "menu opens on every page"),
    ("U08", "UI/UX", "Floating team chat", "Implemented", "app/src/chat.js", "low", "chat widget on every page"),
    ("U09", "UI/UX", "Consent banner with choices", "Implemented", "app/src/main.js", "low", "choice persisted in localStorage"),
    ("U10", "UI/UX", "72 currency options", "Implemented", "app/studio/index.html", "low", "currency select has 72 options"),
    ("U11", "UI/UX", "Responsive widths", "Verified", "craft.json claims, all widths pass", "low", "no horizontal scroll at 390/768/1440"),
    ("U12", "UI/UX", "Public activity feed route", "Implemented", "app/src/mechanisms.js LIVE_FEED", "low", "/live/ renders local bus records"),
    # Agent team (10)
    ("T01", "Team", "58 dashboard actions", "Verified", "app/src/dash-data.js, smoke test", "low", "npm test asserts count"),
    ("T02", "Team", "Role-only team registry", "Verified", "app/src/studio.js ROLES, smoke test", "high", "no model name is a role id"),
    ("T03", "Team", "Swappable engine registry", "Verified", "app/src/registries.js, smoke test", "high", "assignEngine honours override"),
    ("T04", "Team", "Lead and QA roles", "Verified", "app/src/studio.js, smoke test", "low", "ROLES contains lead and QA"),
    ("T05", "Team", "Ten inter-agent languages", "Verified", "app/src/studio.js LANGUAGES, smoke test", "low", "routeLanguage covers 10"),
    ("T06", "Team", "Skills registry", "Verified", "app/src/studio.js SKILLS, smoke test", "low", "skill-retro present"),
    ("T07", "Team", "Hooks", "Verified", "app/src/studio.js HOOKS, smoke test", "low", "hook list non-empty"),
    ("T08", "Team", "Subagent types", "Verified", "app/src/studio.js SUBAGENT_TYPES, smoke test", "low", "types registered"),
    ("T09", "Team", "Workflows", "Verified", "app/src/studio.js WORKFLOWS, smoke test", "low", "workflows registered"),
    ("T10", "Team", "Interactive member picker absent", "Verified", "deep_gap_audit.py marker 1", "high", "audit reports 0 FAIL"),
    # Autonomy and oversight (8)
    ("A01", "Autonomy", "Auto mode intervals", "Implemented", "app/src/studio.js", "high", "hours to years selectable"),
    ("A02", "Autonomy", "Authorise once, remembered", "Implemented", "app/src/actions.js", "high", "approval stored locally"),
    ("A03", "Autonomy", "Human gates on sensitive actions", "Verified", "app/src/studio.js HUMAN_GATES, smoke test", "critical", "payment needs confirm"),
    ("A04", "Autonomy", "Sensitive actions re-ask", "Implemented", "app/src/mechanisms.js approvalFor", "critical", "SENSITIVE set returns ask"),
    ("A05", "Autonomy", "Three approval levels", "Implemented", "app/src/mechanisms.js APPROVAL_LEVELS", "medium", "plan/ask/auto present"),
    ("A06", "Autonomy", "Decision register with reasoning", "Implemented", "app/src/mechanisms.js", "medium", "recordDecision stores reasoning"),
    ("A07", "Autonomy", "Cofounder pushback persona", "Implemented", "app/src/mechanisms.js COFOUNDER_PERSONA", "low", "rules tied to evidence"),
    ("A08", "Autonomy", "Autonomous bootstrap", "Verified", "app/src/studio.js, audit marker", "medium", "audit marker passes"),
    # REA and evidence (8)
    ("R01", "REA", "13-phase REA loop", "Verified", "app/src/studio.js, audit marker", "high", "phase count == 13"),
    ("R02", "REA", "Byte-by-byte coverage sweep", "Verified", "app/src/actions.js BYTE_SWEEP, audit", "high", "100% coverage"),
    ("R03", "REA", "Offset and hash evidence records", "Verified", "scripts/rea_evidence.py", "high", "sha256 + ranges present"),
    ("R04", "REA", "Ten language registry", "Verified", "app/src/studio.js LANGUAGES", "low", "10 entries"),
    ("R05", "REA", "Free services by default", "Verified", "app/src/studio.js FREE_SERVICES, smoke test", "critical", "no paid gate"),
    ("R06", "REA", "Data export before leaving", "Implemented", "app/src/mechanisms.js EXPORT_CHECKLIST", "medium", "export checklist present"),
    ("R07", "REA", "Public feed hides secrets", "Implemented", "app/src/mechanisms.js LIVE_FEED.hides", "high", "secret fields excluded"),
    ("R08", "REA", "Retrospectives", "Verified", "app/src/studio.js, audit marker", "low", "audit marker passes"),
    # Integrations and bridge (12)
    ("I01", "Bridge", "Local bridge auto-detect", "Implemented", "app/bridge/client.js", "medium", "127.0.0.1:8787 probed only if configured"),
    ("I02", "Bridge", "Allowlisted routes", "Implemented", "app/bridge/server.py ROUTES", "critical", "unknown route 404"),
    ("I03", "Bridge", "SMTP email", "Implemented", "app/bridge/server.py send_email", "medium", "missing key returns not configured"),
    ("I04", "Bridge", "Stripe checkout", "Implemented", "app/bridge/payments.py", "critical", "per-transaction confirm"),
    ("I05", "Bridge", "PayPal checkout", "Implemented", "app/bridge/payments.py", "medium", "invoice route present"),
    ("I06", "Bridge", "Crypto payment request", "Implemented", "app/bridge/payments.py crypto_payment", "medium", "URI + QR generated"),
    ("I07", "Bridge", "OAuth token refresh", "Implemented", "app/bridge/server.py refresh_token", "medium", "env-held token only"),
    ("I08", "Bridge", "Report webhook", "Implemented", "app/bridge/server.py webhook", "low", "allowlisted URL"),
    ("I09", "Bridge", "Browser action intents", "Implemented", "app/bridge/server.py _playwright_action", "medium", "local Edge executor passes allowlisted actions"),
    ("I10", "Bridge", "Local speech to text", "Implemented", "app/bridge/server.py media_stt", "low", "faster-whisper route"),
    ("I11", "Bridge", "Local text to speech", "Implemented", "app/bridge/server.py media_tts", "low", "edge-tts route"),
    ("I12", "Bridge", "Local image and video", "Partial", "app/bridge/server.py media_image/video", "low", "placeholders, no provider key route"),
    # Payments and commerce (8)
    ("P01", "Payments", "Invoices and receipts PDF", "Implemented", "app/bridge/payments.py", "medium", "PDF/HTML/JSON output"),
    ("P02", "Payments", "B2C/B2B/A2A modes", "Implemented", "app/bridge/payments.py", "low", "mode selectable"),
    ("P03", "Payments", "Web3 wallet URI + QR", "Implemented", "app/bridge/payments.py", "low", "URI and QR returned"),
    ("P04", "Payments", "No duplicate payment execution", "Implemented", "app/bridge/server.py idem_key/idem_load", "critical", "same idempotency key returns cached result"),
    ("P05", "Treasury", "Paper trading first", "Implemented", "app/src/treasury.js", "high", "default mode paper"),
    ("P06", "Treasury", "Live order human gate", "Implemented", "app/bridge/server.py live_order", "critical", "needs confirm true"),
    ("P07", "Treasury", "Risk caps", "Implemented", "app/src/treasury.js", "high", "caps enforced locally"),
    ("P08", "Commerce", "Marketplace registries", "Reference", "app/src/marketplaces.js", "low", "metadata only, no credentials"),
    # Data ownership and privacy (8)
    ("D01", "Data", "Local-first state", "Implemented", "app/src/actions.js", "high", "works with no bridge"),
    ("D02", "Data", "Portable export snapshot", "Implemented", "app/src/data-ownership.js exportSnapshot", "high", "JSON snapshot produced"),
    ("D03", "Data", "Right to erasure", "Implemented", "app/src/data-ownership.js eraseLocal", "high", "local keys removed"),
    ("D04", "Data", "User-chosen backup targets", "Implemented", "app/src/data-ownership.js BACKUP_TARGETS", "high", "default local only"),
    ("D05", "Data", "No silent upload", "Implemented", "app/src/data-ownership.js PRIVACY_CONTROLS", "critical", "no upload without target"),
    ("D06", "Data", "Secrets only in bridge env", "Implemented", "app/bridge/connectors.py", "critical", "status never returns secrets"),
    ("D07", "Data", "Six GDPR-aligned rights", "Implemented", "app/src/data-ownership.js GDR_RIGHTS", "medium", "rights listed"),
    ("D08", "Data", "Remote backup to own repo/cloud", "Human", "needs your repo and cloud credentials", "medium", "you configure credentials"),
    # Security and compliance (8)
    ("S01", "Security", "Defensive security registry", "Reference", "app/src/security.js", "medium", "controls listed"),
    ("S02", "Security", "STRIDE-style review", "Reference", "app/src/security.js", "low", "threat categories present"),
    ("S03", "Security", "Anti-tampering posture", "Reference", "app/src/security.js", "medium", "red lines listed"),
    ("S04", "Security", "Post-quantum readiness notes", "Reference", "app/src/security.js", "low", "PQC notes present"),
    ("S05", "Security", "Role-based access control", "Implemented", "app/src/actions.js accounts", "high", "permissions local"),
    ("S06", "Security", "Audit log of bridge calls", "Implemented", "app/bridge/server.py audit()", "high", "every call recorded"),
    ("S07", "Compliance", "Clean-room legal posture", "Reference", "docs/LEGAL-REVIEW.md", "high", "no legal advice claimed"),
    ("S08", "Security", "Independent OWASP agentic audit", "Missing", "no external assessment", "high", "third-party report required"),
    # Operations and quality (8)
    ("O01", "Operations", "Products and delivery records", "Implemented", "app/src/operations.js", "low", "local records"),
    ("O02", "Operations", "Complaints handling", "Implemented", "app/src/operations.js", "low", "complaint records"),
    ("O03", "Operations", "Quality gates", "Implemented", "app/src/operations.js", "medium", "gates recorded"),
    ("O04", "Operations", "Governance records", "Implemented", "app/src/governance.js", "medium", "records local"),
    ("O05", "Operations", "Custom internal app templates", "Implemented", "app/src/mechanisms.js", "low", "templates listed"),
    ("O06", "Operations", "Ad campaign model", "Reference", "app/src/mechanisms.js AD_CAMPAIGNS", "low", "no ad spend without authorisation"),
    ("O07", "Operations", "Contract-intelligence pipeline", "Implemented", "app/src/contract-intel.js, 6 tests", "medium", "source-linked report, human go/no-go"),
    ("O08", "Operations", "Solo runner front door", "Verified", "app/src/solo.js, smoke test", "medium", "runTask walks 13 phases"),
    # Knowledge and memory (6)
    ("K01", "Knowledge", "Automatic agent memory", "Implemented", "app/src/studio.js AUTO_MEMORY", "low", "memory persisted"),
    ("K02", "Knowledge", "Obsidian vault mirror", "Implemented", "scripts/sync_second_brain.py", "medium", "sync --check clean"),
    ("K03", "Knowledge", "Project database", "Implemented", "projects/polsia-free-v1/knowledge.db", "low", "DB present"),
    ("K04", "Knowledge", "Knowledge graph", "Verified", "python -m graphify update . succeeds", "low", "graph rebuild reports 2138 nodes, 0 exit"),
    ("K05", "Knowledge", "Competitive intel registry", "Implemented", "app/src/competitive-intel.js", "low", "window.PFV1_INTEL present"),
    ("K06", "Knowledge", "Agent platform registry", "Implemented", "app/src/agent-platforms.js", "low", "landscape listed"),
    # Deployment and scaling (6)
    ("L01", "Deployment", "Local/offline operation", "Verified", "bridge optional, local tests", "high", "all features work with no bridge"),
    ("L02", "Deployment", "One team VM design", "Reference", "docs/DEPLOYMENT-ARCHITECTURE.md", "low", "documented"),
    ("L03", "Deployment", "Per-bot workspaces", "Reference", "docs/DEPLOYMENT-ARCHITECTURE.md", "low", "documented"),
    ("L04", "Deployment", "Serverless glue only", "Reference", "docs/DEPLOYMENT-ARCHITECTURE.md", "low", "documented"),
    ("L05", "Deployment", "Local and cloud model runtimes", "Implemented", "app/src/models.js", "medium", "Ollama/Workers AI pairs"),
    ("L06", "Deployment", "Five deployment modes", "Reference", "app/src/competitive-intel.js", "medium", "modes configurable independently"),
    # Testing and CI (6)
    ("C01", "Testing", "Automated smoke suite", "Verified", "app/tests/smoke.test.js, 24 tests", "high", "npm test 24/24"),
    ("C02", "Testing", "Contract-intelligence tests", "Verified", "app/tests/contract-intel.test.js", "medium", "6 tests pass"),
    ("C03", "Testing", "CI workflow", "Implemented", ".github/workflows", "medium", "workflow file present"),
    ("C04", "Testing", "HTML and JS link audits", "Verified", "scripts/audit-links.py, audit-js-links.py", "high", "0 broken links"),
    ("C05", "Testing", "Deep requirement audit", "Verified", "scripts/deep_gap_audit.py", "high", "0 FAIL"),
    ("C06", "Testing", "Visual regression suite", "Implemented", "scripts/visual_regression.py, 16 captures", "high", "public >=99%, dashboard >=90% vs reference"),
]


def main() -> None:
    assert len(AREAS) == 100, f"expected 100 areas, got {len(AREAS)}"
    ids = [a[0] for a in AREAS]
    assert len(set(ids)) == 100, "duplicate area IDs"
    counts = Counter(a[3] for a in AREAS)
    lines = [
        "# Formal requirement audit — 100 areas",
        "",
        "Generated by `scripts/build_requirement_audit.py` from the research "
        "supplied on 24 November 2026. These are proposed assessment areas, not "
        "100 confirmed defects. Classification is evidence-based: a visible "
        "dashboard is not proof of a working backend.",
        "",
        "## Summary",
        "",
        "| Classification | Count |",
        "|---|---:|",
    ]
    for cls, n in sorted(counts.items()):
        lines.append(f"| {cls} | {n} |")
    lines += ["", "## Registry", "", "| ID | Category | Area | Classification | Evidence | Severity | Acceptance test |", "|---|---|---|---|---|---|---|"]
    for area in AREAS:
        lines.append("| " + " | ".join(a.replace("|", "\\|") for a in area) + " |")
    lines += [
        "",
        "## Notes",
        "",
        "- **Verified** means implemented and supported by a passing test or an "
        "instrumented check, not merely present in a registry.",
        "- **Human** items require credentials, accounts, hardware or a qualified "
        "third party; they are not failures of the build.",
        "- **Missing** items are real gaps with an acceptance test that is not yet met.",
    ]
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {OUT.relative_to(REPO)}: {len(AREAS)} areas, {dict(counts)}")


if __name__ == "__main__":
    main()
