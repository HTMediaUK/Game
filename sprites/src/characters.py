"""The HT team as playable runners, in the same style and poses as Dan.

Each character swaps Dan's head, torso, legs and colours; the arms, run cycle,
jump and landing poses come from dan_v2.py so everyone moves the same way.

    python3 sprites/src/characters.py

Writes sprites/characters/<id>/{stand,run_0..5,jump_up,jump_down,land}.png
plus a line-up preview.
"""
import sys
from pathlib import Path
from PIL import Image

sys.path.insert(0, str(Path(__file__).parent))
import dan_v2 as d  # noqa: E402

OUT = Path(__file__).resolve().parents[1] / "characters"
BASE_PALETTE = dict(d.PALETTE)
BASE_HEAD = dict(d.HEAD)
BASE_TORSO = dict(d.TORSO)
BASE_LEGS = {k: dict(v) for k, v in d.LEGS.items()}

EXTRA = {                                   # colours the team need beyond Dan's
    "B": "#c27840", "V": "#8e5028",         # beard
    "g": "#b8893a",                         # gold necklace
    "p": "#f0a090",                         # rosy cheeks
    "q": "#efe2d0", "Q": "#6e3a2c", "R": "#a87a68",   # gingham
    "O": "#3a2e30", "L": "#e6f2f8",         # glasses rims and lens glint
    "h": "#c8ccd6",                         # silver: earring, nose ring
    "e": "#cf6e3a", "E": "#a8521f", "X": "#7c3a16",   # rust corduroy
    "u": "#bccaee", "U": "#93a2cf", "W": "#f2f4fb",   # blue striped shirt
}
SKIN_ARMS = {"t": "#f2b48c"}                # no tattoo sleeves except Dan's


