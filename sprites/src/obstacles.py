"""Obstacles for Dan to jump over, in the same chunky outlined style.

Camera kit: tripod with camera, flight case (single and stacked), softbox light.
Animals: sheep and Friesian cow, two frames each so their legs shuffle.
Animals face left, towards Dan. Light comes from the top left.

    python3 sprites/src/obstacles.py

Writes one PNG per frame to sprites/obstacles/ plus a line-up preview.
"""
import math
from pathlib import Path
from PIL import Image

OUT = Path(__file__).resolve().parents[1] / "obstacles"

PALETTE = {
    "o": "#120e17",                                   # outline
    "a": "#24222e", "g": "#3a3d4e", "G": "#727892",   # black kit, greys
    "h": "#a9b0c8", "H": "#dfe4ee",                   # aluminium
    "r": "#e43b44", "l": "#2f7fc1", "L": "#8fd3ff",   # tally light, lens glass
    "W": "#ffffff", "w": "#e3e6ee", "v": "#c3c8d6",   # white, wool / hide shade
    "d": "#2a2430", "D": "#4a4452",                   # sheep's face and legs
    "k": "#26222c", "K": "#3d3845",                   # cow patches
    "p": "#f2a0a8", "P": "#d07a86",                   # pink nose, udder
    "c": "#efe3c4",                                   # horns
}


class Sprite:
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.g = [["."] * w for _ in range(h)]

    def put(self, x, y, ch):
        if 0 <= x < self.w and 0 <= y < self.h:
            self.g[y][x] = ch

    def rect(self, x0, y0, x1, y1, ch):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                self.put(x, y, ch)

    def rows(self, y0, x0, lines):
        for j, line in enumerate(lines):
            for i, ch in enumerate(line):
                if ch != ".":
                    self.put(x0 + i, y0 + j, ch)

    def line(self, x0, y0, x1, y1, ch):
        steps = max(abs(x1 - x0), abs(y1 - y0))
        for s in range(steps + 1):
            self.put(round(x0 + (x1 - x0) * s / steps), round(y0 + (y1 - y0) * s / steps), ch)

    def blob(self, cx, cy, rx, ry, ch):
        for y in range(self.h):
            for x in range(self.w):
                if ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= 1:
                    self.put(x, y, ch)

    def image(self):
        # auto outline, then paint
        filled = {(x, y) for y in range(self.h) for x in range(self.w) if self.g[y][x] != "."}
        for y in range(self.h):
            for x in range(self.w):
                if self.g[y][x] == "." and any(
                    (x + dx, y + dy) in filled for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))
                ):
                    self.g[y][x] = "o"
        im = Image.new("RGBA", (self.w, self.h), (0, 0, 0, 0))
        for y in range(self.h):
            for x in range(self.w):
                ch = self.g[y][x]
                if ch != ".":
                    c = PALETTE[ch]
                    im.putpixel((x, y), tuple(int(c[i:i + 2], 16) for i in (1, 3, 5)) + (255,))
        return im


def tripod():
    s = Sprite(19, 27)
    # camera body with a top handle, pointing right
    s.rect(4, 1, 9, 1, "H"); s.put(4, 2, "h"); s.put(9, 2, "h")
    s.rect(2, 3, 11, 8, "a")
    s.rect(2, 3, 11, 3, "G"); s.rect(2, 3, 2, 8, "g")
    s.rect(4, 5, 7, 6, "g")                       # flip-out screen
    s.put(10, 4, "r")                             # recording light
    s.rect(12, 4, 15, 7, "g"); s.rect(12, 4, 15, 4, "G")   # lens
    s.rect(16, 4, 16, 7, "h"); s.put(16, 5, "L"); s.put(16, 6, "l")
    # tripod head and legs
    s.rect(6, 9, 7, 10, "h"); s.rect(4, 11, 9, 11, "G")
    s.line(6, 12, 2, 25, "h"); s.line(7, 12, 3, 25, "H")   # near left leg
    s.line(6, 12, 6, 25, "G")                               # back leg
    s.line(7, 12, 11, 25, "h"); s.line(8, 12, 12, 25, "G")  # near right leg
    s.line(4, 19, 10, 19, "G")                              # spreader
    for x in (2, 3, 6, 11, 12):
        s.put(x, 25, "a")                                   # rubber feet
    return s.image()


def case_body(s, y0):
    """One 20x12 flight case with its top-left corner at (0, y0)."""
    s.rect(1, y0 + 2, 18, y0 + 12, "a")
    s.rect(1, y0 + 2, 18, y0 + 2, "H"); s.rect(1, y0 + 2, 1, y0 + 12, "H")   # lit edges
    s.rect(18, y0 + 3, 18, y0 + 12, "G"); s.rect(2, y0 + 12, 18, y0 + 12, "G")
    s.rect(2, y0 + 5, 17, y0 + 5, "h")                      # lid seam
    for cx, cy in ((1, 2), (17, 2), (1, 11), (17, 11)):     # corner caps
        s.rect(cx, y0 + cy, cx + 1, y0 + cy + 1, "h")
    s.put(1, y0 + 2, "H")
    s.rect(4, y0 + 5, 5, y0 + 6, "H"); s.rect(14, y0 + 5, 15, y0 + 6, "H")    # latches
    s.rect(8, y0, 11, y0, "h"); s.put(8, y0 + 1, "G"); s.put(11, y0 + 1, "G")  # handle
    # "HT" stencilled on the side
    s.rows(y0 + 7, 6, ["W.W.WWW", "WWW..W.", "W.W..W.", "W.W..W."])


