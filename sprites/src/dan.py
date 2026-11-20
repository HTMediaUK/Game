"""Dan (HT's MD) as the main character: 32x32, facing right, holding a drone controller.

Drawn as a character grid. Fill pixels are painted first, then a dark outline
is added automatically around the whole silhouette. Run:

    python3 sprites/src/dan.py

It writes sprites/dan/dan_idle.json, which render.py turns into a PNG.
"""
import json
from pathlib import Path

W = H = 32

PALETTE = {
    "o": "#120e17",  # outline (darker than anything in the sprite)
    # ginger hair and beard: shadows cooler, highlights warmer
    "1": "#7a3424", "2": "#c4612b", "3": "#f09a45",
    # skin
    "s": "#b8705a", "k": "#eaa883", "K": "#ffd3ad",
    # black HT t-shirt
    "a": "#211e2b", "b": "#302c3f", "c": "#46425a",
    # tattoo sleeve ink on skin
    "t": "#6a6f86",
    "w": "#f4f4f4",  # teeth, logo centre
    # camera
    "g": "#3a3d4e", "G": "#727892", "h": "#a9b0c8",
    "l": "#2f7fc1", "L": "#8fd3ff", "r": "#e43b44",
    # HT logo ring
    "Y": "#feae34", "N": "#63c74d", "P": "#b55088",
    # jeans and trainers
    "j": "#2c3a5c", "J": "#41558a",
    "f": "#2a2433", "F": "#d8dee9",
}

grid = [["."] * W for _ in range(H)]


def put(x, y, ch):
    grid[y][x] = ch


def row(y, x0, chars):
    for i, ch in enumerate(chars):
        if ch != ".":
            put(x0 + i, y, ch)


def rect(x0, y0, x1, y1, ch):
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            put(x, y, ch)


# --- Legs and trainers (drawn first so the body sits on top) ---
rect(11, 24, 19, 26, "j")          # hips
rect(11, 24, 12, 26, "J")          # light from top-left
rect(11, 27, 14, 28, "j")          # back leg
rect(16, 27, 19, 28, "j")          # front leg
rect(16, 27, 16, 28, "J")
rect(11, 29, 14, 29, "f")          # back trainer
rect(16, 29, 21, 29, "f")          # front trainer, toe points right
rect(11, 30, 14, 30, "F")          # soles
rect(16, 30, 21, 30, "F")

# --- T-shirt torso ---
rect(11, 15, 20, 23, "b")
row(14, 11, "ccb")                 # back shoulder
row(14, 18, "bbb")                 # front shoulder
rect(11, 15, 12, 22, "c")          # lit side
rect(18, 19, 20, 22, "a")          # shadow side
row(23, 11, "aaaaaaaaaa")          # hem
# HT logo: rainbow ring with a white centre, on the chest
row(16, 14, "rYN")
row(17, 14, "PwN")
row(18, 14, "lPY")

# --- Head (hair, face, beard) ---
head = {
    1:  (15, "3322"),               # swept-up quiff
    2:  (12, "333322222"),
    3:  (10, "3322222222"),
    4:  (10, "22222221KKk"),
    5:  (10, "2222221KKKKk"),
    6:  (10, "222k1kK11k11"),
    7:  (10, "22ks1kkoKkokk"),
    8:  (10, "21ks11kKkkKkk"),   # cheeks lift under the eyes
    9:  (10, "11s111k222221"),
    10: (11, "11222221ww12"),    # small grin
    11: (11, "11222222ss21"),    # lower lip

    12: (12, "1222222221"),
    13: (13, "11222211"),
    14: (14, "1111"),
}
for y, (x0, chars) in head.items():
    row(y, x0, chars)
put(23, 8, "k")                    # nose

# --- Arms: tattooed forearm, both hands on a drone controller ---
rect(17, 15, 19, 17, "b")          # sleeve
row(17, 17, "aaa")
row(18, 17, "kttk")                # forearm with sleeve tattoo
row(19, 17, "sttkk")
row(17, 21, "k")                   # back hand
row(18, 21, "kk")                  # front hand
row(19, 22, "s")

# --- Drone controller, held at chest height ---
rect(22, 16, 27, 18, "g")
row(16, 22, "GhGGhG")              # top face with the two sticks
put(25, 17, "r")                   # status light

# --- Automatic outline around the silhouette ---
filled = {(x, y) for y in range(H) for x in range(W) if grid[y][x] != "."}
for y in range(H):
    for x in range(W):
        if grid[y][x] == "." and any(
            (x + dx, y + dy) in filled for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))
        ):
            put(x, y, "o")

# Inner separation lines so parts don't merge
for x, y in [(13, 14), (18, 14), (16, 27), (15, 28), (15, 29), (15, 30)]:
    if grid[y][x] not in "kK":
        put(x, y, "o")


pixels = [
    {"x": x, "y": y, "color": PALETTE[grid[y][x]]}
    for y in range(H)
    for x in range(W)
    if grid[y][x] != "."
]

out = Path(__file__).resolve().parents[1] / "dan" / "dan_idle.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps({
    "$schema": "pixel-art-studio/v1",
    "width": W, "height": H,
    "background": "transparent",
    "pixel_size": 1,
    "palette": sorted(set(PALETTE.values())),
    "pixels": pixels,
}, indent=1))
print("\n".join("".join(r) for r in grid))
print(f"wrote {out}")
