"""Dan (HT's MD) as the main character: 32x32, facing right, holding a camera.

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
    8:  (10, "21ks11kkkkkkk"),
    9:  (10, "11s111k222221"),
    10: (11, "1122221wwww2"),
    11: (11, "112222222221"),
    12: (12, "1222222221"),
    13: (13, "11222211"),
    14: (14, "1111"),
}
for y, (x0, chars) in head.items():
    row(y, x0, chars)
put(23, 8, "k")                    # nose

# --- Front arm: sleeve, tattooed forearm, hand under the camera ---
rect(17, 15, 19, 17, "b")          # sleeve
row(17, 17, "aaa")
row(19, 17, "kttkkttkk")           # forearm with sleeve tattoo
row(20, 17, "sttkksttk")
row(18, 26, "kk")                  # front hand cupping the lens
row(19, 26, "kk")
row(20, 26, "ks")
row(16, 20, "k")                   # back hand on the camera body
row(17, 20, "s")

# --- Camera, held at chest height, lens forward ---
rect(21, 14, 25, 18, "g")          # camera body
row(14, 21, "GGGGG")               # top edge catches the light
rect(21, 15, 21, 18, "G")
row(13, 22, "hGG")                 # viewfinder bump
put(22, 15, "r")                   # red recording light
rect(26, 14, 28, 17, "G")          # big round lens
row(14, 26, "hhh")
put(26, 17, "g")
rect(29, 15, 29, 16, "l")          # glass
put(29, 15, "L")                   # glint

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
for x in range(17, 26):
    if grid[18][x] in "ab":
        put(x, 18, "a")

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
