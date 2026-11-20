# Dan's Dash: HT's expo game

A simple pixel art running game for HT Media's trade show stand. Dan runs through the British countryside with his drone overhead, jumping over camera kit, cows and sheep, and grabbing pies for super jumps. It runs in a web browser, needs no internet and nothing to install.

## How to play it on the stand laptop

1. Copy this whole folder onto the laptop (or a USB stick).
2. Double-click `index.html`. It opens in Chrome.
3. Press **F** (or F11) for full screen.

For a locked-down kiosk, make a desktop shortcut that runs:

```
chrome --kiosk "C:\path\to\Game\index.html"
```

Alt+F4 closes it.

## Controls

| Key | What it does |
|---|---|
| Space, Up arrow or click | Start, and jump. Hold for a higher jump |
| Type, then Enter | Add your name to the high scores at the end of a run |
| F | Full screen on or off |
| Ctrl+Alt+R | Clear the high score table (asks first) |

## Pie power

Every so often a pie floats past at jump height. Grab it and Dan jumps twice as high for 10 seconds (the timer is at the top of the screen). While powered up he bounces off anything he lands on.

## Client cameos

The hills feature some of HT's clients as generic buildings, with no names or logos: a hospital (Newcastle Hospitals), cows grazing in the fields (ARN), an old pit headframe and winding house (Mining Remediation Authority) and a small white plane in the sky (HII project).

## High scores

The top 10 are saved in Chrome on that laptop, so they survive closing the game and restarting the laptop. They are only on that one laptop and that one browser. Clearing Chrome's browsing data deletes them. If nobody types a name within a minute, the game goes back to the title screen without saving.

## What's here

| Path | What it is |
|---|---|
| `index.html` | The whole game |
| `sprites/` | All the artwork as PNGs |
| `sprites/src/` | Python scripts that draw the artwork (`python3 sprites/src/<name>.py` to redraw) |
| `docs/` | Screenshots |
| `.claude/skills/pixel-art-studio/` | Pixel Art Studio skill (MIT), used by Claude to draw the sprites. Source in its `UPSTREAM.md` |
| `.claude/agents/pixel-art-reviewer.md` | Checks finished sprites against the skill's quality rules |
