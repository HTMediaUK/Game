"""Dan in the chunky big-head style (style references supplied by HT, 20/11/2026).

Big blocky head, solid hair shape, 1x2 eyes, thick brows, small mouth,
flat skin with one shadow tone, heavy dark outline and a short body.
32x32, standing, face turned slightly to the right (the running direction).

    python3 sprites/src/dan_v2.py

Writes sprites/dan/dan_v2_idle.json for render.py.
"""
import json
from pathlib import Path

W = H = 32

PALETTE = {
    "o": "#120e17",                                   # outline
    "x": "#8a3f1f", "y": "#cf6a2c", "z": "#f29a4a",   # ginger hair
    "s": "#d08a68", "k": "#f2b48c", "K": "#ffcfa8",   # skin
    "m": "#c8605a",                                   # mouth
    "a": "#1c1a24", "b": "#2b2836", "c": "#3d3a4c",   # black HT tee
    "t": "#7d8296",                                   # tattoo sleeve ink
    "r": "#e43b44", "Y": "#feae34", "N": "#63c74d",   # HT logo ring
    "P": "#b55088", "l": "#2f7fc1", "w": "#f4f4f4",
    "j": "#2c3a5c", "J": "#41558a",                   # jeans
    "f": "#2a2433", "F": "#e4e8f0",                   # trainers
}

# (x start, row of pixels). "o" inside a row is a drawn line; "." is empty.
ROWS = {
    # head: hair block with a swept-up quiff
    0:  (15, "zzyyy"),
    1:  (11, "yyyzzzzyyyy"),
    2:  (10, "yyzzzzyyyyyyx"),
    3:  (9,  "yyyyyyyyyyyyyx"),
    4:  (9,  "yyyyyyyyyyyyyx"),
    5:  (9,  "yyyxKKKKKKKKyx"),
    6:  (9,  "yyxKKKKKKKKKk"),
    7:  (9,  "yxkKxxKKKxxKk"),   # thick brows
    8:  (9,  "kskKKoKKKKoKk"),   # ear, 1x2 eyes
    9:  (9,  "kskKKoKKKKoKk"),
    10: (9,  "skkKKKKKKsKKk"),   # nose shade
    11: (10, "kkKKKKmmmKKk"),    # small smile
    12: (11, "skkkkkkkkkk"),
    13: (12, "sskkkkkks"),       # jaw
    14: (14, "ssss"),            # neck
    # body: tee with sleeves, tattooed forearms at the sides
    15: (9,  "cbbbbbbbbbbbbb"),
    16: (8,  "ccbcbbbbbbbbbbaa"),
    17: (8,  "ccocbbbbrYNbboba"),  # HT logo on the chest
    18: (8,  "ttocbbbbPwNbbott"),
    19: (8,  "tkocbbbblPYbbotk"),
    20: (8,  "kkocbbbbbbbbbokk"),
    21: (8,  "ttocbbbbbbbbaott"),
    22: (8,  "kkocbbbbbbbbaokk"),  # hands
    23: (8,  "ssoaaaaaaaaaaoss"),
    # jeans and trainers
    24: (11, "JJjjjjjjjj"),
    25: (11, "JJjj..JJjj"),
    26: (11, "JJjj..JJjj"),
    27: (11, "JJjj..JJjj"),
    28: (11, "ffff..fffff"),
    29: (11, "FFFF..FFFFF"),
}


def draw(rows):
    grid = [["."] * W for _ in range(H)]
    for y, (x0, chars) in rows.items():
        for i, ch in enumerate(chars):
            if ch != ".":
                grid[y][x0 + i] = ch
    filled = {(x, y) for y in range(H) for x in range(W) if grid[y][x] != "."}
    for y in range(H):
        for x in range(W):
            if grid[y][x] == "." and any(
                (x + dx, y + dy) in filled for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))
            ):
                grid[y][x] = "o"
    return grid


