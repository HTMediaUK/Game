"""Client landmarks for the hills, the plane in the sky, and the pie power-up.

Landmarks are generic buildings, with no client names or logos on them:
    hospital   Newcastle Hospitals
    field_cow  ARN (cows grazing in the fields)
    old_mine   Mining Remediation Authority
    plane      HII project (flies across the sky in the game)
    pie        power-up: Dan jumps twice as high for a while

    python3 sprites/src/landmarks.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import obstacles  # noqa: E402
from obstacles import Sprite  # noqa: E402

obstacles.PALETTE.update({
    "b": "#b05a3c", "B": "#7e3c2a",                   # brick
    "n": "#2a6fdb", "N": "#1d4fa0",                   # sign blue, plane stripe
    "e": "#a8dcf2", "E": "#5f93b8",                   # window glass
    "m": "#6a6f80", "M": "#4a4e5e",                   # roof slate / steel
    "t": "#9a6a40", "T": "#74492a",                   # timber boards
    "u": "#e8a24a", "U": "#b8722e", "i": "#ffd98a",   # pie crust
})

OUT = Path(__file__).resolve().parents[1] / "landmarks"


def hospital():
    s = Sprite(42, 28)
    s.rect(2, 9, 39, 27, "W")
    s.rect(34, 9, 39, 27, "w")                    # shaded right end
    s.rect(14, 4, 27, 9, "W"); s.rect(25, 4, 27, 9, "w")   # taller centre block
    s.rect(2, 9, 39, 9, "v"); s.rect(14, 4, 27, 4, "v")    # roof edges
    for y in (12, 16, 20):                        # rows of windows
        for x in range(4, 38, 4):
            if not (17 <= x <= 23 and y == 20):
                s.rect(x, y, x + 1, y + 1, "e")
                s.put(x + 1, y + 1, "E")
    for x in range(16, 26, 3):
        s.rect(x, 6, x + 1, 7, "e")
    s.rect(17, 22, 24, 22, "n")                   # entrance canopy
    s.rect(18, 23, 23, 27, "E"); s.rect(20, 23, 21, 27, "e")   # doors
    # blue hospital sign with a white H, on a post
    s.rect(4, 0, 10, 6, "n")
    s.rows(1, 5, ["W...W", "W...W", "WWWWW", "W...W", "W...W"])
    s.rect(7, 7, 7, 8, "G")
    return s.image()


def field_cow():
    """A small Friesian grazing in the fields (head down)."""
    s = Sprite(14, 10)
    s.rect(4, 2, 11, 5, "W"); s.rect(4, 5, 11, 5, "w")    # body
    s.rect(6, 2, 7, 3, "k"); s.rect(10, 4, 11, 5, "k")    # patches
    s.rect(1, 4, 3, 6, "k"); s.rect(1, 7, 2, 7, "p")      # head down, pink nose
    s.put(3, 3, "k")                                      # ear
    for x in (5, 10):
        s.rect(x, 6, x, 7, "w"); s.put(x, 8, "k")         # legs and hooves
    s.rect(12, 2, 12, 5, "k")                             # tail
    return s.image()


def old_mine():
    s = Sprite(36, 32)
    # brick winding house and chimney
    s.rect(19, 20, 34, 31, "b"); s.rect(31, 20, 34, 31, "B")
    for y in (23, 27):
        for x in (21, 26):
            s.rect(x, y, x + 2, y + 2, "E")
    for y in range(17, 20):                       # slate roof
        s.rect(19 - (y - 17), y, 34, y, "m")
    s.rect(29, 6, 31, 16, "b"); s.rect(31, 6, 31, 16, "B"); s.rect(28, 5, 32, 5, "B")
    # pit headframe: A-frame legs, cross braces and the winding wheel
    s.line(4, 31, 12, 8, "G"); s.line(5, 31, 13, 8, "M")
    s.line(20, 31, 14, 8, "G"); s.line(19, 31, 13, 8, "M")
    for y in (14, 20, 26):
        s.line(4 + (31 - y) // 3, y, 19 - (31 - y) // 4, y, "M")
    s.line(7, 26, 16, 14, "M")
    s.blob(13, 6, 5, 5, "a")
    s.blob(13, 6, 3.6, 3.6, "m")
    s.line(10, 6, 16, 6, "a"); s.line(13, 3, 13, 9, "a")
    s.put(13, 6, "h")
    return s.image()


def plane():
    s = Sprite(30, 14)
    for i, y in enumerate(range(1, 7)):                   # tall tail fin
        s.rect(1, y, 2 + i // 2, y, "W")
    s.rect(1, 1, 1, 6, "w")
    s.rect(1, 7, 6, 8, "W")                               # thin tail boom
    s.rect(5, 6, 22, 9, "W"); s.rect(5, 9, 22, 9, "w")    # fuselage
    s.rect(23, 6, 25, 9, "v"); s.rect(26, 7, 26, 8, "M")  # nose and spinner
    s.rect(27, 3, 27, 12, "G")                            # propeller
    s.rect(3, 8, 21, 8, "n")                              # blue stripe
    s.rect(17, 6, 21, 7, "e"); s.put(21, 7, "E")          # cabin windows
    s.rect(10, 4, 24, 4, "W"); s.rect(10, 5, 24, 5, "w")  # high wing
    s.line(14, 6, 16, 9, "v")                             # wing strut
    s.rect(18, 10, 18, 11, "M"); s.rect(17, 12, 19, 12, "a")   # wheel
    return s.image()


def pie():
    s = Sprite(18, 15)
    s.blob(8.5, 9, 7, 5.5, "u")                            # domed crust
    s.rect(4, 6, 7, 6, "i")
    s.rect(3, 7, 4, 7, "i")                                # shine
    s.put(8, 7, "U"); s.put(9, 8, "U"); s.put(11, 6, "U")  # steam vents
    for x in range(1, 17):                                 # crimped rim
        s.put(x, 10, "i" if x % 2 else "U")
    s.rect(1, 11, 16, 11, "H")                             # tin rim
    s.rect(2, 12, 15, 12, "h"); s.rect(3, 13, 14, 13, "G") # tapered tin
    im = s.image()
    for x, y in ((6, 0), (7, 1), (6, 2), (11, 0), (10, 1), (11, 2)):  # steam, no outline
        im.putpixel((x, y), (255, 255, 255, 210))
    return im


LANDMARKS = {"hospital": hospital, "old_mine": old_mine, "field_cow": field_cow}

if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    for name, fn in {**LANDMARKS, "plane": plane, "pie": pie}.items():
        fn().save(OUT / f"{name}.png")
    print(f"wrote landmarks to {OUT}")
