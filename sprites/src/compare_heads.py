"""Builds sprites/dan/head_options.png: heads 1, 2 and 3 side by side,
standing and mid-run, plus each at roughly game size."""
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, str(Path(__file__).parent))
import dan  # noqa: E402

def img(grid):
    im = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
    for y, r in enumerate(grid):
        for x, ch in enumerate(r):
            if ch != ".":
                h = dan.PALETTE[ch]
                im.putpixel((x, y), tuple(int(h[i:i + 2], 16) for i in (1, 3, 5)) + (255,))
    return im

Z, BG = 8, (236, 230, 214, 255)
col_w = 32 * Z * 2 + 24
out = Image.new("RGBA", (col_w * 3 + 40, 32 * Z + 160), BG)
d = ImageDraw.Draw(out)
try:
    font = ImageFont.truetype("DejaVuSans-Bold.ttf", 36)
except OSError:
    font = ImageFont.load_default()
for i, key in enumerate("123"):
    x0 = 20 + i * col_w
    stand = img(dan.draw(dan.LEGS["stand"], "side", head=key))
    run = img(dan.draw(dan.LEGS["contact"], "back", lean=1, head=key))
    d.text((x0, 8), key, fill=(18, 14, 23), font=font)
    out.alpha_composite(stand.resize((32 * Z, 32 * Z), Image.NEAREST), (x0, 56))
    out.alpha_composite(run.resize((32 * Z, 32 * Z), Image.NEAREST), (x0 + 32 * Z + 8, 56))
    out.alpha_composite(stand.resize((96, 96), Image.NEAREST), (x0 + 32 * Z - 48, 32 * Z + 56))
path = Path(__file__).resolve().parents[1] / "dan" / "head_options.png"
out.save(path)
print(f"wrote {path}")
