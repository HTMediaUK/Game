"""British countryside backdrop with wind turbines, in scrolling layers.

The game screen is 320x180 pixels (scaled up to fill the display). Every layer
is 320 wide and tiles seamlessly left to right, so it can scroll forever:

    sky.png           static banded sky
    clouds.png        drifts slowly
    hills_far_N.png   hazy hills and a row of turbines (4 frames: blades turn)
    hills_mid_N.png   patchwork fields, hedgerows, trees, big turbines (4 frames)
    ground.png        grass edge and soil, scrolls at running speed

Run:  python3 sprites/src/backdrop.py
Also writes a still preview and a scrolling GIF with Dan on the ground.
"""
import math
import random
from pathlib import Path
import sys
from PIL import Image

sys.path.insert(0, str(Path(__file__).parent))
import landmarks  # noqa: E402

# Layout of the near hills (one 320px tile). Everything has its own patch of
# hill so nothing overlaps: buildings sit on flattened plots, cows graze on
# gentle slopes in two small groups, and trees are spaced along one hedgerow.
LANDMARK_SPOTS = [(58, landmarks.hospital), (204, landmarks.old_mine)]
LANDMARK_IMAGES = [(x, fn()) for x, fn in LANDMARK_SPOTS]
PLOTS = [(x - 4, x + im.width + 3) for x, im in LANDMARK_IMAGES]   # flattened ground
COW = landmarks.field_cow()
COW_SPOTS = [(14, False), (30, True), (258, False), (272, True)]  # (x, facing right?)
TREE_SPOTS = [46, 112, 160, 182, 250, 300]

W, H = 320, 180
GROUND_Y = 148
TAU = 2 * math.pi
OUT = Path(__file__).resolve().parents[1] / "backdrop"


def hexc(h, a=255):
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5)) + (a,)


def wave(x, *parts):
    """Sum of sines whose periods divide the layer width, so it tiles."""
    return sum(amp * math.sin(TAU * cycles * x / W + phase) for amp, cycles, phase in parts)


def line(img, x0, y0, x1, y1, col):
    """Pixel line, wrapping horizontally so turbines at the edge tile."""
    dx, dy = abs(x1 - x0), -abs(y1 - y0)
    sx, sy = (1 if x0 < x1 else -1), (1 if y0 < y1 else -1)
    err = dx + dy
    while True:
        if 0 <= y0 < img.height:
            img.putpixel((x0 % img.width, y0), col)
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err
        if e2 >= dy:
            err += dy
            x0 += sx
        if e2 <= dx:
            err += dx
            y0 += sy


def turbine(img, x, base_y, tower, blade, angle, col, shade):
    """Tower, nacelle and three blades. Wider towers for nearer turbines."""
    hub_y = base_y - tower
    thick = 2 if tower >= 28 else 1
    for t in range(thick):
        line(img, x + t, base_y, x + t, hub_y, col if t == 0 else shade)
    for k in range(3):
        a = angle + k * TAU / 3
        line(img, x, hub_y, x + round(blade * math.cos(a)), hub_y + round(blade * math.sin(a)), col)
    for dx, dy in ((0, 0), (1, 0), (0, -1), (1, -1)):
        img.putpixel(((x + dx) % img.width, hub_y + dy), shade)


# ---------------------------------------------------------------- sky
def sky():
    img = Image.new("RGBA", (W, H), hexc("#4cb4d4"))
    # each band edge rolls in its own gentle wave, with little scallops on top
    bands = [(58, "#7ad7ea", ((6, 2, 0.3), (3, 5, 1.7))),
             (98, "#b4f2f8", ((5, 3, 2.1), (3, 1, 0.4)))]
    bump = [0, 1, 2, 3, 2, 1, 0, 0]
    for top, colour, parts in bands:
        for x in range(W):
            edge = top + round(wave(x, *parts)) - bump[x % len(bump)]
            for y in range(edge, H):
                img.putpixel((x, y), hexc(colour))
    return img


def clouds():
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    white, shade = hexc("#ffffff"), hexc("#d4f4fb")
    # (centre x, base y, list of (dx, radius) puffs)
    for cx, by, puffs in [
        (50, 34, [(-14, 5), (-4, 8), (8, 7), (17, 4)]),
        (165, 20, [(-12, 6), (0, 9), (12, 6)]),
        (262, 46, [(-8, 5), (2, 7), (11, 4)]),
    ]:
        left = cx + puffs[0][0] - puffs[0][1]
        right = cx + puffs[-1][0] + puffs[-1][1]
        for dx, r in puffs:
            for y in range(by - 2 * r, by + 1):
                for x in range(cx + dx - r, cx + dx + r + 1):
                    if (x - cx - dx) ** 2 + (y - by + r) ** 2 <= r * r:
                        img.putpixel((x % W, y), white if y < by - 2 else shade)
        for x in range(left, right + 1):     # flat cloud base
            for y in (by - 1, by):
                img.putpixel((x % W, y), shade)
    return img


