"""HT logo as pixel art: the ring of coloured segments round a black disc with "ht".

Colours are sampled from HT's logo, in order clockwise from 12 o'clock.
The same ring is reused for UI touches (see HT_COLOURS).

    python3 sprites/src/ht_logo.py

Writes sprites/ui/ht_logo.png (28x28, for the corner of every screen)
and sprites/ui/ht_logo_big.png (64x64).
"""
import math
from pathlib import Path
from PIL import Image

OUT = Path(__file__).resolve().parents[1] / "ui"

# clockwise from 12 o'clock, two segments each (36 segments of 10 degrees)
HT_COLOURS = [
    "#765443", "#c49782", "#657da0", "#566f41", "#8883b5", "#66bfad",   # brown, tan, slate, olive, lavender, mint
    "#d97e30", "#4f5ba9", "#c45b66", "#603b6a", "#9dbc3e", "#e1a22e",   # orange, indigo, coral, plum, lime, mustard
    "#383d97", "#47984a", "#b2383e", "#e5c41f", "#b85895", "#138aa8",   # navy, green, red, yellow, magenta, teal
]
INK = (18, 14, 23, 255)
GREY = (138, 138, 142, 255)

GLYPHS = {  # 3x5 pixel letters
    "h": ["x..", "x..", "xx.", "x.x", "x.x"],
    "t": [".x.", "xxx", ".x.", ".x.", ".xx"],
}


def hexc(h):
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5)) + (255,)


def logo(size, text=True):
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    c = (size - 1) / 2
    r_out = size / 2
    band = max(2.0, size * 0.11)          # coloured band thickness
    for y in range(size):
        for x in range(size):
            dx, dy = x - c, y - c
            r = math.hypot(dx, dy)
            if r > r_out - 0.2:
                continue
            ang = (math.degrees(math.atan2(dx, -dy)) + 360) % 360      # 0 at 12 o'clock, clockwise
            seg = int(ang // 10)
            if r >= r_out - band:
                im.putpixel((x, y), hexc(HT_COLOURS[(seg // 2) % 18]))
            elif r >= r_out - band - 1.2:
                im.putpixel((x, y), INK)                                 # thin gap
            elif r >= r_out - band - 1.2 - max(1.0, size * 0.05):
                im.putpixel((x, y), GREY if seg % 2 == 0 else INK)       # inner grey ticks
            else:
                im.putpixel((x, y), INK)                                 # black centre
    if text:
        scale = 1 if size < 48 else 2
        w = (3 + 1 + 3) * scale
        x0, y0 = round(c - w / 2 + 0.5), round(c - 5 * scale / 2 + 0.5)
        for i, ch in enumerate("ht"):
            for gy, rowp in enumerate(GLYPHS[ch]):
                for gx, p in enumerate(rowp):
                    if p == "x":
                        for sy in range(scale):
                            for sx in range(scale):
                                im.putpixel((x0 + (i * 4 + gx) * scale + sx, y0 + gy * scale + sy), (255, 255, 255, 255))
    return im


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    logo(28).save(OUT / "ht_logo.png")
    logo(64).save(OUT / "ht_logo_big.png")
    print(f"wrote {OUT}/ht_logo.png and ht_logo_big.png")
