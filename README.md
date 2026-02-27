# OC South Pots FATE Tracker

A simple timer tool for predicting when Pots FATEs will spawn in the Occult Crescent South instance in FFXIV.

## How It Works

### The FATE Schedule

When an Occult Crescent South instance is created, Pots FATEs follow a fixed schedule:

- **FATE 1** — ~5 min after creation (North)
- **FATE 2** — ~35 min (South)
- **FATE 3** — ~65 min (North)
- **FATE 4** — ~95 min (South)
- **FATE 5** — ~125 min (North)
- **FATE 6** — ~155 min (South)

FATEs spawn every 30 minutes, alternating between North and South, starting 5 minutes after the instance is created. The instance has a max lifetime of 180 minutes.

### The Problem

You can't directly see when an instance was created. You *can* see how long players have been in the zone, but the instance may have existed before the oldest visible player joined.

### How We Estimate

1. **Initial guess:** You enter the oldest player's time in the zone. We assume that player created the instance, which gives us an estimated instance age. This gets us within roughly ±5 minutes of the real schedule.

2. **Calibration:** When you actually see a FATE pop, you press the North or South button. The tracker snaps the schedule to match reality. Knowing *which* location popped narrows it down to the correct FATE in the sequence, and the timing window tightens from ±5 min to ±1 min.

3. **Re-calibration:** Calibrating on a second observed FATE tightens accuracy further to ±30 seconds.

### Why ±5 Minutes?

The FATEs are 30 minutes apart. If our initial estimate of the instance age is off, it can be off by at most however long the instance existed before the oldest player joined. In practice this is usually small, and a ±5 minute window covers most cases. One calibration effectively eliminates the guesswork.
