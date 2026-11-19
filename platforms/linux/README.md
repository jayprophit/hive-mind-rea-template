# Linux

Supported. Follows the XDG base directory spec; works on Debian/Ubuntu, Fedora and
Arch with the package names swapped.

## Install

```bash
# Prerequisites (Debian/Ubuntu)
sudo apt-get update
sudo apt-get install -y git python3 python3-pip nodejs npm curl

# Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Clone and inspect
git clone https://github.com/jayprophit/hive-mind-rea-template.git ~/hive
cd ~/hive
python3 scripts/doctor.py

# Apply
python3 scripts/bootstrap.py --apply --scaffold-vault

# One model to start
ollama pull lfm3:1.7b
```

Fedora: `sudo dnf install -y git python3 nodejs npm`.

## Paths

| What | Where |
|---|---|
| OpenCode config | `${XDG_CONFIG_HOME:-~/.config}/opencode/opencode.json` |
| Hermes home | `${XDG_DATA_HOME:-~/.local/share}/hermes` |
| Stack data | `${XDG_DATA_HOME:-~/.local/share}/hive-mind` |
| Vault | `<repo>/obsidian-vault` |

## Notes

- The full reverse-engineering toolchain is most at home here: `gdb`, `binutils`,
  `tshark`, `rizin`, `rizin`, and `ghidra` are all packaged or one download away.
- `tshark` needs `sudo usermod -aG wireshark $USER` and a re-login to capture without root.
- On a headless box, skip Grafana and read the vault directly; nothing depends on it.
