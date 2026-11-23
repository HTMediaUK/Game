"""The Scottish canal: where the run goes after the port (30 seconds in).

Generic Scottish canal scenery, no client names or logos:
    canal_far.png      Highland hills: heather slopes in front, grey-blue peaks with snow
    canal_mid.png      the canal: towpath bank, humpback stone bridge, lock gates,
                       lock-keeper's cottage, Scots pines, moored canal boats
    canal_ground.png   gravel towpath with a stone edge
    trans2_*           port-to-canal pieces (like the field-to-port ones)

    python3 sprites/src/canal.py
"""
import math
import random
import sys
from pathlib import Path
from PIL import Image

sys.path.insert(0, str(Path(__file__).parent))
import backdrop as bd  # noqa: E402
import port  # noqa: E402

W, H, GROUND_Y = bd.W, bd.H, bd.GROUND_Y
OUT = bd.OUT
hexc = bd.hexc
rect = port.rect
smooth = port._smooth

CANAL_WATER = 130          # the canal's surface in the near layer


# ---------------------------------------------------------------- far: Highland hills
def back_ridge(x):         # grey-blue peaks
    return round(66 + bd.wave(x, (9, 2, 0.4), (6, 5, 1.9), (3, 11, 0.7))
                 - 10 * abs(math.sin(math.tau * 3 * x / W + 0.5)))


def front_ridge(x):        # heather slopes
    return round(96 + bd.wave(x, (7, 1, 2.2), (5, 3, 0.1), (2, 8, 1.4)))


def paint_hills(img, x, back, front):
    for y in range(back, H):
        snow = y < back + 3 and back < 62
        img.putpixel((x, y), hexc("#f2f5f8" if snow else "#8a9bbd" if y < back + 6 else "#7486ab"))
    for y in range(front, H):
        heather = (x * 3 + y * 7) % 13 == 0
        c = "#a58fc0" if y == front else ("#8a6fa6" if heather else "#6f7f55" if y > front + 10 else "#7a6a92")
        img.putpixel((x, y), hexc(c))


def canal_far():
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for x in range(W):
        paint_hills(img, x, back_ridge(x), front_ridge(x))
    return img


