✅ Week 6 Remediation Plan (Priority 1 CVE Fixes)



File: docs/week-notes/week6-remediation-plan.md

Purpose: Patch critical vulnerabilities (CVSS 9.0+) found in Week 5.



1\. Current Versions (Before Patching)

Container	Current Version	Notes

nextcloud:29-apache	Outdated Apache + PHP libraries	Contains critical OpenSSL, zlib, PHP, and xz-utils vulnerabilities

mariadb:11	Unpatched MariaDB image	No critical CVEs, but dependent libs vulnerable

nginx:alpine	Alpine version behind	zlib + OpenSSL issues apply here too

2\. Required Priority 1 Patches (Immediate)



Based on Week 5 findings:



🔧 Patch Required Libraries



These affect ALL containers and must be updated immediately:



xz-utils



Fixes CVE-2024-3094 (remote backdoor).



OpenSSL



Fixes CVE-2023-3446 (key recovery).



zlib



Fixes CVE-2022-37454 (buffer overflow).



glibc



Fixes CVE-2023-4911 (root privilege escalation).



PHP runtime



Fixes CVE-2024-2756 (heap overflow → RCE).



3\. Target Patched Versions

Component	Version Needed	Reason

nextcloud:29-apache	Latest 29-apache release from Docker Hub	Pulls patched PHP + system libraries

nginx:alpine	Latest Alpine stable	Includes patched OpenSSL/zlib/xz

xz-utils	5.6.x+ (post-backdoor removal)	Removes remote compromise backdoor

OpenSSL	Latest 3.x security release	Fixes key recovery vulnerability

PHP	Latest 8.2 or 8.3 stable in container	Fixes heap overflow

glibc	Latest stable security build	Prevents root escalation

4\. Patch Plan (Per Container)

📌 Nextcloud Container



Replace image with latest patched nextcloud:29-apache



Ensure:



PHP modules updated



xz-utils, zlib, OpenSSL, glibc are patched



Test:



App loads normally



File uploads/downloads work



Logs have no PHP extension errors



📌 Nginx Reverse Proxy



Update to latest nginx:alpine



Validate:



TLS still functional



Proxy configs do not break after OpenSSL upgrade



gzip compression (zlib) still works



📌 MariaDB



(Not Priority 1 but affected by shared libraries)



Test compatibility after base OS patching



No schema changes expected



5\. Breaking Changes to Test



Before deployment, check:



PHP upgrade does not break Nextcloud plugins/apps



Apache module changes do not block WebDAV



TLS configurations still allow Nextcloud sync clients



No permission conflicts after glibc upgrade



Container rebuild does not cause missing extensions



Nextcloud cron jobs still run



6\. Expected Downtime



Estimated: 15–30 minutes total



Breakdown:



Pulling updated images: 2–5 min



Rebuilding stack: 5–10 min



Post-patch validation tests: 5–15 min



7\. Risks if Not Patched



(Put in case your professor checks)



Remote backdoor execution



Host machine compromise via glibc



Account takeover



Database theft



Persistent malicious library injection



8\. Summary of Actions for Week 6



&nbsp;Review Week 5 findings



&nbsp;Identify Priority 1 CVEs



&nbsp;Patch nextcloud:29-apache



&nbsp;Patch nginx:alpine



&nbsp;Rebuild containers with updated base images



&nbsp;Run post-patch functional tests



&nbsp;Document before/after versions

