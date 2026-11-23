# HT Dash: HT's expo game

A simple pixel art running game for HT Media's trade show stand. Dan runs through the British countryside, jumping over camera kit, roadworks, cows and sheep, dodging seagulls and drones, and grabbing pies for super jumps. It runs in a web browser, needs no internet and nothing to install.

## How to play it on the stand laptop

1. Copy this whole folder onto the laptop (or a USB stick).
2. Double-click `index.html`. It opens in Chrome.
3. Press **F** (or F11) for full screen.

For a locked-down kiosk, make a desktop shortcut that runs:

```
chrome --kiosk "C:\path\to\Game\index.html"
```

Alt+F4 closes it.

## Sending it to someone to try

`dist/HT-Dash.html` is the whole game in one file (about 130 KB), with all the artwork packed inside. Send it by email, Teams, Slack or WeTransfer. They save it, double-click it, and it opens in their browser. No folder, no install, no internet needed. Chrome or Edge on Windows work best.

After changing the game, rebuild that file with:

```
python3 tools/build_single_file.py
```

## Controls

Pick a runner with the arrow keys, then the game is played with the **spacebar** only.

| Key | What it does |
|---|---|
| Left / Right arrows | Turn the HT ring on the title screen to choose a runner |
| Space | Start, then jump. Tap for a small hop, hold for a big jump |
| Type, then Enter | Add your name to the high scores at the end of a run |
| F | Full screen on or off |
| Ctrl+Alt+R | Clear the high score table (asks first). Saved entries are kept |
| Ctrl+Alt+E | Download every entry (name, work email, score, runner, date, time) as a spreadsheet (CSV) |

## The runners

Dan (Managing Director) is the default. Use the left and right arrows on the title screen to play as Dave (Production Director), Mark (Creative Director), Beth (Operations & Creative Coordinator), Sam (Editor) or Jonas (Creative Producer) instead. After each run it goes back to Dan. Everyone runs, jumps and wears the cape the same way. The artwork is in `sprites/characters/`, drawn by `sprites/src/characters.py`.

## Getting harder

Every run gets harder with time, so nobody plays for much more than a minute:

| From | What changes |
|---|---|
| Start | Tripods, flight cases and sheep at a gentle pace |
| 8 to 20 seconds | Cows, stacked cases and the roadworks barrier join in |
| 15 seconds | You run from the fields into a port: the quay arrives under your feet past a signpost, the hills slope into the sea, then the container ship, crane, tug and offshore wind farm come into view. Sheep and cows give way to mooring bollards and shipping containers |
| 15 to 18 seconds | Low seagulls and drones: jump over them (drones bob up and down) |
| 22 to 28 seconds | High seagulls and drones: don't jump, or just tap for a small hop underneath |
| 25 seconds | Pairs of obstacles close together: one long, held jump clears both |
| 40 seconds | No more pies |
| 50 seconds | The speed keeps climbing until you crash |

Faint wind streaks start rushing past as the speed picks up. Seagulls and drones glow so they're easy to spot.

## HT colours

- The HT logo sits in the title panel, drawn smoothly rather than as pixels, and the select screen is a big HT ring with the team's faces round it.
- Each runner has their own colour from the logo ring: Dan orange, Dave mint, Mark lime, Beth magenta, Sam teal, Jonas mustard. It's used for their glow and label on the select screen, the game over card, and their name on the high scores.
- Panels have a border made of the logo's colour segments.
- The pie power timer is a mini HT ring whose segments switch off as the power runs out.

The speed rises the whole time and the gaps between obstacles shrink.

## Stepping on obstacles

Land on top of anything (camera kit, animals, containers, even a seagull) and you bounce off it and score **+5**, once per obstacle. Hitting the side still ends the run.

## Pie power

Every so often a pie floats past at jump height. Grab it and Dan puts on a superhero cape, glows gold and jumps twice as high for 10 seconds (the timer is at the top of the screen).  Pies get rarer as the run goes on.

## Client cameos

The hills feature some of HT's clients as generic buildings, with no names or logos: a hospital (Newcastle Hospitals), cows grazing in the fields (ARN), an old pit headframe and winding house (Mining Remediation Authority) and a small white plane in the sky (HII project).

## Names and work emails

At the end of each run the player types their name, presses Enter, then types their work email and presses Enter again. Only the name ever appears on screen; the high score table never shows emails.

Every entry is saved in Chrome on that laptop. It survives refreshing the page, closing Chrome and restarting the laptop. Download them as a spreadsheet with **Ctrl+Alt+E**, ideally at the end of each day. To keep the entries safe:

- always open the game from the same file, in the same place, in the same browser
- don't clear Chrome's browsing data on that laptop until you've downloaded them
- the entries are personal data, so store and use the downloaded file in line with HT's privacy policy

## High scores

When Dan crashes, a film clapperboard drops in and snaps shut, showing the score, today's take number (which go this is today) and the date. The player types their name on the DIRECTOR line and presses Enter.


The top 10 are saved in Chrome on that laptop, so they survive closing the game and restarting the laptop. They are only on that one laptop and that one browser. Clearing Chrome's browsing data deletes them. If nobody types a name within a minute, the game goes back to the title screen without saving.

## What's here

| Path | What it is |
|---|---|
| `index.html` | The whole game |
| `sprites/ui/` | Pixel versions of the HT logo, used in the mockups (the game draws the logo smoothly in code) |
| `sprites/src/port.py` | Draws the port: sea, wind farm, container ship, crane, tug and quayside |
| `sprites/mockups/` | Ideas not in the game: Dan's 3D spin, three select screen designs |
| `dist/HT-Dash.html` | The same game packed into one file to send to people |
| `tools/build_single_file.py` | Rebuilds `dist/HT-Dash.html` |
| `sprites/` | All the artwork as PNGs |
| `sprites/src/` | Python scripts that draw the artwork (`python3 sprites/src/<name>.py` to redraw) |
| `docs/` | Screenshots |
| `memory/` | What HT has taught Claude about the game (`learnings.md` first) |
| `.claude/skills/pixel-art-studio/` | Pixel Art Studio skill (MIT), used by Claude to draw the sprites. Source in its `UPSTREAM.md` |
| `.claude/agents/pixel-art-reviewer.md` | Checks finished sprites against the skill's quality rules |
