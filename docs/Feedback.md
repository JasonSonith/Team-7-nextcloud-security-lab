# Final Report & Slides — Endgame Checklist and Writing Guide

> **Goal:** Turn your draft into a clear, complete, and professional Final Report and Presentation. This document rewrites the instructor’s comments into a direct, beginner‑friendly checklist.

---

## 1) Put Your Team Number Everywhere
- **Action:** Add your **team/group number** to:
  - The **front page** of the **Final Report**
  - The **title slide** of the **Presentation**

---

## 2) Remove the Timeline from the Final Report
- At Final Report time, the work is done—**the timeline is complete**.
- **Action:** Remove the timeline section from the Final Report.

---

## 3) Switch to Past Tense (It’s Done, Not “Going To Do”)
- **Change style:** “We are going to…” → **“We did…”**
- **Example:** “We are going to scan images with Trivy” → **“We scanned images with Trivy and found X high‑severity CVEs.”**

---

## 4) Figures and Tables: Label, Describe Briefly, Discuss in Text
- **Every figure and table needs:**
  - A **label** and a **short caption**.
  - **Discussion in the main text** (not inside the caption).
- **Example label:** `Figure 1.3: Captured Set‑Cookie response headers`
- **In your text:** Refer to it and explain **what it shows** and **why it matters**.

---

## 5) If You Insert/Remove Figures or Tables, Renumber Everything
- **Action:** After any edit, **renumber** all affected figures/tables **and** fix all references in the text.

---

## 6) Label Placement Rules (Don’t Mix Them Up)
- **Figures:** label **below** the figure.
- **Tables:** label **above** the table.
- If a section is only a table (e.g., **Section 2.4**), **add a table label** and **add a short paragraph** explaining it.
  - Example text: “As shown in **Table 2.x**, Encryption and Key Storage …”

---

## 7) Go Deeper: Explain Every Tool, Choice, and Step
The topic is strong, the writing is decent—but **you need far more detail**. Assume the reader is smart but **knows nothing about your tech**. If you don’t explain it, **they won’t understand it**.

### 7a) Justify Design Choices
- **Why Docker?**
  - What alternatives did you consider (e.g., bare metal, VMs, Podman, Kubernetes, systemd‑nspawn)?
  - Why did Docker best fit your goals (reproducibility, isolation, CI, team setup speed, etc.)?
- **What is the CIS Docker Benchmark?**
  - Briefly define it and explain **how you applied it** (which controls, what you changed, what failed/passed).

### 7b) Define the Tools You Used (One‑sentence what + one‑sentence why)
- **Nmap:** Network scanner to discover hosts/ports; used to map exposed services.
- **Nikto:** Web server vulnerability scanner; used for quick misconfig checks.
- **Trivy:** Vulnerability/SCA scanner for container images and filesystems; used to find CVEs and outdated packages.
- **Composer audit:** Checks PHP dependencies for known vulnerabilities; used to surface insecure libraries.
- **Burp Suite (list which modules you used):** Proxy, Repeater, Scanner, Intruder, etc.; used for manual/web security testing.
- **ZAP:** OWASP Zed Attack Proxy; used for automated/web app scanning.
- **Kali Linux:** Security testing distro; used as your attacker/test toolkit.
- **MariaDB:** Your database backend; explain why chosen over MySQL/Postgres.
- **Proxy vs Reverse Proxy:** Proxy = client → internet; Reverse proxy = internet → your app. Explain where you used each (e.g., Nginx).
- **CVE / CVSS:** CVE = vulnerability ID; CVSS = severity score system. Explain how you used scores in decisions.

### 7c) Secrets and Configuration
- **What environment secrets are stored?** (DB passwords, API keys, salts, JWT secrets, etc.)
- **What is `sample.env.example`?** A template showing required keys.
- **Why rename to `.env`?** Actual secrets live in `.env` (not committed). Show **how it’s loaded** and **how it’s kept out of Git**.

> **Rule:** If a non‑technical executive or your parents read this, they should still get it.

---

## 8) User Files & Access (Answer These Clearly)
- **Where are uploaded files stored?** (Which volume/bucket/path?)
- **Auth needed to access them?** (User ID/password? SSO?)
- **Authorization model:** Which **roles/permissions** are required to read/write/delete? Folder vs file‑level rights?
- **Access outside Nextcloud:** Can files be accessed without Nextcloud (e.g., direct storage URL or WebDAV)? If yes, how is it controlled?
- **Sharing:** Can users share files or grant rights to others? **How is this implemented and audited?**

---

## 9) Architecture & Threat Modeling (Don’t Stop at a Pretty Picture)
- You mention **threat models, attack surface, and attack types**, but provide **no detail**.
- **Action:** For your architecture diagram, **walk the reader through**:
  - **Trust boundaries** (where data crosses between systems).
  - **Assets** (files, DB records, credentials).
  - **Entry points** (login, file upload, WebDAV endpoints, APIs).
  - **STRIDE/DREAD or chosen framework** with **concrete findings** and **mitigations**.
