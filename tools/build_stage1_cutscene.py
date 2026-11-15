# NOTE: this REWRITES scenes/cutscenes/stage_1_village.tscn from scratch. Only re-run it if you
# want to regenerate the cutscene; changes made in the Godot editor would be lost.
# Usage: python tools/build_stage1_cutscene.py scenes/cutscenes/stage_1_village.tscn
"""Build scenes/cutscenes/stage_1_village.tscn from the user's layout + the full cutscene animation."""
import sys

OUT = sys.argv[1]

V = lambda x, y: f"Vector2({x:g}, {y:g})"

# --- the user's layout (kept as they placed it) ---------------------------------------------
HOUSES = {1: (-669, 209, 1, 1), 2: (-399, 286, 1.185567, 1.1885246), 3: (250, 236, 1.185567, 1.1885246),
          4: (-829, 350, 1, 1), 5: (793, 288, 1.185567, 1.1885246), 6: (523, 235, 1, 1.1967213)}
BROKEN = {  # name, texture id, position, rotation, scale
    1: ("HouseBrokenFull1", "broken_full", (-680, 246), 0, (0.6716418, 0.67164177)),
    2: ("HouseBrokenFull2", "broken_full", (-407, 322), 3.1415927, (0.758, -0.877)),
    3: ("HouseBrokenFull3", "broken_full", (180.00002, 357), 3.1415927, (0.69985634, -0.7523061)),
    4: ("HouseBrokenRoof4", "broken_roof", (-687, 463), 0, (1, 1)),
    5: ("HouseBrokenFull5", "broken_full", (734.9999, 377), 3.1415927, (0.758, -0.877)),
    6: ("HouseBrokenFull6", "broken_full", (575, 289), 0, (0.6716418, 0.67164177)),
}
FIRES = {1: ((-680, 300), 0.8), 2: ((-401, 325), 1), 3: ((250, 334), 1), 4: ((-720, 485), 0.7),
         5: ((799, 399), 1), 6: ((575, 340), 0.8)}
SMOKES = {1: (-680, 0), 2: (-444, 102), 3: (286, 21), 4: (-720, 200), 5: (828, 119), 6: (575, 40)}
MATES = {4: ((-760, 505), 0.5, 0.1), 2: ((-260, 505), -0.5, 0.45), 3: ((110, 505), 0.5, 0.7),
         6: ((420, 505), -0.5, 0.25), 5: ((690, 505), 0.5, 0.85)}
ORPHEUS = ((-518, 490), 0.6, 0.55)
HITS = {3: 8.0, 5: 8.8, 1: 9.6, 6: 10.4, 2: 11.2, 4: 12.0}  # house -> moment its fireball lands
FALL = 0.9
LENGTH = 25.0
DAVEN = "Background/Mountains/SkyMask/UndoScale/GiantDaven"

L = ['[gd_scene format=3 uid="uid://bcokdu12bfffg"]', ""]
ext = [
    ("script", "Script", "res://scenes/cutscenes/stage_1_village.gd", ""),
    ("camera", "PackedScene", "res://scenes/common/board_camera.tscn", ""),
    ("mountains", "PackedScene", "res://sprites/environment/background/mountains_with_giant_daven.tscn", ""),
    ("cloud1", "Texture2D", "res://sprites/environment/background/cloud_1.png", ' uid="uid://bcrbus5dacl23"'),
    ("cloud2", "Texture2D", "res://sprites/environment/background/cloud_2.png", ' uid="uid://crtsoy1d7qey1"'),
    ("ground", "Texture2D", "res://sprites/environment/ground_line.png", ' uid="uid://cy2clicbv6anq"'),
    ("tree", "Texture2D", "res://sprites/environment/props/tree/tree_full.png", ' uid="uid://tougckaxbkfd"'),
    ("house", "Texture2D", "res://sprites/environment/buildings/house.png", ' uid="uid://dbjpt71yp1xvs"'),
    ("broken_full", "Texture2D", "res://sprites/environment/buildings/house_broken_full.png", ' uid="uid://b305ke5n81gpj"'),
    ("broken_roof", "Texture2D", "res://sprites/environment/buildings/house_broken_roof.png", ' uid="uid://nifu7kpqre0x"'),
    ("villager", "PackedScene", "res://sprites/characters/orpheus/villager.tscn", ""),
    ("fire", "PackedScene", "res://sprites/effects/fire/fire.tscn", ""),
    ("smoke", "PackedScene", "res://sprites/effects/smoke/smoke.tscn", ""),
    ("fireball1", "Texture2D", "res://sprites/projectiles/fireball/fireball_1_full.png", ""),
    ("fireball2", "Texture2D", "res://sprites/projectiles/fireball/fireball_2_full.png", ""),
    ("teeth", "Texture2D", "res://sprites/characters/evil_daven/mouths/evil_daven_mouth_teeth.png", ""),
    ("frown", "Texture2D", "res://sprites/characters/evil_daven/mouths/evil_daven_mouth_frown.png", ""),
]
E = {}
for i, (key, typ, path, uid) in enumerate(ext, 1):
    L.append(f'[ext_resource type="{typ}"{uid} path="{path}" id="{i}_{key}"]')
    E[key] = f'ExtResource("{i}_{key}")'
