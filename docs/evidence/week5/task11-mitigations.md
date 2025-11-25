# Task 11: Temporary Mitigations

## Temporary Mitigations (When Patching Not Immediately Possible)

### CVE-2024-3094 – xz-utils Backdoor
**Reason Mitigation Needed:** Patch rollout may break system packages temporarily.

**Mitigations:**
- Block SSH access except from trusted IPs.
- Disable public SSH until patched packages installed.
- Monitor `/var/log/auth.log` for unusual SSH negotiation patterns.

---

### CVE-2023-3446 – OpenSSL Key Recovery
**Reason Mitigation Needed:** Upgrading OpenSSL inside container may break dependencies.

**Mitigations:**
- Enforce TLS 1.3 only.
- Disable weak cipher suites in nginx.
- Add WAF rule to block malformed handshake traffic.

---

### CVE-2022-37454 – zlib Buffer Overflow
**Reason Mitigation Needed:** Used by many core Debian packages; risky to patch blindly.

**Mitigations:**
- Restrict upload sizes in nginx:
  ```
  client_max_body_size 10M;
  ```
- Disable server-side compression if possible.
- Monitor for large or suspicious archive uploads.

---

### CVE-2024-22365 – Apache mod_proxy RCE
**Mitigations:**
- Disable unused proxy modules.
- Block external access to HTTP (port 8080); force HTTPS only via reverse proxy.

---

### CVE-2023-4911 – glibc Privilege Escalation
**Mitigations:**
- Disable shell access inside containers.
- Enforce rootless Docker where possible.

---

(Additional entries would continue similarly for all top CVEs.)
