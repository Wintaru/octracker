# OC Pots FATE Tracker — Project Context

## What This Is

A single-page web app that predicts when "Pots" FATEs will spawn in Occult Crescent's South Horn or North Horn zones in Final Fantasy XIV. It's a self-contained HTML file using React via CDN (no build tools), hosted on GitHub Pages with a custom subdomain.

## Game Mechanics

- Each Occult Crescent Horn (South Horn, North Horn) is an instanced zone that persists as long as players are in it. Individual players have a 180-minute cap on how long they can stay.
- The Pots FATE schedule is identical in both Horns: ~10 minutes after the instance is created, the first Pots FATE spawns at the **North** location.
- Every 30 minutes after that, a new FATE spawns, alternating North and South.
- Full schedule: North @10m, South @40m, North @70m, South @100m, North @130m, South @160m.
- Players can see how long other players have been in the zone, but NOT when the instance was created.
- "North"/"South" describe a FATE's slot in the shared schedule, not the Horn itself. Each Horn has its own pair of named FATEs at fixed map coordinates:
  - South Horn: **Persistent Pots** (X:25.6, Y:17.1, North slot), **Pleading Pots** (X:11.9, Y:32.0, South slot)
  - North Horn: **Daylight Pottery** (X:26.2, Y:11.6, North slot), **In a Pot of Bother** (X:11.0, Y:25.8, South slot)
  - Source: [Icy Veins — Magic Pot Locations and Rewards](https://www.icy-veins.com/ffxiv/magic-pots)

## How the Tracker Works

1. **Initial estimate:** User enters the oldest player's time in zone (in minutes). We assume that player created the instance. This gives us an estimated instance age, accurate to roughly ±5 minutes.
2. **Live countdown:** A real-time timer ticks from that starting point, showing a confidence window (early/best guess/late) for each upcoming FATE.
3. **Calibration:** When the user sees a FATE actually pop, they press a North or South button. The tracker snaps the schedule to match the observed FATE. Knowing the location filters to only N or S FATEs in the sequence, improving accuracy. First calibration → ±1 min. Second calibration → ±30 sec.

## Tech Stack

- Single `index.html` file, no build step
- React 18 + ReactDOM loaded from cdnjs.cloudflare.com
- Babel standalone for JSX transpilation in-browser
- All state managed with React hooks (useState, useEffect, useCallback)
- No external dependencies, no localStorage, no backend

## Hosting

- GitHub repo: `wintaru/octracker`
- GitHub Pages serves from `main` branch, root directory
- Custom domain: `octracker.abandonedbits.com`
- DNS: CNAME record `octracker` → `wintaru.github.io`

## File Structure

```
/
├── index.html    ← the entire app
├── 404.html      ← redirects path-based share URLs to hash-based (GitHub Pages trick)
├── CLAUDE.md     ← this file
└── README.md     ← explanation of the logic
```

## Key Design Decisions

- Single minutes input (not hours/minutes/seconds) for simplicity — users just type the number they see in-game.
- Confidence windows instead of exact predictions, since the initial estimate has inherent uncertainty.
- North/South calibration buttons instead of a generic "FATE popped" button — knowing the location halves the ambiguity when snapping to the schedule.
- Progressive accuracy: starts rough, gets precise with observation. No calibration needed if ±5 min is acceptable.
- Horn selection (South Horn / North Horn) lives entirely in display data (`ZONES` in `index.html`) — the schedule math (`FATE_START`, `FATE_INTERVAL`, `fateTime`, `fateLoc`) is zone-agnostic since both Horns share the same timing. Adding a future Horn only means adding a `ZONES` entry.
- The zone is encoded as 1 bit in the share-code word format so joined/shared trackers carry the correct Horn.

## Current State

- Core tracker is fully functional, supporting both South Horn and North Horn.
- GitHub Pages is configured, DNS CNAME is set, waiting on propagation/SSL.
- README documents the prediction logic.
