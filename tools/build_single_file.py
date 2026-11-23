"""Packs the whole game into one file, dist/HT-Dash.html, to send to someone.

Every image is embedded inside the HTML, so the file works on its own:
double-click it and it opens in the browser, no folder, no internet.

    python3 tools/build_single_file.py
"""
import base64
import re
from pathlib import Path

root = Path(__file__).resolve().parents[1]
html = (root / "index.html").read_text()

embed = {}
for png in sorted((root / "sprites").rglob("*.png")):
    rel = png.relative_to(root).as_posix()
    if "/src/" in rel or rel.endswith(("preview.png", "lineup.png", "options.png", "_frames.png", "_poses.png")):
        continue
    embed[rel] = "data:image/png;base64," + base64.b64encode(png.read_bytes()).decode()

# keep only images the game actually loads: full paths like "sprites/obstacles/cow_0.png",
# and numbered ones written as templates like `sprites/backdrop/port_far_${i}.png`
used = set(re.findall(r'"(sprites/[^"$]+\.png)"', html))
patterns = []
for tpl in re.findall(r'`(sprites/[^`]+\.png)`', html):
    patterns.append(re.compile("^" + re.sub(r"\\\$\\\{[^}]*\\\}", ".+", re.escape(tpl)) + "$"))
used |= {p for p in embed if any(rx.match(p) for rx in patterns)}
missing = sorted(p for p in used if p not in embed)
assert not missing, f"images the game loads but the build can't find: {missing}"
embed = {k: v for k, v in embed.items() if k in used}

data = "window.EMBED = {\n" + ",\n".join(f'  "{k}": "{v}"' for k, v in embed.items()) + "\n};"
out = html.replace("<script>\n\"use strict\";", f"<script>\n{data}\n</script>\n<script>\n\"use strict\";", 1)
assert out != html, "could not find the game script"
dist = root / "dist"
dist.mkdir(exist_ok=True)
(dist / "HT-Dash.html").write_text(out)
print(f"wrote dist/HT-Dash.html with {len(embed)} images, {len(out) // 1024} KB")
