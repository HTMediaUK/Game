"""Deeper ground: turns the flat strip along the bottom of a ground layer into a wavy,
textured lower layer (darker soil, older concrete, packed gravel) so it reads as ground
going on down, not a band. The wave depends only on x and repeats every 320 pixels, so
every ground piece still joins up with its neighbours."""
import math
import random


def _mix(a, b, k):
    return tuple(round(a[i] + (b[i] - a[i]) * k) for i in range(3)) + (255,)


def deepen(img, upper, lower, seed=7, band=14):
    upper, lower = tuple(upper[:3]), tuple(lower[:3])
    W, H = img.size
    px = img.load()
    rng = random.Random(seed)
    edge = _mix(upper, lower, 0.6)
    fleck_l, fleck_d = _mix(lower, upper, 0.35), _mix(lower, (0, 0, 0), 0.22)
    top = H - band
    depth = [round(8 + 2.2 * math.sin(2 * math.pi * x / 80) + 1.3 * math.sin(2 * math.pi * x / 32 + 1.1))
             for x in range(W)]
    for x in range(W):
        for y in range(top, H):
            if px[x, y][:3] not in (upper, lower):
                continue                                  # keep speckles and details
            deep = y >= H - depth[x]
            px[x, y] = (lower if deep else upper) + (255,)
            if y == H - depth[x]:
                px[x, y] = edge                           # a soft line where the layers meet
    for _ in range(W // 3):                               # flecks in the deeper layer
        x, y = rng.randrange(W), rng.randrange(H - 9, H)
        if y > H - depth[x]:
            c = rng.choice((fleck_l, fleck_d, fleck_d))
            for dx in (0, 1):
                if px[(x + dx) % W, y][:3] == lower:
                    px[(x + dx) % W, y] = c
    for _ in range(W // 40):                              # a few buried stones
        x, y = rng.randrange(W), rng.randrange(H - 5, H - 1)
        if y - 1 > H - depth[x]:
            for dx, dy, c in ((0, 0, fleck_l), (1, 0, fleck_l), (0, 1, fleck_d), (1, 1, fleck_d)):
                px[(x + dx) % W, y + dy] = c
    return img
