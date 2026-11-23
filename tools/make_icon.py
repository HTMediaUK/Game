"""Makes sprites/ui/app_icon.png, the home-screen icon: the HT logo, drawn smoothly
(drawn large, then scaled down), on HT Dash's dark background.

    python3 tools/make_icon.py
"""
import math
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "sprites" / "src"))
from ht_logo import HT_COLOURS  # noqa: E402

BIG, SIZE = 2048, 512
im = Image.new("RGB", (BIG, BIG), (14, 12, 18))
d = ImageDraw.Draw(im)
c, R = BIG / 2, BIG * 0.40
box = lambda r: [c - r, c - r, c + r, c + r]
for k in range(36):
    a0, a1 = -90 + k * 10 + 0.9, -90 + k * 10 + 9.1
    d.pieslice(box(R), a0, a1, fill=HT_COLOURS[(k >> 1) % 18])
    d.pieslice(box(R * 0.8), a0, a1, fill=(14, 12, 18))
    inner = ["#5b5b5d", "#77777a"][k % 2] if k < 18 else ["#cfd0d2", "#e6e7e8"][k % 2]
    d.pieslice(box(R * 0.74), a0 + 1, a1 - 1, fill=inner)
    d.pieslice(box(R * 0.6), a0, a1, fill=(14, 12, 18))
d.ellipse(box(R * 0.56), fill=(22, 20, 26))
try:
    font = ImageFont.truetype("DejaVuSans-Bold.ttf", int(R * 0.62))
except OSError:
    font = ImageFont.load_default()
d.text((c, c), "ht", fill="white", font=font, anchor="mm")
im.resize((SIZE, SIZE), Image.LANCZOS).save(ROOT / "sprites" / "ui" / "app_icon.png")
print("wrote sprites/ui/app_icon.png")
