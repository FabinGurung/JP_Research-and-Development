#!/usr/bin/env python3
"""
Shared static-site primitives. Stable links/escapes/shell are centralized.
This module must remain read-only: never mutate Drive/scientific sources.
"""
from __future__ import annotations
import argparse, html, json, shutil
from pathlib import Path
from urllib.parse import quote

ROOT=Path(__file__).resolve().parents[1]
REPO_URL="https://github.com/FabinGurung/JP_Research-and-Development"
SITE_URL="https://fabingurung.github.io/JP_Research-and-Development/"

def load(path): return json.loads((ROOT/path).read_text(encoding="utf-8"))
def esc(v): return html.escape("" if v is None else str(v))
def branch_url(branch): return f"{REPO_URL}/tree/{quote(branch, safe='/')}"
def drive_url(file_id):
    return f"https://drive.google.com/open?id={file_id}" if file_id else None

def evidence_html(debt):
    parts=[]
    for e in debt.get("evidence",[]):
        u=drive_url(e.get("drive_id")) if e.get("drive_id") else e.get("url")
        if not u or not str(u).startswith("https://"):
            continue
        parts.append(f'<li>{esc(e.get("role"))}: <a href="{esc(u)}">Open evidence</a></li>')
    return "".join(parts) or "<li>No external evidence pointer required.</li>"

def shell(title, body, depth=0):
    prefix="../"*depth
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(title)} · JP R&D</title><link rel="stylesheet" href="{prefix}assets/styles.css"><script defer src="{prefix}assets/theme.js"></script><script defer src="{prefix}assets/motion.js"></script><script defer src="{prefix}assets/prompt-copy.js"></script><script defer src="{prefix}assets/menu.js"></script></head><body><header class="topbar"><div class="wrap nav"><strong>JP R&D</strong><button class="mobile-menu-toggle" type="button" data-mobile-menu aria-controls="site-nav-links" aria-expanded="false">☰ Menu</button><nav class="navlinks" id="site-nav-links"><a href="{prefix}index.html">Home</a><a href="{prefix}start-here/index.html">Start here</a><a href="{prefix}search/index.html">Search library</a><a href="{prefix}researchers/index.html">Researchers</a><a href="{prefix}thesis-infrastructure/index.html">Thesis folders</a><a href="{prefix}owner-prompts/index.html">Chat handovers</a><a href="{prefix}workspace/index.html">Workspace</a><a href="{prefix}controls/latex/index.html">LaTeX control</a><a href="{prefix}controls/index.html">Controls</a><a href="{prefix}debts/index.html">Debts</a><a href="{prefix}roadmap/index.html">Roadmap</a><a href="{prefix}branches/index.html">Branches</a><a href="{prefix}how-to/index.html">How to</a><button type="button" class="theme-switch" data-theme-toggle aria-label="Switch to mauve dusk">☾ Dusk palette</button></nav></div></header>{body}<footer class="wrap footer">JP Research & Development · code + controls + pointers · working artifacts remain in Google Drive.</footer></body></html>"""

def write(out, rel, content):
    p=out/rel; p.parent.mkdir(parents=True,exist_ok=True); p.write_text(content,encoding="utf-8")

