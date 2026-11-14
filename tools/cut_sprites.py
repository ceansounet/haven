"""Cut the Haven drawings into separate transparent sprites.

Usage: python cut.py <asset pack dir> <output sprites dir>
Writes PNGs plus parts.json (positions/pivots used to build the Godot rigs).
"""
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image
from scipy import ndimage

SRC = Path(sys.argv[1])
OUT = Path(sys.argv[2])
MAX_SIDE = 1500  # big photos are scaled so the whole drawing fits in this many pixels
meta = {}


# ---------------------------------------------------------------- helpers
def load(name):
    """Return (rgba float array 0..255 with background removed, ink mask, scale)."""
    im = Image.open(SRC / name)
    if im.mode == "RGBA":
        a = np.asarray(im).astype(np.float32)
        return a, a[:, :, 3] > 40, 1.0
    rgb = np.asarray(im.convert("RGB")).astype(np.float32)
    dark = 255 - rgb.min(axis=2)
    alpha = np.clip((dark - 35) / (150 - 35), 0, 1)
    safe = np.maximum(alpha, 1e-3)[..., None]
    col = np.clip(255 - (255 - rgb) / safe, 0, 255)  # un-mix the white paper
    out = np.dstack([col, alpha * 255])
    W, H = im.size
    scale = min(1.0, MAX_SIDE / max(W, H))
    return out, dark > 90, scale


def components(ink, grow, min_frac):
    grown = ndimage.binary_dilation(ink, iterations=grow) if grow else ink
    lab, _ = ndimage.label(grown)
    H, W = ink.shape
    res = []
    for i, sl in enumerate(ndimage.find_objects(lab), 1):
        m = lab == i
        if (ink & m).sum() >= W * H * min_frac:
            res.append(m)
    return res


def split_bolts(ink, frac, minsize):
    """Pixels belonging to thick strokes (lightning) vs thin ones (cloud outline)."""
    d = ndimage.distance_transform_edt(ink)
    ridge = d[(d >= ndimage.maximum_filter(d, 5)) & ink]
    hw = np.percentile(ridge, 90)
    core = d > hw * frac
    lab, n = ndimage.label(ndimage.binary_dilation(core, iterations=int(hw)))
    sizes = ndimage.sum(core, lab, range(1, n + 1))
    core = core & np.isin(lab, 1 + np.nonzero(sizes > minsize * core.sum())[0])
    return ink & ndimage.binary_dilation(core, iterations=int(hw * 1.6))


def box(shape, x0, y0, x1, y1):
    m = np.zeros(shape, bool)
    m[int(y0):int(y1), int(x0):int(x1)] = True
    return m


def save(img, mask, rel, scale, pivot=None, pad=6, canvas=None):
    """Save the masked part. Returns placement info in scaled source-image pixels."""
    mask = ndimage.binary_dilation(mask, iterations=3)
    ys, xs = np.nonzero(mask & (img[:, :, 3] > 0))
    if canvas is None:
        x0, y0 = max(xs.min() - pad, 0), max(ys.min() - pad, 0)
        x1, y1 = min(xs.max() + pad + 1, img.shape[1]), min(ys.max() + pad + 1, img.shape[0])
    else:
        x0, y0, x1, y1 = canvas
    part = img[y0:y1, x0:x1].copy()
    part[:, :, 3] *= mask[y0:y1, x0:x1]
    pim = Image.fromarray(part.round().astype(np.uint8), "RGBA")
    if scale != 1.0:
        pim = pim.resize((max(1, round(pim.width * scale)), max(1, round(pim.height * scale))), Image.LANCZOS)
    path = OUT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    pim.save(path, optimize=True)
    info = {"center": [(x0 + x1) / 2 * scale, (y0 + y1) / 2 * scale], "size": [pim.width, pim.height]}
    if pivot is not None:
        info["pivot"] = [pivot[0] * scale, pivot[1] * scale]
    meta[rel] = info
    print("saved", rel, pim.size)
    return info


def whole(name, rel, grow=25):
    img, ink, s = load(name)
    keep = np.zeros_like(ink)
    for m in components(ink, grow, 0.0004):
        keep |= m
    save(img, keep & ink | (keep & (img[:, :, 3] > 0)), rel, s)


