"""Make a clearly marked placeholder image for every sprite that is still missing.

Each placeholder is a magenta dashed box with "PLACEHOLDER" and the sprite's name, sized for the
game's scale (the whiteboard is 1920 units wide, Orpheus is about 480 tall). Replace each file with
the real drawing, using the same name minus "placeholder_", and update the scenes using it.

Usage: python tools/make_placeholders.py sprites
Writes sprites/placeholders/**/placeholder_*.png and sprites/placeholders/PLACEHOLDERS.md
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

OUT = Path(sys.argv[1]) / "placeholders"
FONT = "C:/Windows/Fonts/arialbd.ttf"
MAGENTA = (214, 0, 160)

# (folder, name, width, height, shape, what it is / where it goes)
ITEMS = [
    ("stage_3", "enemy", 260, 300, "rect", "Stage 3: bad guy"),
    ("stage_4", "arena_background", 1920, 1164, "rect", "Stage 4: castle arena (inside walls), fills the board"),
    ("stage_4", "ground_cracks", 700, 160, "rect", "Stage 4: cracks when Daven rises"),
    ("stage_4", "dust", 400, 200, "ellipse", "Stage 4: dust when Daven rises"),
    ("stage_4", "robot", 260, 360, "rect", "Stage 4: robot"),
    ("stage_4", "orpheus_eyes_closed", 60, 32, "rect", "Stage 4: Orpheus closed eyes (Orpheus face scale)"),
    ("stage_4", "daven_frozen", 900, 1000, "rect", "Stage 4: ice over Daven, frozen in place and time"),
    ("stage_4", "explosion", 900, 900, "ellipse", "Stage 4: final explosion / blast"),
    ("intro", "classroom_pov", 1920, 1080, "rect", "Intro: classroom seen from a student's desk"),
    ("intro", "whiteboard_frame", 1600, 900, "rect", "Intro: empty whiteboard frame"),
    ("intro", "board_math", 1200, 600, "rect", "Intro: math written on the board"),
    ("intro", "desk_and_arms", 1920, 500, "rect", "Intro: desk + the student's arms"),
    ("intro", "eyelid_top", 1920, 600, "rect", "Intro: top eyelid closing"),
    ("intro", "eyelid_bottom", 1920, 600, "rect", "Intro: bottom eyelid closing"),
]


def font(size):
    return ImageFont.truetype(FONT, max(8, int(size)))


def dashed(d, box, shape, width, dash):
    x0, y0, x1, y1 = box
    if shape == "ellipse":
        d.ellipse(box, outline=MAGENTA, width=width)  # ellipses stay solid; the fill marks them
        return
    for (ax, ay, bx, by) in ((x0, y0, x1, y0), (x1, y0, x1, y1), (x1, y1, x0, y1), (x0, y1, x0, y0)):
        length = max(abs(bx - ax), abs(by - ay))
        steps = max(1, int(length // (dash * 2)))
        for i in range(steps + 1):
            t0, t1 = i * 2 * dash / length, min((i * 2 + 1) * dash / length, 1)
            if t0 > 1:
                break
            d.line([(ax + (bx - ax) * t0, ay + (by - ay) * t0), (ax + (bx - ax) * t1, ay + (by - ay) * t1)],
                   fill=MAGENTA, width=width)


def make(name, w, h, shape):
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    lw = max(2, min(w, h) // 30)
    box = (lw // 2, lw // 2, w - 1 - lw // 2, h - 1 - lw // 2)
    if shape == "ellipse":
        d.ellipse(box, fill=(255, 220, 245, 170))
    else:
        d.rectangle(box, fill=(255, 220, 245, 170))
    dashed(d, box, shape, lw, max(6, min(w, h) // 8))
    # label: "PLACEHOLDER" + the name, as big as fits
    label = name.replace("_", " ")
    small = min(h * 0.18, w * 0.11)
    if small < 12:  # tiny sprite: no room for the "PLACEHOLDER" line
        small = 0
    size = 0
    for s in range(int(min(h * 0.4 if small else h * 0.7, 200)), 8, -1):
        if d.textlength(label, font=font(s)) <= w * 0.86 and s + small * 1.2 <= h * 0.85:
            size = s
            break
    if size == 0:  # still too small for the name: just "PH"
        label, size = "PH", max(9, int(h * 0.55))
    y = (h - (small * 1.2 + size)) / 2
    if small:
        d.text((w / 2, y), "PLACEHOLDER", font=font(small), fill=MAGENTA, anchor="mt")
    d.text((w / 2, y + small * 1.2), label, font=font(size), fill=(60, 0, 50), anchor="mt")
    return im


lines = ["# Placeholder sprites",
         "",
         "Every sprite that is still missing has a placeholder here: a **magenta dashed box** with",
         "\"PLACEHOLDER\" and its name, so it's impossible to miss in the game. Use them in scenes while",
         "the drawings aren't done. To replace one: draw it, save it in the right `sprites/` folder (same",
         "name without `placeholder_`), then in each scene that uses it, drag the new drawing onto the",
         "node's **Texture** in the Inspector. Once nothing uses a placeholder any more, delete it and its row.",
         "",
         "Regenerate them all with `python tools/make_placeholders.py sprites`.",
         "",
         "| Placeholder file | Size (px) | What it stands for |",
         "|---|---|---|"]
for folder, name, w, h, shape, what in ITEMS:
    rel = f"{folder}/placeholder_{name}.png"
    path = OUT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    make(name, w, h, shape).save(path, optimize=True)
    lines.append(f"| `sprites/placeholders/{rel}` | {w} × {h} | {what} |")
    print("made", rel)
lines += ["",
          "Also placeholders (made earlier, used in the main menu):",
          "- the **New game / Continue / Quit game** buttons in `scenes/menus/main_menu.tscn` are drawn by",
          "  Godot with `scenes/menus/placeholder_menu_theme.tres`",
          "- `sprites/ui/placeholder_settings_wheel.png` (the gear in the menu)",
          ""]
(OUT / "PLACEHOLDERS.md").write_text("\n".join(lines), encoding="utf-8", newline="\n")
print(len(ITEMS), "placeholders")