# ---------------------------------------------------------------- near: the canal
def canal_water(img, xs, top=CANAL_WATER):
    for x in xs:
        for y in range(top, H):
            img.putpixel((x, y), hexc("#3f7d8a" if y < top + 2 else "#2f6673"))
        if x % 11 < 4:
            img.putpixel((x, top + 5 + (x // 11) % 3 * 4), hexc("#5d97a3"))


def bank(img, xs, top=112):
    """Grassy far bank of the canal, from `top` down to the water."""
    for x in xs:
        for y in range(top, CANAL_WATER):
            c = "#9bd86e" if y == top else "#7cc35a" if y < top + 8 else "#5f9f45"
            img.putpixel((x, y), hexc(c))
        img.putpixel((x, CANAL_WATER - 1), hexc("#8c8a80"))          # stone coping on the bank


def scots_pine(img, x, base):
    rect(img, x, base - 16, x + 1, base, hexc("#8a4a2c"))           # reddish trunk
    for i, (w, y) in enumerate([(3, base - 22), (5, base - 19), (4, base - 15)]):
        rect(img, x - w + 1, y, x + w, y + 3, hexc("#2f5a34" if i % 2 else "#3d6e3f"))


def cottage(img, x, base):
    rect(img, x, base - 14, x + 26, base, hexc("#f2efe6"))           # white harled walls
    rect(img, x + 22, base - 14, x + 26, base, hexc("#d8d3c6"))
    for i in range(7):                                               # slate roof
        rect(img, x - 2 + i, base - 15 - i, x + 28 - i, base - 15 - i, hexc("#4a4e5e" if i % 2 else "#5a5f70"))
    rect(img, x + 20, base - 26, x + 22, base - 19, hexc("#8a8478"))  # chimney
    rect(img, x + 5, base - 8, x + 8, base, hexc("#2f4a6a"))         # door
    for wx in (12, 18):
        rect(img, wx + x, base - 10, wx + x + 3, base - 7, hexc("#5f93b8"))


def bridge(img, x0, x1, deck):
    """Stone humpback bridge carrying a lane over the canal: a hump on top,
    an arch over the water, stone abutments down to the water at each end."""
    stone, dark, light = hexc("#9a948a"), hexc("#7a756c"), hexc("#b5afa4")
    mid, half = (x0 + x1) / 2, (x1 - x0) / 2
    span = half * 0.62                                   # half-width of the arch opening
    for x in range(x0, x1 + 1):
        top = deck - round(6 * math.cos((x - mid) / (x1 - x0) * math.pi))   # humped parapet
        dx = (x - mid) / span
        arch_top = CANAL_WATER + 2 - round(18 * math.sqrt(max(0.0, 1 - dx * dx))) if abs(dx) < 1 else None
        for y in range(top, CANAL_WATER + 3):
            if arch_top is not None and y >= arch_top:
                break                                    # under the arch: open water
            edge = arch_top is not None and y == arch_top - 1
            c = light if y == top else dark if edge or (x * 3 + (y // 3) * 5) % 11 == 0 else stone
            img.putpixel((x % W, y), c)
        img.putpixel((x % W, top - 1), dark)             # parapet coping


def lock_gate(img, x):
    rect(img, x, CANAL_WATER - 16, x + 2, CANAL_WATER + 6, hexc("#1f1c24"))   # gate
    rect(img, x - 18, CANAL_WATER - 18, x + 2, CANAL_WATER - 16, hexc("#1f1c24"))   # balance beam
    rect(img, x - 18, CANAL_WATER - 18, x - 14, CANAL_WATER - 16, hexc("#f2f2f0"))  # white tip
    rect(img, x - 2, CANAL_WATER - 22, x - 1, CANAL_WATER - 17, hexc("#f2f2f0"))    # white post


def canal_boat(img, x, length, hull, trim, cabin):
    y = CANAL_WATER
    rect(img, x, y - 1, x + length, y + 4, hexc(hull))                # hull
    rect(img, x, y - 1, x + length, y - 1, hexc(trim))
    rect(img, x + 4, y - 7, x + length - 6, y - 2, hexc(cabin))      # cabin
    rect(img, x + 4, y - 7, x + length - 6, y - 7, hexc("#2a2433"))  # roof
    for wx in range(x + 7, x + length - 8, 6):
        rect(img, wx, y - 5, wx + 2, y - 4, hexc("#f2e6b0"))         # portholes
    rect(img, x + length - 10, y - 10, x + length - 9, y - 8, hexc("#2a2433"))   # chimney
    for fx in range(x + 8, x + 16, 2):                               # flowers on the roof
        img.putpixel((fx, y - 8), hexc(["#e43b44", "#feae34", "#b85895"][fx % 3]))


def canal_mid():
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    canal_water(img, range(W))
    bank(img, range(W))
    for x in (8, 20, 196, 214, 300):
        scots_pine(img, x, 113)
    cottage(img, 150, 112)
    bridge(img, 36, 104, 108)
    lock_gate(img, 128)
    canal_boat(img, 224, 44, "#2f5d3f", "#e5c41f", "#b2383e")
    canal_boat(img, 276, 36, "#23305a", "#e8e0c8", "#47984a")
    return img


def canal_ground():
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    rng = random.Random(21)
    for x in range(W):
        img.putpixel((x, GROUND_Y), hexc("#d2ccbf"))                 # stone edge along the water
        img.putpixel((x, GROUND_Y + 1), hexc("#a39d90"))
        for y in range(GROUND_Y + 2, H):
            img.putpixel((x, y), hexc("#b8a888" if y < H - 6 else "#9a8c70"))
    for _ in range(300):                                             # gravel
        x, y = rng.randrange(W), rng.randrange(GROUND_Y + 3, H - 6)
        img.putpixel((x, y), hexc(rng.choice(("#cbbd9c", "#9e8f72", "#d8cdb3"))))
    for x in range(0, W, 24):                                        # stone joints
        img.putpixel((x, GROUND_Y), hexc("#a39d90"))
    return img


# ---------------------------------------------------------------- port-to-canal pieces
def trans2_far(frame):
    sea = Image.open(OUT / f"port_far_{frame}.png").convert("RGBA")
    out = sea.copy()
    for x in range(150, W):                                          # the hills rise out of the sea
        k = smooth((x - 150) / 100)
        back = round(port.HORIZON + (back_ridge(x) - port.HORIZON) * k)
        front = round(port.HORIZON + 2 + (front_ridge(x) - port.HORIZON - 2) * k)
        if k > 0.02:
            paint_hills(out, x, min(back, port.HORIZON), max(front, back + 2))
    return out


def trans2_mid():
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    port.water(img, range(0, 120))                                   # still the harbour
    for x in range(120, 200):                                        # harbour water narrows into the canal
        k = smooth((x - 120) / 80)
        top = round(port.WATER + (CANAL_WATER - port.WATER) * k)
        canal_water(img, [x], top)
    canal = canal_mid()
    for x in range(120, W):                                          # the bank rises out of the water
        k = smooth((x - 120) / 80)
        if k <= 0:
            continue
        top = round(CANAL_WATER - (CANAL_WATER - 112) * k)
        if x >= 200:
            for y in range(H):
                px = canal.getpixel((x, y))
                if px[3]:
                    img.putpixel((x, y), px)
        else:
            bank(img, [x], top)
    scots_pine(img, 176, 113)
    return img


def trans2_ground():
    quay = Image.open(OUT / "port_ground.png").convert("RGBA")
    path = canal_ground()
    out = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    out.alpha_composite(quay.crop((0, 0, 150, H)), (0, 0))
    out.alpha_composite(path.crop((150, 0, W, H)), (150, 0))
    # a thistle sign where the quay meets the towpath
    post, board = hexc("#7a4e2c"), hexc("#efe2c4")
    for y in range(GROUND_Y - 22, GROUND_Y):
        out.putpixel((156, y), post); out.putpixel((157, y), post)
    for y in range(GROUND_Y - 30, GROUND_Y - 20):
        for x in range(146, 168):
            edge = y in (GROUND_Y - 30, GROUND_Y - 21) or x in (146, 167)
            out.putpixel((x, y), hexc("#2a2433") if edge else board)
    thistle = [".p.p.", "ppppp", ".ggg.", "..g..", ".g.g."]
    for j, row in enumerate(thistle):
        for i, ch in enumerate(row):
            if ch != ".":
                out.putpixel((149 + i, GROUND_Y - 28 + j), hexc("#8a4fa6" if ch == "p" else "#47984a"))
    for i, (dx, dy) in enumerate([(0, 0), (1, 1), (2, 2), (1, 3), (0, 4)]):
        out.putpixel((162 + dx, GROUND_Y - 27 + dy), hexc("#2c3a64"))
    for x in range(156, 162):
        out.putpixel((x, GROUND_Y - 25), hexc("#2c3a64"))
    return out


if __name__ == "__main__":
    canal_far().save(OUT / "canal_far.png")
    canal_mid().save(OUT / "canal_mid.png")
    canal_ground().save(OUT / "canal_ground.png")
    for f in range(4):
        trans2_far(f).save(OUT / f"trans2_far_{f}.png")
    trans2_mid().save(OUT / "trans2_mid.png")
    trans2_ground().save(OUT / "trans2_ground.png")
    strip = Image.new("RGBA", (W * 3, H))
    sky = Image.open(OUT / "sky.png").convert("RGBA")
    for k, names in enumerate([("port_far_0", "port_mid", "port_ground"),
                               ("trans2_far_0", "trans2_mid", "trans2_ground"),
                               ("canal_far", "canal_mid", "canal_ground")]):
        strip.alpha_composite(sky, (k * W, 0))
        for n in names:
            strip.alpha_composite(Image.open(OUT / f"{n}.png").convert("RGBA"), (k * W, 0))
    strip.resize((W * 3 * 2, H * 2), Image.NEAREST).save(OUT / "canal_preview.png")
    print(f"wrote canal layers to {OUT}")
