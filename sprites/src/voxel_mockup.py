"""Mockup: Dan as a little 3D model made of cubes (voxels), rendered back into
pixel art from any angle, so a jump can show his sides and back.

His front is his current sprite exactly; depth is added per body part
(head, torso, arms, legs, trainers). Rendered with a tiny ray-marcher at low
resolution, flat shaded with light from the top left, then given the game's
dark outline.

    python3 sprites/src/voxel_mockup.py

Writes sprites/mockups/dan_turntable.png and sprites/mockups/dan_spin_jump.gif.
"""
import math
from pathlib import Path
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "mockups"
SPRITE = np.array(Image.open(ROOT / "characters" / "dan" / "stand.png").convert("RGBA"))
OUTLINE = np.array([0x12, 0x0e, 0x17])

HAIR = np.array([0xcf, 0x6a, 0x2c])
HAIR_DARK = np.array([0x8a, 0x3f, 0x1f])
SKIN = np.array([0xf2, 0xb4, 0x8c])
SKIN_SHADE = np.array([0xd0, 0x8a, 0x68])
SHIRT = np.array([0x2b, 0x28, 0x36])
JEANS = np.array([0x2c, 0x3a, 0x5c])
SHOE = np.array([0x2a, 0x24, 0x33])
SOLE = np.array([0xe4, 0xe8, 0xf0])

W, H, D = 32, 32, 14          # model grid: x across, y down, z front-to-back


def solid(x, y):
    px = SPRITE[y, x]
    return px[3] > 0 and not np.array_equal(px[:3], OUTLINE)


def build():
    """Colour grid (D, H, W, 3) and a filled mask."""
    col = np.zeros((D, H, W, 3), dtype=np.uint8)
    fill = np.zeros((D, H, W), dtype=bool)

    def put(x, y, z, c):
        if 0 <= x < W and 0 <= y < H and 0 <= z < D:
            col[z, y, x] = c
            fill[z, y, x] = True

    for y in range(H):
        for x in range(W):
            if not solid(x, y):
                continue
            front = SPRITE[y, x, :3]
            if y <= 14 and 9 <= x <= 22:                       # head
                edge = min(x - 9, 22 - x)                       # 0 at the sides
                for z in range(0, 12):
                    # round the head: trim the back corners and the top back edge
                    if edge == 0 and (z == 0 or z >= 10):
                        continue
                    if y <= 1 and z >= 10:
                        continue
                    if z == 0:
                        c = front                               # the drawn face, front layer only
                    elif y <= 5 or z >= 6:
                        c = HAIR if (y <= 9 or z >= 8) else HAIR_DARK   # hair over the top and back
                    elif edge <= 1 and 7 <= y <= 10 and 3 <= z <= 5:
                        c = SKIN_SHADE                          # ears
                    elif edge <= 1 and y <= 7:
                        c = HAIR_DARK                           # sideburns
                    else:
                        c = SKIN if y < 12 else SKIN_SHADE
                    put(x, y, z, c)
            elif y <= 23 and 10 <= x <= 21:                    # torso, back corners rounded
                edge = min(x - 10, 21 - x)
                for z in range(2, 10):
                    if edge == 0 and z in (2, 9):
                        continue
                    put(x, y, z, front if z == 2 else SHIRT)
            elif y <= 23:                                      # arms
                for z in range(4, 8):
                    put(x, y, z, front)
            elif y <= 27:                                      # legs
                for z in range(3, 8):
                    put(x, y, z, front if z == 3 else JEANS)
            else:                                              # trainers, toes forward
                for z in range(1, 9):
                    put(x, y, z, SOLE if y == 29 else SHOE)
    return col, fill


