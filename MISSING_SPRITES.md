# Missing sprites (checked against the storyboard)

✅ = already drawn (see `sprites/README.md`)  ·  ❌ = still to draw  ·  ♻️ = reuse an existing sprite

🟪 = a **placeholder** exists for it: a magenta dashed box labelled "PLACEHOLDER" that can be used in scenes until the
drawing is done. The full list of placeholder files is in `sprites/placeholders/PLACEHOLDERS.md`.
Every ❌ below has one.

## Main characters and objects (from the storyboard's sprite list)
| Sprite | Status |
|---|---|
| Orpheus | ✅ body, arms, legs, tail, 5 eye/eyebrow sets (incl. teary), 6 mouths |
| Boss evil Daven | ✅ redrawn from `Evil daven.png` in black + red marker, with arms, feet, spikes, pupils, 4 mouths and 2 eyebrow sets |
| Daven collectible | ✅ body, spikes, arms, feet, eyes, cheeks, mouth |
| Old master | ✅ old Orpheus with a beard, sitting cross-legged on his cloud (tail, head, beard, arms, legs, eyes, mouth) |
| Tree | ✅ |
| Trampoline | ✅ 5 animation frames |
| Blocks | ✅ plain, brick, cracked, mystery |
| Platforms / terrain | ♻️ built from the blocks |
| Fireball | ✅ 2 versions |
| Ice ball | ✅ 2 versions, made from the fireballs with the flame turned to ice |

