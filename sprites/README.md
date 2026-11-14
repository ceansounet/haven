# Haven sprites

Every source drawing has been cut out with a transparent background, split into
separate parts where that helps animation, and named `lowercase_with_underscores`.

The untouched source drawings are in `asset pack 1 - ORIGINAL BACKUP/`. Godot ignores that folder
(it contains a `.gdignore` file), and older versions are also in the git history.

## Ready-made Godot scenes

| Scene | What it is |
|---|---|
| `characters/orpheus/orpheus_rig.tscn` | Orpheus assembled from his parts, ready for cut-out animation |
| `characters/evil_daven/marker/evil_daven_marker.tscn` | the boss Evil Daven, black + red marker version |
| `characters/evil_daven/color/evil_daven_color.tscn` | the boss Evil Daven, full colour version (same parts and positions) |
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
The boss, redrawn from `Evil daven.png` (in the project root) as separate parts, in two versions
with identical shapes: `marker/` (black + red marker, painted with a brush sampled from the scanned
drawings) and `color/` (the painting's colours with a marker-stroke fill).
| File | Part |
|---|---|
| `evil_daven_body` | squircle body |
| `evil_daven_spikes_back`, `evil_daven_spikes_front` | the two layers of spikes |
| `evil_daven_ear_left` / `_right`, `evil_daven_arm_left` / `_right`, `evil_daven_foot_left` / `_right` | ears, arms (rotate at the shoulder), feet (rotate at the hip) |
| `evil_daven_eye_left` / `_right`, `evil_daven_pupil_left` / `_right` | bloodshot eyes, pupils (move them to make him look around) |
| `evil_daven_cheek_left` / `_right` | blush |
| `eyebrows/`: `angry` (default), `worried` | |
| `mouths/`: `frown` (default), `grin`, `teeth`, `open` | |

Redraw him with `python tools/draw_evil_daven.py sprites` (or add `marker` / `color` for one version).

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

### ui
- `game_icon.png`

## Sizes
The large photos were scaled down (whole drawing ≤ 1500 px; environment sheet to ⅓) so the files stay
light. Parts of the same character share the same scale, so they still line up. Use the node
`scale` in Godot to size things in your levels.

## Re-cutting
`tools/cut_sprites.py` and `tools/build_rigs.py` regenerate everything:
`python tools/cut_sprites.py "asset pack 1 - ORIGINAL BACKUP" sprites`, then
`python tools/build_rigs.py sprites/parts.json sprites`.
Some of the cuts use coordinates measured on these exact drawings, so new drawings need new cut rules.
