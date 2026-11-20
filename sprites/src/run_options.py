"""Three alternative back-foot styles for Dan's run, side by side in one GIF.

    A  toe push-off: back leg stretches out with the toe on the ground
    B  heel kick: back foot flicks up behind, sole facing backwards
    C  short steps: small strides, both feet close to the ground
"""
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, str(Path(__file__).parent))
import dan_v2 as d  # noqa: E402

OPTIONS = {
    "A": {
        "contact": {24: (11, "JJjjjjjjjj"), 25: (10, "jjjj...JJJJ"), 26: (9, "jjjj.....JJJJ"),
                    27: (8, "jjj.......JJJ"), 28: (7, "fff........ffff"),
                    29: (6, "FF" + "." * 11 + "FFFFF")},
        "pass":    {24: (11, "JJjjjjjjjj"), 25: (11, "jjjj.JJJJ"), 26: (10, "jjjj..JJJJ"),
                    27: (9, "ffff...JJJJ"), 28: (9, "FFF....fffff"), 29: (16, "FFFFF")},
    },
    "B": {
        "contact": {24: (11, "JJjjjjjjjj"), 25: (10, "jjjj...JJJJ"), 26: (9, "jjjj.....JJJJ"),
                    27: (8, "jjj.......JJJ"), 28: (7, "fff........ffff"),
                    29: (6, "FF" + "." * 11 + "FFFFF")},
        "pass":    {24: (11, "JJjjjjjjjj"), 25: (5, "Ff...jjjjj.JJJJ"), 26: (5, "Ffjjjjjj....JJJJ"),
                    27: (16, "JJJJ"), 28: (16, "fffff"), 29: (16, "FFFFF")},
    },
    "C": {
        "contact": {24: (11, "JJjjjjjjjj"), 25: (11, "jjjj.JJJJ"), 26: (10, "jjjj..JJJJ"),
                    27: (9, "jjjj....JJJJ"), 28: (8, "ffff.....fffff"), 29: (8, "FFFF.....FFFFF")},
        "pass":    {24: (11, "JJjjjjjjjj"), 25: (11, "jjj.JJJJ"), 26: (12, "jjj.JJJ"),
                    27: (11, "ffff.JJJ"), 28: (11, "FFFF.fffff"), 29: (16, "FFFFF")},
    },
}


def frames(opt):
    d.LEGS["opt_contact"] = OPTIONS[opt]["contact"]
    d.LEGS["opt_pass"] = OPTIONS[opt]["pass"]
    grids = [
        d.pose("opt_contact", "L_back", "R_forward"),
        d.pose("opt_contact", "L_back", "R_forward", bob=1),
        d.pose("opt_pass", "L_down", "R_down"),
        d.pose("opt_contact", "L_forward", "R_down", swap=True),
        d.pose("opt_contact", "L_forward", "R_down", bob=1, swap=True),
        d.pose("opt_pass", "L_down", "R_down", swap=True),
    ]
    out = []
    for g in grids:
        im = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
        for y in range(32):
            for x in range(32):
                if g[y][x] != ".":
                    c = d.PALETTE[g[y][x]]
                    im.putpixel((x, y), tuple(int(c[i:i + 2], 16) for i in (1, 3, 5)) + (255,))
        out.append(im)
    return out


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    ground = Image.open(root / "backdrop" / "ground.png").convert("RGBA")
    sets = {k: frames(k) for k in OPTIONS}
    Z, cell = 6, 52
    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", 30)
    except OSError:
        font = ImageFont.load_default()
    gif = []
    for f in range(24):
        scene = Image.new("RGBA", (cell * 3, 44), (180, 230, 240, 255))
        g = ground.crop(((f * 3) % 160, 148, (f * 3) % 160 + cell * 3, 180))
        scene.alpha_composite(g.crop((0, 0, cell * 3, 8)), (0, 36))
        for i, k in enumerate(OPTIONS):
            scene.alpha_composite(sets[k][f % 6], (i * cell + 10, 6))
        big = scene.resize((scene.width * Z, scene.height * Z), Image.NEAREST)
        dr = ImageDraw.Draw(big)
        for i, k in enumerate(OPTIONS):
            dr.text((i * cell * Z + 14, 8), k, fill=(18, 14, 23), font=font)
        gif.append(big.convert("RGB"))
    gif[0].save(root / "dan" / "run_options.gif", save_all=True, append_images=gif[1:], duration=100, loop=0)
    # still sheet: each option's 6 frames in a row
    sheet = Image.new("RGBA", (6 * 34 * 4, 3 * 34 * 4), (236, 230, 214, 255))
    for r, k in enumerate(OPTIONS):
        for c, im in enumerate(sets[k]):
            sheet.alpha_composite(im.resize((128, 128), Image.NEAREST), (c * 136, r * 136))
    sheet.save(root / "dan" / "run_options_frames.png")
    print("wrote run_options.gif and run_options_frames.png")
