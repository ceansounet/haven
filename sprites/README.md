# Haven sprites

Every source drawing has been cut out with a transparent background, split into
separate parts where that helps animation, and named `lowercase_with_underscores`.

The untouched source drawings are in `source drawings/` at the project root. Godot ignores that folder
(it contains a `.gdignore` file), and older versions are also in the git history.

## Ready-made Godot scenes

| Scene | What it is |
|---|---|
| `characters/orpheus/orpheus_rig.tscn` | Orpheus assembled from his parts, ready for cut-out animation |
| `characters/evil_daven/evil_daven.tscn` | the boss Evil Daven, assembled from his parts |
| `characters/old_master/old_master.tscn` | the old master on his cloud, with a `float` animation (autoplays) and a `talk` animation (`TalkPlayer`) |
| `collectibles/daven_collectible/daven_collectible.tscn` | the Daven collectible assembled from its parts (so it can wiggle or bounce when picked up) |
| `environment/props/trampoline/trampoline.tscn` | AnimatedSprite2D with an `idle` and a `bounce` animation |

### How to animate a rig
1. Open the rig scene (or drag it into your level).
2. Add an **AnimationPlayer** under the root node.
3. Key the `rotation`, `position` or `scale` of the parts. Each part already rotates around its joint:
   arms around the shoulder, legs around the hip and the tail around its base.
4. To change an expression, key the `texture` property of `Face/Eyes`, `Face/Mouth` or
   `Face/Eyebrows` and drop in a sprite from `eyes/` or `mouths/`.

Parent/child links: the arms, tail and face follow the **Body**, so moving the body moves
them too. The tail and the collectible's spikes have `show_behind_parent` on, so they draw behind the body.

The Orpheus parts were laid out on the sheet roughly where they belong, and the rig keeps those
spots. The face position is my best guess, so nudge the parts in the editor if needed.

## What's where