# ---------------------------------------------------------------- Orpheus
img, ink, s = load("Orpheus dino asset pack.png")
c = components(ink, 2, 0.00005)
O = "characters/orpheus/"
# indices follow the scan order printed by analyze.py
parts = {
    "mouths/orpheus_mouth_frown.png": [c[1]],
    "mouths/orpheus_mouth_wobbly.png": [c[3]],
    "mouths/orpheus_mouth_flat.png": [c[7]],
    "mouths/orpheus_mouth_zigzag.png": [c[0]],
    "mouths/orpheus_mouth_smile.png": [c[5]],
    "mouths/orpheus_mouth_open.png": [c[6]],
    "eyes/orpheus_eyebrows_worried.png": [c[8], c[9]],
    "eyes/orpheus_eyebrows_angry.png": [c[10], c[11]],
    "eyes/orpheus_eyes_wavy.png": [c[13]],
    "eyes/orpheus_eyes_happy.png": [c[14], c[15]],
}
for rel, ms in parts.items():
    save(img, np.any(ms, axis=0), O + rel, s)
save(img, c[2], O + "orpheus_body.png", s, pivot=(170, 340))
save(img, c[4], O + "orpheus_arm_raised.png", s, pivot=(255, 115))
save(img, c[12], O + "orpheus_arm_down.png", s, pivot=(280, 155))
save(img, c[16], O + "orpheus_tail.png", s, pivot=(66, 285))
save(img, c[17], O + "orpheus_hand_1.png", s, pivot=(278, 292))
save(img, c[18], O + "orpheus_hand_2.png", s, pivot=(307, 292))
save(img, c[19], O + "orpheus_leg_back.png", s, pivot=(80, 350))
save(img, c[20], O + "orpheus_leg_front.png", s, pivot=(235, 376))

# ---------------------------------------------------------------- Daven
img, ink, s = load("daven.jpg")
c = components(ink, 2, 0.00003)
D = "characters/daven/"
P = 4032 / 1400  # analyze preview -> original pixels
shape = ink.shape
arm_l = c[0] & box(shape, 140 * P, 622 * P, 233 * P, 714 * P)
foot_l = c[0] & box(shape, 0, 915 * P, 320 * P, 9999)
body_from_c0 = c[0] & box(shape, 222 * P, 600 * P, 9999, 9999) & ~arm_l & ~foot_l
arm_r = c[2] & box(shape, 800 * P, 0, 9999, 712 * P)
spikes = (c[0] & ~arm_l & ~foot_l & ~body_from_c0) | c[1] | c[3]
body = (c[2] & ~arm_r) | body_from_c0
save(img, spikes, D + "daven_spikes.png", s, pivot=(1500, 2700))
save(img, body, D + "daven_body.png", s, pivot=(1500, 2700))
save(img, arm_l, D + "daven_arm_left.png", s, pivot=(660, 1960))
save(img, arm_r, D + "daven_arm_right.png", s, pivot=(2310, 1980))
save(img, foot_l, D + "daven_foot_left.png", s, pivot=(800, 2700))
save(img, c[11], D + "daven_foot_right.png", s, pivot=(1950, 2740))
save(img, c[5], D + "daven_eye_left.png", s)
save(img, c[4], D + "daven_eye_right.png", s)
save(img, c[7] | c[9] | c[10], D + "daven_cheek_left.png", s)
save(img, c[6], D + "daven_cheek_right.png", s)
save(img, c[8], D + "daven_mouth.png", s)

# ---------------------------------------------------------------- environment sheet
img, ink, s = load("environment.jpg")
s = 1.0 / 3  # items are small on this sheet; a third keeps blocks ~110 px
c = components(ink, 20, 0.0004)
names = ["items/wand.png", "items/key.png", "effects/zigzag_1.png", "effects/zigzag_2.png",
         "blocks/block_mystery.png", "blocks/block_cracked.png", "blocks/block_brick.png",
         "blocks/block_plain.png", "buildings/house.png", "props/fence_gate.png"]
for m, rel in zip(c, names):
    save(img, m, "environment/" + rel if not rel.startswith("effects") else rel, s)

# ---------------------------------------------------------------- clouds (3 clouds; inner strokes merged)
img, ink, s = load("clouds.jpg")
c = components(ink, 25, 0.0004)
c[2] = c[2] | c[3] | c[4] | c[5]
for i, m in enumerate([c[1], c[0], c[2]], 1):
    save(img, m, f"environment/background/cloud_{i}.png", s)

# ---------------------------------------------------------------- raindrops
img, ink, s = load("raindrops.jpg")
c = components(ink, 10, 0.0004)
order = [(1, "streak_long"), (0, "streak_curved"), (2, "dot"), (3, "streak_slanted"),
         (4, "drop_small"), (5, "drop_big")]
