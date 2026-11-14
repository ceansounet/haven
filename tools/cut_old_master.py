"""Cut 'old master orpheus.png' into animatable parts and build his Godot scene (riding a cloud).

The drawing is split along its own marker lines: every white area enclosed by lines is a part,
and the lines around it go with it. Areas hidden behind the beard and arms get a white fill,
so nothing shows through when those parts move.

Usage: python tools/cut_old_master.py sprites
Output: sprites/characters/old_master/*.png + old_master.tscn
"""
import sys
from pathlib import Path

import numpy as np
from PIL import Image
from scipy import ndimage

ROOT = Path(__file__).parent.parent
SRC = ROOT / "source drawings" / "old master orpheus.png"
SPR = Path(sys.argv[1])
REL = "characters/old_master/"
OUT = SPR / REL
OUT.mkdir(parents=True, exist_ok=True)

img = np.asarray(Image.open(SRC).convert("RGBA")).astype(np.float32)
alpha = img[..., 3] > 40
dark = alpha & (img[..., :3].max(axis=2) < 110)
white = alpha & ~dark
lab, _ = ndimage.label(white)


def region(*seeds):
    m = np.zeros_like(white)
    for x, y in seeds:
        m |= lab == lab[y, x]
    return m


head = region((170, 70))
beard = region((195, 150), (213, 182))
arms = region((210, 212), (135, 215))
tail = region((75, 260))
torso = region((170, 290))
leg_back = region((130, 360))
leg_front = region((205, 370))

# eyes and mouth: small line marks floating inside the head
dlab, dn = ndimage.label(dark)
face = np.zeros_like(dark)
for i, sl in enumerate(ndimage.find_objects(dlab), 1):
    comp = dlab == i
    if comp.sum() < 300 and not (ndimage.binary_dilation(comp, iterations=2) & ~(comp | head)).any():
        face |= comp
fy = np.nonzero(face)[0]
eyes = face & (np.arange(face.shape[0])[:, None] < 80)
mouth = face & ~eyes


def lines_of(reg, grow=7):
    return dark & ndimage.binary_dilation(reg, iterations=grow) & ~face


meta = {}


def save(name, own, pivot, under=None, keep_lines=True):
    """own: pixels copied from the drawing; under: extra white fill behind it."""
    out = np.zeros_like(img)
    if under is not None:
        out[under] = (255, 255, 255, 255)
    out[own] = img[own]
    ys, xs = np.nonzero(out[..., 3] > 0)
    x0, y0 = max(xs.min() - 3, 0), max(ys.min() - 3, 0)
    x1, y1 = min(xs.max() + 4, img.shape[1]), min(ys.max() + 4, img.shape[0])
    Image.fromarray(out[y0:y1, x0:x1].round().astype(np.uint8), "RGBA").save(OUT / f"{name}.png", optimize=True)
    meta[name] = {"center": ((x0 + x1) / 2, (y0 + y1) / 2), "pivot": pivot}
    print("saved", name, (x1 - x0, y1 - y0))


# torso: fill white behind the arms and the top of the legs, using the torso's own width
torso_under = np.zeros_like(torso)
for y in range(188, 346):
    ref = min(max(y, 240), 300)
    xs = np.nonzero(torso[ref])[0]
    torso_under[y, xs.min():xs.max() + 1] = True
head_under = (ndimage.binary_dilation(beard, iterations=4) & ~ndimage.binary_dilation(arms, iterations=2)) | ndimage.binary_dilation(face, iterations=2)

save("old_master_tail", tail | lines_of(tail), (100, 292))
save("old_master_torso", torso | lines_of(torso), (172, 335), under=torso_under)
save("old_master_head", head | lines_of(head), (165, 196), under=head_under)
save("old_master_beard", beard | lines_of(beard, 6), (192, 120))
save("old_master_arms", arms | lines_of(arms), (175, 214))
save("old_master_leg_back", leg_back | lines_of(leg_back), (125, 318))
save("old_master_leg_front", leg_front | lines_of(leg_front), (200, 335))
save("old_master_eyes_closed", eyes, None)
save("old_master_mouth", mouth, None)

# his cloud: a cloud from the environment sheet, with the inside filled white so he sits in it
cloud = np.asarray(Image.open(SPR / "environment/background/cloud_1.png").convert("RGBA")).astype(np.float32)
ink = cloud[..., 3] > 60
inside = ndimage.binary_fill_holes(ndimage.binary_closing(ink, iterations=6)) & ~ink
cloud[inside] = (255, 255, 255, 255)
cim = Image.fromarray(cloud.round().astype(np.uint8), "RGBA")
cim = cim.resize((round(cim.width * 0.46), round(cim.height * 0.46)), Image.LANCZOS)
cim.save(OUT / "old_master_cloud.png", optimize=True)
meta["old_master_cloud"] = {"center": (162, 450), "pivot": None}
print("saved old_master_cloud", cim.size)

