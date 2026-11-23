"""The port: where the run goes after 15 seconds.

Layers match the countryside ones (320x180, tile left to right):
    port_far_N.png   sea to the horizon, an offshore wind farm (4 frames: blades turn),
                     a ship far out
    port_mid.png     a big container ship (containers in HT colours), a dockside
                     crane and a tug, on the water
    port_ground.png  the quayside: a hazard-striped edge and concrete

    python3 sprites/src/port.py
"""
import math
import random
import sys
from pathlib import Path
from PIL import Image

sys.path.insert(0, str(Path(__file__).parent))
import backdrop as bd  # noqa: E402
import ht_logo  # noqa: E402

W, H, GROUND_Y = bd.W, bd.H, bd.GROUND_Y
OUT = bd.OUT
hexc = bd.hexc
HT = [hexc(c) for c in ht_logo.HT_COLOURS]


def rect(img, x0, y0, x1, y1, col):
    for y in range(max(0, y0), min(H, y1 + 1)):
        for x in range(x0, x1 + 1):
            img.putpixel((x % W, y), col)


# ---------------------------------------------------------------- far: sea and wind farm
HORIZON = 100


def port_far(frame):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    bands = [(HORIZON, "#a9d8ec"), (HORIZON + 3, "#7fbfe0"), (HORIZON + 9, "#5ba6d2"), (HORIZON + 20, "#4590c2")]
    for x in range(W):
        for i, (y0, c) in enumerate(bands):
            y1 = bands[i + 1][0] if i + 1 < len(bands) else H
            for y in range(y0, y1):
                img.putpixel((x, y), hexc(c))
    rng = random.Random(5)
    for _ in range(60):                                    # glints on the water
        x, y = rng.randrange(W), rng.randrange(HORIZON + 4, H)
        for dx in range(rng.choice((2, 3))):
            img.putpixel(((x + dx) % W, y), hexc("#d8f0fa"))
    # a ship far out on the horizon
    rect(img, 196, HORIZON - 3, 222, HORIZON - 1, hexc("#5d6f86"))
    rect(img, 199, HORIZON - 5, 214, HORIZON - 4, hexc("#7d8ea6"))
    rect(img, 217, HORIZON - 7, 220, HORIZON - 4, hexc("#9aa9bd"))
    # offshore wind farm: two rows, yellow transition pieces at the waterline
    for row, (base, tower, spacing, start) in enumerate([(HORIZON + 1, 11, 22, 6), (HORIZON + 6, 17, 34, 20)]):
        for i, x in enumerate(range(start, W, spacing)):
            bd.turbine(img, x, base, tower, tower // 3 + 1, frame * math.tau / 12 + i * 0.9 + row,
                       hexc("#f2f7fa"), hexc("#c8dbe3"))
            img.putpixel((x, base), hexc("#e5c41f"))
            img.putpixel((x, base - 1), hexc("#e5c41f"))
    return img


# ---------------------------------------------------------------- mid: ship, crane, tug
WATER = 122


