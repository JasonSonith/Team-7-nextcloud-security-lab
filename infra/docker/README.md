# infra/docker — HTTPS reverse proxy (443) with nginx

Goal: Put Nextcloud behind an nginx reverse proxy that terminates TLS on port 443. Leave 80 filtered. Backend app stays on the existing `app` container (port 80 inside the Docker network). Host IP: `10.0.0.47`.

---

## 1) Compose change

Edit `infra/docker/docker-compose.yml`. Under the top-level `services:` add the proxy. Do **not** add a second `services:` key.

```yaml
  proxy:
    image: nginx:alpine
    ports:
      - "443:443"
    volumes:
      - ./nginx/conf.d:/etc/nginx/conf.d:ro
      - ./nginx/certs:/etc/nginx/certs:ro
    depends_on:
      - app
    restart: unless-stopped
```

Check:
```powershell
docker compose -f infra/docker/docker-compose.yml config --services
# expect: app, db, proxy
```

---

## 2) TLS assets

Files on host:
- `infra/docker/nginx/certs/lab.crt` — self-signed public cert for `10.0.0.47`.
- `infra/docker/nginx/certs/lab.key` — private key. **Do not commit.** Target perms `600`.

Mounted read-only into the container:
```
./nginx/certs  ->  /etc/nginx/certs  :ro
./nginx/conf.d ->  /etc/nginx/conf.d :ro
```

Generate or rotate (self-signed for IP):
```powershell
mkdir infra\docker
ginx\conf.d -Force
mkdir infra\docker
ginx\certs -Force

docker run --rm -v ${PWD}\infra\docker
ginx\certs:/certs alpine sh -lc `
  "apk add --no-cache openssl >/dev/null &&    openssl req -x509 -newkey rsa:2048 -nodes -days 30    -subj '/CN=10.0.0.47'    -keyout /certs/lab.key -out /certs/lab.crt &&    chmod 600 /certs/lab.key && chmod 644 /certs/lab.crt"
```

`.gitignore` entries:
```
infra/docker/nginx/certs/lab.key
```
You may commit `lab.crt` if you want clients to trust it manually.

---

## 3) nginx config

Create `infra/docker/nginx/conf.d/nextcloud.conf`:

```nginx
server {
  listen 443 ssl http2;
  server_name 10.0.0.47;

  ssl_certificate     /etc/nginx/certs/lab.crt;
  ssl_certificate_key /etc/nginx/certs/lab.key;

  # HSTS for the IP (lab only)
  add_header Strict-Transport-Security "max-age=31536000" always;

  location / {
    proxy_pass http://app:80;
    proxy_set_header Host $host:$server_port;  # yields 10.0.0.47:443
    proxy_set_header X-Forwarded-Proto https;
    proxy_set_header X-Forwarded-For $remote_addr;
  }
}
```

Notes:
- Terminates TLS on host 443 using `lab.crt` and `lab.key`.
- Proxies to `app:80` in the compose network.
- Adds HSTS. Browser must accept the self-signed cert once.
- If apps mis-handle the `:443` suffix, change `proxy_set_header Host $host;`.

Optional hardening for large uploads and websocket upgrades:
```nginx
ssl_session_timeout 10m;
ssl_protocols TLSv1.2 TLSv1.3;
ssl_prefer_server_ciphers on;
map $http_upgrade $connection_upgrade { default upgrade; '' close; }
location / {
  proxy_pass http://app:80;
  proxy_http_version 1.1;
  proxy_set_header Host $host:$server_port;
  proxy_set_header X-Forwarded-Proto https;
  proxy_set_header X-Forwarded-For $remote_addr;
  proxy_set_header Upgrade $http_upgrade;
  proxy_set_header Connection $connection_upgrade;
  client_max_body_size 1G;
}
```

---

## 4) Bring up proxy

```powershell
docker compose -f infra/docker/docker-compose.yml up -d proxy
docker compose ps
docker compose logs -f proxy
docker compose exec proxy nginx -t
```

Reload after cert rotation:
```powershell
docker compose -f infra/docker/docker-compose.yml exec proxy nginx -s reload
```

Rollback:
```powershell
docker compose stop proxy
docker compose rm -f proxy
```

---

## 5) Verify from Kali

Headers and HSTS:
```bash
curl -vkI https://10.0.0.47
```

Certificate details:
```bash
openssl s_client -connect 10.0.0.47:443 -servername 10.0.0.47 </dev/null 2>/dev/null  | openssl x509 -noout -issuer -enddate -subject
```

TLS versions and ciphers:
```bash
nmap --script ssl-enum-ciphers -p 443 10.0.0.47 -oN scans/nmap-ssl-enum.txt
```

---

## 6) Evidence to commit

- `infra/docker/nginx/conf.d/nextcloud.conf`
- `scans/nmap-ssl-enum.txt`
- `docs/evidence/week2/<timestamp>-https-head.txt`
- `docs/evidence/week2/<timestamp>-cert-issuer-expiry.txt`

Do **not** commit:
- `infra/docker/nginx/certs/lab.key`

---

## 7) Common errors

- **no such service: proxy**  
  Proxy block not under the existing `services:` or YAML indent wrong.

- **502/Bad Gateway**  
  `app` service name or internal port not `80`. Fix and redeploy.

- **Permission denied on key**  
  Ensure `lab.key` has mode `600` and volume is `:ro`.

- **Uploads fail**  
  Increase `client_max_body_size` and reload nginx.

---

## 8) What this setup achieves

- HTTPS on 443 with self-signed cert for lab use.
- Backend untouched. Only the edge terminates TLS.
- HSTS enforces HTTPS during testing.
- Clear key custody: `lab.key` stays local, read-only in container.
