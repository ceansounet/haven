# Missing sprites (checked against the storyboard)

✅ = already drawn (see `sprites/README.md`)  ·  ❌ = still to draw  ·  ♻️ = reuse an existing sprite

## Main characters and objects (from the storyboard's sprite list)
| Sprite | Status |
|---|---|
| Orpheus | ✅ body, arms, legs, tail, 5 eye/eyebrow sets (incl. teary), 6 mouths |
| Boss evil Daven | ✅ redrawn from `Evil daven.png` in two versions (black + red marker, and full colour), with arms, feet, spikes, pupils, 4 mouths and 2 eyebrow sets |
| Daven collectible | ✅ body, spikes, arms, feet, eyes, cheeks, mouth |
| Old master | ❌ (storyboard idea: Orpheus with a long beard, so a **beard** piece + maybe a hat/robe on top of the Orpheus rig) |
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
| Ground | ❌ just a few lines of marker |
| Destroyed / burning house | ❌ |
| Fire on the ground (flames, smoke) | ❌ (♻️ the fireball flame could work for small fires) |
| Orpheus crying, swearing revenge | ✅ teary eyes + frown, angry eyebrows |
| Sky / background | ✅ clouds, mountains |

## Stage 2: training
| Sprite | Status |
|---|---|
| Old master | ❌ (see the top of this list) |
| Master's cloud | ♻️ `cloud_1..3` |
| Scarecrow (boss) | ❌ |
| Key (reward for beating the scarecrow) | ✅ |
| Mystery cube | ✅ `block_mystery` |
| Boots (double jump) | ❌ |
| Magic wand | ✅ |
| Fire ball / ice ball | ✅ |
| Dash effect | ❌ |
| Jump / double-jump puff | ❌ |
| Tip speech bubble | ❌ |

## Stage 3: travel to the castle
| Sprite | Status |
|---|---|
| Traps (spikes, etc.) | ❌ |
| Bad guys / enemies | ❌ |
| Backgrounds | ✅ mountains, clouds, tree |
| Castle from outside | ✅ tower, center wall, gate (portcullis) |
| Storm on arrival: thunder cloud, rain, thunder | ✅ `thunder_cloud_1..2`, `raindrop_*`, `thunder_1..2` |

## Stage 4: boss fight
| Sprite | Status |
|---|---|
| Castle arena (inside walls / background) | ❌ (floor ♻️ blocks) |
| Boss Daven | ✅ |
| Daven rising from the ground (cracks / dust) | ❌ |
| Daven's fireballs | ✅ |
| Lava (rising) | ❌ |
| Robots | ❌ |
| Frozen robot / ice block effect | ❌ |
| Small Daven running, arms flailing | ♻️ the Evil Daven rig scaled down, arms and feet animated |
| Speech bubbles ("waaaa", "what's that, I didn't sign for this!") | ❌ |
| Orpheus closed eyes | ❌ |
| Floating aura around Orpheus | ❌ |
| Powerful orb | ❌ |
| Daven frozen in place and time | ❌ (ice overlay or color tint) |
| Final explosion / blast | ❌ |
| Storm during the fight (goes away when Daven is beaten) | ✅ same as stage 3 |
| "The end" screen | ❌ |

## Menus and UI
| Sprite | Status |
|---|---|
| "Main menu" button | ❌ |
| "New game" button | ❌ |
| "Continue" button | ❌ (+ a grayed-out version for when there's no save) |
| "Settings" button | ❌ |
| "Quit game" button | ❌ |
| Settings wheel (gear icon) | ❌ |
| Player health: 3 hearts | ❌ (a full heart + an empty heart is enough) |
| Boss health bar | ❌ |
| Game icon | ✅ `sprites/ui/game_icon.png` |

Tip: for buttons, draw a **normal**, **hover** and **pressed** version of each (or one blank
button + the text drawn separately), so Godot's `TextureButton` can show them reacting.

## Game intro (to do last, waiting for a good whiteboard)
| Sprite | Status |
|---|---|
| Classroom seen from a student's desk (POV) | ❌ |
| Whiteboard (empty frame) | ❌ |
| Math written on the board (before it changes) | ❌ |
| Desk + the student's arms (for putting the head down) | ❌ |
| Eyelids closing / blink overlay | ❌ |
| Menu drawn on the whiteboard | ♻️ the menu buttons above |
