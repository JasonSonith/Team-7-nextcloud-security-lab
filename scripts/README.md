## Current tools

### `nextcloud_apps_audit.py` ✨ NEW
Automated Nextcloud apps inventory tool using the OCS API.

- **Input:** Nextcloud URL + credentials (from .env or CLI)
- **Output:**
  - `YYYYMMDD-HHMM_apps-audit_inventory.csv` — app inventory
  - `YYYYMMDD-HHMM_apps-audit_inventory.json` — machine-readable format
  - `YYYYMMDD-HHMM_apps-audit_summary.txt` — human-readable summary

**Quick start:**
```bash
cd scripts
source venv/bin/activate
python nextcloud_apps_audit.py \
  --url http://10.0.0.47:8080 \
  --env-file ../infra/docker/.env \
  --verbose
```

**Dependencies:**
- Python 3
- `pip install requests python-dotenv` (already installed in venv)

---

### `nmap-parser.py`
Parses Nmap output into a tidy CSV and an optional heatmap image.

- **Input:** Nmap XML (`-oX`) or normal `.nmap`/text output.
- **Output:**
  - `scans/nmap-parsed.csv` — columns: host, ip, proto, port, state, service, product, version
  - `scans/nmap-heatmap.png` — grid of open ports by host

**Quick start**
```bash
# 1) Run an XML scan
mkdir -p scans
nmap -Pn -p 80,8080 -sS -T4 10.0.0.47 -oX scans/nmap-80-8080.xml

# 2) Parse to CSV (+ heatmap)
chmod +x scripts/nmap-parser.py
./scripts/nmap-parser.py -i scans/nmap-80-8080.xml
# or for plain text scans:
./scripts/nmap-parser.py -i scans/nmap-80-8080.txt
```

**Dependencies**
- Python 3
- Optional for heatmap: `pip install matplotlib numpy`

## Roadmap (coming soon)

- `semgrep_runner.py` — run Semgrep rule packs, emit SARIF + Markdown.
- `trivy_summary.py` — summarize Docker image and config CVEs from Trivy JSON.
- `zap_drive.py` — ZAP spider + active scan, export HTML/PDF reports.
- `session_flags_check.py` — verify `Secure`, `HttpOnly`, `SameSite` on session cookies.
- `csrf_probe.py` — detect CSRF protections and failure cases.
- `upload_matrix.py` — systematic file upload tests (MIME, extensions, double-ext).
- `repo_guard.py` — enforce repo structure and output locations in CI.

## Conventions

- Put raw scans under `scans/`.
- Put dynamic-test artifacts under `dynamic-testing/`.
- Name evidence with a timestamp: `YYYYMMDD-HHMM_<area>_<step>.<ext>`

## Virtual Environment

A Python virtual environment is set up in `scripts/venv/` with the necessary dependencies. Activate it with:
```bash
source scripts/venv/bin/activate
```
