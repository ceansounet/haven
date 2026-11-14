"""Build Godot cut-out rig scenes from parts.json. Usage: python rigs.py <parts.json> <project sprites dir>"""
import json
import sys
from pathlib import Path

meta = json.loads(Path(sys.argv[1]).read_text())
SPR = Path(sys.argv[2])
RES = "res://sprites/"


def v(x, y):
    return f"Vector2({x:.1f}, {y:.1f})"


def scene(path, origin, nodes, extra_header=""):
    """nodes: list of (name, parent, rel_or_None, pivot_override, props)."""
    tex = []
    for n in nodes:
        if n[2] and n[2] not in tex:
            tex.append(n[2])
    out = ["[gd_scene format=3]", ""]
    for i, t in enumerate(tex, 1):
        out.append(f'[ext_resource type="Texture2D" path="{RES}{t}" id="{i}"]')
    out += ["", f'[node name="{Path(path).stem.title().replace("_", "")}" type="Node2D"]', ""]
    pivots = {".": origin}
    for name, parent, rel, pivot, props in nodes:
        key = name if parent == "." else f"{parent}/{name}"
        if rel:
            m = meta[rel]
            piv = pivot or m.get("pivot") or m["center"]
        else:
            piv = pivot
        pivots[key] = piv
        ppiv = pivots[parent]
        out.append(f'[node name="{name}" type="{"Sprite2D" if rel else "Node2D"}" parent="{parent}"]')
        out.append(f"position = {v(piv[0] - ppiv[0], piv[1] - ppiv[1])}")
        if rel:
            out.append(f'texture = ExtResource("{tex.index(rel) + 1}")')
            c = piv if pivot else m["center"]  # an explicit placement centres the sprite there
            if abs(c[0] - piv[0]) > 0.05 or abs(c[1] - piv[1]) > 0.05:
                out.append(f"offset = {v(c[0] - piv[0], c[1] - piv[1])}")
        out += props + [""]
    (SPR / path).write_text("\n".join(out), encoding="utf-8")
    print("wrote", path)


# ---------------- Orpheus (sheet already lays the parts out roughly in place)
O = "characters/orpheus/"
behind = ["show_behind_parent = true"]
hidden = ["visible = false"]
scene(O + "orpheus_rig.tscn", (170, 494), [
    ("LegBack", ".", O + "orpheus_leg_back.png", None, []),
    ("LegFront", ".", O + "orpheus_leg_front.png", None, []),
    ("Body", ".", O + "orpheus_body.png", None, []),
    ("Tail", "Body", O + "orpheus_tail.png", None, behind),
    ("ArmDown", "Body", O + "orpheus_arm_down.png", None, []),
    ("Hand1", "Body", O + "orpheus_hand_1.png", None, []),
    ("Hand2", "Body", O + "orpheus_hand_2.png", None, []),
    ("ArmRaised", "Body", O + "orpheus_arm_raised.png", None, []),
    ("Face", "Body", None, (180, 70), []),
    ("Eyebrows", "Body/Face", O + "eyes/orpheus_eyebrows_worried.png", (172, 34), hidden),
    ("Eyes", "Body/Face", O + "eyes/orpheus_eyes_happy.png", (172, 52), []),
    ("Mouth", "Body/Face", O + "mouths/orpheus_mouth_smile.png", (200, 96), []),
])

# ---------------- Daven (drawn in one piece, so every part is already in place)
D = "characters/daven/"
d = meta[D + "daven_body.png"]
scene(D + "daven_rig.tscn", (d["pivot"][0], d["pivot"][1] + 60), [
    ("Body", ".", D + "daven_body.png", None, []),
    ("Spikes", "Body", D + "daven_spikes.png", None, behind),
    ("ArmLeft", "Body", D + "daven_arm_left.png", None, []),
    ("ArmRight", "Body", D + "daven_arm_right.png", None, []),
    ("FootLeft", "Body", D + "daven_foot_left.png", None, []),
    ("FootRight", "Body", D + "daven_foot_right.png", None, []),
    ("Face", "Body", None, meta[D + "daven_mouth.png"]["center"], []),
    ("EyeLeft", "Body/Face", D + "daven_eye_left.png", None, []),
    ("EyeRight", "Body/Face", D + "daven_eye_right.png", None, []),
    ("CheekLeft", "Body/Face", D + "daven_cheek_left.png", None, []),
    ("CheekRight", "Body/Face", D + "daven_cheek_right.png", None, []),
    ("Mouth", "Body/Face", D + "daven_mouth.png", None, []),
])

# ---------------- Trampoline bounce animation
T = "environment/props/trampoline/"
frames = sorted(p.name for p in (SPR / T).glob("trampoline_*.png"))
seq = [2, 3, 4, 3, 2, 1, 0, 1, 2]  # rest -> squash -> launch -> settle
lines = ["[gd_scene format=3]", ""]
for i, f in enumerate(frames, 1):
    lines.append(f'[ext_resource type="Texture2D" path="{RES}{T}{f}" id="{i}"]')
anim = ", ".join('{"duration": 1.0, "texture": ExtResource("%d")}' % (i + 1) for i in seq)
lines += ["", '[sub_resource type="SpriteFrames" id="frames"]',
          'animations = [{"frames": [%s], "loop": false, "name": &"bounce", "speed": 15.0}, '
          '{"frames": [{"duration": 1.0, "texture": ExtResource("3")}], "loop": true, "name": &"idle", "speed": 5.0}]' % anim,
          "", '[node name="Trampoline" type="AnimatedSprite2D"]',
          'sprite_frames = SubResource("frames")', 'animation = &"idle"', ""]
(SPR / T / "trampoline.tscn").write_text("\n".join(lines), encoding="utf-8")
print("wrote trampoline.tscn")
