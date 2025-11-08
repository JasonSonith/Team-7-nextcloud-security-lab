# Docker Startup Guide

## Quick Start

```bash
# From repository root
docker-compose -f infra/docker/docker-compose.yml up -d
```

**Note:** Use `docker-compose` (with hyphen), not `docker compose` (with space), as the compose plugin appears to be broken in this environment.

## Prerequisites

### 1. Check if docker-compose is installed

```bash
docker-compose --version
```

### 2. Install docker-compose (if needed)

```bash
# Download latest version
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

# Make executable
sudo chmod +x /usr/local/bin/docker-compose

# Verify installation
docker-compose --version
```

### 3. Ensure .env file exists

```bash
# Check if .env exists
ls -la infra/docker/.env

# If not, copy from example and configure
cp infra/docker/.env.example infra/docker/.env
nano infra/docker/.env  # Edit with your credentials
```

### 4. Generate TLS certificates (for proxy service)

```bash
# Create cert directory if it doesn't exist
mkdir -p infra/docker/nginx/certs

# Generate self-signed cert (30-day validity)
docker run --rm -v $(pwd)/infra/docker/nginx/certs:/certs alpine sh -lc \
  "apk add --no-cache openssl >/dev/null && \
   openssl req -x509 -newkey rsa:2048 -nodes -days 30 \
   -subj '/CN=10.0.0.47' \
   -keyout /certs/lab.key -out /certs/lab.crt && \
   chmod 600 /certs/lab.key && chmod 644 /certs/lab.crt"
```

## Common Commands

### Start the stack

```bash
docker-compose -f infra/docker/docker-compose.yml up -d
```

### Check service status

```bash
docker-compose -f infra/docker/docker-compose.yml ps
```

### View logs

```bash
# All services
docker-compose -f infra/docker/docker-compose.yml logs -f

# Specific service
docker-compose -f infra/docker/docker-compose.yml logs -f app
docker-compose -f infra/docker/docker-compose.yml logs -f db
docker-compose -f infra/docker/docker-compose.yml logs -f proxy
```

### Stop the stack

```bash
docker-compose -f infra/docker/docker-compose.yml down
```

### Restart a service

```bash
docker-compose -f infra/docker/docker-compose.yml restart app
```

### Rebuild and restart

```bash
docker-compose -f infra/docker/docker-compose.yml up -d --build
```

### Remove everything (including volumes)

```bash
docker-compose -f infra/docker/docker-compose.yml down -v
```

## Access Nextcloud

Once services are running:

- **HTTP (direct to app):** http://10.0.0.47:8080
- **HTTPS (via nginx proxy):** https://10.0.0.47

**Note:** You'll need to accept the self-signed certificate warning in your browser for HTTPS.

### Login Credentials

Use the credentials from your `.env` file:
- Username: Value of `NEXTCLOUD_ADMIN_USER`
- Password: Value of `NEXTCLOUD_ADMIN_PASSWORD`

## Troubleshooting

### Services won't start

```bash
# Check Docker daemon is running
sudo systemctl status docker

# Start Docker daemon if needed
sudo systemctl start docker
```

### Port conflicts

```bash
# Check if ports 443 or 8080 are already in use
sudo netstat -tulpn | grep -E ':(443|8080)'

# Or using ss
sudo ss -tulpn | grep -E ':(443|8080)'
```

### Permission errors with volumes

```bash
# Fix ownership (may be needed for WSL)
sudo chown -R $(id -u):$(id -g) infra/docker/nginx/certs
```

### Reset everything

```bash
# Stop and remove containers, networks, volumes
docker-compose -f infra/docker/docker-compose.yml down -v

# Remove any orphaned containers
docker container prune

# Start fresh
docker-compose -f infra/docker/docker-compose.yml up -d
```

## Nginx Proxy Operations

### Test nginx configuration

```bash
docker-compose -f infra/docker/docker-compose.yml exec proxy nginx -t
```

### Reload nginx (after config changes)

```bash
docker-compose -f infra/docker/docker-compose.yml exec proxy nginx -s reload
```

### View nginx error logs

```bash
docker-compose -f infra/docker/docker-compose.yml exec proxy cat /var/log/nginx/error.log
```
