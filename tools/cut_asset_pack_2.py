"""Cut 'source drawings/asset pack 2' into labelled sprites (and a few ready-made scenes).

Usage: python tools/cut_asset_pack_2.py sprites
"""
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image
from scipy import ndimage

SRC = Path(__file__).parent.parent / "source drawings" / "asset pack 2"
OUT = Path(sys.argv[1])
DEFAULT_SCALE = 0.37  # same as asset pack 1's photos
meta = {}

RED = np.array([196, 58, 58], np.float32)
BLUE = np.array([46, 118, 214], np.float32)
GREY = np.array([175, 175, 175], np.float32)


# ----------------------------------------------------------------- helpers
def load(name):
    rgb = np.asarray(Image.open(SRC / name).convert("RGB")).astype(np.float32)
    dark = 255 - rgb.min(axis=2)
    alpha = np.clip((dark - 35) / (150 - 35), 0, 1)
    col = np.clip(255 - (255 - rgb) / np.maximum(alpha, 1e-3)[..., None], 0, 255)
    return np.dstack([col, alpha * 255]), dark > 90


def comps(ink, grow=20, min_frac=0.0002):
    lab, _ = ndimage.label(ndimage.binary_dilation(ink, iterations=grow))
    H, W = ink.shape
    out = []
    for i, sl in enumerate(ndimage.find_objects(lab), 1):
        m = lab == i
        if (ink & m).sum() >= W * H * min_frac:
            out.append(m)
    return out


def bbox(mask):
    ys, xs = np.nonzero(mask)
    return xs.min(), ys.min(), xs.max() + 1, ys.max() + 1


def part(img, mask, fill_white=False):
    """RGBA of just this part (soft edges kept)."""
    m = ndimage.binary_dilation(mask, iterations=3)
    out = img.copy()
    out[..., 3] *= m
    if fill_white:
        inside = ndimage.binary_fill_holes(ndimage.binary_closing(mask, iterations=8)) & ~mask
        a = out[..., 3:4] / 255
        out[inside, :3] = (out[inside, :3] * a[inside] + 255 * (1 - a[inside]))
        out[inside, 3] = 255
    return out


def recolor(img, color):
    """Turn the ink into another marker colour, keeping its streaks."""
    out = img.copy()
    ink = out[..., 3] > 0
    dark = 255 - out[..., :3].mean(axis=2)
    ref = np.percentile(dark[out[..., 3] > 200], 90)
    k = np.clip(dark / max(ref, 1), 0, 1.15)[..., None]
    out[..., :3] = np.where(ink[..., None], 255 - (255 - color) * k, out[..., :3])
    return out


def save(rgba, rel, scale=DEFAULT_SCALE, box=None, pad=8):
    """Crop to the part (or to box = (x0, y0, x1, y1) for a shared canvas), scale, save."""
    if box is None:
        ys, xs = np.nonzero(rgba[..., 3] > 0)
        box = (max(xs.min() - pad, 0), max(ys.min() - pad, 0),
               min(xs.max() + pad + 1, rgba.shape[1]), min(ys.max() + pad + 1, rgba.shape[0]))
    x0, y0, x1, y1 = (int(v) for v in box)
    canvas = np.zeros((y1 - y0, x1 - x0, 4), np.float32)
    sx0, sy0, sx1, sy1 = max(x0, 0), max(y0, 0), min(x1, rgba.shape[1]), min(y1, rgba.shape[0])
    canvas[sy0 - y0:sy1 - y0, sx0 - x0:sx1 - x0] = rgba[sy0:sy1, sx0:sx1]
    im = Image.fromarray(canvas.round().clip(0, 255).astype(np.uint8), "RGBA")
    if scale != 1:
        im = im.resize((max(1, round(im.width * scale)), max(1, round(im.height * scale))), Image.LANCZOS)
    path = OUT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    im.save(path, optimize=True)
    meta[rel] = {"center": ((x0 + x1) / 2 * scale, (y0 + y1) / 2 * scale), "size": im.size, "scale": scale}
    print("saved", rel, im.size)
    return im


def union_box(masks, pad=10):
    xs0, ys0, xs1, ys1 = zip(*(bbox(m) for m in masks))
    return min(xs0) - pad, min(ys0) - pad, max(xs1) + pad, max(ys1) + pad