L.append("")

# --- animation tracks --------------------------------------------------------------------------
tracks = []


def value(path, keys, interp=1, discrete=False):
    keys = sorted(keys, key=lambda k: k[0])
    times = ", ".join(f"{k[0]:g}" for k in keys)
    trans = ", ".join(f"{k[2] if len(k) > 2 else 1:g}" for k in keys)
    vals = ", ".join(k[1] for k in keys)
    tracks.append(("value", path, interp,
                   f'{{"times": PackedFloat32Array({times}), "transitions": PackedFloat32Array({trans}), '
                   f'"update": {1 if discrete else 0}, "values": [{vals}]}}'))


def method(path, calls):
    calls = sorted(calls)
    times = ", ".join(f"{t:g}" for t, _, _ in calls)
    trans = ", ".join("1" for _ in calls)
    vals = ", ".join('{"args": [%s], "method": &"%s"}' % (args, m) for _, m, args in calls)
    tracks.append(("method", path, 1,
                   f'{{"times": PackedFloat32Array({times}), "transitions": PackedFloat32Array({trans}), "values": [{vals}]}}'))


T, F = "true", "false"
# giant Daven: rises 3 -> 7 s, angry teeth while throwing, sinks 13.5 -> 16.5 s
value(f"{DAVEN}:scale", [(0, V(0.6, 0.6))], discrete=True)
value(f"{DAVEN}:position", [(0, V(0, 900)), (3.0, V(0, 900), 0.5), (7.0, V(0, 170)), (13.5, V(0, 170), 2.0),
                            (16.5, V(0, 900))], interp=1)
value(f"{DAVEN}/Body/Face/Mouth:texture", [(0, E["frown"]), (7.0, E["teeth"]), (13.0, E["frown"])], discrete=True)
for arm, sign in (("ArmLeft", 1), ("ArmRight", -1)):
    keys = [(0, "0.0"), (7.0, "0.0")]
    t, k = 7.3, 0
    while t < 12.8:
        keys.append((round(t, 2), f"{sign * (0.4 if k % 2 == 0 else -0.2):g}"))
        t += 0.35
        k += 1
    keys.append((13.1, "0.0"))
    value(f"{DAVEN}/Body/{arm}:rotation", keys, interp=2)

# screen shake: rumble while he rises, a jolt at each hit
shake = [(0, V(0, 0)), (3.0, V(0, 0))]
t, k = 3.1, 0
while t < 7.0:
    shake.append((round(t, 2), V(5 if k % 2 == 0 else -5, -3 if k % 3 == 0 else 3)))
    t += 0.12
    k += 1
shake.append((7.05, V(0, 0)))
for h, t in HITS.items():
    shake += [(t, V(0, 0)), (t + 0.05, V(14, -8)), (t + 0.1, V(-10, 6)), (t + 0.18, V(0, 0))]
for group in ("Background", "village", "characters", "effects"):
    value(f"{group}:position", shake)

# houses, broken houses, fires, smoke, fireballs, mates
for i, (h, t) in enumerate(sorted(HITS.items(), key=lambda kv: kv[1]), 1):
    value(f"village/House{h}:visible", [(0, T), (t, F)], discrete=True)
    value(f"village/{BROKEN[h][0]}:visible", [(0, F), (t, T)], discrete=True)
    value(f"effects/Fire{h}:visible", [(0, F), (t, T)], discrete=True)
    value(f"effects/Smoke{h}:emitting", [(0, F), (t, T)], discrete=True)
    hx, hy = HOUSES[h][:2]
    start = (hx + 420, hy - 1150)
    fb = f"effects/Fireball{h}"
    value(f"{fb}:visible", [(0, F), (t - FALL, T), (t, F)], discrete=True)
    value(f"{fb}:position", [(0, V(*start)), (t - FALL, V(*start)), (t, V(hx, hy))])
    value(f"{fb}:rotation", [(0, "0.0"), (t - FALL, "0.0"), (t, "-12.0")])
    if h in MATES:
        method(f"characters/Mate{h}", [(4.0, "set_mood", '"scared"'), (t, "die", "")])
