# Nextcloud Security Lab - Docker Startup Guide

This guide covers how to start, stop, and manage the Nextcloud security lab Docker environment.

## Prerequisites

- Docker Desktop installed and running
- `.env` file configured in `/infra/docker/` (copy from `.env.example` if needed)
- TLS certificates generated in `nginx/certs/` (lab.crt and lab.key)

## Quick Start

### Start All Services

From the project root or the `infra/docker/` directory:

```bash
docker compose -f /home/Jason/Team-7-nextcloud-security-lab/infra/docker/docker-compose.yml up -d
```

Or if you're already in `infra/docker/`:

```bash
docker compose up -d
```

**What this does:**
- Starts MariaDB database (db service)
- Starts Nextcloud application (app service) on port 8080
- Starts nginx reverse proxy (proxy service) on port 443
- Runs in detached mode (-d flag means background)

### Check Service Status

```bash
docker compose -f /home/Jason/Team-7-nextcloud-security-lab/infra/docker/docker-compose.yml ps
```

**Expected output:**
```
NAME             IMAGE                 STATUS       PORTS
docker-app-1     nextcloud:29-apache   Up 5 hours   0.0.0.0:8080->80/tcp
docker-db-1      mariadb:11            Up 5 hours   3306/tcp
docker-proxy-1   nginx:alpine          Up 5 hours   0.0.0.0:443->443/tcp
```

### Access Nextcloud

- **HTTPS (recommended):** https://10.0.0.47
- **HTTP (direct to app):** http://10.0.0.47:8080

**Credentials:** Use the admin credentials from your `.env` file:
- Username: Value of `NEXTCLOUD_ADMIN_USER`
- Password: Value of `NEXTCLOUD_ADMIN_PASSWORD`

## Common Operations

### View Logs

**All services:**
```bash
docker compose -f /home/Jason/Team-7-nextcloud-security-lab/infra/docker/docker-compose.yml logs -f
```

**Specific service (proxy, app, or db):**
```bash
docker compose -f /home/Jason/Team-7-nextcloud-security-lab/infra/docker/docker-compose.yml logs -f proxy
docker compose -f /home/Jason/Team-7-nextcloud-security-lab/infra/docker/docker-compose.yml logs -f app
docker compose -f /home/Jason/Team-7-nextcloud-security-lab/infra/docker/docker-compose.yml logs -f db
```

**What the flags mean:**
- `logs`: Shows container output (stdout and stderr)
- `-f`: "Follow" mode - keeps streaming new logs as they arrive (like `tail -f`)

Press `Ctrl+C` to stop following logs.

### Stop Services (Keep Data)

```bash
docker compose -f /home/Jason/Team-7-nextcloud-security-lab/infra/docker/docker-compose.yml stop
```

**What this does:**
- Stops all containers
- Preserves volumes (database and Nextcloud files remain intact)
- You can restart later with `docker compose up -d`

### Stop and Remove Containers (Keep Data)

```bash
docker compose -f /home/Jason/Team-7-nextcloud-security-lab/infra/docker/docker-compose.yml down
```

**What this does:**
- Stops all containers
- Removes containers (but NOT volumes)
- Database and Nextcloud data persist
- Next `docker compose up -d` will recreate containers with existing data

### Complete Reset (Delete All Data)

```bash
docker compose -f /home/Jason/Team-7-nextcloud-security-lab/infra/docker/docker-compose.yml down -v
```

**WARNING:** This deletes everything!
- Stops and removes all containers
- Deletes named volumes (`db` and `nc`)
- All database records and uploaded files are lost
- Useful for starting fresh after destructive security tests
- Next startup will be like first-time installation

### Restart a Single Service

```bash
docker compose -f /home/Jason/Team-7-nextcloud-security-lab/infra/docker/docker-compose.yml restart proxy
docker compose -f /home/Jason/Team-7-nextcloud-security-lab/infra/docker/docker-compose.yml restart app
docker compose -f /home/Jason/Team-7-nextcloud-security-lab/infra/docker/docker-compose.yml restart db
```

**Use case:** After changing nginx config or rotating TLS certificates

### Reload nginx Without Restart

After updating nginx configuration or certificates:

```bash
docker compose -f /home/Jason/Team-7-nextcloud-security-lab/infra/docker/docker-compose.yml exec proxy nginx -t
docker compose -f /home/Jason/Team-7-nextcloud-security-lab/infra/docker/docker-compose.yml exec proxy nginx -s reload
```

