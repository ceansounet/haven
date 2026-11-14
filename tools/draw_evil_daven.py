"""Redraw the boss Evil Daven (from 'Evil daven.png') in the marker style of the other sprites,
as separate parts, and build an animatable Godot rig for him.

Two versions with the exact same shapes:
  marker/  black + red marker only, white fill (like Orpheus)
  color/   the painting's colours, filled with marker-brush strokes

Usage: python tools/draw_evil_daven.py sprites
Output: sprites/characters/evil_daven/<version>/*.png + evil_daven_<version>.tscn
"""
import math
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage

sys.path.insert(0, str(Path(__file__).parent))
import marker_brush  # noqa: E402

ROOT = Path(sys.argv[1]) / "characters" / "evil_daven"
SS = 2                      # supersampling for smooth edges
W, H = 1000, 1100           # logical canvas; the whole character is drawn on it


def rgb(*c):
    return np.array(c, np.float32)


INK = rgb(24, 20, 20)
RED = rgb(196, 58, 58)
WHITE = rgb(255, 255, 255)
STYLES = {
    "marker": dict(
        outline=INK, spikes_back_line=RED, spikes_front_line=INK,
        spikes_back=WHITE, spikes_front=WHITE, skin=WHITE, eye=WHITE,
        ear_inner=None, ear_inner_line=RED, cheek=None, cheek_line=RED,
        vein=RED, pupil=INK, mouth=INK, textured=False, brush=True),
    "color": dict(
        outline=INK, spikes_back_line=INK, spikes_front_line=INK,
        spikes_back=rgb(150, 74, 48), spikes_front=rgb(178, 94, 62), skin=rgb(244, 168, 138), eye=WHITE,
        ear_inner=rgb(230, 136, 128), ear_inner_line=None, cheek=rgb(236, 128, 124), cheek_line=None,
        vein=rgb(222, 92, 92), pupil=rgb(84, 32, 24), mouth=rgb(92, 34, 26), textured=True, brush=False),
}


