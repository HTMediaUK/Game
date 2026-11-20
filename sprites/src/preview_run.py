"""Builds sprites/dan/dan_run_preview.gif: Dan running with the drone overhead."""
from pathlib import Path
from PIL import Image, ImageDraw

root = Path(__file__).resolve().parents[1]
run = Image.open(root / "dan" / "dan_run_sheet.png").convert("RGBA")
drone = Image.open(root / "drone" / "drone_sheet.png").convert("RGBA")
fw = run.width // 6

SW, SH, Z = 96, 54, 6
SKY, GROUND, DASH = (236, 230, 214), (120, 104, 92), (90, 76, 68)
frames = []
for t in range(36):                      # 6 run loops at 10 fps
    scene = Image.new("RGBA", (SW, SH), SKY + (255,))
    d = ImageDraw.Draw(scene)
    d.rectangle([0, 46, SW, SH], fill=GROUND + (255,))
    d.line([0, 46, SW, 46], fill=(60, 50, 46, 255))
    for x in range(-12, SW + 12, 12):    # ground scrolls left
        xx = x - (t * 3) % 12
        d.line([xx, 50, xx + 4, 50], fill=DASH + (255,))
    bob = 0 if (t // 4) % 2 == 0 else 1
    scene.alpha_composite(drone.crop(((t % 2) * 24, 0, (t % 2) * 24 + 24, 10)), (34, 2 + bob))
    scene.alpha_composite(run.crop(((t % 6) * fw, 0, (t % 6) * fw + 32, 32)), (28, 15))
    frames.append(scene.resize((SW * Z, SH * Z), Image.NEAREST).convert("RGB"))
out = root / "dan" / "dan_run_preview.gif"
frames[0].save(out, save_all=True, append_images=frames[1:], duration=100, loop=0)
print(f"wrote {out}")
