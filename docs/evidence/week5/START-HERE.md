# Week 5: CVE Mapping & Remediation - START HERE

Welcome to Week 5! This week you'll scan your Nextcloud stack for vulnerabilities, understand what they mean, and propose fixes.

## What You Need to Know

**CVE** = Common Vulnerabilities and Exposures
- A unique ID for security bugs (like CVE-2024-1234)
- Tracked in public databases so everyone can see what's broken

**SCA** = Software Composition Analysis
- Tools that scan your code and containers for known CVEs
- Like a virus scanner but for software vulnerabilities

**CVSS** = Common Vulnerability Scoring System
- A score from 0-10 rating how dangerous a vulnerability is
- 9.0-10.0 = CRITICAL (drop everything and fix!)
- 7.0-8.9 = HIGH (fix this week)
- 4.0-6.9 = MEDIUM (fix during maintenance)
- 0.1-3.9 = LOW (just monitor it)

## What You'll Do This Week

1. Run vulnerability scanners on your Docker containers
2. Count how many CVEs you found
3. Pick the 10-15 scariest ones
4. Research what each CVE means
5. Figure out how to fix them
6. Write a report explaining everything

## Three Documents to Guide You

### 1. QUICK-START-CHECKLIST.md (Start Here!)
- Simple checkbox list of tasks
- All commands copy-paste ready
- Expected time: 6-8 hours total
- **Location:** `/home/Jason/Team-7-nextcloud-security-lab/docs/evidence/week5/QUICK-START-CHECKLIST.md`

### 2. WEEK-5-CVE-MAPPING-GUIDE.md (Detailed Explanations)
- Step-by-step instructions with examples
- Explains what each command does
- Troubleshooting tips
- CVSS scoring explained simply
- **Location:** `/home/Jason/Team-7-nextcloud-security-lab/docs/week-notes/WEEK-5-CVE-MAPPING-GUIDE.md`

### 3. This Document (START-HERE.md)
- You're reading it now!
- Quick orientation

## Quick Start (5 Steps)

### Step 1: Read the Checklist
```bash
cat /home/Jason/Team-7-nextcloud-security-lab/docs/evidence/week5/QUICK-START-CHECKLIST.md
```

### Step 2: Start Your Docker Stack
```bash
cd /home/Jason/Team-7-nextcloud-security-lab/infra/docker
docker-compose up -d
docker ps  # Should see 3 containers
```

### Step 3: Run First Scan (Trivy on Nextcloud)
```bash
trivy image nextcloud:29-apache --format table --output /home/Jason/Team-7-nextcloud-security-lab/docs/evidence/week5/trivy-scans/nextcloud-app-trivy.txt

# View results
cat /home/Jason/Team-7-nextcloud-security-lab/docs/evidence/week5/trivy-scans/nextcloud-app-trivy.txt
```

### Step 4: Follow the Full Checklist
Open the QUICK-START-CHECKLIST.md and work through each checkbox.

### Step 5: Document Your Findings
Use the template examples in WEEK-5-CVE-MAPPING-GUIDE.md to write your final report.

## What Success Looks Like

By the end of Week 5, you should have:
- Scan results showing all CVEs in your stack
- A list of 10-15 critical vulnerabilities with explanations
- CVSS scores documented for each (with breakdowns)
- A priority list: which to fix first
- Specific upgrade commands to patch vulnerabilities
- A complete findings report in markdown format

## Common Questions

**Q: I found 200+ CVEs! Is that bad?**
A: Totally normal. Most will be LOW or MEDIUM severity. You only need to deeply analyze the CRITICAL and HIGH ones (usually 10-30 CVEs).

**Q: How long will this take?**
A: Plan for 6-8 hours total:
- 1 hour to run all scans
- 2-3 hours to analyze results
- 2-3 hours to write findings report
- 1 hour buffer for troubleshooting

**Q: What if I don't understand CVSS scores?**
A: That's why we made the guide! Section "Understanding CVSS Scores" in WEEK-5-CVE-MAPPING-GUIDE.md breaks it down with examples.

**Q: Do I need to fix the vulnerabilities this week?**
A: No! Week 5 is about finding and documenting them. Week 6 is when you actually apply the fixes.

**Q: What tools do I need?**
A: Just Trivy (for container scanning) is required. Composer audit and OWASP Dependency-Check are optional extras.

**Q: Can I skip the detailed CVSS breakdown?**
A: Not recommended. Understanding how CVSS scores are calculated is a key learning objective. It's how security teams prioritize fixes in real jobs.

## Tips for Success

1. **Start with the checklist** - it has all commands ready to copy-paste
2. **Run scans first, analyze later** - get all data collection done in one session
3. **Focus on CRITICAL severity** - don't try to analyze all 200 CVEs
4. **Use NVD website** - https://nvd.nist.gov/ has explanations for every CVE
5. **Take breaks** - vulnerability analysis can be mentally draining
6. **Ask for help** - if stuck, reference the troubleshooting section in the guide

## File Organization

All your Week 5 work goes here:
```
/home/Jason/Team-7-nextcloud-security-lab/docs/evidence/week5/
├── trivy-scans/           # Scan outputs from Trivy
├── composer-audit/        # PHP dependency scan results
├── dependency-check/      # OWASP DC reports (optional)
├── cve-research/          # Your analysis notes
├── QUICK-START-CHECKLIST.md
└── START-HERE.md          # You are here!

/home/Jason/Team-7-nextcloud-security-lab/docs/findings/
└── week-5-findings.md     # Your final report goes here
```

## Next Steps

1. **Right now:** Open QUICK-START-CHECKLIST.md
2. **Then:** Start checking off tasks one by one
3. **When stuck:** Reference WEEK-5-CVE-MAPPING-GUIDE.md for details
4. **At the end:** Review the completion checklist in the guide

## Ready to Start?

Open the checklist and begin:
```bash
nano /home/Jason/Team-7-nextcloud-security-lab/docs/evidence/week5/QUICK-START-CHECKLIST.md
```

Or if you prefer to read the full guide first:
```bash
less /home/Jason/Team-7-nextcloud-security-lab/docs/week-notes/WEEK-5-CVE-MAPPING-GUIDE.md
```

**Good luck! You've got this!**

Remember: Finding vulnerabilities is what security professionals DO. It's not a failure - it's exactly what you're supposed to discover. Your job is to understand and document them clearly.