# ---------------------------------------------------------------- hills
def far_ridge(x):
    return round(103 + wave(x, (6, 2, 0.0), (4, 5, 1.0), (2, 9, 2.0)))


def _mid_raw(x):
    return 126 + wave(x, (8, 1, 2.0), (5, 3, 0.5), (2, 7, 1.3))


def _smooth(t):
    return t * t * (3 - 2 * t)


def mid_ridge(x):
    """Near hills, levelled under each building with a smooth shoulder either side."""
    x %= W
    r = _mid_raw(x)
    for a, b in PLOTS:
        level = sum(_mid_raw(i) for i in range(a, b + 1)) / (b - a + 1)
        if a <= x <= b:
            return round(level)
        if a - 12 < x < a:
            r += (level - r) * _smooth((x - (a - 12)) / 12)
        elif b < x < b + 12:
            r += (level - r) * _smooth(((b + 12) - x) / 12)
    return round(r)


FAR_TURBINES = [(18 + i * 46, (18, 22, 16)[i % 3]) for i in range(7)]   # evenly spaced
MID_TURBINES = [(134, 36), (314, 32)]   # in the gaps between the far ones


def hills_far(frame):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    top, body = hexc("#b9e0cf"), hexc("#9ccdb6")
    for x in range(W):
        r = far_ridge(x)
        img.putpixel((x, r), top)
        for y in range(r + 1, H):
            img.putpixel((x, y), body)
    for i, (x, tower) in enumerate(FAR_TURBINES):
        angle = frame * TAU / 12 + i * 0.7
        turbine(img, x, far_ridge(x) + 2, tower, tower // 3 + 1, angle,
                hexc("#eef5f8"), hexc("#c8dbe3"))
    return img


# Each field type has a light / mid / dark ramp and its own texture.
FIELD_TYPES = {
    "meadow":   ("#9bd86e", "#7cc35a", "#5f9f45", "specks"),
    "pasture":  ("#a9e07a", "#8fd16a", "#6fb04f", "stripes"),
    "grazing":  ("#87c060", "#6bb04c", "#518c3a", "specks"),
    "rapeseed": ("#f6e57a", "#e6d25a", "#c4ad3c", "flowers"),
    "ploughed": ("#c09a68", "#a98a5c", "#846742", "furrows"),
}
# Four big fields across, split once by a hedgerow: (above hedge, below hedge)
COLUMNS = [0, 120, 196, 252, W]
FIELDS = [("meadow", "ploughed"), ("pasture", "grazing"), ("meadow", "rapeseed"), ("grazing", "pasture")]
HEDGE_DEPTH = 15
HEDGE_ROWS = (HEDGE_DEPTH,)


def field_at(x, y):
    depth = y - mid_ridge(x)
    col_i = max(i for i, c in enumerate(COLUMNS[:-1]) if c <= x)
    return FIELD_TYPES[FIELDS[col_i][0 if depth < HEDGE_DEPTH else 1]]