### characters/orpheus
| File | Part |
|---|---|
| `orpheus_body.png` | head + torso (white-filled) |
| `orpheus_arm_raised.png`, `orpheus_arm_down.png` | the two arms |
| `orpheus_leg_back.png`, `orpheus_leg_front.png` | legs |
| `orpheus_tail.png` | tail |
| `eyes/orpheus_eyes_happy.png` | `^ ^` |
| `eyes/orpheus_eyes_teary.png` | teary eyes (crying face) |
| `eyes/orpheus_eyes_wavy.png` | `~ ~` |
| `eyes/orpheus_eyebrows_angry.png` | `\ /` |
| `eyes/orpheus_eyebrows_worried.png` | `/ \` |
| `mouths/orpheus_mouth_smile.png` | smile |
| `mouths/orpheus_mouth_frown.png` | frown |
| `mouths/orpheus_mouth_flat.png` | straight line |
| `mouths/orpheus_mouth_open.png` | `v` open mouth |
| `mouths/orpheus_mouth_wobbly.png` | wobbly smile |
| `mouths/orpheus_mouth_zigzag.png` | zigzag (scared / gritting) |

### characters/evil_daven
The boss, redrawn from `source drawings/Evil daven.png` as separate parts in black + red marker,
painted with a brush sampled from the scanned drawings.
| File | Part |
|---|---|
| `evil_daven_body` | squircle body |
| `evil_daven_spikes_back`, `evil_daven_spikes_front` | the two layers of spikes |
| `evil_daven_ear_left` / `_right`, `evil_daven_arm_left` / `_right`, `evil_daven_foot_left` / `_right` | ears, arms (rotate at the shoulder), feet (rotate at the hip) |
| `evil_daven_eye_left` / `_right`, `evil_daven_pupil_left` / `_right` | bloodshot eyes, pupils (move them to make him look around) |
| `evil_daven_cheek_left` / `_right` | blush |
| `eyebrows/`: `angry` (default), `worried` | |
| `mouths/`: `frown` (default), `grin`, `teeth`, `open` | |

Redraw him with `python tools/draw_evil_daven.py sprites`.

### characters/old_master
Cut from `source drawings/old master orpheus.png` along his own lines, so every part keeps the
original drawing. White is filled in behind the beard, arms, eyes and mouth so nothing shows
through when they move.
| File | Part |
|---|---|
| `old_master_head`, `old_master_beard` | head (nods around the neck), beard (sways) |
| `old_master_eyes_closed`, `old_master_mouth` | closed wise eyes, mouth line (swap with Orpheus's eyes and mouths) |
| `old_master_arms` | crossed arms |
| `old_master_torso`, `old_master_tail` | body, tail (sways) |
| `old_master_leg_back`, `old_master_leg_front` | crossed legs |
| `old_master_cloud` | the cloud he rides (`cloud_1`, filled white) |

To make him talk while giving advice: `$TalkPlayer.play("talk")`, and `$TalkPlayer.stop()` when he's done.
Recut him with `python tools/cut_old_master.py sprites`.

### collectibles/daven_collectible
The little Daven collectible (this is **not** the boss Daven, who isn't drawn yet), cut into
`daven_collectible_body`, `_spikes`, `_arm_left` / `_right`, `_foot_left` / `_right`,
`_eye_left` / `_right`, `_cheek_left` / `_right`, `_mouth`.
Its body is outline only (no white fill), so the background shows through it.

### environment
- `blocks/`: `block_plain`, `block_brick`, `block_cracked`, `block_mystery` (the `?` cube)
- `items/`: `wand`, `key`
- `buildings/house.png`
- `castle/`: `castle_tower`, `castle_center_wall` (wall with arch), `castle_gate_portcullis` (the grid)
- `props/fence_gate.png`
- `props/tree/`: `tree_full`, plus `tree_trunk` + `tree_foliage` (so the leaves can sway)
- `props/trampoline/`: 5 frames on the same canvas size with the feet aligned
  (`1_stretched_high` → `5_squashed_deep`)
- `background/`: `cloud_1..3`, `mountain_range`

### projectiles
- `fireball/`: two fireballs, each as `_full`, `_flame` (red) and `_core` (black spiral), so the
  core can spin inside the flame
- `iceball/`: the same two balls with the flame recoloured to ice blue (`_full`, `_ice`, `_core`),
  keeping the marker texture

### effects/weather
The storm that rolls in when arriving at the castle and lasts until Daven is beaten.
- `thunder_cloud/`: two thunder clouds, each as `_full`, `_cloud` and `_lightning` (to flash the bolts)
- `thunder/`: `thunder_1`, `thunder_2` (the small zigzag bolts)
- `rain/`: 6 raindrop shapes

### classroom
- `classroom_background.png`: the classroom picture used behind everything by the board camera (temporary picture)

### ui
- `game_icon.png`

## Sizes
The large photos were scaled down (whole drawing ≤ 1500 px; environment sheet to ⅓) so the files stay
light. Parts of the same character share the same scale, so they still line up. Use the node
`scale` in Godot to size things in your levels.

## Re-cutting
`tools/cut_sprites.py` and `tools/build_rigs.py` regenerate everything:
`python tools/cut_sprites.py "source drawings/asset pack 1" sprites`, then
`python tools/build_rigs.py sprites/parts.json sprites`.
Some of the cuts use coordinates measured on these exact drawings, so new drawings need new cut rules.

## Placeholders
Every sprite that is still missing has a magenta placeholder in `placeholders/`. The full list is in
[placeholders/PLACEHOLDERS.md](placeholders/PLACEHOLDERS.md).

## Asset pack 2

Cut from `source drawings/asset pack 2/` by `tools/cut_asset_pack_2.py`, scenes built by
`tools/build_pack2_scenes.py`.

### Ready-made scenes
| Scene | What it does |
|---|---|
| `characters/scarecrow/scarecrow.tscn` | the scarecrow boss in parts: pole, body, arms (rotate at the shoulder), head + hat |
| `effects/fire/fire.tscn` | flickering fire; pick `fire_1` or `fire_2` with **Texture**. Its position is the bottom of the flames |
| `effects/smoke/smoke.tscn` | rising smoke made of your 14 wisps; **Emitting** turns it on/off |
| `effects/dash/dash.tscn` | dash speed lines: call `burst()` when dashing (plays once on its own when it appears); Scale x = -1 for a dash to the left |
| `effects/aura/aura.tscn` | the aura, 2 frames looping |
| `projectiles/power_orb/power_orb.tscn` | the power orb, 3 frames looping |
| `effects/lava/lava.tscn` | lava flowing left to right (**Scroll Speed**) that can rise (**Rise Speed**, or `rise_to(y, seconds)`); its position is the lava surface |
| `ui/boss_bar/boss_health_bar.tscn` | boss health bar: set **Value** from 0 (empty) to 100 (full) |
| `environment/background/mountains_with_giant_daven.tscn` | the mountains with giant Evil Daven hidden behind them; animations **rise** and **sink** |

### Pictures
- `ui/buttons/`: New game, Continue, Settings, Quit game, Main menu, each with a red `_hover`
  version, plus `button_continue_disabled` (grey). The main menu uses them.
- `ui/settings_wheel.png` (+ `_hover`), used in the main menu
- `ui/hearts/`: `heart_1`, `heart_2`, `heart_3` as drawn. `heart_empty_standin` is a faded grey
  copy, because no empty heart was drawn.
- `ui/speech/`: `speech_bubble_round`, `speech_bubble_long`, `speech_bubble_small`
- `ui/text/`: `text_waaa` (+ every letter in `waaa_letters/`), `text_i_didnt_sign_for_this`
- `ui/the_end/`: `the_end_text`, `the_end_frame`, `the_end_full`
- `ui/alphabet/`: your handwritten alphabet, `letter_a` … `letter_z`
- `environment/buildings/`: `house_broken_wall`, `house_broken_roof`, `house_broken_full`
- `environment/traps/`: `spikes`, `circular_saw`
- `environment/items/boots.png`, `environment/ground_line.png`
- `effects/`: `ice_block` (recoloured blue), `jump_puff`, `fire/fire_1..2`, `smoke/smoke_wisp_01..14`,
  `dash/dash_line_01..16`, `aura/aura_1..2`, `lava/lava_surface` + `lava_body` (both repeat seamlessly)
- `projectiles/power_orb/power_orb_1..3`
- `environment/background/mountain_range_sky_mask.png`: the sky above the mountain ridge, used
  to hide giant Daven behind the mountains (made by `tools/make_mountain_mask.py`)