for i, name in order:
    save(img, c[i], f"effects/rain/raindrop_{name}.png", s)

# ---------------------------------------------------------------- trampoline: 5 frames, same canvas, feet aligned
img, ink, s = load("trampoline.jpg")
img = np.pad(img, ((200, 200), (200, 200), (0, 0)))
ink = np.pad(ink, 200)
c = components(ink, 10, 0.0004)
bbs = []
for m in c:
    ys, xs = np.nonzero(m & ink)
    bbs.append((xs.min(), ys.min(), xs.max(), ys.max()))
w = max(b[2] - b[0] for b in bbs) + 20
h = max(b[3] - b[1] for b in bbs) + 20
labels = ["stretched_high", "stretched", "rest", "squashed", "squashed_deep"]
for i, (m, b) in enumerate(zip(c, bbs)):
    cx = (b[0] + b[2]) // 2
    canvas = (cx - w // 2, b[3] + 10 - h, cx - w // 2 + w, b[3] + 10)
    canvas = (max(canvas[0], 0), max(canvas[1], 0), canvas[2], canvas[3])
    save(img, m, f"environment/props/trampoline/trampoline_{i + 1}_{labels[i]}.png", s, canvas=canvas)

# ---------------------------------------------------------------- fireballs: flame and spinning core apart
for k, name in ((1, "fireball1.jpg"), (2, "fireball2.jpg")):
    img, ink, s = load(name)
    rgb = img[:, :, :3]
    red = (rgb[:, :, 0] - rgb[:, :, 1] > 60)
    keep = np.zeros_like(ink)
    for m in components(ink, 15, 0.002):
        keep |= m
    flame = keep & ndimage.binary_closing(red, iterations=2)
    core = keep & ink & ~ndimage.binary_dilation(flame, iterations=2)
    lab, n = ndimage.label(core)
    core = lab == 1 + int(np.argmax(ndimage.sum(core, lab, range(1, n + 1))))  # biggest black blob = spiral
    flame &= ~ndimage.binary_dilation(core, iterations=6)
    keep = flame | core
    save(img, keep, f"projectiles/fireball/fireball_{k}_full.png", s)
    save(img, flame, f"projectiles/fireball/fireball_{k}_flame.png", s)
    save(img, core, f"projectiles/fireball/fireball_{k}_core.png", s)

# ---------------------------------------------------------------- evil clouds: thin cloud lines vs thick bolts
for k, name in ((1, "evilcloud1.jpg"), (2, "evilcloud2.jpg")):
    img, ink, s = load(name)
    keep = np.zeros_like(ink)
    for m in components(ink, 25, 0.0004):
        keep |= m
    ink = ink & keep
    bolts = split_bolts(ink, 0.75, 0.05)  # lightning is drawn with a thicker brush
    if k == 2:  # hand fixes, measured on a 900px preview
        F = 2834 / 900
        bolts &= ~box(ink.shape, 130 * F, 265 * F, 190 * F, 360 * F)  # cloud curl, not lightning
        bolts |= ink & box(ink.shape, 295 * F, 180 * F, 355 * F, 365 * F)  # zigzag inside the cloud
        bolts |= ink & box(ink.shape, 0, 740 * F, 175 * F, 9999)  # thin tail of the left bolt
    cloud = ink & ~bolts
    save(img, ink, f"effects/evil_cloud/evil_cloud_{k}_full.png", s)
    save(img, cloud, f"effects/evil_cloud/evil_cloud_{k}_cloud.png", s)
    save(img, bolts, f"effects/evil_cloud/evil_cloud_{k}_lightning.png", s)

# ---------------------------------------------------------------- tree: foliage vs trunk (for swaying)
img, ink, s = load("tree.jpg")
T = 2048 / 2000
trunk = ink & (box(ink.shape, 0, 1300 * T, 1105 * T, 9999) | box(ink.shape, 0, 1580 * T, 9999, 9999))
save(img, ink, "environment/props/tree/tree_full.png", s)
save(img, trunk, "environment/props/tree/tree_trunk.png", s)
save(img, ink & ~trunk, "environment/props/tree/tree_foliage.png", s)

# ---------------------------------------------------------------- single pieces
whole("casteltower.jpg", "environment/castle/castle_tower.png")
whole("castlegate.jpg", "environment/castle/castle_gate_portcullis.png")
whole("castlecenter.jpg", "environment/castle/castle_center_wall.png")
whole("mountainrange.jpg", "environment/background/mountain_range.png")

(OUT / "parts.json").write_text(json.dumps(meta, indent=1))