**What these do:**
- `nginx -t`: Tests configuration for syntax errors (always run this first!)
- `nginx -s reload`: Gracefully reloads nginx without dropping connections

### Execute Commands Inside Containers

**Get a shell in Nextcloud container:**
```bash
docker compose -f /home/Jason/Team-7-nextcloud-security-lab/infra/docker/docker-compose.yml exec app bash
```

**Run occ command (Nextcloud CLI):**
```bash
docker compose -f /home/Jason/Team-7-nextcloud-security-lab/infra/docker/docker-compose.yml exec -u www-data app php occ status
```

**Access MariaDB:**
```bash
docker compose -f /home/Jason/Team-7-nextcloud-security-lab/infra/docker/docker-compose.yml exec db mariadb -u root -p
# Enter MYSQL_ROOT_PASSWORD from .env when prompted
```

## Network Architecture

The Docker stack uses these networks:

```
┌───────────────────────────────────────────────────┐
│ Host: 10.0.0.47                                   │
│                                                    │
│  Port 443 ─┐                                      │
│            ↓                                       │
│       ┌─────────────┐                             │
│       │ nginx:alpine│ (proxy)                     │
│       │   TLS       │                             │
│       └──────┬──────┘                             │
│              │ port 80                            │
│              ↓                                     │
│       ┌──────────────┐                            │
│       │ nextcloud:29 │ (app)                      │
│  8080→│   apache     │                            │
│       └──────┬───────┘                            │
│              │ port 3306                          │
│              ↓                                     │
│       ┌──────────────┐                            │
│       │  mariadb:11  │ (db)                       │
│       │              │                            │
│       └──────────────┘                            │
│                                                    │
│  Docker internal bridge network                   │
└───────────────────────────────────────────────────┘
         ↑
         │
    Access from:
    - Windows host (localhost, 10.0.0.47)
    - Kali WSL (10.0.0.47)
    - Network clients (10.0.0.47)
```

## Security Testing Workflow

### Before Testing

1. **Ensure services are running:**
   ```bash
   docker compose -f /home/Jason/Team-7-nextcloud-security-lab/infra/docker/docker-compose.yml ps
   ```

2. **Check logs for errors:**
   ```bash
   docker compose -f /home/Jason/Team-7-nextcloud-security-lab/infra/docker/docker-compose.yml logs --tail 50
   ```

3. **Verify network access from Kali WSL:**
   ```bash
   curl -I http://10.0.0.47:8080
   curl -kI https://10.0.0.47
   ```

### After Destructive Tests

If you've performed tests that may have corrupted data or changed configurations:

```bash
# Complete reset
docker compose -f /home/Jason/Team-7-nextcloud-security-lab/infra/docker/docker-compose.yml down -v

# Fresh start
docker compose -f /home/Jason/Team-7-nextcloud-security-lab/infra/docker/docker-compose.yml up -d

# Wait for initialization (30-60 seconds)
sleep 60

# Verify services
docker compose -f /home/Jason/Team-7-nextcloud-security-lab/infra/docker/docker-compose.yml ps
```

## Troubleshooting

### Services Won't Start

**Check Docker Desktop is running:**
```bash
docker version
```

**Check for port conflicts:**
```bash
# Windows PowerShell:
netstat -ano | findstr :443
netstat -ano | findstr :8080

# WSL/Linux:
sudo netstat -tlnp | grep -E ':(443|8080)'
```

**View container logs for errors:**
```bash
docker compose -f /home/Jason/Team-7-nextcloud-security-lab/infra/docker/docker-compose.yml logs proxy
docker compose -f /home/Jason/Team-7-nextcloud-security-lab/infra/docker/docker-compose.yml logs app
docker compose -f /home/Jason/Team-7-nextcloud-security-lab/infra/docker/docker-compose.yml logs db
```

### Can't Access HTTPS (Port 443)

**Verify nginx proxy is running:**
```bash
docker compose -f /home/Jason/Team-7-nextcloud-security-lab/infra/docker/docker-compose.yml ps proxy
```

**Check TLS certificates exist:**
```bash
ls -lh /home/Jason/Team-7-nextcloud-security-lab/infra/docker/nginx/certs/
# Should show lab.crt and lab.key
```

**Test nginx configuration:**
```bash
docker compose -f /home/Jason/Team-7-nextcloud-security-lab/infra/docker/docker-compose.yml exec proxy nginx -t
```

