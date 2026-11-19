# Agent actions: what is allowed, what needs a human

This file is the contract between the human and **any** agent working in this
repository — OpenCode, Hermes, Claude, Codex, a local model, or something not
written yet. Read it before acting.

The rule is simple: **reading is free, writing is cheap, spending is not.**

---

## Tier 0 — do it without asking

| Action | Notes |
|---|---|
| Read files, logs, configs, databases | Never modify what you read |
| Run `scripts/doctor.py` | Read-only health check |
| Search the web, fetch pages | `scripts/research.py` |
| Take browser snapshots, screenshots | Evidence gathering |
| Inspect processes, services, memory, disk | Read-only host queries |
| Write scratch files to the OS temp directory | Use `%TEMP%` / `$TMPDIR` / `/tmp` |

## Tier 1 — do it, then say what you did

| Action | Notes |
|---|---|
| Write files inside this repository | Follow existing layout and style |
| Install a **user-scope** package: `pip install --user`, `npm i -g`, `uv tool install` | Never system-wide without Tier 2 |
| Create or edit a note in the Obsidian vault | Append, do not overwrite history |
| Generate reports, charts, diagrams, Office documents | `scripts/office.py`, `scripts/viz.py` |
| Fill a form field, select an option, tick a checkbox in a browser | Reversible; do not submit |
| Change a service from Automatic to Manual | Reversible with one command |
| Write to `HKCU` / a user dotfile | User-scope only |

## Tier 2 — ask first, every time

| Action | Why |
|---|---|
| **Buy anything** | Money leaves the account |
| **Sell anything** | Money and third parties |
| Place a bid, book travel, reserve stock | Creates a commitment |
| Submit a payment, order or booking form | Irreversible |
| Enter card, bank or government ID details | Never do this without an explicit, in-conversation instruction naming the site |
| Send email, message or post publicly | Cannot be unsent |
| Delete files outside this repo | Could destroy the human's work |
| Install anything system-wide / with elevation | Affects the whole machine |
| Change BIOS, firmware or partition tables | Brick risk |
| Rotate, revoke or create credentials | Can lock the human out |

### The purchase protocol

Before any transaction, print and wait for explicit confirmation:

```
ABOUT TO BUY
  Item     : <exact product name and model number>
  Seller   : <site and seller account>
  Price    : <item price> + <shipping> = <total>
  Delivery : <address summary, last line only>
  Payment  : <card brand and last 4 digits — never the full number>
  Returns  : <window and conditions>
Confirm? Reply "yes" to continue.
```

Rules:

1. **One confirmation, one purchase.** A "yes" covers that item at that price
   only. Never reuse it for a second cart, a second item, or a re-price.
2. **Checkout stops at the final button.** Fill the basket, then hand control
   back. The human clicks "Pay".
3. **If the price changes** at any step, stop and re-confirm.
4. **Never store credentials.** No card numbers in files, configs, notes or
   commit history. If you find one, report it — do not use it.
5. **Never defeat a paywall, CAPTCHA, or verification step.**

### The sale protocol

Selling additionally requires: the human owns the item, the listing text is
shown before publishing, and the price floor is stated in the conversation.
Publishing a listing counts as "post publicly" — Tier 2.

---

## Installing software

Prefer the least invasive route that works, in this order:

1. **Already present?** Check `scripts/doctor.py` before installing anything.
2. **Project-local**: `pip install --target ./.venv`, `npm i --no-save`
3. **User-scope**: `pip install --user`, `npm i -g`, `uv tool install`
4. **System-wide**: ask first (Tier 2)

Platform commands:

| Task | Windows | macOS | Linux |
|---|---|---|---|
| Python packages | `python -m pip install --user X` | `python3 -m pip install --user X` | `python3 -m pip install --user X` |
| Global CLI | `npm i -g X` | `npm i -g X` | `npm i -g X` (or use `nvm`) |
| Package manager | `winget install X` | `brew install X` | `apt/dnf/pacman install X` |
| Elevation | UAC prompt, user clicks | `sudo`, user types password | `sudo` |

**Never** invent an administrator password, and never try to bypass UAC, `sudo`
or a password prompt. If elevation is needed, prepare the exact command, show
it, and let the human run it.

### Reporting dependencies

If a script needs a package that is missing, say so in this shape:

```
Missing  : openpyxl
Needed by: scripts/office.py --to xlsx
Install  : python -m pip install --user openpyxl
Fallback : --to csv works without it
```

Always check whether a fallback exists before asking the human to install.

---

## Producing output

| Want | Command | Opens in |
|---|---|---|
| Spreadsheet | `office.py --to xlsx out.xlsx` | Excel, Google Sheets, LibreOffice Calc |
| Document | `office.py --to docx out.docx` | Word, Google Docs, LibreOffice Writer |
| Slides | `office.py --to pptx out.pptx` | PowerPoint, Google Slides, LibreOffice Impress |
| Plain table | `office.py --to csv out.csv` | Everything, including Google Sheets |
| Chart | `viz.py --chart bar ... -o out.svg` | Browsers, Word, PowerPoint, Google Slides |
| Diagram | `viz.py --mermaid flowchart ...` | GitHub, GitLab, Obsidian, the Review pane |
| Web page | `viz.py ... --html` | Any browser |

`.docx`, `.xlsx` and `.pptx` are ZIP-based Open XML. Google Drive converts them
on upload, so the same file serves both Microsoft and Google workspaces. When
the human needs a native Google file, upload the Microsoft one and let Drive
convert, or hand over the `.csv` for Sheets.

---

## Housekeeping

- Leave the machine measurably better than you found it: report bytes freed,
  services changed, and what you did **not** do.
- Never claim a step succeeded without a command output that shows it.
- If something is not installed and cannot be found, say **"it does not exist
  on this machine"** rather than assuming it is broken.
- Keep notes in the vault and commit code; a fix that exists only in a chat
  log is lost.
