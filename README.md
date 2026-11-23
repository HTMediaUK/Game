# HT Dash: HT's expo game

A simple pixel art running game for HT Media's trade show stand. Dan runs through the British countryside, a port and a Scottish canal, jumping over camera kit, cows and sheep, dodging seagulls and drones, and grabbing pies for super jumps. It runs in a web browser, needs no internet once loaded, and nothing to install.

**Play it online:** https://htmediauk.github.io/Game/ (once GitHub Pages is switched on, see below)

## Play it from GitHub (any computer, iPad or phone)

To turn this repo into a web address, a repo admin does this once:

1. **Settings → General → Danger zone → Change visibility → Public.** (GitHub Pages is free for public repos.)
2. **Settings → Pages → Build and deployment:** Source **Deploy from a branch**, Branch **main**, folder **/ (root)**, then **Save**.
3. Wait a minute or two. The game is then at **https://htmediauk.github.io/Game/**. Every change merged into `main` goes live a minute or so later.

## Play it on an iPad

1. Open **https://htmediauk.github.io/Game/** in **Safari** (with Wi-Fi, the first time).
2. Tap **Share → Add to Home Screen**. Open it from the new **HT Dash** icon: it runs full screen like an app and keeps working with no internet.
3. For the stand, turn on **Guided Access** (Settings → Accessibility → Guided Access) so visitors can't leave the game.

On a touchscreen: **swipe or tap a face** to choose a runner, tap **PLAY**, **tap to jump** (hold for a big jump), tap the boxes to type a name and email, then tap **SAVE**. Staff: **hold the HT logo for 3 seconds** for settings.

Entries are saved on the iPad itself. The automatic Notepad backup only works on a computer (Chrome or Edge), so on an iPad use **Settings → Download all entries** at the end of each day; it saves a spreadsheet to the Files app. The iPad and the laptop keep separate scoreboards and entries.

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
| Ctrl+Alt+S | Settings (staff, from the title screen): save location, download entries, reset high scores |
| Ctrl+Alt+B | Choose (or reconnect) the Notepad backup file |
| Ctrl+Alt+E | Download every entry (name, work email, score, runner, date, time) as a spreadsheet (CSV) |

## The runners

Dan (Managing Director) is the default. Use the left and right arrows on the title screen to play as Dave (Production Director), Mark (Creative Director), Beth (Operations & Creative Coordinator), Sam (Editor) or Jonas (Creative Producer) instead. After each run it goes back to Dan. Everyone runs, jumps and wears the cape the same way. The artwork is in `sprites/characters/`, drawn by `sprites/src/characters.py`.

## Getting harder

Every run gets harder with time, so nobody plays for much more than a minute:

| From | What changes |
|---|---|
| Start | Tripods, flight cases and sheep at a gentle pace |
| 8 to 20 seconds | Cows, stacked cases and the roadworks barrier join in |
| 8 seconds | Cows join in: Friesian, Hereford, Belted Galloway, Jersey and Highland |
| 15 seconds | You run from the fields into a port: the quay arrives under your feet past a signpost, the hills slope into the sea, then the container ship, crane, tug and offshore wind farm come into view. Sheep and cows give way to mooring bollards and shipping containers |
| 15 to 18 seconds | Low seagulls and drones: jump over them (drones bob up and down) |
| 22 to 28 seconds | High seagulls and drones: don't jump, or just tap for a small hop underneath |
| 25 seconds | Pairs of obstacles close together: one long, held jump clears both |
| 40 seconds | No more pies |
| 30 seconds | The port gives way to a Scottish canal: Highland hills with snow on the tops, canal boats, a stone humpback bridge, lock gates, a lock-keeper's cottage and a gravel towpath. Highland cows, sheep and bollards to jump |
| 50 seconds | The speed keeps climbing until you crash |

Faint wind streaks start rushing past as the speed picks up. Seagulls and drones glow so they're easy to spot.

## HT colours

- The HT logo sits in the title panel, drawn smoothly rather than as pixels, and the select screen is a big HT ring with the team's faces round it.
- Each runner has their own colour from the logo ring: Dan orange, Dave mint, Mark lime, Beth magenta, Sam teal, Jonas mustard. It's used for their glow and label on the select screen, the game over card, and their name on the high scores.
- Panels have a border made of the logo's colour segments.
- The pie power timer is a mini HT ring whose segments switch off as the power runs out.