# ---------------------------------------------------------------- poses
# Upper body without arms; arms are added per pose so they can swing.
HEAD = {y: v for y, v in ROWS.items() if y <= 14}
TORSO = {
    15: (10, "cbbbbbbbbbbb"),
    16: (10, "bcbbbbbbbbbb"),
    17: (11, "cbwbwbwwwb"),          # "HT" in white across the chest
    18: (11, "cbwwwbbwbb"),
    19: (11, "cbwbwbbwbb"),
    20: (11, "cbwbwbbwbb"),
    21: (11, "cbbbbbbbba"),
    22: (11, "cbbbbbbbba"),
    23: (11, "aaaaaaaaaa"),
}

# Arms as (x, y, colour). "S" is sleeve; it takes the shade of that side.
# Right-hand side of the picture is his front arm, left-hand side his back arm.
SLEEVE_R = [(22, 15, "S"), (22, 16, "S"), (23, 16, "S"), (22, 17, "S"), (23, 17, "S")]
SLEEVE_L = [(9, 15, "S"), (8, 16, "S"), (9, 16, "S"), (8, 17, "S"), (9, 17, "S")]
ARMS = {
    # hanging at the side, tattoo sleeve showing
    "R_down": SLEEVE_R + [(22, 18, "t"), (23, 18, "t"), (22, 19, "t"), (23, 19, "k"), (22, 20, "k"),
                          (23, 20, "k"), (22, 21, "t"), (23, 21, "t"), (22, 22, "k"), (23, 22, "k"),
                          (22, 23, "s"), (23, 23, "s")],
    "L_down": SLEEVE_L + [(8, 18, "t"), (9, 18, "t"), (8, 19, "k"), (9, 19, "t"), (8, 20, "k"),
                          (9, 20, "k"), (8, 21, "t"), (9, 21, "t"), (8, 22, "k"), (9, 22, "k"),
                          (8, 23, "s"), (9, 23, "s")],
    # running: front arm pumps forward with a fist at chest height
    "R_forward": SLEEVE_R + [(22, 18, "t"), (23, 18, "k"), (24, 18, "t"), (24, 17, "t"), (25, 17, "k"),
                             (25, 16, "t"), (26, 16, "k"), (26, 15, "k"), (27, 15, "k"), (27, 16, "s")],
    # running: back arm swings across the body
    "L_forward": SLEEVE_L + [(9, 18, "t"), (10, 18, "t"), (11, 18, "k"), (12, 18, "t"), (13, 18, "k"),
                             (14, 17, "k"), (14, 18, "k"), (10, 19, "s"), (11, 19, "k"), (12, 19, "t"),
                             (13, 19, "k"), (14, 19, "s")],
    # swung back and out
    "L_back": SLEEVE_L + [(8, 18, "t"), (7, 18, "t"), (7, 19, "k"), (6, 19, "t"), (6, 20, "k"),
                          (5, 20, "t"), (5, 21, "k"), (4, 21, "k"), (5, 22, "s"), (4, 22, "s")],
    "R_out": SLEEVE_R + [(23, 18, "t"), (24, 18, "t"), (24, 19, "k"), (25, 19, "t"), (25, 20, "k"),
                         (26, 20, "t"), (26, 21, "k"), (27, 21, "k"), (26, 22, "s"), (27, 22, "s")],
    # jumping: fist punched up in the air
    "R_up": [(22, 15, "S"), (22, 16, "S"), (23, 15, "S"), (23, 14, "S"), (24, 14, "S"),
             (23, 13, "t"), (24, 13, "t"), (23, 12, "k"), (24, 12, "t"), (24, 11, "t"), (25, 11, "k"),
             (24, 10, "k"), (25, 10, "k"), (24, 8, "k"), (25, 8, "k"), (24, 9, "k"), (25, 9, "s")],
}

