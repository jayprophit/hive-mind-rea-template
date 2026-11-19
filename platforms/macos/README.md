# macOS

Supported. Paths resolve to `~/Library/Application Support`; binaries are looked up
in `/opt/homebrew/bin` and `/usr/local/bin` as well as `PATH`.

## Install

```bash
# Prerequisites
xcode-select --install                 # git + compilers
brew install ollama node python@3.12

# Clone and inspect
git clone https://github.com/jayprophit/hive-mind-rea-template.git ~/hive
cd ~/hive
python3 scripts/doctor.py

# Apply
python3 scripts/bootstrap.py --apply --scaffold-vault

# One model to start
ollama serve &
ollama pull lfm3:1.7b
```

## Paths

| What | Where |
|---|---|
| OpenCode config | `~/.config/opencode/opencode.json` |
| Hermes home | `~/Library/Application Support/hermes` |
| Stack data | `~/Library/Application Support/hive-mind` |
| Vault | `<repo>/obsidian-vault` |

## Notes

- Apple silicon runs CPU inference considerably faster than Intel Macs; a 3B model is
  comfortable at 16 GB unified memory.
- Ghidra and JADX need a JDK 21: `brew install --cask temurin@21`.
- No equivalent of the Windows maintenance script is needed; `doctor.py` covers health.
