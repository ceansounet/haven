"""Build the Godot scenes for asset pack 2 (run after cut_asset_pack_2.py).

Usage: python tools/build_pack2_scenes.py sprites
"""
import json
import sys
from pathlib import Path

SPR = Path(sys.argv[1])
meta = json.loads((SPR / "asset_pack_2_parts.json").read_text())


def ext(lines, items):
    """items: list of (type, res path) -> returns {path: id}."""
    ids = {}
    for i, (typ, path) in enumerate(items, 1):
        lines.append(f'[ext_resource type="{typ}" path="res://{path}" id="{i}"]')
        ids[path] = i
    lines.append("")
    return ids


def write(rel, lines):
    (SPR / rel).write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    print("wrote", rel)


def frames_scene(rel, name, textures, speed):
    L = ["[gd_scene format=3]", ""]
    ids = ext(L, [("Texture2D", f"sprites/{t}") for t in textures])
    fr = ", ".join('{"duration": 1.0, "texture": ExtResource("%d")}' % ids[f"sprites/{t}"] for t in textures)
    L += ['[sub_resource type="SpriteFrames" id="SpriteFrames_1"]',
          f'animations = [{{"frames": [{fr}], "loop": true, "name": &"default", "speed": {speed}}}]', "",
          f'[node name="{name}" type="AnimatedSprite2D"]', 'sprite_frames = SubResource("SpriteFrames_1")',
          'autoplay = "default"']
    write(rel, L)


# aura (2 frames) and power orb (3 frames), looping
frames_scene("effects/aura/aura.tscn", "Aura", ["effects/aura/aura_1.png", "effects/aura/aura_2.png"], 4.0)
frames_scene("projectiles/power_orb/power_orb.tscn", "PowerOrb",
             [f"projectiles/power_orb/power_orb_{i}.png" for i in (1, 2, 3)], 8.0)

# fire: flicker around the base
L = ["[gd_scene format=3]", ""]
ids = ext(L, [("Script", "sprites/effects/fire/fire.gd"), ("Texture2D", "sprites/effects/fire/fire_1.png")])
L += ['[sub_resource type="Animation" id="Animation_flicker"]', 'resource_name = "flicker"', "length = 0.8",
      "loop_mode = 1",
      'tracks/0/type = "value"', 'tracks/0/path = NodePath("Flame:scale")', "tracks/0/interp = 2",
      "tracks/0/loop_wrap = true",
      'tracks/0/keys = {"times": PackedFloat32Array(0, 0.2, 0.45, 0.65, 0.8), "transitions": '
      'PackedFloat32Array(1, 1, 1, 1, 1), "update": 0, "values": [Vector2(1, 1), Vector2(1.05, 0.93), '
      'Vector2(0.96, 1.07), Vector2(1.03, 0.97), Vector2(1, 1)]}',
      'tracks/1/type = "value"', 'tracks/1/path = NodePath("Flame:skew")', "tracks/1/interp = 2",
      "tracks/1/loop_wrap = true",
      'tracks/1/keys = {"times": PackedFloat32Array(0, 0.3, 0.6, 0.8), "transitions": '
      'PackedFloat32Array(1, 1, 1, 1), "update": 0, "values": [0.0, 0.06, -0.05, 0.0]}', "",
      '[sub_resource type="AnimationLibrary" id="AnimationLibrary_1"]',
      '_data = {&"flicker": SubResource("Animation_flicker")}', "",
      '[node name="Fire" type="Node2D"]', f'script = ExtResource("{ids["sprites/effects/fire/fire.gd"]}")',
      f'texture = ExtResource("{ids["sprites/effects/fire/fire_1.png"]}")', "",
      '[node name="Flame" type="Sprite2D" parent="."]',
      f'texture = ExtResource("{ids["sprites/effects/fire/fire_1.png"]}")', "",
      '[node name="AnimationPlayer" type="AnimationPlayer" parent="."]',
      'libraries = {&"": SubResource("AnimationLibrary_1")}', 'autoplay = &"flicker"']
write("effects/fire/fire.tscn", L)

# smoke: script spawns wisps
wisps = sorted(k for k in meta if k.startswith("effects/smoke/smoke_wisp_"))
L = ["[gd_scene format=3]", ""]
ids = ext(L, [("Script", "sprites/effects/smoke/smoke.gd")] + [("Texture2D", f"sprites/{w}") for w in wisps])
arr = ", ".join(f'ExtResource("{ids["sprites/" + w]}")' for w in wisps)
L += ['[node name="Smoke" type="Node2D"]', f'script = ExtResource("{ids["sprites/effects/smoke/smoke.gd"]}")',
      f"wisps = Array[Texture2D]([{arr}])"]
write("effects/smoke/smoke.tscn", L)