def gingham(x, y):
    sx, sy = (x // 2) % 2, (y // 2) % 2
    return "Q" if sx and sy else "R" if sx or sy else "q"


def row_of(x0, x1, y, fn):
    return (x0, "".join(fn(x, y) for x in range(x0, x1 + 1)))


# ---------------------------------------------------------------- Beth
BETH_HEAD = {
    0:  (13, "zxzxzxz"),            # braided crown
    1:  (11, "yyzyyyxyyzyy"),       # centre parting
    2:  (10, "zxzyyyxyyyzxz"),
    3:  (9,  "zxyyyyyxyyyyxz"),
    4:  (9,  "zyyyyyyxyyyyyz"),
    5:  (9,  "yyyyKKKKKKKyyy"),
    6:  (9,  "yyyKKKKKKKKKyy"),
    7:  (9,  "yzKKKxKKKKxKzy"),     # waves framing the face, fine arched brows
    8:  (9,  "zyKKooKKKKooyz"),     # eyes with lashes
    9:  (9,  "yzKKKoKKKKoKzy"),
    10: (9,  "zykKpKKKKsKpyz"),     # rosy cheeks
    11: (9,  "yzkKKKKmmKKkzy"),     # small pink lips
    12: (9,  "zyyskkkkkksyyz"),
    13: (9,  "yzz.skkkks.zzy"),
    14: (9,  "zyy..ssss..yyz"),     # long hair falling past the jaw
}
BETH_TORSO = {
    15: (10, "zybbbbbbbbyz"),       # hair falling in front of her shoulders
    16: (10, "yzbbbgbbgbzy"),       # gold chain
    17: (11, "zybbggbbyz"),         # pendant, curl ends
    18: (11, "cbbbbbbbbb"),
    19: (11, "cbbbbbbbba"),
    20: (12, "bbbbbbbb"),           # fitted at the waist
    21: (11, "QQQQQQQQQQ"),         # high-waisted skirt with an elastic band
    22: row_of(11, 20, 22, gingham),
    23: row_of(10, 21, 23, gingham),
}
SKIRT = {24: (11, 20), 25: (10, 21), 26: (10, 21), 27: (9, 22), 28: (9, 22)}
BETH_LEGS = {
    "stand":   {**{y: row_of(a, b, y, gingham) for y, (a, b) in SKIRT.items()},
                29: (10, "ffff..ffff")},
    "run_a":   {**{y: row_of(a - (1 if y >= 27 else 0), b, y, gingham) for y, (a, b) in SKIRT.items()},
                29: (8, "fff.......fff")},          # hem swings back, feet apart
    "run_b":   {**{y: row_of(a, b, y, gingham) for y, (a, b) in SKIRT.items()},
                29: (12, "fff.fff")},               # feet together
    "knee_up": {**{y: row_of(a, b, y, gingham) for y, (a, b) in SKIRT.items() if y <= 27},
                28: (10, "fff....fff")},            # feet tucked up in the air
}

# ---------------------------------------------------------------- Sam
SAM_HEAD = {
    0:  (13, "zzzyy"),
    1:  (10, "zzzzyyyyyyy"),
    2:  (9,  "zzyyyyyyyyyyx"),
    3:  (9,  "yyyyyyyyyyyyyx"),
    4:  (9,  "yyyyyyyyyyyyyx"),
    5:  (9,  "yyyyyyyyyyyKKx"),     # fringe swept across
    6:  (9,  "yyyKKyyyyKKKKy"),
    7:  (9,  "yyKKxxKKKxxKyy"),
    8:  (9,  "yykKKoKKKKoKyy"),
    9:  (9,  "yykKKoKKKKoKyy"),
    10: (9,  "yykKKKKKKshKyy"),     # nose ring
    11: (9,  "yykBBBBmmmBkyy"),     # moustache, slight smile
    12: (10, "yBBBBBBBBBBy"),       # short beard along the jaw
    13: (12, "VBBBBBBV"),
    14: (14, "ssss"),
}

# ---------------------------------------------------------------- Jonas
JONAS_HEAD = {
    0:  (12, "zy.yz.zy"),           # spiky top
    1:  (11, "yzyyzyyzyy"),
    2:  (10, "yyyyyyyyyyyx"),
    3:  (10, "yyyyyyyyyyyx"),
    4:  (9,  "xyyyyyyyyyyyyx"),
    5:  (9,  "xyKKKKKKKKKKyx"),     # short sides
    6:  (9,  "xKKKxxKKKxxKKx"),     # brows
    7:  (9,  "kKKKOOKKKOOKKk"),     # round glasses
    8:  (9,  "kOOOLKOOOLKOOk"),     # lenses with a glint, arms back to the ears
    9:  (9,  "skKOKoOKOKoOKs"),     # eyes inside the lenses
    10: (9,  "kKKKOOKsKOOKKh"),     # earring
    11: (10, "kkKKKKmmmKKk"),
    12: (11, "skkkBBBBkkk"),        # goatee
    13: (12, "sskBBBBks"),
    14: (14, "ssss"),
}
JONAS_TORSO = {
    15: (10, "eeeeaaaaEEEE"),       # open rust corduroy shirt over a black tee
    16: (10, "eEeeaaaaeEEE"),
    **{y: (11, "eEeaaaaEeX") for y in range(17, 23)},
    23: (11, "XXXaaaaXXX"),
}

# ---------------------------------------------------------------- Mark
MARK_HEAD = {
    0:  (12, "zzzyyy"),
    1:  (10, "zzzzyyyyyyy"),
    2:  (9,  "zzyyyyyyyyyyx"),
    3:  (9,  "yyyyyyyyyyyyyx"),
    4:  (9,  "yyyyyyyyyyyyxx"),
    5:  (9,  "yyxKKKKKKKKKKx"),
    6:  (9,  "yxKKKKKKKKKKKk"),
    7:  (9,  "yxkKxxKKKxxKk"),
    8:  (9,  "kskKKoKKKKoKk"),
    9:  (9,  "kskKKoKKKKoKk"),
    10: (9,  "skBKKKKKKsKBB"),      # beard starts at the sideburns
    11: (10, "kBBBBBmmmBBB"),       # trimmed ginger beard, straight mouth
    12: (11, "BBBBBBBBBBB"),
    13: (12, "VBBBBBBBV"),          # shaped at the chin
    14: (14, "ssss"),
}


def mark_shirt(x, y):
    if x == 16:
        return "W" if y in (18, 21) else "U"        # button placket
    if x % 3 == 0:
        return "W"                                  # white stripe
    return "U" if x >= 19 else "u"


MARK_TORSO = {
    15: (10, "uuuWkkkkWuuu"),       # open collar
    16: (10, "uuuuWkkWuuuu"),
    **{y: row_of(11, 20, y, mark_shirt) for y in range(17, 23)},
    23: (11, "UUUUUUUUUU"),
}

CHARACTERS = {
    "dan":   {"name": "Dan", "role": "Managing Director"},
    "mark":  {"name": "Mark", "role": "Creative Director", "head": MARK_HEAD, "torso": MARK_TORSO,
              "palette": {"x": "#7e4526", "y": "#b06a3c", "z": "#d9925a", "m": "#a65a4a",
                          "c": "#c9d4f2", "b": "#a8b6e0", "j": "#2c3550", "J": "#3e4a6c", **SKIN_ARMS}},
    "beth":  {"name": "Beth", "role": "Operations & Creative Coordinator", "head": BETH_HEAD,
              "torso": BETH_TORSO, "legs": BETH_LEGS,
              "palette": {"x": "#a8803e", "y": "#dcb468", "z": "#f4dc96", "m": "#e06a82", **SKIN_ARMS}},
    "sam":   {"name": "Sam", "role": "Editor", "head": SAM_HEAD,
              "palette": {"x": "#3e2416", "y": "#5e3a24", "z": "#8a5a38",
                          "B": "#7a4e34", "V": "#5a3624", **SKIN_ARMS}},
    "jonas": {"name": "Jonas", "role": "Creative Producer", "head": JONAS_HEAD, "torso": JONAS_TORSO,
              "palette": {"x": "#241914", "y": "#3e2c24", "z": "#6a4c3c",
                          "c": "#cf6e3a", "b": "#a8521f", "j": "#2a2a32", "J": "#3c3c48", **SKIN_ARMS}},
}


def frames_for(cid):
    c = CHARACTERS[cid]
    d.PALETTE = {**BASE_PALETTE, **EXTRA, **c.get("palette", {})}
    d.HEAD = c.get("head", BASE_HEAD)
    d.TORSO = c.get("torso", BASE_TORSO)
    d.LEGS = {**{k: dict(v) for k, v in BASE_LEGS.items()}, **c.get("legs", {})}
    p = d.pose
    return {
        "run_0": p("run_a", "L_back", "R_forward"),
        "run_1": p("run_a", "L_back", "R_forward", bob=1),
        "run_2": p("run_b", "L_down", "R_down"),
        "run_3": p("run_a", "L_forward", "R_down", swap=True),
        "run_4": p("run_a", "L_forward", "R_down", bob=1, swap=True),
        "run_5": p("run_b", "L_down", "R_down", swap=True),
        "jump_up": p("knee_up", "L_back", "R_up"),
        "jump_down": p("stand", "L_back", "R_out"),
        "land": p("stand", "L_down", "R_down", bob=1),
        "stand": p("stand", "L_down", "R_down"),
    }


def main():
    lineup = []
    for cid in CHARACTERS:
        folder = OUT / cid
        folder.mkdir(parents=True, exist_ok=True)
        for name, grid in frames_for(cid).items():
            d.save_png(grid, folder / f"{name}.png")
        lineup.append(Image.open(folder / "stand.png").convert("RGBA"))
    sheet = Image.new("RGBA", (len(lineup) * 40, 34), (236, 230, 214, 255))
    for i, im in enumerate(lineup):
        sheet.alpha_composite(im, (i * 40 + 4, 1))
    sheet.resize((sheet.width * 5, sheet.height * 5), Image.NEAREST).save(OUT / "lineup.png")
    print(f"wrote {len(CHARACTERS)} characters to {OUT}")


if __name__ == "__main__":
    main()