def flight_case():
    s = Sprite(20, 14)
    case_body(s, 0)
    return s.image()


def flight_cases_stacked():
    s = Sprite(20, 26)
    case_body(s, 12)
    case_body(s, 0)
    return s.image()


def softbox():
    s = Sprite(16, 34)
    s.rect(1, 0, 14, 11, "w"); s.rect(2, 1, 13, 10, "W")    # diffuser panel, facing us
    s.rect(1, 0, 14, 0, "G"); s.rect(14, 0, 14, 11, "G"); s.rect(1, 11, 14, 11, "G")
    s.rect(1, 0, 1, 11, "h")
    s.rect(3, 2, 6, 3, "H")                                  # glow
    s.rect(7, 12, 8, 13, "a")                                # mount
    s.rect(7, 14, 7, 29, "h"); s.rect(8, 14, 8, 29, "G")    # pole
    s.line(7, 29, 2, 32, "h"); s.line(8, 29, 13, 32, "G"); s.rect(7, 30, 8, 32, "G")
    return s.image()


def sheep(frame):
    s = Sprite(22, 17)
    # legs first (behind the wool); the pairs swap between frames
    legs = [(7, 14), (10, 16)] if frame == 0 else [(8, 15), (9, 17)]
    for x_front, x_back in legs:
        for x in (x_front, x_back):
            s.rect(x, 11, x, 15, "d")
    # woolly body: a blob with bumpy edges
    s.blob(13, 7, 8, 5, "w")
    for bx in (7, 10, 13, 16, 19):
        s.blob(bx, 3, 2.2, 2, "W")
    s.blob(12, 6, 7, 4, "W")
    s.rect(7, 10, 19, 11, "v")                              # shadow underneath
    # black face, ear and a woolly cap
    s.rect(1, 4, 5, 9, "d"); s.rect(1, 4, 3, 5, "D")
    s.put(6, 4, "d"); s.put(7, 5, "D")                      # ear
    s.rect(3, 3, 6, 3, "W")
    s.put(2, 6, "W")                                        # eye
    s.put(0, 8, "d")                                        # nose
    return s.image()


def cow(frame):
    s = Sprite(32, 24)
    leg_x = [9, 13, 23, 27] if frame == 0 else [10, 12, 24, 26]
    for x in leg_x:
        s.rect(x, 16, x + 1, 21, "w")
        s.rect(x, 22, x + 1, 22, "k")                       # hooves
    s.rect(9, 5, 29, 16, "W")                               # body
    s.rect(9, 15, 29, 16, "w")                              # belly shade
    s.blob(15, 8, 4, 3, "k"); s.blob(24, 12, 4, 3, "k"); s.blob(27, 6, 2.5, 2, "k")
    s.rect(20, 17, 23, 17, "p"); s.put(21, 18, "P"); s.put(23, 18, "P")  # udder
    s.line(30, 6, 31, 14, "k")                              # tail
    s.rect(30, 15, 31, 16, "K")
    # head: black with a white blaze, pink muzzle, horns and ear
    s.rect(1, 3, 8, 12, "k"); s.rect(1, 3, 4, 4, "K")
    s.rect(3, 4, 4, 10, "W")                                # blaze
    s.rect(0, 10, 5, 13, "p"); s.put(1, 12, "P"); s.put(4, 12, "P")
    s.put(6, 6, "W")                                        # eye glint
    s.put(2, 2, "c"); s.put(6, 2, "c"); s.put(1, 1, "c"); s.put(7, 1, "c")
    s.rect(8, 4, 9, 5, "K")                                 # ear
    return s.image()


SPRITES = {
    "tripod": [tripod()],
    "flight_case": [flight_case()],
    "flight_cases_stacked": [flight_cases_stacked()],
    "softbox": [softbox()],
    "sheep": [sheep(0), sheep(1)],
    "cow": [cow(0), cow(1)],
}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for name, frames in SPRITES.items():
        for i, im in enumerate(frames):
            im.save(OUT / (f"{name}_{i}.png" if len(frames) > 1 else f"{name}.png"))
    # line-up on a plain ground strip
    gap, z = 10, 6
    width = sum(f[0].width for f in SPRITES.values()) + gap * (len(SPRITES) + 1)
    height = max(f[0].height for f in SPRITES.values()) + 8
    lineup = Image.new("RGBA", (width, height), (236, 230, 214, 255))
    for x in range(width):
        for y in range(height - 4, height):
            lineup.putpixel((x, y), (98, 177, 60, 255))
    x = gap
    for frames in SPRITES.values():
        im = frames[0]
        lineup.alpha_composite(im, (x, height - 4 - im.height))
        x += im.width + gap
    lineup.resize((width * z, height * z), Image.NEAREST).save(OUT / "obstacles_lineup.png")
    print(f"wrote obstacles to {OUT}")


if __name__ == "__main__":
    main()