def port_mid():
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for x in range(W):                                     # nearer water, a little darker
        for y in range(WATER, H):
            img.putpixel((x, y), hexc("#3b7fb3" if y < WATER + 2 else "#336f9e"))
        if x % 9 < 3:
            img.putpixel((x, WATER + 6 + (x // 9) % 4 * 4), hexc("#5d9ac6"))
    # container ship: hull, red waterline, HT on the bow
    x0, x1 = 14, 196
    for y in range(110, 131):
        inset = max(0, y - 124)                            # hull narrows below the waterline
        rect(img, x0 + inset + (8 - min(8, y - 110)), y, x1 - inset, y,
             hexc("#b2383e") if y >= 126 else hexc("#23305a"))
    rect(img, x0 + 8, 110, x1, 110, hexc("#3a4a7a"))      # deck edge
    for i, ch in enumerate(["W.W.WWW", "WWW..W.", "W.W..W.", "W.W..W."]):
        for j, p in enumerate(ch):
            if p == "W":
                img.putpixel((x0 + 16 + j, 114 + i), hexc("#f2f4f8"))
    # containers in HT colours, stacked on deck
    rng = random.Random(11)
    for bay in range(14):
        bx = 38 + bay * 9
        for tier in range(rng.choice((2, 3, 3, 4))):
            c = HT[rng.randrange(18)]
            rect(img, bx, 105 - tier * 5, bx + 7, 109 - tier * 5, c)
            for dx in (2, 5):                              # corrugation
                img.putpixel((bx + dx, 107 - tier * 5), tuple(int(v * 0.75) for v in c[:3]) + (255,))
    # bridge at the stern, funnel with HT stripes
    rect(img, 172, 86, 192, 109, hexc("#eef1f6"))
    for wy in (90, 96, 102):
        rect(img, 174, wy, 190, wy + 1, hexc("#5f93b8"))
    rect(img, 180, 76, 188, 85, hexc("#2c2a34"))
    for i in range(3):
        rect(img, 180, 78 + i * 2, 188, 78 + i * 2, HT[(i * 6 + 6) % 18])
    # dockside crane (ship to shore): two legs, a long boom out over the ship
    red, white = hexc("#b2383e"), hexc("#eef1f6")
    for lx in (226, 246):
        rect(img, lx, 66, lx + 2, GROUND_Y + 2, red)
        for y in range(70, GROUND_Y, 12):
            rect(img, lx, y, lx + 2, y + 1, white)
    rect(img, 226, 92, 248, 94, red)                       # cross beam
    rect(img, 150, 64, 272, 66, white)                     # boom
    rect(img, 266, 58, 274, 66, red)                       # machinery house
    for i in range(6):
        img.putpixel((236 + i % 2, 46 + i * 3), red)
    rect(img, 236, 46, 237, 63, red)                       # apex
    bd.line(img, 237, 46, 150, 64, red)                    # stays
    bd.line(img, 237, 46, 272, 63, red)
    rect(img, 116, 67, 122, 70, hexc("#2c2a34"))           # trolley, cable and spreader over the containers
    rect(img, 118, 71, 119, 84, hexc("#2c2a34"))
    rect(img, 113, 85, 124, 86, hexc("#e5c41f"))
    # tug boat
    rect(img, 282, 122, 308, 127, hexc("#b2383e"))
    rect(img, 286, 116, 298, 121, hexc("#eef1f6"))
    rect(img, 288, 118, 296, 118, hexc("#5f93b8"))
    rect(img, 293, 111, 295, 115, hexc("#2c2a34"))
    return img


# ---------------------------------------------------------------- ground: quayside
def port_ground():
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    rng = random.Random(9)
    for x in range(W):
        img.putpixel((x, GROUND_Y), hexc("#d6d9df"))       # lit edge
        stripe = "#e5c41f" if (x // 6) % 2 == 0 else "#2a2433"
        for y in (GROUND_Y + 1, GROUND_Y + 2):
            img.putpixel((x, y), hexc(stripe))             # hazard edge
        for y in range(GROUND_Y + 3, H):
            c = "#9a9ea6" if y < H - 6 else "#7a7e86"
            if x % 40 == 0:
                c = "#82868e"                              # slab joints
            img.putpixel((x, y), hexc(c))
    for _ in range(160):                                   # wear and stains
        x, y = rng.randrange(W), rng.randrange(GROUND_Y + 6, H - 6)
        c = rng.choice(("#a9adb5", "#8c9098"))
        img.putpixel((x, y), hexc(c))
        img.putpixel(((x + 1) % W, y), hexc(c))
    return img


if __name__ == "__main__":
    for f in range(4):
        port_far(f).save(OUT / f"port_far_{f}.png")
    port_mid().save(OUT / "port_mid.png")
    port_ground().save(OUT / "port_ground.png")
    s = Image.open(OUT / "sky.png").convert("RGBA")
    for layer in ("clouds.png", "port_far_0.png", "port_mid.png", "port_ground.png"):
        s.alpha_composite(Image.open(OUT / layer).convert("RGBA"))
    s.resize((W * 4, H * 4), Image.NEAREST).save(OUT / "port_preview.png")
    print(f"wrote port layers to {OUT}")