# Leg poses replace rows 24-29 and stay put when the body bobs.
# Run poses have the near leg (J) forward; the other half of the cycle swaps them.
LEGS = {
    "stand": {y: v for y, v in ROWS.items() if y >= 24},
    "run_a": {24: (11, "JJjjjjjjjj"), 25: (9, "jjjj....JJJJ"), 26: (8, "jjjj......JJJJ"),
              27: (7, "ffff........JJJ"), 28: (7, "FFF.........ffff"), 29: (19, "FFFF")},
    "run_b": {24: (11, "JJjjjjjjjj"), 25: (9, "jjjj..JJJJ"), 26: (7, "ffjj....JJJJ"),
              27: (7, "FF......JJJJ"), 28: (15, "ffffff"), 29: (15, "FFFFFF")},
    "knee_up": {24: (11, "JJjjjjjjjj"), 25: (11, "jjj.JJJJJJ"), 26: (11, "jjj.JJJJJJ"),
                27: (11, "jjj.....JJ"), 28: (10, "ffff.....ffff"), 29: (10, "FFFF.....FFFF")},
}


def pose(legs, left, right, bob=0, swap=False):
    """Build a frame: legs fixed to the ground, upper body dropped by `bob` pixels."""
    rows = {}
    for y, (x0, chars) in {**HEAD, **TORSO}.items():
        rows[y + bob] = (x0, chars)
    for y, (x0, chars) in LEGS[legs].items():
        if y not in rows:
            rows[y] = (x0, chars.translate(str.maketrans("Jj", "jJ")) if swap else chars)
    grid = draw(rows)
    for arm, sleeve in ((left, "c"), (right, "b")):
        for x, y, ch in ARMS[arm]:
            grid[y + bob][x] = sleeve if ch == "S" else ch
    # re-run the outline so the arms get one too
    for y in range(H):
        for x in range(W):
            if grid[y][x] == "o":
                grid[y][x] = "."
    rows2 = {y: (0, "".join(grid[y])) for y in range(H)}
    return draw(rows2)


def save_png(grid, path):
    from PIL import Image
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for y in range(H):
        for x in range(W):
            ch = grid[y][x]
            if ch != ".":
                c = PALETTE[ch]
                im.putpixel((x, y), tuple(int(c[i:i + 2], 16) for i in (1, 3, 5)) + (255,))
    im.save(path)


if __name__ == "__main__":
    g = pose("stand", "L_down", "R_down")
    out = Path(__file__).resolve().parents[1] / "dan" / "dan_v2_idle.json"
    out.write_text(json.dumps({
        "$schema": "pixel-art-studio/v1",
        "width": W, "height": H, "background": "transparent", "pixel_size": 1,
        "palette": sorted(set(PALETTE.values())),
        "pixels": [{"x": x, "y": y, "color": PALETTE[g[y][x]]}
                   for y in range(H) for x in range(W) if g[y][x] != "."],
    }, indent=1))
    d = out.parent
    # 6-frame run: contact, dip, passing, then the same with the legs swapped.
    # Arms pump opposite to the legs.
    run = [
        pose("run_a", "L_back", "R_forward"),
        pose("run_a", "L_back", "R_forward", bob=1),
        pose("run_b", "L_down", "R_down"),
        pose("run_a", "L_forward", "R_down", swap=True),
        pose("run_a", "L_forward", "R_down", bob=1, swap=True),
        pose("run_b", "L_down", "R_down", swap=True),
    ]
    for old in d.glob("dan_v2_run_*.png"):
        old.unlink()
    for i, g2 in enumerate(run):
        save_png(g2, d / f"dan_v2_run_{i}.png")
    save_png(pose("knee_up", "L_back", "R_up"), d / "dan_v2_jump_up.png")     # fist in the air
    save_png(pose("stand", "L_back", "R_out"), d / "dan_v2_jump_down.png")    # arms out, coming down
    save_png(pose("stand", "L_down", "R_down", bob=1), d / "dan_v2_land.png") # squash on landing
    save_png(pose("stand", "L_down", "R_down"), d / "dan_v2_stand.png")
    print(f"wrote {out} and run/jump frames")
