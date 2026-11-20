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


if __name__ == "__main__":
    g = draw(ROWS)
    out = Path(__file__).resolve().parents[1] / "dan" / "dan_v2_idle.json"
    out.write_text(json.dumps({
        "$schema": "pixel-art-studio/v1",
        "width": W, "height": H, "background": "transparent", "pixel_size": 1,
        "palette": sorted(set(PALETTE.values())),
        "pixels": [{"x": x, "y": y, "color": PALETTE[g[y][x]]}
                   for y in range(H) for x in range(W) if g[y][x] != "."],
    }, indent=1))
    print("\n".join("".join(r) for r in g))
    print(f"wrote {out}")
