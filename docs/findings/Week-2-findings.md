# Week 2 — Configuration Audit

Brief: Capture key settings and document secrets handling.

## Findings

### Secrets in app config
- `passwordsalt` present in `config.php`.  ✅ Redact in evidence. :contentReference[oaicite:0]{index=0}
- `secret` present in `config.php`.  ✅ Redact in evidence. :contentReference[oaicite:1]{index=1}
- `dbpassword` in `config.php` is a lab default (`changeme-app`). ➜ Rotate. :contentReference[oaicite:2]{index=2}

### DB container environment
- `MARIADB_ROOT_PASSWORD` is set (in container env). Handle as secret; never commit. :contentReference[oaicite:3]{index=3}
- `MARIADB_PASSWORD` is set (app user password). Must match the app’s `dbpassword`. :contentReference[oaicite:4]{index=4}
- `MARIADB_USER=nextcloud`. Expected for this lab. :contentReference[oaicite:5]{index=5}

## Paths and trust (unchanged from Week 1)
- Data directory: `/var/www/html/data` (default).
- Trusted domains: `["localhost", "10.0.0.47"]` (local only).

## Evidence policy
- Raw dumps (e.g., `CONFIG-raw.txt`) are **ignored** by Git.
- Redacted evidence (`CONFIG-redacted.txt`) is committed.
- DB env snapshot (`20251018-db-env.txt`) and config grep (`20251018-grep-config-secrets.txt`) are committed.

## Required actions
1. **Rotate DB app password**  
   - Choose a strong value for the app DB password.
   - Update it consistently:
     - Container env (`MARIADB_PASSWORD` / `.env`)  
     - Nextcloud `config.php` → `dbpassword`
   - Restart stack and re-test login.

2. **Keep secrets out of Git**  
   - `.env` stays local.  
   - Only redacted files are committed.

3. **Track versions for reproducibility**  
   - Save `occ -V` output in `docs/evidence/week2/`.
