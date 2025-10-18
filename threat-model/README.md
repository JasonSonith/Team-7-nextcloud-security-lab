# Nextcloud Lab — Data Flow Diagram (DFD)

This README documents the Week-2 DFD for Team 7’s Nextcloud security lab. The diagram file is maintained in `threat-model/diagram.drawio.png`. Keep this README in the same folder.

## Diagram

![Nextcloud Lab DFD](./Data-flow-diagram.png)

**Source:** `threat-model/diagram.drawio` (editable) → exported as `threat-model/diagram.drawio.png`.

## Scope Nodes

- **Browsers (User/Admin)** — external clients.
- **Kali (Burp/ZAP proxy)** — attacker/test VM.
- **Reverse proxy (Nginx/Caddy)** — optional TLS termination and routing.
- **Nextcloud app (container)** — application service.
- **MariaDB (container)** — database for users/shares/metadata.
- **Host volumes** — app data, config, uploads.
- **Docker network** — bridge where app and DB communicate.
- **Host OS** — Docker engine and bind-mounted storage.

## Trust Boundaries

- **Host OS** — dashed rounded container around Docker engine, app, DB, volumes, reverse proxy.
- **Docker network** — dashed container around **Nextcloud** and **MariaDB**.
- **App↔DB split** — thin dashed line between app and DB labeled `app↔db`.
- **VM** — dashed container around **Kali (Burp/ZAP)**.
- **Edge labels** where zones meet: `host↔VM`, `VM↔Docker network`, `app↔db`.

## Numbered Flows

1. **Login credentials** — Browser → App (username/password POST).  
2. **Session cookie** — App → Browser (Set-Cookie) and Browser → App on requests.  
3. **CSRF token** — App → Browser; Browser → App on state-changing actions.  
4. **WebDAV auth** — Client → App using HTTP Basic to `/remote.php/dav/files/<user>/`.  
5. **File upload** — Browser → App; App → Host volumes (write).  
6. **File download** — App → Browser; App → Host volumes (read).  
7. **Admin API/config** — Admin Browser → App (management endpoints).  
8. **App↔DB queries** — SQL over Docker bridge for auth, shares, metadata.  
9. **Proxy pass (optional)** — Browser/Kali → Reverse proxy → App.

Security-sensitive flows: **1–4**. Require TLS and secure cookie flags.

## Data at Rest and Keys

- **MariaDB**: users, shares, metadata.  
- **Host volumes**: app data, config, uploads, potential keys/secrets.  
- **Reverse proxy**: TLS certs/keys if terminating TLS on host.

## Styling Conventions (draw.io)

- Dark canvas `#0f1115`. Boundaries: 4px **dashed**, radius 12, ~8% white fill.  
- Sensitive arrows red; others neutral. Small lock icon next to 1–4.  
- Use orthogonal connectors and numbered badges `1..9` near mid-arrow.  
- Fonts: Inter/Roboto 12–14 pt; monospace for paths and IPs.

## How to Reproduce

1. Open `threat-model/diagram.drawio` in draw.io.  
2. Ensure **More Shapes…** libraries: Cisco, AWS, Azure, GCP, Material, Simple Icons.  
3. Keep nodes, boundaries, and flows as specified above.  
4. Export: **PNG** at 2× or 3× → overwrite `threat-model/diagram.drawio.png`.

## Evidence Checklist

- [ ] `threat-model/diagram.drawio` committed.  
- [ ] `threat-model/diagram.drawio.png` exported and committed.  
- [ ] README updated if topology changes.  
- [ ] Numbered flows 1–9 visible and legend present in the diagram.