# dash: every line where it was drawn, centred on the whole drawing
lines = sorted(k for k in meta if k.startswith("effects/dash/dash_line_"))
full = meta["effects/dash/dash_full.png"]["center"]
L = ["[gd_scene format=3]", ""]
ids = ext(L, [("Script", "sprites/effects/dash/dash.gd")] + [("Texture2D", f"sprites/{w}") for w in lines])
L += ['[node name="Dash" type="Node2D"]', f'script = ExtResource("{ids["sprites/effects/dash/dash.gd"]}")', ""]
for i, w in enumerate(lines, 1):
    c = meta[w]["center"]
    L += [f'[node name="Line{i:02d}" type="Sprite2D" parent="."]',
          f"position = Vector2({c[0] - full[0]:.1f}, {c[1] - full[1]:.1f})",
          f'texture = ExtResource("{ids["sprites/" + w]}")', ""]
write("effects/dash/dash.tscn", L)

# lava
L = ["[gd_scene format=3]", ""]
ids = ext(L, [("Script", "sprites/effects/lava/lava.gd"), ("Texture2D", "sprites/effects/lava/lava_surface.png"),
              ("Texture2D", "sprites/effects/lava/lava_body.png")])
L += ['[node name="Lava" type="Node2D"]', f'script = ExtResource("{ids["sprites/effects/lava/lava.gd"]}")', "",
      '[node name="Fill" type="ColorRect" parent="."]', "mouse_filter = 2", "",
      '[node name="Body" type="Sprite2D" parent="."]', "texture_repeat = 2",
      f'texture = ExtResource("{ids["sprites/effects/lava/lava_body.png"]}")', "centered = false",
      "region_enabled = true", "",
      '[node name="Surface" type="Sprite2D" parent="."]', "texture_repeat = 2",
      f'texture = ExtResource("{ids["sprites/effects/lava/lava_surface.png"]}")', "centered = false",
      "region_enabled = true"]
write("effects/lava/lava.tscn", L)

# boss health bar
L = ["[gd_scene format=3]", ""]
ids = ext(L, [("Texture2D", "sprites/ui/boss_bar/boss_bar_empty.png"),
              ("Texture2D", "sprites/ui/boss_bar/boss_bar_full.png")])
L += ['[node name="BossHealthBar" type="TextureProgressBar"]', "offset_right = 1000.0", "offset_bottom = 170.0",
      "mouse_filter = 2", "value = 100.0",
      f'texture_under = ExtResource("{ids["sprites/ui/boss_bar/boss_bar_empty.png"]}")',
      f'texture_progress = ExtResource("{ids["sprites/ui/boss_bar/boss_bar_full.png"]}")']
write("ui/boss_bar/boss_health_bar.tscn", L)

# scarecrow rig: origin at the bottom of the pole
SC = "characters/scarecrow/"
pole = meta[SC + "scarecrow_pole.png"]
origin = (pole["center"][0], pole["center"][1] + pole["size"][1] / 2)
hat = meta[SC + "scarecrow_hat.png"]
head = meta[SC + "scarecrow_head.png"]
head_top = (head["center"][0], head["center"][1] - head["size"][1] / 2 + 12)
nodes = [  # name, parent, file, pivot, extra
    ("Pole", ".", "scarecrow_pole.png", None, []),
    ("Body", ".", "scarecrow_body.png", None, []),
    ("ArmLeft", "Body", "scarecrow_arm_left.png", None, ["show_behind_parent = true"]),
    ("ArmRight", "Body", "scarecrow_arm_right.png", None, ["show_behind_parent = true"]),
    ("Head", "Body", "scarecrow_head.png", None, []),
    ("Hat", "Body/Head", "scarecrow_hat.png", head_top, ["scale = Vector2(0.5, 0.5)"]),
]
L = ["[gd_scene format=3]", ""]
ids = ext(L, [("Texture2D", f"sprites/{SC}{n[2]}") for n in nodes])
L += ['[node name="Scarecrow" type="Node2D"]', ""]
piv = {".": origin}
for name, parent, f, pivot, extra in nodes:
    m = meta[SC + f]
    p = pivot or m.get("pivot") or m["center"]
    piv[name if parent == "." else f"{parent}/{name}"] = p
    pp = piv[parent]
    L.append(f'[node name="{name}" type="Sprite2D" parent="{parent}"]')
    L.append(f"position = Vector2({p[0] - pp[0]:.1f}, {p[1] - pp[1]:.1f})")
    L.append(f'texture = ExtResource("{ids["sprites/" + SC + f]}")')
    if name == "Hat":  # sit the hat's brim on top of the head
        L.append(f"offset = Vector2(0, {-m['size'][1] / 2 + 20:.1f})")
    else:
        c = m["center"]
        if abs(c[0] - p[0]) > 0.05 or abs(c[1] - p[1]) > 0.05:
            L.append(f"offset = Vector2({c[0] - p[0]:.1f}, {c[1] - p[1]:.1f})")
    L += extra + [""]
write(SC + "scarecrow.tscn", L)

(SPR / "asset_pack_2_parts.json").unlink()