## Stage 1: village cutscene
| Sprite | Status |
|---|---|
| Village houses | ♻️ duplicates of `house.png` |
| Fence | ✅ `fence_gate` |
| Villagers (Orpheus's peers) | ♻️ duplicates of Orpheus |
| Ground | ❌ just a few lines of marker · 🟪 **placeholder:** `sprites/placeholders/stage_1/placeholder_ground.png` |
| Destroyed / burning house | ❌ · 🟪 **placeholder:** `sprites/placeholders/stage_1/placeholder_house_destroyed.png` |
| Fire on the ground (flames, smoke) | ❌ (♻️ the fireball flame could work for small fires) · 🟪 **placeholder:** `sprites/placeholders/stage_1/placeholder_fire.png`, `sprites/placeholders/stage_1/placeholder_smoke.png` |
| Orpheus crying, swearing revenge | ✅ teary eyes + frown, angry eyebrows |
| Sky / background | ✅ clouds, mountains |

## Stage 2: training
| Sprite | Status |
|---|---|
| Old master | ✅ |
| Master's cloud | ✅ part of the old master scene |
| Scarecrow (boss) | ❌ · 🟪 **placeholder:** `sprites/placeholders/stage_2/placeholder_scarecrow.png` |
| Key (reward for beating the scarecrow) | ✅ |
| Mystery cube | ✅ `block_mystery` |
| Boots (double jump) | ❌ · 🟪 **placeholder:** `sprites/placeholders/stage_2/placeholder_boots.png` |
| Magic wand | ✅ |
| Fire ball / ice ball | ✅ |
| Dash effect | ❌ · 🟪 **placeholder:** `sprites/placeholders/stage_2/placeholder_dash_effect.png` |
| Jump / double-jump puff | ❌ · 🟪 **placeholder:** `sprites/placeholders/stage_2/placeholder_jump_puff.png` |
| Tip speech bubble | ❌ · 🟪 **placeholder:** `sprites/placeholders/stage_2/placeholder_tip_speech_bubble.png` |

## Stage 3: travel to the castle
| Sprite | Status |
|---|---|
| Traps (spikes, etc.) | ❌ · 🟪 **placeholder:** `sprites/placeholders/stage_3/placeholder_spike_trap.png` |
| Bad guys / enemies | ❌ · 🟪 **placeholder:** `sprites/placeholders/stage_3/placeholder_enemy.png` |
| Backgrounds | ✅ mountains, clouds, tree |
| Castle from outside | ✅ tower, center wall, gate (portcullis) |
| Storm on arrival: thunder cloud, rain, thunder | ✅ `thunder_cloud_1..2`, `raindrop_*`, `thunder_1..2` |

## Stage 4: boss fight
| Sprite | Status |
|---|---|
| Castle arena (inside walls / background) | ❌ (floor ♻️ blocks) · 🟪 **placeholder:** `sprites/placeholders/stage_4/placeholder_arena_background.png` |
| Boss Daven | ✅ |
| Daven rising from the ground (cracks / dust) | ❌ · 🟪 **placeholder:** `sprites/placeholders/stage_4/placeholder_ground_cracks.png`, `sprites/placeholders/stage_4/placeholder_dust.png` |
| Daven's fireballs | ✅ |
| Lava (rising) | ❌ · 🟪 **placeholder:** `sprites/placeholders/stage_4/placeholder_lava.png` |
| Robots | ❌ · 🟪 **placeholder:** `sprites/placeholders/stage_4/placeholder_robot.png` |
| Frozen robot / ice block effect | ❌ · 🟪 **placeholder:** `sprites/placeholders/stage_4/placeholder_ice_block.png` |
| Small Daven running, arms flailing | ♻️ the Evil Daven rig scaled down, arms and feet animated |
| Speech bubbles ("waaaa", "what's that, I didn't sign for this!") | ❌ · 🟪 **placeholder:** `sprites/placeholders/stage_4/placeholder_speech_bubble.png` |
| Orpheus closed eyes | ❌ · 🟪 **placeholder:** `sprites/placeholders/stage_4/placeholder_orpheus_eyes_closed.png` |
| Floating aura around Orpheus | ❌ · 🟪 **placeholder:** `sprites/placeholders/stage_4/placeholder_aura.png` |
| Powerful orb | ❌ · 🟪 **placeholder:** `sprites/placeholders/stage_4/placeholder_orb.png` |
| Daven frozen in place and time | ❌ (ice overlay or color tint) · 🟪 **placeholder:** `sprites/placeholders/stage_4/placeholder_daven_frozen.png` |
| Final explosion / blast | ❌ · 🟪 **placeholder:** `sprites/placeholders/stage_4/placeholder_explosion.png` |
| Storm during the fight (goes away when Daven is beaten) | ✅ same as stage 3 |
| "The end" screen | ❌ · 🟪 **placeholder:** `sprites/placeholders/stage_4/placeholder_the_end.png` |

## Menus and UI
| Sprite | Status |
|---|---|
| "Main menu" button | ❌ · 🟪 **placeholder:** `sprites/placeholders/ui/placeholder_button_main_menu.png` |
| "New game" button | ❌ · 🟪 **placeholder:** `sprites/placeholders/ui/placeholder_button_new_game.png` |
| "Continue" button | ❌ (+ a grayed-out version for when there's no save) · 🟪 **placeholder:** `sprites/placeholders/ui/placeholder_button_continue.png`, `sprites/placeholders/ui/placeholder_button_continue_disabled.png` |
| "Settings" button | ❌ · 🟪 **placeholder:** `sprites/placeholders/ui/placeholder_button_settings.png` |
| "Quit game" button | ❌ · 🟪 **placeholder:** `sprites/placeholders/ui/placeholder_button_quit_game.png` |
| Settings wheel (gear icon) | ❌ · 🟪 **placeholder:** `sprites/ui/placeholder_settings_wheel.png` (already used in the main menu) |
| Player health: 3 hearts | ❌ (a full heart + an empty heart is enough) · 🟪 **placeholder:** `sprites/placeholders/ui/placeholder_heart_full.png`, `sprites/placeholders/ui/placeholder_heart_empty.png` |
| Boss health bar | ❌ · 🟪 **placeholder:** `sprites/placeholders/ui/placeholder_boss_health_bar_frame.png`, `sprites/placeholders/ui/placeholder_boss_health_bar_fill.png` |
| Game icon | ✅ `sprites/ui/game_icon.png` |

⚠️ **Placeholders to replace:** the main menu (`scenes/menus/main_menu.tscn`) uses temporary buttons drawn by Godot (`placeholder_menu_theme.tres`) and a temporary gear icon. Once the drawings exist, swap them in (e.g. turn the buttons into `TextureButton`s) and delete the placeholders.

Tip: for buttons, draw a **normal**, **hover** and **pressed** version of each (or one blank
button + the text drawn separately), so Godot's `TextureButton` can show them reacting.

## Game intro (to do last, waiting for a good whiteboard)
| Sprite | Status |
|---|---|
| Classroom seen from a student's desk (POV) | ❌ · 🟪 **placeholder:** `sprites/placeholders/intro/placeholder_classroom_pov.png` |
| Whiteboard (empty frame) | ❌ · 🟪 **placeholder:** `sprites/placeholders/intro/placeholder_whiteboard_frame.png` |
| Math written on the board (before it changes) | ❌ · 🟪 **placeholder:** `sprites/placeholders/intro/placeholder_board_math.png` |
| Desk + the student's arms (for putting the head down) | ❌ · 🟪 **placeholder:** `sprites/placeholders/intro/placeholder_desk_and_arms.png` |
| Eyelids closing / blink overlay | ❌ · 🟪 **placeholder:** `sprites/placeholders/intro/placeholder_eyelid_top.png`, `sprites/placeholders/intro/placeholder_eyelid_bottom.png` |
| Menu drawn on the whiteboard | ♻️ the menu buttons above |