# ----------------------------------------------------------------- marker helpers
def smooth_noise(gen, scale, shape=(H * SS, W * SS)):
    small = gen.standard_normal((shape[0] // scale + 2, shape[1] // scale + 2)).astype(np.float32)
    return np.asarray(Image.fromarray(small).resize((shape[1], shape[0]), Image.BICUBIC))


_g = np.random.default_rng(1)
NOISE_T = smooth_noise(_g, 60)      # line thickness wobble
NOISE_C = smooth_noise(_g, 6)       # ink grain
# marker-brush fill: parallel diagonal strokes ~16px wide, each a bit lighter/darker, darker overlaps
_yy, _xx = np.mgrid[0:H * SS, 0:W * SS]
_u = (_xx * 0.8 + _yy * 0.6 + 14 * SS * smooth_noise(_g, 90)) / (22 * SS)
_band = _g.standard_normal(int(_u.max()) + 3).astype(np.float32)
_frac = _u - np.floor(_u)
STREAK = (_band[np.floor(_u).astype(int)] * 0.022
          - 0.02 * np.exp(-((_frac - 0.0) ** 2) / 0.003) - 0.02 * np.exp(-((_frac - 1.0) ** 2) / 0.003)
          + 0.014 * smooth_noise(_g, 14))
del _yy, _xx, _u, _frac

rng = np.random.default_rng(7)

# which real marker cross-section to use where: smooth, so sheen streaks run along the strokes
_sel = smooth_noise(_g, 160)
SELECT = (np.argsort(np.argsort(_sel.ravel())).reshape(_sel.shape) / _sel.size).astype(np.float32)
del _sel
SCANS = Path(__file__).parent.parent / "asset pack 1 - ORIGINAL BACKUP"
_brushes = {}


NOISE_EDGE = smooth_noise(_g, 3)  # fine bristle noise for ragged edges


def roughen(mask, amount=1.3):
    """Ragged marker edge: push the boundary in/out by a pixel or two of fine noise."""
    signed = ndimage.distance_transform_edt(mask) - ndimage.distance_transform_edt(~mask)
    return signed > NOISE_EDGE * amount * SS * 0.5


def brush(kind):
    if kind not in _brushes:
        src = SCANS / ("castlecenter.jpg" if kind == "black" else "fireball1.jpg")
        _brushes[kind] = marker_brush.sample_profiles(src, kind)[0]
    return _brushes[kind]


def catmull(points, closed=True, steps=14):
    p = [np.array(q, float) for q in points]
    p = ([p[-1]] + p + [p[0], p[1]]) if closed else ([p[0]] + p + [p[-1]])
    out = []
    for i in range(1, len(p) - 2):
        p0, p1, p2, p3 = p[i - 1], p[i], p[i + 1], p[i + 2]
        for t in np.linspace(0, 1, steps, endpoint=False):
            t2, t3 = t * t, t * t * t
            out.append(0.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t2
                              + (-p0 + 3 * p1 - 3 * p2 + p3) * t3))
    if not closed:
        out.append(p[-2])
    return out


def wobble(points, amount=4.0):
    return [(x + rng.normal(0, amount), y + rng.normal(0, amount)) for x, y in points]


def blank():
    return Image.new("L", (W * SS, H * SS), 0)


def poly_mask(points, jitter=4.0, smooth=True):
    pts = catmull(wobble(points, jitter)) if smooth else wobble(points, jitter)
    im = blank()
    ImageDraw.Draw(im).polygon([(x * SS, y * SS) for x, y in pts], fill=255)
    return np.asarray(im) > 0


def rounded(mask, r):
    """Round off sharp corners (spike tips) by r logical pixels."""
    core = ndimage.distance_transform_edt(mask) > r * SS
    return ndimage.distance_transform_edt(~core) <= r * SS


def ellipse_pts(cx, cy, rx, ry, n=16, a0=0.0):
    return [(cx + rx * math.cos(a0 + 2 * math.pi * i / n), cy + ry * math.sin(a0 + 2 * math.pi * i / n))
            for i in range(n)]


def squircle_pts(cx, cy, a, b, n=4.0, count=40):
    pts = []
    for i in range(count):
        t = 2 * math.pi * i / count
        c, s = math.cos(t), math.sin(t)
        pts.append((cx + a * math.copysign(abs(c) ** (2 / n), c), cy + b * math.copysign(abs(s) ** (2 / n), s)))
    return pts


def capsule_mask(a, b, width):
    im = blank()
    d = ImageDraw.Draw(im)
    d.line([(a[0] * SS, a[1] * SS), (b[0] * SS, b[1] * SS)], fill=255, width=int(width * SS))
    for x, y in (a, b):
        r = width * SS / 2
        d.ellipse([x * SS - r, y * SS - r, x * SS + r, y * SS + r], fill=255)
    return np.asarray(im) > 0


def stroke_mask(points, width=11.0, closed=False, jitter=2.5):
    pts = catmull(wobble(points, jitter), closed=closed, steps=20)
    im = blank()
    d = ImageDraw.Draw(im)
    for x, y in pts:
        xi, yi = int(np.clip(x * SS, 0, W * SS - 1)), int(np.clip(y * SS, 0, H * SS - 1))
        r = width * SS / 2 * (1 + 0.12 * NOISE_T[yi, xi])
        d.ellipse([x * SS - r, y * SS - r, x * SS + r, y * SS + r], fill=255)
    return np.asarray(im) > 0


def star(cx, cy, n, r_in, r_out, a0, jitter, skip_down=0.6):
    pts = []
    for i in range(n):
        ang = a0 + 2 * math.pi * i / n
        if i % 2 == 0 and math.sin(ang) < skip_down:
            rx, ry = r_out[0] + rng.normal(0, jitter), r_out[1] + rng.normal(0, jitter)
        else:
            rx, ry = r_in
        pts.append((cx + rx * math.cos(ang), cy + ry * math.sin(ang)))
    return pts


def mirror(points):
    return [(W - x, y) for x, y in points]


# ----------------------------------------------------------------- drawing one version
def draw(version):
    global rng
    rng = np.random.default_rng(7)  # same shapes for every version
    st = STYLES[version]
    out_dir = ROOT / version
    meta = {}

    class Layer:
        def __init__(self):
            self.img = np.zeros((H * SS, W * SS, 4), np.float32)

        def blend(self, mask, rgba):
            a = rgba[:, 3:4] / 255
            old = self.img[mask]
            self.img[mask, :3] = rgba[:, :3] * a + old[:, :3] * (1 - a)
            self.img[mask, 3] = np.clip(rgba[:, 3] + old[:, 3] * (1 - a[:, 0]), 0, 255)

        def brushed(self, mask, color, across):
            mask = roughen(mask)
            kind = "red" if np.allclose(color, RED) else "black"
            self.blend(mask, marker_brush.paint(mask, across, SELECT, brush(kind)))
            return self

        def fill(self, mask, color):
            if st["brush"] and np.allclose(color, INK):  # solid black areas (pupils, mouth)
                d = ndimage.distance_transform_edt(mask)
                return self.brushed(mask, color, 0.5 * np.clip(d / (12 * SS), 0, 1))
            col = np.broadcast_to(color, self.img.shape[:2] + (3,))
            if st["textured"] and not np.all(color == 255):
                col = color[None, None, :] * (1 + STREAK[..., None])
            self.img[mask, :3] = np.clip(col, 0, 255)[mask]
            self.img[mask, 3] = 255
            return self

        def ink(self, mask, color=None, across=None):
            color = INK if color is None else color
            if st["brush"] and mask.any() and (np.allclose(color, INK) or np.allclose(color, RED)):
                if across is None:  # open stroke: edge -> centre of the brush
                    d = ndimage.distance_transform_edt(mask)
                    across = 0.5 * np.clip(d / max(np.percentile(d[mask], 95), 1), 0, 1)
                return self.brushed(mask, color, across)
            col = color[None, None, :] * (1 + 0.06 * NOISE_C[..., None])
            self.img[mask, :3] = np.clip(col, 0, 255)[mask]
            self.img[mask, 3] = 255
            return self

        def shape(self, mask, fill=WHITE, line=None, thick=12.0):
            if fill is not None:
                self.fill(mask, fill)
            if line is not None or fill is not None:
                dist = ndimage.distance_transform_edt(mask)
                tt = thick * SS * (1 + 0.15 * NOISE_T)
                self.ink(mask & (dist <= tt), st["outline"] if line is None else line, across=dist / tt)
            return self

        def save(self, name, pivot):
            ys, xs = np.nonzero(self.img[..., 3] > 0)
            pad = 6 * SS
            x0, y0 = max(xs.min() - pad, 0), max(ys.min() - pad, 0)
            x1, y1 = min(xs.max() + pad, W * SS), min(ys.max() + pad, H * SS)
            x0, y0, x1, y1 = (v - v % SS for v in (x0, y0, x1 + SS, y1 + SS))
            crop = Image.fromarray(self.img[y0:y1, x0:x1].round().astype(np.uint8), "RGBA")
            crop = crop.resize((crop.width // SS, crop.height // SS), Image.LANCZOS)
            path = out_dir / f"{name}.png"
            path.parent.mkdir(parents=True, exist_ok=True)
            crop.save(path, optimize=True)
            meta[name] = {"center": ((x0 + x1) / 2 / SS, (y0 + y1) / 2 / SS), "pivot": pivot}
            print(version, "saved", name, crop.size)

    BODY_C = (500, 705)
    # two rings of rounded spikes behind the body
    back = rounded(poly_mask(star(500, 690, 26, (200, 250), (430, 530), math.pi, 10, 0.75), 3, smooth=False), 26)
    Layer().shape(back, st["spikes_back"], st["spikes_back_line"]).save("evil_daven_spikes_back", (500, 940))
    front = rounded(poly_mask(star(500, 700, 22, (200, 250), (355, 425), math.pi + math.pi / 22, 8, 0.7), 3,
                               smooth=False), 22)
    Layer().shape(front, st["spikes_front"], st["spikes_front_line"]).save("evil_daven_spikes_front", (500, 940))

    # squircle hedgehog body
    body = poly_mask(squircle_pts(*BODY_C, 222, 262, 3.6), 3)
    Layer().shape(body, st["skin"]).save("evil_daven_body", (500, 940))

    for side, sx in (("left", 1), ("right", -1)):
        ex = 500 - sx * 205
        ear = Layer().shape(poly_mask(ellipse_pts(ex, 520, 62, 66), 3), st["skin"])
        inner = [(ex - sx * 30, 490), (ex - sx * 42, 520), (ex - sx * 30, 552)]
        if st["ear_inner"] is not None:
            ear.fill(poly_mask(ellipse_pts(ex - sx * 18, 520, 30, 38), 2), st["ear_inner"])
        if st["ear_inner_line"] is not None:
            ear.ink(stroke_mask(inner, 9), st["ear_inner_line"])
        ear.save(f"evil_daven_ear_{side}", (500 - sx * 178, 520))

    for side, sx in (("left", 1), ("right", -1)):
        sh, wr = (500 - sx * 175, 740), (500 - sx * 335, 490)
        m = capsule_mask(sh, wr, 72)
        palm = (500 - sx * 352, 460)
        m |= poly_mask(ellipse_pts(*palm, 56, 52), 2)
        base = math.atan2(wr[1] - sh[1], wr[0] - sh[0])
        for k, da in enumerate((-0.75, -0.05, 0.65)):
            L = 92 if k == 1 else 80
            m |= capsule_mask(palm, (palm[0] + L * math.cos(base + da), palm[1] + L * math.sin(base + da)), 42)
        Layer().shape(m, st["skin"]).save(f"evil_daven_arm_{side}", sh)

    for side, sx in (("left", 1), ("right", -1)):
        hip = (500 - sx * 95, 925)
        m = capsule_mask(hip, (500 - sx * 105, 990), 78)
        m |= poly_mask(ellipse_pts(500 - sx * 117, 1015, 82, 46), 3)
        Layer().shape(m, st["skin"]).save(f"evil_daven_foot_{side}", hip)

    for side, sx in (("left", 1), ("right", -1)):
        ex, ey = 500 - sx * 84, 545
        eye = Layer().shape(poly_mask(ellipse_pts(ex, ey, 80, 68, 18), 2), st["eye"], thick=11)
        for _ in range(4):
            a = rng.uniform(0.25, math.pi - 0.25)
            p0 = (ex + 64 * math.cos(a) * 1.15, ey + 64 * math.sin(a) * 0.95)
            p1 = (ex + 34 * math.cos(a) * 1.15 + rng.normal(0, 6), ey + 30 * math.sin(a) + rng.normal(0, 6))
            mid = ((p0[0] + p1[0]) / 2 + rng.normal(0, 7), (p0[1] + p1[1]) / 2 + rng.normal(0, 7))
            eye.ink(stroke_mask([p0, mid, p1], 4.5, jitter=1.5), st["vein"])
        eye.save(f"evil_daven_eye_{side}", (ex, ey))
        pupil = Layer().fill(poly_mask(ellipse_pts(ex + sx * 8, ey + 4, 25, 25), 1.5), st["pupil"])
        pupil.ink(np.zeros_like(body), INK)
        pupil.save(f"evil_daven_pupil_{side}", (ex + sx * 8, ey + 4))

    for side, sx in (("left", 1), ("right", -1)):
        chx, chy = 500 - sx * 132, 645
        ch = Layer()
        oval = poly_mask(ellipse_pts(chx, chy, 36, 30), 2)
        if st["cheek"] is not None:
            ch.fill(oval, st["cheek"])
        if st["cheek_line"] is not None:
            ch.shape(oval, None, st["cheek_line"], thick=7)
            for k in (-14, 0, 14):
                ch.ink(stroke_mask([(chx - 14 + k, chy + 16), (chx + 10 + k, chy - 16)], 6), st["cheek_line"])
        ch.save(f"evil_daven_cheek_{side}", (chx, chy))

    eb_l = [(338, 462), (400, 486), (468, 520)]
    Layer().ink(stroke_mask(eb_l, 19) | stroke_mask(mirror(eb_l), 19)).save(
        "eyebrows/evil_daven_eyebrows_angry", (500, 490))
    eb_w = [(352, 484), (408, 464), (462, 448)]
    Layer().ink(stroke_mask(eb_w, 15) | stroke_mask(mirror(eb_w), 15)).save(
        "eyebrows/evil_daven_eyebrows_worried", (500, 467))

    dy = 22  # mouths sit a little lower on the squircle face
    MOUTH = (500, 680 + dy)
    sh = lambda pts: [(x, y + dy) for x, y in pts]
    grin = sh([(418, 658), (460, 662), (500, 660), (542, 657), (586, 650), (568, 684), (536, 706), (500, 712),
               (462, 706), (432, 686)])
    Layer().fill(poly_mask(grin, 2), st["mouth"]).save("mouths/evil_daven_mouth_grin", MOUTH)
    Layer().fill(poly_mask(ellipse_pts(500, 688 + dy, 44, 56, 14), 2), st["mouth"]).save(
        "mouths/evil_daven_mouth_open", MOUTH)
    Layer().ink(stroke_mask(sh([(408, 714), (448, 680), (500, 668), (552, 680), (592, 714)]), 17), st["mouth"]).save(
        "mouths/evil_daven_mouth_frown", MOUTH)
    teeth = Layer().shape(poly_mask(sh([(424, 658), (576, 658), (580, 708), (420, 708)]), 2),
                          WHITE, st["mouth"], thick=11)
    teeth.ink(stroke_mask(sh([(426, 683), (450, 668), (475, 698), (500, 668), (525, 698), (550, 668), (575, 683)]), 8),
              st["mouth"])
    teeth.save("mouths/evil_daven_mouth_teeth", MOUTH)

    write_rig(version, meta)


# ----------------------------------------------------------------- Godot rig
def write_rig(version, meta):
    rel = f"characters/evil_daven/{version}/"
    behind = ["show_behind_parent = true"]
    nodes = [  # name, parent, sprite (None = empty Node2D), pivot override, extra properties
        ("FootLeft", ".", "evil_daven_foot_left", None, []),
        ("FootRight", ".", "evil_daven_foot_right", None, []),
        ("Body", ".", "evil_daven_body", None, []),
        ("SpikesBack", "Body", "evil_daven_spikes_back", None, behind),
        ("SpikesFront", "Body", "evil_daven_spikes_front", None, behind),
        ("EarLeft", "Body", "evil_daven_ear_left", None, behind),
        ("EarRight", "Body", "evil_daven_ear_right", None, behind),
        ("ArmLeft", "Body", "evil_daven_arm_left", None, behind),
        ("ArmRight", "Body", "evil_daven_arm_right", None, behind),
        ("Face", "Body", None, (500, 580), []),
        ("CheekLeft", "Body/Face", "evil_daven_cheek_left", None, []),
        ("CheekRight", "Body/Face", "evil_daven_cheek_right", None, []),
        ("EyeLeft", "Body/Face", "evil_daven_eye_left", None, []),
        ("PupilLeft", "Body/Face/EyeLeft", "evil_daven_pupil_left", None, []),
        ("EyeRight", "Body/Face", "evil_daven_eye_right", None, []),
        ("PupilRight", "Body/Face/EyeRight", "evil_daven_pupil_right", None, []),
        ("Eyebrows", "Body/Face", "eyebrows/evil_daven_eyebrows_angry", None, []),
        ("Mouth", "Body/Face", "mouths/evil_daven_mouth_frown", None, []),
    ]
    tex = [n[2] for n in nodes if n[2]]
    lines = ["[gd_scene format=3]", ""]
    for i, t in enumerate(tex, 1):
        lines.append(f'[ext_resource type="Texture2D" path="res://sprites/{rel}{t}.png" id="{i}"]')
    lines += ["", f'[node name="EvilDaven{version.title()}" type="Node2D"]', ""]
    piv = {".": (500, 1070)}  # between the feet, on the ground
    for name, parent, sprite, override, props in nodes:
        p = override or meta[sprite]["pivot"]
        piv[name if parent == "." else f"{parent}/{name}"] = p
        pp = piv[parent]
        lines.append(f'[node name="{name}" type="{"Sprite2D" if sprite else "Node2D"}" parent="{parent}"]')
        lines.append(f"position = Vector2({p[0] - pp[0]:.1f}, {p[1] - pp[1]:.1f})")
        if sprite:
            c = meta[sprite]["center"]
            lines.append(f'texture = ExtResource("{tex.index(sprite) + 1}")')
            if abs(c[0] - p[0]) > 0.05 or abs(c[1] - p[1]) > 0.05:
                lines.append(f"offset = Vector2({c[0] - p[0]:.1f}, {c[1] - p[1]:.1f})")
        lines += props + [""]
    (ROOT / version / f"evil_daven_{version}.tscn").write_text("\n".join(lines), encoding="utf-8", newline="\n")
    print("wrote", f"evil_daven_{version}.tscn")


for v in (sys.argv[2:] or STYLES):
    draw(v)
