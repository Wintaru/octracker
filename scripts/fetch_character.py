#!/usr/bin/env python3
"""
Fetches character profile data from the FFXIV Lodestone and writes
it to character.json in the repo root. Designed to run in GitHub Actions.
"""

import json
import re
import sys
import urllib.request
from datetime import date

CHARACTER_ID = "492391"
LODESTONE_URL = f"https://na.finalfantasyxiv.com/lodestone/character/{CHARACTER_ID}/"
OUTPUT_PATH = "character.json"

def fetch_page(url):
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (compatible; octracker-bot/1.0)"
    })
    with urllib.request.urlopen(req, timeout=15) as resp:
        return resp.read().decode("utf-8")

def parse_character(html):
    def find(pattern, default=""):
        m = re.search(pattern, html, re.S)
        return m.group(1).strip() if m else default

    avatar_url = find(r'frame__chara__face.*?<img src="([^"]+)"')
    name       = find(r'frame__chara__name">([^<]+)<')
    title      = find(r'frame__chara__title">([^<]+)<')
    world_raw  = find(r'frame__chara__world">(?:<[^>]+>)*([^<]+)<')

    # "Ultros [Primal]" → server="Ultros", datacenter="Primal"
    server, datacenter = "", ""
    if "[" in world_raw:
        server, rest = world_raw.split("[", 1)
        server = server.strip()
        datacenter = rest.rstrip("]").strip()

    # Free company name and crest (3 layered images)
    fc_name = find(r'character__freecompany__name.*?<a[^>]+>([^<]+)</a>')
    fc_crest_section = re.search(r'character__freecompany__crest__image(.*?)</div>', html, re.S)
    fc_crest = re.findall(r'<img src="([^"]+)"', fc_crest_section.group(1)) if fc_crest_section else []

    return {
        "name":        name,
        "title":       title,
        "server":      server,
        "datacenter":  datacenter,
        "avatarUrl":   avatar_url,
        "freeCompany": fc_name,
        "fcCrest":     fc_crest,
        "lodestoneUrl": LODESTONE_URL,
        "updatedAt":   date.today().isoformat(),
    }

def main():
    print(f"Fetching {LODESTONE_URL} ...")
    try:
        html = fetch_page(LODESTONE_URL)
    except Exception as e:
        print(f"ERROR: Failed to fetch page: {e}", file=sys.stderr)
        sys.exit(1)

    data = parse_character(html)

    missing = [k for k, v in data.items() if not v and k != "title"]
    if missing:
        print(f"WARNING: Missing fields: {missing}", file=sys.stderr)

    with open(OUTPUT_PATH, "w") as f:
        json.dump(data, f, indent=2)
        f.write("\n")

    print(f"Wrote {OUTPUT_PATH}:")
    print(json.dumps(data, indent=2))

if __name__ == "__main__":
    main()
