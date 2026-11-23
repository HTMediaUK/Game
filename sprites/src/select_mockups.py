"""Three ideas for a more interesting character select screen (mockups only).

    A  Camera viewfinder: the chosen runner big in a camera frame, REC and
       timecode, a TV-style name caption, the team as clips along the bottom
    B  Edit suite: a preview monitor above, the team as coloured clips on a
       timeline with the playhead on the chosen one
    C  HT ring: the logo ring large in the middle, the chosen runner inside it,
       everyone's faces round the ring

    python3 sprites/src/select_mockups.py

Writes sprites/mockups/select_A_viewfinder.png, select_B_edit_suite.png,
select_C_ht_ring.png and select_options.png (all three together).
"""
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageEnhance

sys.path.insert(0, str(Path(__file__).parent))
import ht_logo  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "mockups"
W, H, Z = 320, 180, 4
TEAM = [("dan", "DAN", "Managing Director"), ("dave", "DAVE", "Production Director"),
        ("mark", "MARK", "Creative Director"), ("beth", "BETH", "Operations & Creative Coordinator"),
        ("sam", "SAM", "Editor"), ("jonas", "JONAS", "Creative Producer")]
CHOSEN = 0
COLOURS = [ht_logo.hexc(c) for c in ht_logo.HT_COLOURS]
CLIP_COLOURS = [COLOURS[i] for i in (17, 6, 13, 16, 3, 7)]   # teal, orange, green, magenta, olive, indigo


def font(size, mono=False):
    name = "DejaVuSansMono-Bold.ttf" if mono else "DejaVuSans-Bold.ttf"
    try:
        return ImageFont.truetype(name, size)
    except OSError:
        return ImageFont.load_default()


def sprite(cid, frame="stand"):
    return Image.open(ROOT / "characters" / cid / f"{frame}.png").convert("RGBA")


def head(cid):
    return sprite(cid).crop((8, 0, 24, 16))


def backdrop():
    bd = ROOT / "backdrop"
    s = Image.new("RGBA", (W, H))
    for n in ("sky.png", "clouds.png", "hills_far_0.png", "hills_mid_0.png", "ground.png"):
        s.alpha_composite(Image.open(bd / n).convert("RGBA"))
    return s


def big(im, k):
    return im.resize((im.width * k, im.height * k), Image.NEAREST)


