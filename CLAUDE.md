# OC South Pots FATE Tracker — Project Context

## What This Is

A single-page web app that predicts when "Pots" FATEs will spawn in the Occult Crescent South zone in Final Fantasy XIV. It's a self-contained HTML file using React via CDN (no build tools), hosted on GitHub Pages with a custom subdomain.

## Game Mechanics

- Occult Crescent South is an instanced zone that persists as long as players are in it. Individual players have a 180-minute cap on how long they can stay.
- ~5 minutes after the instance is created, the first Pots FATE spawns at the **North** location.
- Every 30 minutes after that, a new FATE spawns, alternating North and South.
- Full schedule: North @5m, South @35m, North @65m, South @95m, North @125m, South @155m.
- Players can see how long other players have been in the zone, but NOT when the instance was created.

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

## Current State

- Core tracker is fully functional.
- GitHub Pages is configured, DNS CNAME is set, waiting on propagation/SSL.
- README documents the prediction logic.