**Regenerate certificates if needed:**
```powershell
# From Windows PowerShell in infra/docker/ directory:
docker run --rm -v ${PWD}/nginx/certs:/certs alpine sh -lc \
  "apk add --no-cache openssl >/dev/null && \
   openssl req -x509 -newkey rsa:2048 -nodes -days 30 \
   -subj '/CN=10.0.0.47' \
   -keyout /certs/lab.key -out /certs/lab.crt && \
   chmod 600 /certs/lab.key && chmod 644 /certs/lab.crt"
```

### Database Connection Errors

**Verify .env file exists:**
```bash
cat /home/Jason/Team-7-nextcloud-security-lab/infra/docker/.env
```

**Ensure database is healthy:**
```bash
docker compose -f /home/Jason/Team-7-nextcloud-security-lab/infra/docker/docker-compose.yml logs db | grep -i error
docker compose -f /home/Jason/Team-7-nextcloud-security-lab/infra/docker/docker-compose.yml exec db mariadb -u root -p -e "SHOW DATABASES;"
```

### Nextcloud Shows Installation Wizard

This means volumes were lost or it's first startup.

**Expected on first run** - complete the wizard manually or let the app container initialize automatically using environment variables from `.env`.

**Unexpected after prior use** - you may have run `docker compose down -v` which deleted volumes. Restore from backup or start fresh.

## Shell Aliases (Optional)

Add to your `~/.bashrc` or `~/.zshrc` for convenience:

```bash
# Nextcloud Docker Lab Shortcuts
alias nc-up='docker compose -f /home/Jason/Team-7-nextcloud-security-lab/infra/docker/docker-compose.yml up -d'
alias nc-down='docker compose -f /home/Jason/Team-7-nextcloud-security-lab/infra/docker/docker-compose.yml down'
alias nc-reset='docker compose -f /home/Jason/Team-7-nextcloud-security-lab/infra/docker/docker-compose.yml down -v && docker compose -f /home/Jason/Team-7-nextcloud-security-lab/infra/docker/docker-compose.yml up -d'
alias nc-logs='docker compose -f /home/Jason/Team-7-nextcloud-security-lab/infra/docker/docker-compose.yml logs -f'
alias nc-ps='docker compose -f /home/Jason/Team-7-nextcloud-security-lab/infra/docker/docker-compose.yml ps'
```

Reload shell: `source ~/.bashrc`

Then use: `nc-up`, `nc-down`, `nc-reset`, `nc-logs`, `nc-ps`

## Directory Structure

```
infra/docker/
├── docker-compose.yml          # Service definitions
├── .env                        # Secrets (gitignored)
├── .env.example                # Template for .env
├── STARTUP.md                  # This file
├── nginx/
│   ├── conf.d/
│   │   └── default.conf        # nginx reverse proxy config
│   └── certs/
│       ├── lab.crt             # TLS certificate (30-day self-signed)
│       └── lab.key             # TLS private key (gitignored)
└── volumes/                    # Created automatically by Docker
    ├── db/                     # MariaDB data
    └── nc/                     # Nextcloud files
```

## Best Practices

1. **Always test nginx config before reload:**
   ```bash
   docker compose exec proxy nginx -t && docker compose exec proxy nginx -s reload
   ```

2. **Check service health before testing:**
   ```bash
   docker compose ps
   curl -I http://10.0.0.47:8080
   ```

3. **Save evidence before reset:**
   - Export Burp/ZAP projects
   - Save scan outputs to `/docs/evidence/week-N/`
   - Document findings in `/docs/findings/week-N-findings.md`

4. **Use volume backups for important states:**
   ```bash
   # Backup volumes
   docker run --rm -v docker_db:/data -v $(pwd):/backup alpine tar czf /backup/db-backup.tar.gz -C /data .
   docker run --rm -v docker_nc:/data -v $(pwd):/backup alpine tar czf /backup/nc-backup.tar.gz -C /data .
   ```

5. **Review logs after changes:**
   ```bash
   docker compose logs --tail 100
   ```

## Related Documentation

- Main project README: `/README.md`
- CLAUDE.md (project guidance): `/CLAUDE.md`
- Docker Compose file: `/infra/docker/docker-compose.yml`
- nginx config: `/infra/docker/nginx/conf.d/default.conf`
- Threat model: `/threat-model/STRIDE.md`