def finish(scene, texts, name):
    """Scale the pixel scene up, then draw crisp text on top."""
    out = big(scene, Z)
    d = ImageDraw.Draw(out)
    for (x, y, s, colour, size, anchor, mono) in texts:
        d.text((x * Z, y * Z), s, fill=colour, font=font(size * Z, mono), anchor=anchor,
               stroke_width=Z // 2 if size >= 6 else 0, stroke_fill=(18, 14, 23))
    out.convert("RGB").save(OUT / name)
    return out


def logo_corner(scene):
    scene.alpha_composite(Image.open(ROOT / "ui" / "ht_logo.png").convert("RGBA"), (4, 4))


# ---------------------------------------------------------------- A: viewfinder
def option_a():
    s = backdrop()
    shade = Image.new("RGBA", (W, H), (18, 14, 23, 70))
    s.alpha_composite(shade)
    d = ImageDraw.Draw(s)
    white = (255, 255, 255, 255)
    for (x, y, dx, dy) in [(44, 18, 1, 1), (296, 18, -1, 1), (24, 140, 1, -1), (296, 140, -1, -1)]:
        d.line([(x, y), (x + 14 * dx, y)], fill=white)                 # viewfinder corners
        d.line([(x, y), (x, y + 14 * dy)], fill=white)
    d.line([(157, 79), (163, 79)], fill=white); d.line([(160, 76), (160, 82)], fill=white)
    d.ellipse([(262, 9), (267, 14)], fill=(228, 59, 68, 255))           # REC dot
    d.rectangle([(292, 22), (304, 27)], outline=white); d.rectangle([(305, 24), (306, 25)], fill=white)
    d.rectangle([(294, 24), (301, 25)], fill=(99, 199, 77, 255))       # battery
    cid = TEAM[CHOSEN][0]
    s.alpha_composite(big(sprite(cid, "run_0"), 3), (150, 148 - 90))
    # lower-third caption with an HT colour stripe
    d.rectangle([(26, 110), (150, 136)], fill=(18, 14, 23, 225))
    for i in range(6):
        d.rectangle([(26, 110 + i * 4), (29, 113 + i * 4)], fill=COLOURS[i * 3])
    # the team as clips along the bottom
    for i, (c, _, _) in enumerate(TEAM):
        x = 52 + i * 38
        d.rectangle([(x, 151), (x + 30, 177)], fill=(18, 14, 23, 200),
                    outline=COLOURS[17] if i == CHOSEN else (90, 84, 102, 255))
        s.alpha_composite(big(head(c), 1), (x + 7, 156))
    logo_corner(s)
    texts = [(270, 12, "REC", (255, 255, 255), 6, "lm", True),
             (296, 34, "00:00:12:08", (255, 255, 255), 5, "rm", True),
             (34, 118, TEAM[CHOSEN][1], (255, 255, 255), 10, "lm", False),
             (34, 130, TEAM[CHOSEN][2], (255, 226, 176), 5.5, "lm", False),
             (160, 98, "", (255, 255, 255), 6, "mm", False),
             (88, 60, "LEFT / RIGHT: CHOOSE", (255, 255, 255), 5.5, "mm", False),
             (88, 69, "SPACE: ACTION!", (255, 226, 176), 6, "mm", False)]
    for i, (_, n, _) in enumerate(TEAM):
        texts.append((52 + i * 38 + 15, 174, n, (255, 255, 255) if i == CHOSEN else (170, 165, 180), 3.5, "mm", False))
    return finish(s, texts, "select_A_viewfinder.png")


# ---------------------------------------------------------------- B: edit suite
def option_b():
    s = Image.new("RGBA", (W, H), (30, 28, 38, 255))
    d = ImageDraw.Draw(s)
    # program monitor
    d.rectangle([(68, 12), (252, 114)], fill=(18, 14, 23, 255), outline=(70, 66, 84, 255))
    view = backdrop().crop((0, 57, 180, 156))
    view.alpha_composite(big(sprite(TEAM[CHOSEN][0], "run_0"), 2), (58, 91 - 60))
    s.alpha_composite(view, (70, 14))
    # timeline
    d.rectangle([(0, 118), (W, H)], fill=(22, 20, 28, 255))
    for x in range(28, W, 6):
        d.line([(x, 120), (x, 122 if x % 30 else 124)], fill=(110, 104, 124, 255))
    d.rectangle([(4, 132), (22, 162)], fill=(44, 40, 54, 255))
    for i, (c, _, _) in enumerate(TEAM):
        x = 28 + i * 48
        col = CLIP_COLOURS[i]
        dim = col if i == CHOSEN else tuple(int(v * 0.6) for v in col[:3]) + (255,)
        d.rectangle([(x, 132), (x + 45, 162)], fill=dim,
                    outline=(255, 255, 255, 255) if i == CHOSEN else (18, 14, 23, 255))
        s.alpha_composite(head(c), (x + 2, 134))
    px = 28 + CHOSEN * 48 + 22
    d.line([(px, 118), (px, 170)], fill=(228, 59, 68, 255))           # playhead
    d.polygon([(px - 3, 118), (px + 3, 118), (px, 122)], fill=(228, 59, 68, 255))
    logo_corner(s)
    texts = [(70, 7, "PROGRAM", (170, 165, 180), 4.5, "lm", True),
             (252, 7, "00:00:12:08", (170, 165, 180), 4.5, "rm", True),
             (13, 147, "V1", (200, 195, 210), 5, "mm", True),
             (160, 172, "LEFT / RIGHT: SCRUB THE TIMELINE     SPACE: PLAY", (255, 226, 176), 4.5, "mm", False),
             (160, 104, f"{TEAM[CHOSEN][1]}  ·  {TEAM[CHOSEN][2]}", (255, 255, 255), 6, "mm", False)]
    for i, (_, n, _) in enumerate(TEAM):
        texts.append((28 + i * 48 + 19, 152, n, (255, 255, 255), 4, "lm", False))
    return finish(s, texts, "select_B_edit_suite.png")


# ---------------------------------------------------------------- C: HT ring
def option_c():
    s = ImageEnhance.Brightness(backdrop()).enhance(0.45)
    ring = ht_logo.logo(120, text=False)
    s.alpha_composite(ring, (160 - 60, 8))
    s.alpha_composite(big(sprite(TEAM[CHOSEN][0], "run_0"), 2), (160 - 32, 68 - 34))
    # faces round the ring, chosen one at the top with a glow
    import math
    for i, (c, _, _) in enumerate(TEAM):
        a = math.radians(-90 + (i - CHOSEN) * 60)
        x = round(160 + 54 * math.cos(a)) - 8
        y = round(68 + 54 * math.sin(a)) - 8
        d = ImageDraw.Draw(s)
        d.ellipse([(x - 3, y - 3), (x + 18, y + 18)], fill=(18, 14, 23, 255),
                  outline=(255, 255, 255, 255) if i == CHOSEN else (90, 84, 102, 255), width=1)
        s.alpha_composite(head(c), (x, y))
    logo_corner(s)
    texts = [(160, 152, TEAM[CHOSEN][1], (255, 255, 255), 10, "mm", False),
             (160, 163, TEAM[CHOSEN][2], (255, 226, 176), 5.5, "mm", False),
             (160, 174, "LEFT / RIGHT: TURN THE RING     SPACE: PLAY", (200, 195, 210), 4.5, "mm", False),
             (276, 14, "HT DASH", (255, 255, 255), 9, "mm", False)]
    return finish(s, texts, "select_C_ht_ring.png")


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    shots = [option_a(), option_b(), option_c()]
    sheet = Image.new("RGB", (W * 2 * 3 + 40, H * 2 + 60), (255, 255, 255))
    d = ImageDraw.Draw(sheet)
    for i, (im, label) in enumerate(zip(shots, ["A  Camera viewfinder", "B  Edit suite", "C  HT ring"])):
        sheet.paste(im.resize((W * 2, H * 2), Image.LANCZOS).convert("RGB"), (i * (W * 2 + 20), 50))
        d.text((i * (W * 2 + 20) + 4, 12), label, fill=(18, 14, 23), font=font(26))
    sheet.save(OUT / "select_options.png")
    print(f"wrote select mockups to {OUT}")
