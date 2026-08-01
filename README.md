# OC Pots FATE Tracker

A simple timer tool for predicting when Pots FATEs will spawn in the Occult Crescent South Horn or North Horn instances in FFXIV.

## How It Works

### The FATE Schedule

When an Occult Crescent instance is created, Pots FATEs follow a fixed schedule, identical in both Horns:

- **FATE 1** — ~10 min after creation (North)
- **FATE 2** — ~40 min (South)
- **FATE 3** — ~70 min (North)
- **FATE 4** — ~100 min (South)
- **FATE 5** — ~130 min (North)
- **FATE 6** — ~160 min (South)

FATEs spawn every 30 minutes, alternating between North and South, starting 10 minutes after the instance is created. The instance has a max lifetime of 180 minutes.

### The Two Horns

"North" and "South" describe a FATE's slot in the schedule above, not the Horn zone. Each Horn has its own pair of named Pots FATEs at fixed map coordinates:

| Horn | North slot | South slot |
|---|---|---|
| South Horn | Persistent Pots (X:25.6, Y:17.1) | Pleading Pots (X:11.9, Y:32.0) |
| North Horn | Daylight Pottery (X:26.2, Y:11.6) | In a Pot of Bother (X:11.0, Y:25.8) |

Pick your Horn on the setup screen before starting the tracker.

### The Problem

You can't directly see when an instance was created. You *can* see how long players have been in the zone, but the instance may have existed before the oldest visible player joined.

### How We Estimate

1. **Initial guess:** You enter the oldest player's time in the zone. We assume that player created the instance, which gives us an estimated instance age. This gets us within roughly ±5 minutes of the real schedule.

2. **Calibration:** When you actually see a FATE pop, you press the North or South button. The tracker snaps the schedule to match reality. Knowing *which* location popped narrows it down to the correct FATE in the sequence, and the timing window tightens from ±5 min to ±1 min.

3. **Re-calibration:** Calibrating on a second observed FATE tightens accuracy further to ±30 seconds.

### Why ±5 Minutes?

The FATEs are 30 minutes apart. If our initial estimate of the instance age is off, it can be off by at most however long the instance existed before the oldest player joined. In practice this is usually small, and a ±5 minute window covers most cases. One calibration effectively eliminates the guesswork.