method("characters/Orpheus", [(4.0, "set_mood", '"scared"'), (17.0, "look_around", "")])
method(".", [(LENGTH, "go_to_training", "")])

L += ['[sub_resource type="Animation" id="Animation_cutscene"]', 'resource_name = "cutscene"', f"length = {LENGTH:g}"]
for n, (typ, path, interp, keys) in enumerate(tracks):
    L += [f'tracks/{n}/type = "{typ}"', f"tracks/{n}/imported = false", f"tracks/{n}/enabled = true",
          f'tracks/{n}/path = NodePath("{path}")', f"tracks/{n}/interp = {interp}",
          f"tracks/{n}/loop_wrap = true", f"tracks/{n}/keys = {keys}"]
L += ["", '[sub_resource type="AnimationLibrary" id="AnimationLibrary_cutscene"]',
      '_data = {&"cutscene": SubResource("Animation_cutscene")}', ""]

# --- nodes --------------------------------------------------------------------------------------
def node(name, typ, parent, props, instance=None):
    head = f'[node name="{name}"' + (f' type="{typ}"' if typ else "") + (f' parent="{parent}"' if parent else "")
    if instance:
        head += f" instance={E[instance]}"
    L.append(head + "]")
    L.extend(props)
    L.append("")


node("Stage1Village", "Node2D", None, [f'script = {E["script"]}'])
node("BoardCamera", None, ".", [], "camera")
node("Background", "Node2D", ".", [])
node("Mountains", None, "Background", [f"position = {V(31, -98.75)}", f"scale = {V(1.1946404, 0.89047617)}"], "mountains")
node("Cloud1", "Sprite2D", "Background", [f"position = {V(-437, -408)}", f'texture = {E["cloud1"]}'])
node("Cloud2", "Sprite2D", "Background", [f"position = {V(555, -381)}", f'texture = {E["cloud2"]}'])
node("TreeFull", "Sprite2D", "Background", [f"position = {V(-59, 174)}", f"scale = {V(0.28966132, 0.2972789)}",
                                             f'texture = {E["tree"]}'])
node("GroundLine", "Sprite2D", "Background", [f"position = {V(-18, 515)}", f'texture = {E["ground"]}'])
node("village", "Node2D", ".", [])
for h in sorted(HOUSES):
    x, y, sx, sy = HOUSES[h]
    props = [f"position = {V(x, y)}"] + ([f"scale = {V(sx, sy)}"] if (sx, sy) != (1, 1) else []) + [f'texture = {E["house"]}']
    node(f"House{h}", "Sprite2D", "village", props)
for h in sorted(BROKEN):
    name, tex, pos, rot, sc = BROKEN[h]
    props = ["visible = false", f"position = {V(*pos)}"] + ([f"rotation = {rot}"] if rot else []) + \
            ([f"scale = {V(*sc)}"] if sc != (1, 1) else []) + [f'texture = {E[tex]}']
    node(name, "Sprite2D", "village", props)
node("characters", "Node2D", ".", [])
for h in sorted(MATES):
    pos, s, phase = MATES[h]
    node(f"Mate{h}", None, "characters", [f"position = {V(*pos)}", f"scale = {V(s, abs(s))}", f"idle_phase = {phase}"],
         "villager")
pos, s, phase = ORPHEUS
node("Orpheus", None, "characters", [f"position = {V(*pos)}", f"scale = {V(s, s)}", f"idle_phase = {phase}"], "villager")
node("effects", "Node2D", ".", [])
for h in sorted(FIRES):
    pos, s = FIRES[h]
    node(f"Fire{h}", None, "effects", ["visible = false", f"position = {V(*pos)}"] +
         ([f"scale = {V(s, s)}"] if s != 1 else []), "fire")
for h in sorted(SMOKES):
    node(f"Smoke{h}", None, "effects", [f"position = {V(*SMOKES[h])}", "emitting = false", "spawn_every = 0.5",
                                         "rise = 300.0", "lifetime = 2.0", "wisp_scale = 0.45"], "smoke")
for i, h in enumerate(sorted(HITS)):
    hx, hy = HOUSES[h][:2]
    node(f"Fireball{h}", "Sprite2D", "effects", ["visible = false", f"position = {V(hx + 420, hy - 1150)}",
                                                  f"scale = {V(0.12, 0.12)}",
                                                  f'texture = {E["fireball1" if i % 2 == 0 else "fireball2"]}'])
node("AnimationPlayer", "AnimationPlayer", ".", ['libraries = {&"": SubResource("AnimationLibrary_cutscene")}',
                                                 'autoplay = &"cutscene"'])
open(OUT, "w", encoding="utf-8", newline="\n").write("\n".join(L))
print("tracks:", len(tracks))
