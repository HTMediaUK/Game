"""HT drone that hovers above Dan: 24x10, side view facing right, 2 frames.

The two frames swap the propeller blur so the rotors look like they spin.
Run:

    python3 sprites/src/drone.py

It writes sprites/drone/drone.json (both frames) for render.py and animate.py.
"""
import json
from pathlib import Path

W, H = 24, 10

PALETTE = {
    "o": "#120e17",  # outline
    "W": "#eef1f7", "h": "#b9c0d4", "G": "#7b8299", "g": "#3e4255",  # body
    "p": "#cfd6e6",  # propeller blur
    "l": "#2f7fc1", "L": "#8fd3ff",  # gimbal camera glass
    "r": "#e43b44", "N": "#63c74d",  # nav lights: red front, green back
}


def draw(props):
    grid = [["."] * W for _ in range(H)]

    def row(y, x0, chars):
        for i, ch in enumerate(chars):
            if ch != ".":
                grid[y][x0 + i] = ch

    row(5, 8, "WWWWWWWW")    # body top, lit
    row(6, 7, "hWWWWWWhhh")
    row(7, 8, "GGhhhhGG")    # body underside
    row(5, 3, "gGGGG")       # back arm
    row(5, 16, "GGGGg")      # front arm
    row(4, 3, "gg")          # back motor
    row(4, 19, "gg")         # front motor
    row(6, 3, "N")           # green light at the back
    row(6, 20, "r")          # red light at the front
    row(8, 11, "gl")         # gimbal camera under the body
    row(8, 13, "L")
    row(3, 3, "gg")          # rotor hubs
    row(3, 19, "gg")
    for x0, chars in props:  # propeller blur
        row(2, x0, chars)

    # Automatic outline around the silhouette
    filled = {(x, y) for y in range(H) for x in range(W) if grid[y][x] != "."}
    for y in range(H):
        for x in range(W):
            if grid[y][x] == "." and any(
                (x + dx, y + dy) in filled for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))
            ):
                grid[y][x] = "o"
    return grid


frames = [
    draw([(0, "ppppppp"), (16, "ppppppp")]),   # blades side-on: wide blur
    draw([(2, "ppp"), (18, "ppp")]),           # blades end-on: short blur
]

out = Path(__file__).resolve().parents[1] / "drone" / "drone.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps({
    "$schema": "pixel-art-studio/v1",
    "width": W, "height": H,
    "background": "transparent",
    "pixel_size": 1,
    "palette": sorted(set(PALETTE.values())),
    "frames": [
        {"id": i, "duration_ms": 60, "pixels": [
            {"x": x, "y": y, "color": PALETTE[g[y][x]]}
            for y in range(H) for x in range(W) if g[y][x] != "."
        ]}
        for i, g in enumerate(frames)
    ],
    "tags": [{"name": "hover", "from": 0, "to": 1, "direction": "forward"}],
}, indent=1))
for g in frames:
    print("\n".join("".join(r) for r in g), "\n")
print(f"wrote {out}")
