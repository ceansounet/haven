# Missing sprites (checked against the storyboard)

✅ = already drawn (see `sprites/README.md`)  ·  ❌ = still to draw  ·  ♻️ = reuse an existing sprite

🟪 = a **placeholder** exists for it: a magenta dashed box labelled "PLACEHOLDER" that can be used in scenes until the
drawing is done. The full list of placeholder files is in `sprites/placeholders/PLACEHOLDERS.md`.
Every ❌ below has one.

Also drawn (not in the story yet): a handwritten alphabet, one picture per letter in `sprites/ui/alphabet/`.

## Main characters and objects (from the storyboard's sprite list)

|Sprite|Status|
|-|-|
|Orpheus|✅ body, arms, legs, tail, 5 eye/eyebrow sets (incl. teary), 6 mouths|
|Boss evil Daven|✅ redrawn from `Evil daven.png` in black + red marker, with arms, feet, spikes, pupils, 4 mouths and 2 eyebrow sets|
|Daven collectible|✅ body, spikes, arms, feet, eyes, cheeks, mouth|
|Old master|✅ old Orpheus with a beard, sitting cross-legged on his cloud (tail, head, beard, arms, legs, eyes, mouth)|
|Tree|✅|
|Trampoline|✅ 5 animation frames|
|Blocks|✅ plain, brick, cracked, mystery|
|Platforms / terrain|♻️ built from the blocks|
|Fireball|✅ 2 versions|
|Ice ball|✅ 2 versions, made from the fireballs with the flame turned to ice|

## Stage 1: village cutscene

