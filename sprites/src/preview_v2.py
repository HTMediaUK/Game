"""Builds sprites/dan/dan_v2_preview.gif: Dan running, jumping and landing."""
from pathlib import Path
from PIL import Image

root = Path(__file__).resolve().parents[1]
bd = root / "backdrop"
D = lambda n: Image.open(root / "dan" / f"dan_v2_{n}.png").convert("RGBA")
run = [D(f"run_{i}") for i in range(6)]
up, down, land = D("jump_up"), D("jump_down"), D("land")
layers = [Image.open(bd / n).convert("RGBA") for n in ("sky.png", "clouds.png")]
far = [Image.open(bd / f"hills_far_{i}.png").convert("RGBA") for i in range(4)]
mid = [Image.open(bd / f"hills_mid_{i}.png").convert("RGBA") for i in range(4)]
ground = Image.open(bd / "ground.png").convert("RGBA")
W, H, Z = 320, 180, 3


def tile(dst, layer, off):
    o = int(off) % W
    dst.alpha_composite(layer, (-o, 0)); dst.alpha_composite(layer, (W - o, 0))


frames, dist, y, vy, clock, landing = [], 0.0, 0.0, 0.0, 0.0, 0
script = ["run"] * 24 + ["jump"] + ["run"] * 40 + ["jump"] + ["run"] * 30
for step in script:
    for _ in range(6):                       # 6 game ticks per GIF frame (10 fps)
        dist += 2.6
        if step == "jump" and y == 0 and vy == 0:
            vy = -5.3
        if vy or y:
            vy += 0.3; y += vy
            if y >= 0:
                y, vy, landing = 0, 0, 6
        else:
            clock += 0.16
        landing = max(0, landing - 1)
        step = "run"
    s = layers[0].copy(); tile(s, layers[1], dist * 0.05)
    tick = len(frames)
    tile(s, far[tick % 4], dist * 0.1); tile(s, mid[tick % 4], dist * 0.3); tile(s, ground, dist)
    img = (up if vy < 0 else down) if (vy or y) else land if landing else run[int(clock) % 6]
    s.alpha_composite(img, (60, 118 + round(y)))
    frames.append(s.crop((0, 40, W, H)).resize((W * Z, (H - 40) * Z), Image.NEAREST).convert("RGB"))
frames[0].save(root / "dan" / "dan_v2_preview.gif", save_all=True, append_images=frames[1:], duration=100, loop=0)
print("wrote dan_v2_preview.gif")