def hills_mid(frame):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    rng = random.Random(7)
    for x in range(W):
        r = mid_ridge(x)
        # Light comes from the top left: slopes facing left catch it,
        # slopes facing right fall into shadow.
        slope = mid_ridge((x + 3) % W) - mid_ridge((x - 3) % W)
        base = 2 if slope >= 3 else 0 if slope <= -3 else 1
        for y in range(r, H):
            depth = y - r
            light, mid, dark, texture = field_at(x, y)
            ramp = [light, mid, dark]
            shade = 0 if depth < 2 else base       # sunlit crest
            if texture == "furrows" and depth % 4 == 0:
                shade = min(2, shade + 1)          # furrows follow the hill
            elif texture == "stripes" and (x + depth) // 6 % 2 == 0:
                shade = max(0, shade - 1)          # mown stripes
            elif texture == "specks" and (x * 7 + y * 13) % 23 == 0:
                shade = min(2, shade + 1)          # tufts
            elif texture == "flowers" and (x * 5 + y * 3) % 13 == 0:
                shade = max(0, shade - 1)          # bright flower heads
            img.putpixel((x, y), hexc(ramp[shade]))
        img.putpixel((x, r), hexc("#c3eb98"))      # rim light on the ridge
        for d in HEDGE_ROWS:                        # hedgerows, with a shadow below
            if r + d + 1 < H:
                leafy = (x * 3) % 5 == 0
                img.putpixel((x, r + d - 1), hexc("#4f8f3f") if leafy else hexc("#3f7a35"))
                img.putpixel((x, r + d), hexc("#2f5f2a"))
                img.putpixel((x, r + d + 1), hexc(field_at(x, r + d + 1)[2]))
    for c in COLUMNS[:-1]:                          # field boundaries down the hill
        for y in range(mid_ridge(c) + 1, H):
            img.putpixel((c, y), hexc("#2f5f2a"))
            img.putpixel((c + 1, y), hexc(field_at(c + 1, y)[2]))
    # trees along the hedges: shadow on the ground first, then the canopy
    for x in TREE_SPOTS:
        y = mid_ridge(x) + HEDGE_DEPTH - 1
        for dx in range(0, 5):
            img.putpixel(((x + dx) % W, y + 1), hexc("#2f5f2a"))
        for dx in range(-3, 4):
            for dy in range(-6, 1):
                d2 = dx * dx + (dy + 3) ** 2
                if d2 <= 10:
                    if dx + dy < -5:
                        col = "#6aab4c"                # sunlit top left
                    elif dx + dy > -1:
                        col = "#24502a"                # shadow side
                    else:
                        col = "#3d7f39"
                    img.putpixel(((x + dx) % W, y + dy), hexc(col))
    from PIL import ImageOps
    for x0, flip in COW_SPOTS:                # feet on the grass, halfway down the top field
        im = ImageOps.mirror(COW) if flip else COW
        feet = mid_ridge(x0 + im.width // 2) + 9
        img.alpha_composite(im, (x0, feet - im.height + 2))
    for x0, im in LANDMARK_IMAGES:            # stand on the flattened plot
        base = mid_ridge(x0 + im.width // 2) + 2
        img.alpha_composite(im, (x0, base - im.height + 1))
    for i, (x, tower) in enumerate(MID_TURBINES):
        angle = frame * TAU / 12 + i * 1.3
        turbine(img, x, mid_ridge(x) + 2, tower, tower // 3, angle,
                hexc("#ffffff"), hexc("#c9d5df"))
    return img


# ---------------------------------------------------------------- ground
def ground():
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    rng = random.Random(3)
    light, mid, dark = hexc("#9bdc55"), hexc("#62b13c"), hexc("#3d8a2a")
    soil, soil_l, soil_d, bottom = hexc("#8b5a3c"), hexc("#a3704c"), hexc("#6e4430"), hexc("#5e372a")
    tuft = [0, 1, 3, 1, 0, 2, 4, 2, 0, 1, 2, 0, 3, 5, 3, 1]   # grass hanging into soil
    for x in range(W):
        img.putpixel((x, GROUND_Y), light)
        for y in range(GROUND_Y + 1, GROUND_Y + 4):
            img.putpixel((x, y), mid)
        hang = tuft[x % len(tuft)]
        for y in range(GROUND_Y + 4, GROUND_Y + 4 + hang):
            img.putpixel((x, y), dark if y == GROUND_Y + 3 + hang else mid)
        for y in range(GROUND_Y + 4 + hang, H):
            img.putpixel((x, y), bottom if y >= H - 6 else soil)
    # speckles in 2x2 blocks, wrapped so the soil tiles
    for _ in range(420):
        x, y = rng.randrange(W), rng.randrange(GROUND_Y + 8, H - 6)
        c = rng.choice((soil_l, soil_d))
        for dx in (0, 1):
            img.putpixel(((x + dx) % W, y), c)
    return img


# ---------------------------------------------------------------- preview
def tile(dst, layer, offset):
    o = int(offset) % W
    dst.alpha_composite(layer, (-o, 0))
    dst.alpha_composite(layer, (W - o, 0))


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    layers = {"sky": sky(), "clouds": clouds(), "ground": ground()}
    far = [hills_far(f) for f in range(4)]
    mid = [hills_mid(f) for f in range(4)]
    for name, im in layers.items():
        im.save(OUT / f"{name}.png")
    for f in range(4):
        far[f].save(OUT / f"hills_far_{f}.png")
        mid[f].save(OUT / f"hills_mid_{f}.png")

    dan_path = OUT.parent / "dan" / "dan_v2_stand.png"
    dan = Image.open(dan_path).convert("RGBA") if dan_path.exists() else None

    def scene(t):
        s = layers["sky"].copy()
        tile(s, layers["clouds"], t * 0.15)
        tile(s, far[t % 4], t * 0.3)
        tile(s, mid[t % 4], t * 0.8)
        tile(s, layers["ground"], t * 3)
        if dan:
            s.alpha_composite(dan, (60, GROUND_Y - 30))
        return s

    scene(0).resize((W * 4, H * 4), Image.NEAREST).save(OUT / "backdrop_preview.png")
    frames = [scene(t).resize((W * 3, H * 3), Image.NEAREST).convert("RGB") for t in range(80)]
    frames[0].save(OUT / "backdrop_preview.gif", save_all=True, append_images=frames[1:],
                   duration=60, loop=0)
    print(f"wrote layers and previews to {OUT}")


if __name__ == "__main__":
    main()