|Sprite|Status|
|-|-|
|Village houses|♻️ duplicates of `house.png`|
|Fence|✅ `fence\_gate`|
|Villagers (Orpheus's peers)|♻️ duplicates of Orpheus|
|Ground|✅ `environment/ground\_line.png`|
|Destroyed / burning house|✅ `house\_broken\_full` (or the two pieces `house\_broken\_wall` + `house\_broken\_roof`)|
|Fire on the ground (flames, smoke)|✅ `effects/fire/fire.tscn` (flickering, 2 drawings) + `effects/smoke/smoke.tscn` (rising wisps)|
|Orpheus crying, swearing revenge|✅ teary eyes + frown, angry eyebrows|
|Sky / background|✅ clouds, mountains|

## Stage 2: training

|Sprite|Status|
|-|-|
|Old master|✅|
|Master's cloud|✅ part of the old master scene|
|Scarecrow (boss)|✅ `characters/scarecrow/scarecrow.tscn`: head, arms, body, pole + hat|
|Key (reward for beating the scarecrow)|✅|
|Mystery cube|✅ `block\_mystery`|
|Boots (double jump)|✅ `environment/items/boots.png`|
|Magic wand|✅|
|Fire ball / ice ball|✅|
|Dash effect|✅ `effects/dash/dash.tscn` (16 speed lines that shoot back and fade)|
|Jump / double-jump puff|✅ `effects/jump\_puff.png`|
|Tip speech bubble|✅ 3 bubbles in `ui/speech/`|

## Stage 3: travel to the castle

|Sprite|Status|
|-|-|
|Traps (spikes, etc.)|✅ `environment/traps/spikes.png`, `environment/traps/circular\_saw.png`|
|Bad guys / enemies|❌ · 🟪 **placeholder:** `sprites/placeholders/stage\_3/placeholder\_enemy.png`|
|Backgrounds|✅ mountains, clouds, tree|
|Castle from outside|✅ tower, center wall, gate (portcullis)|
|Storm on arrival: thunder cloud, rain, thunder|✅ `thunder\_cloud\_1..2`, `raindrop\_\*`, `thunder\_1..2`|

## Stage 4: boss fight

|Sprite|Status|
|-|-|
|Castle arena (inside walls / background)|❌ (floor ♻️ blocks) · 🟪 **placeholder:** `sprites/placeholders/stage\_4/placeholder\_arena\_background.png`|
|Boss Daven|✅|
|Daven rising from the ground (cracks / dust)|❌ · 🟪 **placeholder:** `sprites/placeholders/stage\_4/placeholder\_ground\_cracks.png`, `sprites/placeholders/stage\_4/placeholder\_dust.png`|
|Daven's fireballs|✅|
|Lava (rising)|✅ `effects/lava/lava.tscn`: scrolls left to right, can rise|
|Robots|❌ · 🟪 **placeholder:** `sprites/placeholders/stage\_4/placeholder\_robot.png`|
|Frozen robot / ice block effect|✅ `effects/ice\_block.png` (recoloured blue)|
|Small Daven running, arms flailing|♻️ the Evil Daven rig scaled down, arms and feet animated|
|Speech bubbles ("waaaa", "what's that, I didn't sign for this!")|✅ bubbles in `ui/speech/`, texts `ui/text/text\_waaa.png` (+ each letter) and `ui/text/text\_i\_didnt\_sign\_for\_this.png`|
|Orpheus closed eyes|❌ · 🟪 **placeholder:** `sprites/placeholders/stage\_4/placeholder\_orpheus\_eyes\_closed.png`|
|Floating aura around Orpheus|✅ `effects/aura/aura.tscn` (2 frames)|
|Powerful orb|✅ `projectiles/power\_orb/power\_orb.tscn` (3 frames)|
|Daven frozen in place and time|❌ (ice overlay or color tint) · 🟪 **placeholder:** `sprites/placeholders/stage\_4/placeholder\_daven\_frozen.png`|
|Final explosion / blast|❌ · 🟪 **placeholder:** `sprites/placeholders/stage\_4/placeholder\_explosion.png`|
|Storm during the fight (goes away when Daven is beaten)|✅ same as stage 3|
|"The end" screen|✅ `ui/the\_end/` (text, frame, both)|

## Menus and UI

|Sprite|Status|
|-|-|
|"Main menu" button|✅ `ui/buttons/button\_main\_menu.png` (+ red hover)|
|"New game" button|✅ used in the main menu (+ red hover)|
|"Continue" button|✅ used in the main menu (+ red hover, + grey when there's no save)|
|"Settings" button|✅ `ui/buttons/button\_settings.png` (+ red hover)|
|"Quit game" button|✅ used in the main menu (+ red hover)|
|Settings wheel (gear icon)|✅ used in the main menu (+ red hover)|
|Player health: 3 hearts|✅ 3 hearts in `ui/hearts/` · ❌ no empty heart drawn: `heart\_empty\_standin.png` is a faded copy standing in for it|
|Boss health bar|✅ `ui/boss\_bar/boss\_health\_bar.tscn` (set its Value 0 to 100)|
|Game icon|✅ `sprites/ui/game\_icon.png`|


Tip: for buttons, draw a **normal**, **hover** and **pressed** version of each (or one blank
button + the text drawn separately), so Godot's `TextureButton` can show them reacting.

## Game intro (to do last, waiting for a good whiteboard)

|Sprite|Status|
|-|-|
|Classroom seen from a student's desk (POV)|❌ · 🟪 **placeholder:** `sprites/placeholders/intro/placeholder\_classroom\_pov.png`|
|Whiteboard (empty frame)|❌ · 🟪 **placeholder:** `sprites/placeholders/intro/placeholder\_whiteboard\_frame.png`|
|Math written on the board (before it changes)|❌ · 🟪 **placeholder:** `sprites/placeholders/intro/placeholder\_board\_math.png`|
|Desk + the student's arms (for putting the head down)|❌ · 🟪 **placeholder:** `sprites/placeholders/intro/placeholder\_desk\_and\_arms.png`|
|Eyelids closing / blink overlay|❌ · 🟪 **placeholder:** `sprites/placeholders/intro/placeholder\_eyelid\_top.png`, `sprites/placeholders/intro/placeholder\_eyelid\_bottom.png`|
|Menu drawn on the whiteboard|♻️ the menu buttons above|
