# Week 1 — Accounts, Sharing, Surface (Findings)

## Summary
Lab users created. Team share set with least-privilege. External surface limited to HTTP on 8080. Evidence below.

## Evidence
- **Dashboard reachable** from Kali after initial setup.
- **Users**: `admin`, `alice` (group `users`), `bob` (group `users`). Quotas unlimited in lab.
- **Team share** folder with explicit permissions: `alice` view-only, `bob` view-only, link sharing toggled per UI.
- **Port scan** of host shows only 8080/tcp open.

### Screenshots
1) Setup dashboard  
![Setup dashboard](../evidence/week1/20251010-setup-dashboard.png)

2) Team share permissions  
![Team share permissions](../evidence/week1/20251010-team-share-with-permissions.png)

3) User list  
![User list](../evidence/week1/20251010-user-page.png)

### Nmap result (local host `10.0.0.47`)
File: `scans/nmap-local.txt`
PORT STATE SERVICE VERSION
8080/tcp open http Apache httpd 2.4.62 ((Debian))


## Findings
- **Principle of Least Privilege**: No write access granted to students on shared folder yet.
- **Exposure**: Only HTTP 8080 is open on the host. Database remains internal to Docker network.
- **Identity**: Default `admin` present. Separate standard users confirmed.

## Actions
- Create unique strong passwords and store in lab vault.
- Add write permission for one test user next week to validate access controls.
- Prepare TLS reverse proxy on 443 and disable 8080 from untrusted networks in Week 2.
- Document user creation steps in `docs/runbooks/nextcloud-users.md`.
