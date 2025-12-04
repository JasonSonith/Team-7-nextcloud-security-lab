# Methodology Script (Slides 1-2)
## Estimated Speaking Time: 3.5-4 minutes

---

## SLIDE 1 - Methodology (Weeks 1-4)

Alright, let's talk about how we actually did this assessment. [pause] We broke our testing into seven weeks, each with a specific focus, so I'll walk you through what we did and what we found.

**Week 1** was all about getting the environment up and running. We built out our three-container lab—Nextcloud, MariaDB, and nginx—and made sure everything was actually working. Nothing fancy here, just confirming we could log in, the containers could talk to each other, and we had a stable baseline to test against.

Moving into **Week 2**, we started thinking like actual users. We created lab accounts with different permission levels and configured group roles following least privilege—so not everyone's an admin. We also ran our first Nmap scan to see what ports were exposed to the outside world. Turned out it was just port 8080, which was good to know before we started poking at things.

**Week 3** got more interesting. This is where we started digging into the configuration files. [gesture to audience] You know how sometimes secrets end up in plaintext? Yeah, we found that. The config.php file had plaintext password salts, database credentials, secret keys—all just sitting there. We also looked at the .env files and started documenting what wasn't configured yet, like HTTPS, secure cookie flags, and HSTS headers. Basically, we built a list of things that needed fixing.

Now **Week 4**—this is where we really started testing. [pause] We fired up Burp Suite and tested authentication flows, session handling, cookie security, CSRF protection, the password policy, and brute-force behavior. Then we ran the OWASP ZAP baseline scan, which crawled 32 URLs and ran 67 different security rules against our application.

[gesture to slide] On the left here, you can see the ZAP report. It passed most of the rules—56 out of 67—but it did flag some issues. The big one was a vulnerable JavaScript library, which got tagged as high severity. Then we had a bunch of medium-severity Content Security Policy problems—stuff like missing directives, wildcards where there shouldn't be, and unsafe inline styles. The rest were mostly low-severity informational findings like server headers leaking version info. [pause] The good news? No critical vulnerabilities at this point. But we knew we had work to do.

---

## SLIDE 2 - Methodology (Weeks 5-7)

So that brings us to the second half of our timeline.

**Week 5** was all about container security and file handling. We went pretty deep on file uploads—testing malicious files, double extensions, trying to crash the system with huge files, and even testing WebDAV operations. We threw everything at it: Unicode filenames, really long filenames, HTML and JavaScript payloads embedded in files, SVG scripts, even malware test files just to see what would happen. [pause] At the same time, we reviewed the container security posture—checked Docker configurations against the CIS Benchmark, looked for privilege escalation risks, and audited how secrets were being managed inside the containers.

Then came **Week 6**, which was... honestly kind of brutal. [slight laugh] We ran Trivy—that's a vulnerability scanner for container images—on all three of our containers. It found over 187 unique CVEs. Twenty-one of those were critical. [pause] So yeah, we had a lot to fix. We went through and prioritized everything based on severity and whether it was actually exploitable in our setup, and that gave us a clear roadmap for hardening.

**Week 7** was remediation time. We patched all the Priority 1 CVEs by upgrading our images—Nextcloud, MariaDB, and nginx—to versions where those vulnerabilities were fixed. [gesture to slide] You can see on the left here part of our updated docker-compose file. We pinned MariaDB to version 11.8.5, which dropped the critical CVE count to zero and left us with just 27 lower-severity issues. Nextcloud got bumped to version 29.0.16.1, which included patches for some nasty authentication bypass bugs.

But we didn't stop there. We also applied full container hardening—dropped all Linux capabilities, enforced no-new-privileges, made filesystems read-only where possible, ran everything as non-root, and added resource limits so a container couldn't eat all the CPU or memory. [pause] Then we re-scanned everything with Trivy to prove the fixes actually worked, compared the before-and-after CVE counts, and documented all the evidence for the final report.

[pause, slightly slower] So in seven weeks, we went from a baseline deployment with 200-plus vulnerabilities down to a hardened configuration with zero critical CVEs and a much smaller attack surface. And we documented every step of the way so it's reproducible.

---

## Delivery Notes:
- **Total word count:** ~730 words (~3.5-4 minutes at natural speaking pace)
- **Tone:** Confident, conversational, professional but not stiff
- **Pacing:** Slow down slightly when listing technical details (CVE counts, tool names) so audience can absorb
- **Gestures:** Reference slide visuals at marked points to direct audience attention
- **Energy:** Week 6 reaction ("honestly kind of brutal") adds personality—deliver with slight self-deprecating humor
- **Transitions:** Natural phrases like "So that brings us to..." and "Then came Week 6..." keep flow smooth
- **Emphasis:** Pause before key numbers (187 CVEs, 21 critical, zero critical after patching) for impact
