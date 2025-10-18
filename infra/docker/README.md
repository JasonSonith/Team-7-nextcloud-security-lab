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