def frames_same_canvas(img, masks, rel_fmt, scale, align="center"):
    """Save several frames on one canvas size so they line up when animated."""
    boxes = [bbox(m) for m in masks]
    w = max(b[2] - b[0] for b in boxes) + 20
    h = max(b[3] - b[1] for b in boxes) + 20
    for i, (m, b) in enumerate(zip(masks, boxes), 1):
        cx = (b[0] + b[2]) // 2
        if align == "bottom":
            box = (cx - w // 2, b[3] + 10 - h, cx - w // 2 + w, b[3] + 10)
        else:
            cy = (b[1] + b[3]) // 2
            box = (cx - w // 2, cy - h // 2, cx - w // 2 + w, cy - h // 2 + h)
        save(part(img, m), rel_fmt.format(i), scale, box)


def ink_sorted(ink, grow=20, min_frac=0.0002, key=lambda b: (b[1], b[0])):
    cs = comps(ink, grow, min_frac)
    return sorted(cs, key=lambda m: key(bbox(m)))


# ----------------------------------------------------------------- simple single drawings
for src, rel, scale in [
    ("boot.jpg", "environment/items/boots.png", 0.15),
    ("circ saw.jpg", "environment/traps/circular_saw.png", 0.2),
    ("spikes.jpg", "environment/traps/spikes.png", 0.12),
    ("smoke puff double jump.jpg", "effects/jump_puff.png", 0.15),
    ("scarecrow hat.jpg", "characters/scarecrow/scarecrow_hat.png", 0.16),
    ("ground.jpg", "environment/ground_line.png", 0.52),
    ("I didnt.jpg", "ui/text/text_i_didnt_sign_for_this.png", 0.25),
    ("fire1.jpg", "effects/fire/fire_1.png", 0.15),
    ("fire2.jpg", "effects/fire/fire_2.png", 0.15),
]:
    img, ink = load(src)
    keep = np.zeros_like(ink)
    for m in comps(ink):
        keep |= m
    save(part(img, keep & ink | keep & (img[..., 3] > 0)), rel, scale)

# ice block: drawn in black, recoloured to blue marker
img, ink = load("ice block.jpg")
keep = np.zeros_like(ink)
for m in comps(ink):
    keep |= m
save(recolor(part(img, keep), BLUE), "effects/ice_block.png", 0.2)

# ----------------------------------------------------------------- separated pieces
img, ink = load("broken house.jpg")
wall, roof = ink_sorted(ink, key=lambda b: b[0])
s = 0.2
save(part(img, wall), "environment/buildings/house_broken_wall.png", s)
save(part(img, roof), "environment/buildings/house_broken_roof.png", s)
save(part(img, wall | roof), "environment/buildings/house_broken_full.png", s)

img, ink = load("speech.jpg")
for m, name in zip(ink_sorted(ink), ["speech_bubble_round", "speech_bubble_long", "speech_bubble_small"]):
    save(part(img, m), f"ui/speech/{name}.png", 0.3)

img, ink = load("hearts.jpg")
hearts = ink_sorted(ink, key=lambda b: b[0])
for i, m in enumerate(hearts, 1):
    save(part(img, m), f"ui/hearts/heart_{i}.png", 0.12)
# no empty heart was drawn: a faded grey copy of heart 2 stands in for it
empty = recolor(part(img, hearts[1]), GREY)
empty[..., 3] *= 0.6
save(empty, "ui/hearts/heart_empty_standin.png", 0.12)

img, ink = load("smoke.jpg")
smoke = ink_sorted(ink)
for i, m in enumerate(smoke, 1):
    save(part(img, m), f"effects/smoke/smoke_wisp_{i:02d}.png", 0.2)
save(part(img, np.any(smoke, axis=0)), "effects/smoke/smoke_full.png", 0.2)

img, ink = load("dash.jpg")
dash = ink_sorted(ink)
for i, m in enumerate(dash, 1):
    save(part(img, m), f"effects/dash/dash_line_{i:02d}.png", 0.2)
save(part(img, np.any(dash, axis=0)), "effects/dash/dash_full.png", 0.2)

img, ink = load("waaa.jpg")
letters = ink_sorted(ink, key=lambda b: b[0])
save(part(img, np.any(letters, axis=0)), "ui/text/text_waaa.png", 0.25)
for i, m in enumerate(letters, 1):
    save(part(img, m), f"ui/text/waaa_letters/waaa_{i:02d}.png", 0.25)

img, ink = load("the end.jpg")
cs = ink_sorted(ink)
frame = max(cs, key=lambda m: (bbox(m)[2] - bbox(m)[0]))
text = np.any([m for m in cs if m is not frame], axis=0)
save(part(img, frame), "ui/the_end/the_end_frame.png", 0.52)
save(part(img, text), "ui/the_end/the_end_text.png", 0.52)
save(part(img, frame | text), "ui/the_end/the_end_full.png", 0.52)

# alphabet: one picture per letter (dots of i / j stay with their letter)
img, ink = load("alphabet.jpg")
lab, n = ndimage.label(ndimage.binary_dilation(ink, iterations=6))
pieces = [lab == i for i in range(1, n + 1) if (ink & (lab == i)).sum() > 1500]
rows = {0: [], 1: []}
for m in pieces:
    x0, y0, x1, y1 = bbox(m)
    rows[0 if (y0 + y1) / 2 < 1790 else 1].append(m)
letters = []
for r in (0, 1):
    groups = []
    for m in sorted(rows[r], key=lambda m: bbox(m)[0]):
        x0, _, x1, _ = bbox(m)
        if groups and x0 < groups[-1][1] - 10:  # overlaps the previous letter: same letter
            groups[-1] = (groups[-1][0] | m, max(groups[-1][1], x1))
        else:
            groups.append((m, x1))
    letters += [g[0] for g in groups]
print("alphabet letters found:", len(letters))
for ch, m in zip("abcdefghijklmnopqrstuvwxyz", letters):
    save(part(img, m & ink), f"ui/alphabet/letter_{ch}.png", 0.25)

# ----------------------------------------------------------------- animation frames
img, ink = load("aura.jpg")
frames_same_canvas(img, ink_sorted(ink), "effects/aura/aura_{}.png", 0.3, align="bottom")

img, ink = load("power orb.jpg")
cs = ink_sorted(ink)
orbs = []
for m in cs:  # the first orb's inner core is a separate stroke: keep it with its orb
    if orbs and np.all(np.array(bbox(m)[:2]) >= np.array(bbox(orbs[-1])[:2])) and \
            np.all(np.array(bbox(m)[2:]) <= np.array(bbox(orbs[-1])[2:])):
        orbs[-1] = orbs[-1] | m
    else:
        orbs.append(m)
frames_same_canvas(img, orbs, "projectiles/power_orb/power_orb_{}.png", 0.2)

# ----------------------------------------------------------------- boss bar (both on one canvas)
e_img, e_ink = load("boss bar empty.jpg")
f_img, f_ink = load("boss bar full.jpg")
eb, fb = bbox(np.any(comps(e_ink), axis=0)), bbox(np.any(comps(f_ink), axis=0))
target_w = 1000
for img_, b, rel in ((e_img, eb, "ui/boss_bar/boss_bar_empty.png"), (f_img, fb, "ui/boss_bar/boss_bar_full.png")):
    crop = img_[b[1]:b[3], b[0]:b[2]]
    im = Image.fromarray(crop.round().clip(0, 255).astype(np.uint8), "RGBA").resize((target_w, 170), Image.LANCZOS)
    (OUT / rel).parent.mkdir(parents=True, exist_ok=True)
    im.save(OUT / rel, optimize=True)
    print("saved", rel, im.size)

# ----------------------------------------------------------------- lava: seamless strip + body
img, ink = load("lava.jpg")
keep = np.zeros_like(ink)
for m in comps(ink):
    keep |= m
lava = part(img, keep)
x0, y0, x1, y1 = bbox(keep)
strip = lava[y0 - 10:y1 + 10, x0:x1]
ov = 300  # cross-fade the ends so it repeats without a seam
w = strip.shape[1] - ov
t = np.linspace(0, 1, ov)[None, :, None]
tile = strip[:, :w].copy()
tile[:, :ov] = strip[:, w:] * (1 - t) + strip[:, :ov] * t
im = Image.fromarray(tile.round().clip(0, 255).astype(np.uint8), "RGBA")
im = im.resize((round(im.width * 0.5), round(im.height * 0.5)), Image.LANCZOS)
(OUT / "effects/lava").mkdir(parents=True, exist_ok=True)
im.save(OUT / "effects/lava/lava_surface.png", optimize=True)
print("saved effects/lava/lava_surface.png", im.size)
# body: the dotted part under the wavy line, repeated in both directions
line_bottom = int(np.percentile(np.nonzero(keep[:, (x0 + x1) // 2])[0], 15)) + 120
body = tile[line_bottom - (y0 - 10):]
hb = body.shape[0] // 2
body = np.concatenate([body, body[:hb, ::-1]], axis=0)  # stack a mirrored copy for a taller tile
im = Image.fromarray(body.round().clip(0, 255).astype(np.uint8), "RGBA")
im = im.resize((round(im.width * 0.5), round(im.height * 0.5)), Image.LANCZOS)
im.save(OUT / "effects/lava/lava_body.png", optimize=True)
print("saved effects/lava/lava_body.png", im.size)

# ----------------------------------------------------------------- menu buttons (+ red hover, grey disabled)
BUTTON_W = 600
img, ink = load("menu buttons.jpg")
cs = ink_sorted(ink)
boxes = []
for m in cs:  # each box swallows the letters inside it
    b = bbox(m)
    for bb in boxes:
        if b[0] >= bb[1][0] - 5 and b[2] <= bb[1][2] + 5 and b[1] >= bb[1][1] - 5 and b[3] <= bb[1][3] + 5:
            bb[0] |= m
            break
    else:
        boxes.append([m, b])
names = ["new_game", "continue", "settings", "quit_game"]
buttons = [(img, bm[0], n) for bm, n in zip(sorted(boxes, key=lambda bb: bb[1][1]), names)]
mimg, mink = load("main menu button.jpg")
buttons.append((mimg, np.any(comps(mink), axis=0), "main_menu"))
for im_, m, n in buttons:
    p = part(im_, m)
    b = bbox(m)
    sc = BUTTON_W / (b[2] - b[0] + 20)
    save(p, f"ui/buttons/button_{n}.png", sc)
    save(recolor(p, RED), f"ui/buttons/button_{n}_hover.png", sc)
    if n == "continue":
        save(recolor(p, GREY), "ui/buttons/button_continue_disabled.png", sc)

img, ink = load("settings wheel.jpg")
keep = np.any(comps(ink), axis=0)
p = part(img, keep)
b = bbox(keep)
sc = 150 / (b[2] - b[0] + 20)
save(p, "ui/settings_wheel.png", sc)
save(recolor(p, RED), "ui/settings_wheel_hover.png", sc)

# ----------------------------------------------------------------- scarecrow, in animatable parts
img, ink = load("scarecrow.jpg")
H, W = ink.shape
yy, xx = np.mgrid[0:H, 0:W]
head = ink & (yy < 1722) & (xx > 1050) & (xx < 1700)
arm_l = ink & (xx < 1020) & (yy >= 1760) & (yy < 2120)
arm_r = ink & (xx > 1780) & (yy >= 1760) & (yy < 2200)
pole = ink & (yy > 2905) & (xx > 1250) & (xx < 1600)
body = ink & ~head & ~arm_l & ~arm_r & ~pole & (yy >= 1700)
SC = 0.2
parts = {"head": (head, (1400, 1765)), "arm_left": (arm_l, (1030, 1985)), "arm_right": (arm_r, (1770, 1995)),
         "body": (body, (1420, 2900)), "pole": (pole, (1420, 2920))}
for name, (m, pivot) in parts.items():
    save(part(img, m, fill_white=name in ("head", "body")), f"characters/scarecrow/scarecrow_{name}.png", SC)
    meta[f"characters/scarecrow/scarecrow_{name}.png"]["pivot"] = (pivot[0] * SC, pivot[1] * SC)
save(part(img, ink, fill_white=False), "characters/scarecrow/scarecrow_full.png", SC)

(OUT / "asset_pack_2_parts.json").write_text(json.dumps(meta, indent=1, default=float))