The speed rises the whole time and the gaps between obstacles shrink.

## Settings (for staff)

On the title screen press **Ctrl+Alt+S**. Up/Down to move, Enter to select, Esc to close.

- **Save location:** shows the Notepad backup file and whether it's on; Enter to choose it (or allow it again after a refresh).
- **Download all entries:** a spreadsheet of every name, email and score.
- **Reset high scores:** press Enter twice to confirm. Only the scoreboard is cleared; names and emails already saved are kept.

## Lives and game stats

Everyone gets **3 lives** (hearts, top left). Hit something and you lose one, flash for a second and a half, and keep running. The third hit ends the run. Change `LIVES` in `index.html` for more or fewer.

Each runner has two made-up game stats out of 5, shown as bars on the intro screen. **Speed** makes the world move faster (more points, less time to react) and **Jump** makes them jump higher (clears tall things, but you can land on the next obstacle). Each pair adds up to 6, so nobody is simply better:

| Runner | Speed | Jump |
|---|---|---|
| Dan | 3 | 3 |
| Dave | 2 | 4 |
| Mark | 4 | 2 |
| Beth | 3 | 3 |
| Sam | 1 | 5 |
| Jonas | 3 | 3 |

## Stepping on obstacles

Land on top of anything (camera kit, animals, containers, even a seagull) and you bounce off it and score **+5**, once per obstacle. Each +5 pops up in the next colour from the HT logo. Hitting the side still ends the run.

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

### Automatic Notepad backup

At the start of each day, press **Ctrl+Alt+B** on the title screen and choose where to save `HT-Dash-entries.txt`. A OneDrive or Google Drive folder is best, so it's copied online too; a USB stick works as well. After every entry the game rewrites that file with every entry so far, one line each:

```
23/11/2026  15:24  |  DAN  |  dan@example.co.uk  |  27
```

A small line at the bottom right of the title screen shows whether the backup is **on** (green, with the number of entries and the time it last saved) or needs attention (amber). After a refresh or restart Chrome may need you to press **Ctrl+Alt+B** once to allow it again; the status line says when. It works in Chrome and Edge, from the game file on the laptop (not from the web link).

## High scores

When Dan crashes, a film clapperboard drops in and snaps shut, showing the score, today's take number (which go this is today) and the date. The player types their name on the DIRECTOR line and presses Enter.


The top 10 are saved in Chrome on that laptop, so they survive closing the game and restarting the laptop. They are only on that one laptop and that one browser. Clearing Chrome's browsing data deletes them. If nobody types a name within a minute, the game goes back to the title screen without saving.

## What's here

| Path | What it is |
|---|---|
| `index.html` | The whole game |
| `sw.js`, `manifest.webmanifest` | Let it work offline and install to an iPad's home screen when hosted |
| `tools/make_icon.py` | Draws the home-screen icon (`sprites/ui/app_icon.png`) |
| `sprites/ui/` | Pixel versions of the HT logo, used in the mockups (the game draws the logo smoothly in code) |
| `sprites/src/port.py` | Draws the port: sea, wind farm, container ship, crane, tug and quayside |
| `sprites/src/canal.py` | Draws the Scottish canal: Highland hills, canal, boats, bridge, lock, cottage and towpath |
| `sprites/mockups/` | Ideas not in the game: Dan's 3D spin, three select screen designs |
| `dist/HT-Dash.html` | The same game packed into one file to send to people |
| `tools/build_single_file.py` | Rebuilds `dist/HT-Dash.html` |
| `sprites/` | All the artwork as PNGs |
| `sprites/src/` | Python scripts that draw the artwork (`python3 sprites/src/<name>.py` to redraw) |
| `docs/` | Screenshots |
| `memory/` | What HT has taught Claude about the game (`learnings.md` first) |
| `.claude/skills/pixel-art-studio/` | Pixel Art Studio skill (MIT), used by Claude to draw the sprites. Source in its `UPSTREAM.md` |
| `.claude/agents/pixel-art-reviewer.md` | Checks finished sprites against the skill's quality rules |