# ----------------------------------------------------------------- Godot scene
ORIGIN = (162, 520)
behind = ["show_behind_parent = true"]
nodes = [  # name, parent, sprite, extra properties
    ("Float", ".", None, []),
    ("Body", "Float", "old_master_torso", []),
    ("Tail", "Float/Body", "old_master_tail", behind),
    ("Head", "Float/Body", "old_master_head", []),
    ("Eyes", "Float/Body/Head", "old_master_eyes_closed", []),
    ("Mouth", "Float/Body/Head", "old_master_mouth", []),
    ("Beard", "Float/Body/Head", "old_master_beard", []),
    ("Arms", "Float/Body", "old_master_arms", []),
    ("LegBack", "Float/Body", "old_master_leg_back", []),
    ("LegFront", "Float/Body", "old_master_leg_front", []),
    ("Cloud", "Float", "old_master_cloud", []),
]
tex = [f"{REL}{n[2]}.png" for n in nodes if n[2]]
tex.append("characters/orpheus/mouths/orpheus_mouth_open.png")  # used by the talk animation
ids = {t: i + 1 for i, t in enumerate(tex)}
L = ["[gd_scene format=3]", ""]
for t, i in ids.items():
    L.append(f'[ext_resource type="Texture2D" path="res://sprites/{t}" id="{i}"]')
mouth_id, open_id = ids[f"{REL}old_master_mouth.png"], ids["characters/orpheus/mouths/orpheus_mouth_open.png"]
L += ["",
      '[sub_resource type="Animation" id="Animation_float"]',
      'resource_name = "float"', "length = 2.4", "loop_mode = 1",
      'tracks/0/type = "value"', 'tracks/0/path = NodePath("Float:position")', "tracks/0/interp = 2",
      "tracks/0/loop_wrap = true",
      'tracks/0/keys = {"times": PackedFloat32Array(0, 1.2, 2.4), "transitions": PackedFloat32Array(1, 1, 1), '
      '"update": 0, "values": [Vector2(0, 0), Vector2(0, -10), Vector2(0, 0)]}',
      'tracks/1/type = "value"', 'tracks/1/path = NodePath("Float/Body/Tail:rotation")', "tracks/1/interp = 2",
      "tracks/1/loop_wrap = true",
      'tracks/1/keys = {"times": PackedFloat32Array(0, 1.2, 2.4), "transitions": PackedFloat32Array(1, 1, 1), '
      '"update": 0, "values": [0.0, 0.12, 0.0]}',
      'tracks/2/type = "value"', 'tracks/2/path = NodePath("Float/Body/Head/Beard:rotation")', "tracks/2/interp = 2",
      "tracks/2/loop_wrap = true",
      'tracks/2/keys = {"times": PackedFloat32Array(0, 1.2, 2.4), "transitions": PackedFloat32Array(1, 1, 1), '
      '"update": 0, "values": [0.0, -0.06, 0.0]}',
      "",
      '[sub_resource type="Animation" id="Animation_talk"]',
      'resource_name = "talk"', "length = 0.4", "loop_mode = 1",
      'tracks/0/type = "value"', 'tracks/0/path = NodePath("Float/Body/Head/Mouth:texture")', "tracks/0/interp = 1",
      "tracks/0/loop_wrap = true",
      f'tracks/0/keys = {{"times": PackedFloat32Array(0, 0.2), "transitions": PackedFloat32Array(1, 1), '
      f'"update": 1, "values": [ExtResource("{open_id}"), ExtResource("{mouth_id}")]}}',
      "",
      '[sub_resource type="AnimationLibrary" id="AnimationLibrary_float"]',
      '_data = {&"float": SubResource("Animation_float")}',
      "",
      '[sub_resource type="AnimationLibrary" id="AnimationLibrary_talk"]',
      '_data = {&"talk": SubResource("Animation_talk")}',
      "",
      '[node name="OldMaster" type="Node2D"]', ""]
piv = {".": ORIGIN, "Float": ORIGIN}
for name, parent, sprite, props in nodes:
    key = name if parent == "." else f"{parent}/{name}"
    if sprite:
        m = meta[sprite]
        p = m["pivot"] or m["center"]
    else:
        p = ORIGIN
    piv[key] = p
    pp = piv[parent]
    L.append(f'[node name="{name}" type="{"Sprite2D" if sprite else "Node2D"}" parent="{parent}"]')
    if (p[0] - pp[0], p[1] - pp[1]) != (0, 0):
        L.append(f"position = Vector2({p[0] - pp[0]:.1f}, {p[1] - pp[1]:.1f})")
    if sprite:
        c = m["center"]
        L.append(f'texture = ExtResource("{ids[REL + sprite + ".png"]}")')
        if abs(c[0] - p[0]) > 0.05 or abs(c[1] - p[1]) > 0.05:
            L.append(f"offset = Vector2({c[0] - p[0]:.1f}, {c[1] - p[1]:.1f})")
    L += props + [""]
L += ['[node name="FloatPlayer" type="AnimationPlayer" parent="."]',
      'libraries = {&"": SubResource("AnimationLibrary_float")}', 'autoplay = &"float"', "",
      '[node name="TalkPlayer" type="AnimationPlayer" parent="."]',
      'libraries = {&"": SubResource("AnimationLibrary_talk")}', ""]
(OUT / "old_master.tscn").write_text("\n".join(L), encoding="utf-8", newline="\n")
print("wrote old_master.tscn")