- A good graphic **plus** a clear explanation = understanding.

---

## 10) Explain PHP‑FPM (Keep It Simple)
- **What it is:** PHP‑FPM = FastCGI Process Manager for PHP; it runs PHP scripts efficiently behind a web server (e.g., Nginx).
- **Why you used it:** performance, isolation, process management.
- **How it fits your stack:** Nginx (reverse proxy) → PHP‑FPM (executes PHP) → MariaDB (data).

---

## 11) Define Every Term You Mention
When you write “PermissionsMask”, “jail”, “cache”, “base storage”, etc., **define them** where they appear:
- **Permissions mask (umask):** default permission bits for new files/dirs.
- **Jail/Chroot/Container:** isolation mechanism; say which one you used and **why**.
- **Cache:** what’s cached (static assets? sessions?), where, and how it’s invalidated.
- **Base storage:** what backend (local volume, NFS, S3), and why it’s safe (encryption, backups, IAM).
- **Encryption & key storage:** what’s encrypted at rest/in transit, where keys live, who can access, and how keys rotate.

---

## 12) Peer Review Before Submission
- **Action:** Have one or more people read the paper end‑to‑end.
- Fix clarity errors like: **Page 10, 2nd paragraph** — “The first line of dense …”

---

## 13) Trivy, Code Scanning, and SCA — Put It In the Right Box
- **What is Trivy?** Scanner for **images and filesystems** (OS packages + app deps).
- **“Scanning images” means:** analyzing container images for known CVEs and misconfigs.
- **Why under “Code Review with Tools”?** If you used it to scan **dependencies (SCA)** or **IaC**, say so explicitly. Otherwise, place it under **Security Testing/Scanning**.
- **What is SCA (Software Composition Analysis)?** Checking third‑party libraries for known vulnerabilities and licenses.
- **How does Trivy scan a filesystem for CVEs?** It fingerprints packages and versions, compares against vulnerability databases, and reports CVEs.
- As before, **explain**: Burp, ZAP, Nikto, auth endpoints, session management, CSRF, CORS, file uploads, WebDAV, information leakage, **abuse cases**, **STRIDE**, **DREAD**, etc.
  - For each, give **what it is**, **why it matters**, **what you did**, and **what you found/changed**.

---

## 14) Overall Feedback
- **You’re on track.** The subject is strong and the first draft is solid.
- **Next step:** **Expand every section.** Define and explain your tools, abbreviations, tasks, and workflow.
- Don’t make the reader guess. **If it’s not written, they won’t know.**
- Handle these details and you’ll land a **strong Final Report**.

---

## Quick Submission Checklist (Copy/Paste)
- [ ] Team number on report cover and presentation title slide.
- [ ] Timeline removed from Final Report.
- [ ] All prose in **past tense**.
- [ ] Every figure/table labeled correctly (figure: below; table: above).
- [ ] Captions are short; full explanation is in the main text.
- [ ] All figures/tables **renumbered** after edits; all references updated.
- [ ] Docker choice justified; CIS Docker Benchmark explained and applied.
- [ ] All tools defined (what + why) and tied to findings.
- [ ] Secrets handling documented; `.env` process explained; `.gitignore` shown.
- [ ] User files: storage path, authN/authZ model, sharing policy, external access clarified.
- [ ] Architecture diagram **explained** (threats, mitigations, trust boundaries).
- [ ] PHP‑FPM role in the stack explained.
- [ ] Trivy/SCA placement correct; scanning scope and results summarized.
- [ ] Peer review completed; typos and unclear lines fixed.

---

## Example Caption + Text (Template)
**Figure 2.3: Login flow with session issuance**  
_In the figure above, the reverse proxy terminates TLS and forwards PHP requests to PHP‑FPM. On successful authentication, the app sets a `Set‑Cookie` with the `HttpOnly`, `Secure`, and `SameSite=Lax` attributes. We chose `SameSite=Lax` to reduce CSRF risk without breaking normal navigation. Session IDs are stored server‑side in MariaDB with a 30‑minute idle timeout._

---

## Appendix: `.env` Hygiene (Mini‑Snippet)
```bash
# .gitignore
.env
.env.*
```

```env
# sample.env.example (template only; no real secrets)
DB_HOST=mariadb
DB_USER=nextcloud
DB_NAME=nextcloud
DB_PASSWORD=CHANGE_ME
JWT_SECRET=CHANGE_ME
```

**How it works:** Copy `sample.env.example` → `.env`, fill real secrets, and keep `.env` out of Git. Your compose file or app reads from `.env` at runtime.