def render(col, fill, yaw, pitch=0.16, size=56, scale=1.0):
    """Orthographic ray-march. Returns an RGBA image `size` x `size`."""
    cx, cy, cz = 15.5, 15.5, 6.0
    cyw, syw, cp, sp = math.cos(yaw), math.sin(yaw), math.cos(pitch), math.sin(pitch)
    right = np.array([cyw, 0.0, -syw])
    fwd = np.array([syw * cp, sp, cyw * cp])                  # looking towards +z, tilted down
    up = np.cross(fwd, right)
    up = -up if up[1] > 0 else up                              # screen-down = +y in the grid
    u = (np.arange(size) - size / 2 + 0.5) / scale
    uu, vv = np.meshgrid(u, u)
    origin = (np.array([cx, cy, cz])[None, None, :]
              + uu[..., None] * right + vv[..., None] * (-up) - fwd * 40)
    pos = origin.copy()
    hit = np.zeros((size, size), dtype=bool)
    rgb = np.zeros((size, size, 3))
    prev = np.floor(pos).astype(int)
    light = np.array([-0.55, -1.0, -0.6])
    light /= np.linalg.norm(light)
    for _ in range(330):
        pos = pos + fwd * 0.25
        idx = np.floor(pos).astype(int)
        x, y, z = idx[..., 0], idx[..., 1], idx[..., 2]
        inside = (x >= 0) & (x < W) & (y >= 0) & (y < H) & (z >= 0) & (z < D) & ~hit
        if inside.any():
            filled = np.zeros_like(inside)
            filled[inside] = fill[z[inside], y[inside], x[inside]]
            if filled.any():
                d = idx - prev                                 # which face we came through
                normal = np.zeros(idx.shape)
                for a in range(3):
                    normal[..., a] = np.where(d[..., a] != 0, -np.sign(d[..., a]), 0)
                normal[(normal == 0).all(-1)] = [0, 0, -1]
                # front faces at full brightness, tops brighter, sides and back darker
                front_lit = float((np.array([0, 0, -1]) * light).sum())
                shade = 1.0 + 0.45 * ((normal * light).sum(-1) - front_lit)
                c = col[z.clip(0, D - 1), y.clip(0, H - 1), x.clip(0, W - 1)].astype(float)
                rgb[filled] = np.clip(c[filled] * shade[filled, None], 0, 255)
                hit |= filled
        prev = idx
    img = np.zeros((size, size, 4), dtype=np.uint8)
    img[hit, :3] = rgb[hit]
    img[hit, 3] = 255
    # the game's dark outline around the silhouette
    pad = np.pad(hit, 1)
    ring = (~hit) & (pad[:-2, 1:-1] | pad[2:, 1:-1] | pad[1:-1, :-2] | pad[1:-1, 2:])
    img[ring, :3] = OUTLINE
    img[ring, 3] = 255
    return Image.fromarray(img)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    col, fill = build()

    # game frames for Dan's spin jump: the model turning through 30-330 degrees
    # (front on, the game uses his drawn sprite)
    game_dir = ROOT / "characters" / "dan"
    for i, deg in enumerate(range(30, 331, 30)):
        render(col, fill, math.radians(deg)).save(game_dir / f"spin_{i:02d}.png")

    # turntable: eight angles, plus the current flat sprite for comparison
    angles = [i * math.pi / 4 for i in range(8)]
    views = [render(col, fill, a) for a in angles]
    sheet = Image.new("RGBA", (9 * 50, 60), (236, 230, 214, 255))
    flat = Image.fromarray(SPRITE)
    sheet.alpha_composite(flat, (9, 18))
    for i, v in enumerate(views):
        sheet.alpha_composite(v, (50 * (i + 1) - 3, 2))
    sheet.resize((sheet.width * 4, sheet.height * 4), Image.NEAREST).save(OUT / "dan_turntable.png")

    # spin jump on the game's backdrop: stand, rise and spin once, land
    bd = ROOT / "backdrop"
    scene_layers = [Image.open(bd / n).convert("RGBA") for n in ("sky.png", "clouds.png", "hills_far_0.png",
                                                                 "hills_mid_0.png", "ground.png")]
    frames = []
    n_air = 16
    steps = [0] * 6 + list(range(1, n_air + 1)) + [0] * 8
    for i, k in enumerate(steps):
        s = Image.new("RGBA", (320, 180))
        for layer in scene_layers:
            s.alpha_composite(layer, (-(i * 2) % 320 - 320, 0))
            s.alpha_composite(layer, (-(i * 2) % 320, 0))
        if k:
            t = k / (n_air + 1)
            height = round(4 * 50 * t * (1 - t))
            yaw = 2 * math.pi * min(1, t * 1.15)
        else:
            height, yaw = 0, 0.0
        facing_us = min(yaw, 2 * math.pi - yaw) < 0.35
        if facing_us:                                          # front on: his normal drawn sprite
            run = ROOT / "characters" / "dan" / f"run_{i % 6}.png"
            img = Image.open(run if not k else ROOT / "characters" / "dan" / "jump_up.png").convert("RGBA")
            s.alpha_composite(img, (60, 148 - 30 - height))
        else:                                                  # mid-spin: the 3D model
            s.alpha_composite(render(col, fill, yaw), (60 - 12, 148 - 44 - height))
        frames.append(s.crop((0, 30, 200, 160)).resize((600, 390), Image.NEAREST).convert("RGB"))
    frames[0].save(OUT / "dan_spin_jump.gif", save_all=True, append_images=frames[1:], duration=70, loop=0)
    print(f"wrote mockups to {OUT}")


if __name__ == "__main__":
    main()
