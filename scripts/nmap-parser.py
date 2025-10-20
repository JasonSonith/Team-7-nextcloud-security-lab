#!/usr/bin/env python3
# parse_nmap.py
# Parse Nmap output (XML preferred; normal text tolerated) -> CSV + optional heatmap.

import argparse
import csv
import os
import re
import sys
from collections import defaultdict

def parse_xml(path):
    import xml.etree.ElementTree as ET
    rows = []
    tree = ET.parse(path)
    root = tree.getroot()
    for host in root.findall("host"):
        status = host.find("status")
        if status is not None and status.get("state") != "up":
            continue
        addr = next((a.get("addr") for a in host.findall("address") if a.get("addrtype") in ("ipv4","ipv6")), "")
        hostname = ""
        hostnames = host.find("hostnames")
        if hostnames is not None:
            hn = hostnames.find("hostname")
            if hn is not None:
                hostname = hn.get("name","")
        ports = host.find("ports")
        if ports is None:
            continue
        for p in ports.findall("port"):
            proto = p.get("protocol","")
            portid = p.get("portid","")
            state = ""
            service = ""
            product = ""
            version = ""
            st = p.find("state")
            if st is not None:
                state = st.get("state","")
            sv = p.find("service")
            if sv is not None:
                service = sv.get("name","")
                product = sv.get("product","") or ""
                version = sv.get("version","") or ""
            rows.append({
                "host": hostname or addr,
                "ip": addr,
                "proto": proto,
                "port": int(portid) if portid.isdigit() else portid,
                "state": state,
                "service": service,
                "product": product,
                "version": version,
            })
    return rows

# Very simple normal-output parser. Expects sections with "Nmap scan report for" and a PORT table.
SCAN_FOR_RE = re.compile(r"^Nmap scan report for (.+?)(?: \(([\d.:a-fA-F]+)\))?$")
PORT_LINE_RE = re.compile(r"^(\d+)\/(tcp|udp)\s+(\S+)\s+(\S+.*)?$")  # 22/tcp open ssh OpenSSH 8.9p1

def parse_normal(path):
    rows = []
    current_host = ""
    current_ip = ""
    in_ports = False
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = line.rstrip("\n")
            m = SCAN_FOR_RE.match(line)
            if m:
                current_host = m.group(1).strip()
                current_ip = (m.group(2) or "").strip()
                in_ports = False
                continue
            if line.startswith("PORT") and "STATE" in line and "SERVICE" in line:
                in_ports = True
                continue
            if in_ports:
                if not line or line.startswith("Nmap done:") or line.startswith("MAC Address:"):
                    in_ports = False
                    continue
                pm = PORT_LINE_RE.match(line)
                if pm:
                    port = int(pm.group(1))
                    proto = pm.group(2)
                    state = pm.group(3)
                    rest = pm.group(4) or ""
                    # Split service and optional product/version heuristically
                    parts = rest.split(None, 1)
                    service = parts[0] if parts else ""
                    product = ""
                    version = ""
                    if len(parts) == 2:
                        product = parts[1]
                    rows.append({
                        "host": current_host or current_ip,
                        "ip": current_ip,
                        "proto": proto,
                        "port": port,
                        "state": state,
                        "service": service,
                        "product": product,
                        "version": version,
                    })
    return rows

def write_csv(rows, out_csv):
    os.makedirs(os.path.dirname(out_csv), exist_ok=True)
    cols = ["host","ip","proto","port","state","service","product","version"]
    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for r in sorted(rows, key=lambda x: (str(x["host"]), x["proto"], int(x["port"]) if isinstance(x["port"], int) or str(x["port"]).isdigit() else 0)):
            w.writerow(r)

def make_heatmap(rows, out_png):
    # Minimal dependency: matplotlib only if requested.
    try:
        import matplotlib.pyplot as plt
        import numpy as np
    except Exception as e:
        print(f"[warn] matplotlib not available: {e}", file=sys.stderr)
        return
    # Build grid of hosts x ports with 1 for open.
    hosts = sorted({r["host"] for r in rows})
    ports = sorted({r["port"] for r in rows if str(r["port"]).isdigit()}, key=int)
    idx_h = {h:i for i,h in enumerate(hosts)}
    idx_p = {p:i for i,p in enumerate(ports)}
    grid = np.zeros((len(hosts), len(ports)), dtype=int)
    for r in rows:
        if r["state"] == "open" and str(r["port"]).isdigit():
            grid[idx_h[r["host"]], idx_p[int(r["port"])]] = 1
    os.makedirs(os.path.dirname(out_png), exist_ok=True)
    plt.figure(figsize=(max(6, len(ports)*0.25), max(4, len(hosts)*0.3)))
    plt.imshow(grid, aspect="auto", interpolation="nearest")
    plt.title("Open Ports Heatmap")
    plt.xlabel("Port")
    plt.ylabel("Host")
    plt.xticks(ticks=range(len(ports)), labels=ports, rotation=90)
    plt.yticks(ticks=range(len(hosts)), labels=hosts)
    plt.tight_layout()
    plt.savefig(out_png, dpi=200)
    plt.close()

def main():
    ap = argparse.ArgumentParser(description="Parse Nmap output into CSV and optional heatmap.")
    ap.add_argument("-i","--input", required=True, help="Path to Nmap XML (-oX) or normal output file.")
    ap.add_argument("-o","--out-csv", default="scans/nmap-parsed.csv", help="CSV output path.")
    ap.add_argument("--heatmap", default="scans/nmap-heatmap.png", help="PNG heatmap output path. Use 'none' to skip.")
    args = ap.parse_args()

    if not os.path.isfile(args.input):
        print(f"[error] file not found: {args.input}", file=sys.stderr)
        sys.exit(2)

    rows = []
    try:
        if args.input.lower().endswith(".xml"):
            rows = parse_xml(args.input)
        else:
            rows = parse_normal(args.input)
    except Exception as e:
        print(f"[error] parse failed: {e}", file=sys.stderr)
        sys.exit(1)

    if not rows:
        print("[warn] no rows parsed. Check input format.", file=sys.stderr)

    write_csv(rows, args.out_csv)
    if args.heatmap.lower() != "none":
        make_heatmap(rows, args.heatmap)
    print(f"[ok] wrote {len(rows)} rows -> {args.out_csv}")
    if args.heatmap.lower() != "none":
        print(f"[ok] wrote heatmap -> {args.heatmap}")

if __name__ == "__main__":
    main()
