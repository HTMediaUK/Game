"""Dan (HT's MD) as the main character: 32x32, facing right.

Draws a standing frame and a 6-frame run cycle. Fill pixels are painted first,
then a dark outline is added automatically around the whole silhouette. Run:

    python3 sprites/src/dan.py

It writes sprites/dan/dan_idle.json and sprites/dan/dan_run.json for
render.py and animate.py.
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
    # HT logo ring
    "r": "#e43b44", "Y": "#feae34", "N": "#63c74d", "P": "#b55088", "l": "#2f7fc1",
    # jeans (J = near leg, lit; j = far leg and shadow) and trainers
    "j": "#2c3a5c", "J": "#41558a",
    "f": "#2a2433", "F": "#d8dee9",
}

HEAD = {
    1:  (15, "3322"),               # swept-up quiff
    2:  (12, "333322222"),
    3:  (10, "3322222222"),
    4:  (10, "22222221KKk"),
    5:  (10, "2222221KKKKk"),
    6:  (10, "222k1kK11k11"),
    7:  (10, "22ks1kkoKkokk"),
    8:  (10, "21ks11kKkkKkk"),      # cheeks lift under the eyes
    9:  (10, "11s111k222221"),
    10: (11, "11222221ww12"),       # small grin
    11: (11, "11222222ss21"),       # lower lip
    12: (12, "1222222221"),
    13: (13, "11222211"),
    14: (14, "1111"),
}

# Legs from y=25 down to the ground (y=30), columns starting at x=6.
# Each run pose is drawn once with the near leg (J) as the stance leg;
# the other half of the cycle swaps the legs over.
LEGS = {
    "stand": [
        "......jjjj.JJJJ.....",
        "......jjjj.JJJJ.....",
        "......jjjj.JJJJ.....",
        "......jjjj.JJJJ.....",
        ".....fffff.ffffff...",
        ".....FFFFF.FFFFFF...",
    ],
    "contact": [                    # front foot lands, back foot leaves
        "....jjjj..JJJJJ.....",
        "...jjjj....JJJJ.....",
        "..jjjj......JJJJ....",
        ".ffff........JJJ....",
        ".FFF.........ffff...",
        ".............FFFFF..",
    ],
    "down": [                       # weight over the stance leg, back heel kicks up
        "...jjjjj..JJJJ......",
        ".jjjjj.....JJJ......",
        "ffjj.......JJJ......",
        "FF.........JJJ......",
        "..........ffff......",
        "..........FFFFF.....",
    ],
    "push": [                       # stance leg pushes off, other knee drives forward
        ".....JJJ...jjjjjj...",
        "....JJJ.......jjj...",
        "...JJJ........jjj...",
        "..JJJ.........ffff..",
        ".ffff.........FFFF..",
        ".FFF................",
    ],
}

# Near arm (his left, facing us) pixels as (x, y, colour), drawn over the torso.
ARMS = {
    "side": [(18, 18, "k"), (19, 18, "t"), (18, 19, "t"), (19, 19, "k"),
             (18, 20, "k"), (19, 20, "t"), (18, 21, "k"), (19, 21, "s")],
    "forward": [(20, 17, "k"), (21, 17, "t"), (22, 17, "t"), (20, 18, "s"),
                (21, 18, "k"), (22, 18, "t"), (23, 16, "k"), (23, 17, "k"),
                (24, 16, "k"), (24, 17, "s")],
    "back": [(16, 18, "k"), (17, 18, "t"), (15, 19, "t"), (16, 19, "k"),
             (13, 20, "k"), (14, 20, "t"), (11, 21, "k"), (12, 21, "k"),
             (11, 22, "s"), (12, 22, "s")],
}
# The far arm peeks out on the opposite swing.
FAR_ARM = {
    "forward": [(21, 19, "k"), (22, 19, "s")],
    "back": [(9, 19, "s"), (9, 20, "s")],
    "side": [],
}


def swap_legs(rows):
    table = str.maketrans("Jj", "jJ")
    return [r.translate(table) for r in rows]


def draw(legs, arm, bob=0, lean=0):
    grid = [["."] * W for _ in range(H)]

    def put(x, y, ch):
        if 0 <= x < W and 0 <= y < H:
            grid[y][x] = ch

    def row(y, x0, chars):
        for i, ch in enumerate(chars):
            if ch != ".":
                put(x0 + i, y, ch)

    def rect(x0, y0, x1, y1, ch):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                put(x, y, ch)

    # Legs, then hips
    for i, r in enumerate(legs):
        row(25 + i, 6, r)
    rect(11, 24, 19, 24, "j")
    rect(11, 24, 12, 24, "J")

    # Far arm sits behind the body
    far = {"forward": "back", "back": "forward", "side": "side"}[arm]
    for x, y, ch in FAR_ARM[far if arm != "side" else "side"]:
        put(x, y + bob, ch)

    # T-shirt torso (moves down with the bob)
    b = bob
    rect(11, 15 + b, 20, 23 + b, "b")
    row(14 + b, 11, "ccb")
    row(14 + b, 18, "bbb")
    rect(11, 15 + b, 12, 22 + b, "c")
    rect(18, 19 + b, 20, 22 + b, "a")
    row(23 + b, 11, "aaaaaaaaaa")
    row(16 + b, 14, "rYN")          # HT logo
    row(17 + b, 14, "PwN")
    row(18 + b, 14, "lPY")
    rect(17, 15 + b, 19, 17 + b, "b")  # sleeve
    row(17 + b, 17, "aaa")

    # Head
    for y, (x0, chars) in HEAD.items():
        row(y + b, x0 + lean, chars)
    put(23 + lean, 8 + b, "k")      # nose

    # Near arm on top
    for x, y, ch in ARMS[arm]:
        put(x, y + b, ch)

    # Automatic outline around the silhouette
    filled = {(x, y) for y in range(H) for x in range(W) if grid[y][x] != "."}
    for y in range(H):
        for x in range(W):
            if grid[y][x] == "." and any(
                (x + dx, y + dy) in filled for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))
            ):
                put(x, y, "o")
    # Keep the head and shoulders apart
    for x in (13, 18):
        if grid[14 + b][x] in "bc":
            put(x, 14 + b, "o")
    return grid


def to_pixels(grid):
    return [
        {"x": x, "y": y, "color": PALETTE[grid[y][x]]}
        for y in range(H) for x in range(W) if grid[y][x] != "."
    ]


def save(name, frames, tag):
    out = Path(__file__).resolve().parents[1] / "dan" / f"{name}.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    data = {
        "$schema": "pixel-art-studio/v1",
        "width": W, "height": H,
        "background": "transparent",
        "pixel_size": 1,
        "palette": sorted(set(PALETTE.values())),
    }
    if len(frames) == 1:
        data["pixels"] = to_pixels(frames[0])
    else:
        data["frames"] = [
            {"id": i, "duration_ms": 100, "pixels": to_pixels(g)} for i, g in enumerate(frames)
        ]
        data["tags"] = [{"name": tag, "from": 0, "to": len(frames) - 1, "direction": "forward"}]
    out.write_text(json.dumps(data, indent=1))
    print(f"wrote {out}")


idle = draw(LEGS["stand"], "side")

# 6-frame run at 10 fps: near leg stance (3 frames), then far leg stance (3 frames).
# Arms swing opposite to the legs; the body drops 1px on the "down" frames.
run = [
    draw(LEGS["contact"], "back", lean=1),
    draw(LEGS["down"], "side", bob=1, lean=1),
    draw(LEGS["push"], "forward", lean=1),
    draw(swap_legs(LEGS["contact"]), "forward", lean=1),
    draw(swap_legs(LEGS["down"]), "side", bob=1, lean=1),
    draw(swap_legs(LEGS["push"]), "back", lean=1),
]

if __name__ == "__main__":
    save("dan_idle", [idle], "idle")
    save("dan_run", run, "run")
    for g in run:
        print("\n".join("".join(r) for r in g[13:]), "\n")
