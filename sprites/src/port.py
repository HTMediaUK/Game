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
from soil import deepen  # noqa: E402
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


def water(img, xs):
    """Nearer water, a little darker than the sea out at the horizon, with ripples."""
    for x in xs:
        for y in range(WATER, H):
            img.putpixel((x, y), hexc("#3b7fb3" if y < WATER + 2 else "#336f9e"))
        if x % 9 < 3:
            img.putpixel((x, WATER + 6 + (x // 9) % 4 * 4), hexc("#5d9ac6"))


def draw_crane(img):
    """Ship-to-shore container crane, side on: two braced legs on bogies, a box
    girder out over the ship with a backreach behind, an A-frame tower with stay
    cables, a machinery house, and a trolley with cab, hoist ropes and spreader."""
    red, red_d, white = hexc("#c23b33"), hexc("#8e2a22"), hexc("#eef1f6")
    steel, cable, yellow = hexc("#3a3d4e"), hexc("#4a4e5e"), hexc("#e5c41f")
    sea_leg, land_leg = 218, 252                          # leg x positions (3px wide)
    girder_y = 64                                         # top of the main girder
    tip, back = 132, 284                                  # boom tip over the ship, end of the backreach
    # legs, lit on the left, with white bands
    for lx in (sea_leg, land_leg):
        rect(img, lx, girder_y + 5, lx + 2, GROUND_Y - 5, red)
        rect(img, lx + 2, girder_y + 5, lx + 2, GROUND_Y - 5, red_d)
        for y in range(girder_y + 14, GROUND_Y - 8, 18):
            rect(img, lx, y, lx + 2, y + 1, white)
        rect(img, lx - 3, GROUND_Y - 4, lx + 5, GROUND_Y - 1, steel)     # bogie
        for wx in (lx - 2, lx + 1, lx + 4):
            img.putpixel((wx, GROUND_Y - 1), hexc("#1c1a22"))            # wheels
    # portal beams and cross bracing between the legs
    for by in (girder_y + 34, GROUND_Y - 22):
        rect(img, sea_leg, by, land_leg + 2, by + 2, red)
        rect(img, sea_leg, by + 2, land_leg + 2, by + 2, red_d)
    bd.line(img, sea_leg + 3, girder_y + 6, land_leg - 1, girder_y + 33, red_d)
    bd.line(img, land_leg - 1, girder_y + 6, sea_leg + 3, girder_y + 33, red_d)
    # main girder: boom out over the water, backreach behind, with a truss pattern
    rect(img, tip, girder_y, back, girder_y + 4, red)
    rect(img, tip, girder_y, back, girder_y, hexc("#e0584e"))
    rect(img, tip, girder_y + 4, back, girder_y + 4, red_d)
    for x in range(tip + 2, back - 2, 6):
        bd.line(img, x, girder_y + 1, x + 3, girder_y + 3, red_d)
        bd.line(img, x + 3, girder_y + 3, x + 6, girder_y + 1, red_d)
    rect(img, tip - 2, girder_y - 1, tip, girder_y + 5, red_d)           # boom tip
    # A-frame tower above the legs, stays to the boom tip, mid-boom and backreach
    apex = (236, girder_y - 28)
    bd.line(img, sea_leg + 1, girder_y, apex[0] - 1, apex[1], red)
    bd.line(img, sea_leg + 2, girder_y, apex[0], apex[1], red)
    bd.line(img, land_leg + 1, girder_y, apex[0] + 1, apex[1], red_d)
    rect(img, apex[0] - 2, apex[1] - 2, apex[0] + 2, apex[1] + 1, red)
    for target in ((tip, girder_y), (182, girder_y)):
        bd.line(img, apex[0], apex[1], target[0], target[1], cable)
    bd.line(img, apex[0], apex[1], back - 2, girder_y, cable)
    # machinery house on the backreach
    rect(img, 260, girder_y - 9, 282, girder_y - 1, white)
    rect(img, 260, girder_y - 9, 282, girder_y - 9, hexc("#c8d0dc"))
    for wx in (263, 269, 275):
        rect(img, wx, girder_y - 6, wx + 3, girder_y - 5, hexc("#5f93b8"))
    # trolley with the driver's cab, hoist ropes, spreader and a container on the hook
    tx = 146
    rect(img, tx, girder_y + 5, tx + 10, girder_y + 7, steel)
    rect(img, tx + 1, girder_y + 8, tx + 7, girder_y + 13, white)
    rect(img, tx + 2, girder_y + 9, tx + 6, girder_y + 11, hexc("#5f93b8"))
    for rx in (tx + 2, tx + 8):
        rect(img, rx, girder_y + 8, rx, 84, cable)
    rect(img, tx - 1, 85, tx + 11, 86, yellow)
    rect(img, tx - 1, 87, tx + 11, 91, HT[17])
    rect(img, tx - 1, 91, tx + 11, 91, tuple(int(v * 0.7) for v in HT[17][:3]) + (255,))


def draw_tug(img):
    rect(img, 282, 122, 308, 127, hexc("#b2383e"))
    rect(img, 286, 116, 298, 121, hexc("#eef1f6"))
    rect(img, 288, 118, 296, 118, hexc("#5f93b8"))
    rect(img, 293, 111, 295, 115, hexc("#2c2a34"))


def port_mid():
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    water(img, range(W))
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
    draw_crane(img)
    draw_tug(img)
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
    deepen(img, hexc("#9a9ea6"), hexc("#7a7e86"), seed=5)  # older concrete below
    return img


# ---------------------------------------------------------------- field-to-port pieces
# One 320px piece per layer that starts as the countryside tile (so the left
# edge joins it seamlessly) and ends as the port tile (so the right edge joins
# that). In the game each layer reaches its piece at its own parallax speed.
def _smooth(t):
    t = max(0.0, min(1.0, t))
    return t * t * (3 - 2 * t)


def _sink(src, base, x0, x1, depth):
    """Copy `src` onto `base`, sliding columns x0..x1 down so the hills sink out of sight."""
    out = base.copy()
    for x in range(W):
        shift = 0 if x < x0 else round(depth * _smooth((x - x0) / (x1 - x0)))
        if x > x1:
            continue
        for y in range(H):
            sy = y - shift
            if 0 <= sy < H:
                px = src.getpixel((x, sy))
                if px[3]:
                    out.putpixel((x, y), px)
    return out


def trans_far(frame):
    country = Image.open(OUT / f"hills_far_{frame}.png").convert("RGBA")
    sea = port_far(frame)
    base = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    base.alpha_composite(sea.crop((150, 0, W, H)), (150, 0))    # the sea opens up behind the sinking hills
    return _sink(country, base, 150, 250, 60)


def trans_mid(frame):
    country = Image.open(OUT / f"hills_mid_{frame}.png").convert("RGBA")
    base = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    water(base, range(120, W))                                                # open water ahead
    draw_crane(base)                                                            # crane and tug
    draw_tug(base)
    out = _sink(country, base, 120, 200, 45)
    for x in range(128, 200):                                   # a strip of sand where the hill meets the water
        out.putpixel((x, WATER - 1), hexc("#e8d6a0"))
    return out


def trans_ground():
    country = Image.open(OUT / "ground.png").convert("RGBA")
    quay = port_ground()
    out = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    out.alpha_composite(country.crop((0, 0, 150, H)), (0, 0))
    out.alpha_composite(quay.crop((150, 0, W, H)), (150, 0))
    for x in range(150, 162):                                   # grass runs out onto the quay
        for y in range(GROUND_Y, GROUND_Y + 3 - (x - 150) // 4):
            out.putpixel((x, y), hexc("#62b13c" if y > GROUND_Y else "#9bdc55"))
    # wooden signpost with an anchor, where the field meets the quay
    post, board = hexc("#7a4e2c"), hexc("#efe2c4")
    for y in range(GROUND_Y - 22, GROUND_Y):
        out.putpixel((156, y), post); out.putpixel((157, y), post)
    for y in range(GROUND_Y - 30, GROUND_Y - 20):
        for x in range(146, 168):
            edge = y in (GROUND_Y - 30, GROUND_Y - 21) or x in (146, 167)
            out.putpixel((x, y), hexc("#2a2433") if edge else board)
    anchor = ["..x..", ".xxx.", "..x..", "..x..", "x.x.x", ".xxx."]
    for j, row in enumerate(anchor):
        for i, ch in enumerate(row):
            if ch == "x":
                out.putpixel((149 + i, GROUND_Y - 28 + j), hexc("#2c3a64"))
    for i, (dx, dy) in enumerate([(0, 0), (1, 1), (2, 2), (1, 3), (0, 4)]):   # arrow
        out.putpixel((162 + dx, GROUND_Y - 27 + dy), hexc("#b2383e"))
    for x in range(156, 162):
        out.putpixel((x, GROUND_Y - 25), hexc("#b2383e"))
    return out


if __name__ == "__main__":
    for f in range(4):
        port_far(f).save(OUT / f"port_far_{f}.png")
    port_mid().save(OUT / "port_mid.png")
    port_ground().save(OUT / "port_ground.png")
    for f in range(4):
        trans_far(f).save(OUT / f"trans_far_{f}.png")
        trans_mid(f).save(OUT / f"trans_mid_{f}.png")
    trans_ground().save(OUT / "trans_ground.png")
    # preview: country tile, then the field-to-port piece, then the port tile, side by side
    strip = Image.new("RGBA", (W * 3, H))
    sky = Image.open(OUT / "sky.png").convert("RGBA")
    for k in range(3):
        strip.alpha_composite(sky, (k * W, 0))
    for k, names in enumerate([("hills_far_0", "hills_mid_0", "ground"), ("trans_far_0", "trans_mid_0", "trans_ground"),
                               ("port_far_0", "port_mid", "port_ground")]):
        for n in names:
            strip.alpha_composite(Image.open(OUT / f"{n}.png").convert("RGBA"), (k * W, 0))
    strip.resize((W * 3 * 2, H * 2), Image.NEAREST).save(OUT / "transition_preview.png")
    s = Image.open(OUT / "sky.png").convert("RGBA")
    for layer in ("clouds.png", "port_far_0.png", "port_mid.png", "port_ground.png"):
        s.alpha_composite(Image.open(OUT / layer).convert("RGBA"))
    s.resize((W * 4, H * 4), Image.NEAREST).save(OUT / "port_preview.png")
    print(f"wrote port layers to {OUT}")
