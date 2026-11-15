# Making the Stage 1 cutscene: the village is destroyed

A step-by-step guide that assumes you've never used Godot. Follow it in order; every number given
(positions, sizes, times) is a starting point you can change afterwards.

**What you'll build (about 25 seconds):**

| Time | What happens |
|---|---|
| 0 → 5 s | A peaceful village: houses, a fence, a tree, mountains and clouds. Orpheus and three villagers stand around. |
| 5 → 9 s | Giant Evil Daven rises from behind the mountains (the mountains hide his lower half). |
| 9 → 13 s | He throws three fireballs. Each one hits a house: the house is destroyed, a fire starts with smoke, and the villager next to it disappears. |
| 13.5 → 16.5 s | Daven sinks back behind the mountains. |
| 16.5 → 19 s | Orpheus is alone: teary eyes, sad mouth. |
| 19 → 24 s | Angry eyebrows, and a speech bubble: "I will avenge you all!" |
| 25 s | The game moves on to Stage 2 (training). |

Everything used here is drawn now. (If you started with the magenta placeholders for the ground,
destroyed house, fire or smoke, section 11 shows how to swap them for the drawings.)

---

## 1. The Godot window in 2 minutes

When the project is open, the window has these parts:

- **Scene dock** (top left): the list of everything in the scene you're editing, as a tree.
  Things lower in the list are drawn **on top of** things higher up.
- **FileSystem dock** (bottom left): the project's files (`res://` = the project folder).
- **The viewport** (middle): where you see and move things. Make sure **2D** is selected in the
  bar at the very top of the window.
- **Inspector** (right): the settings of whatever is selected in the Scene dock.
- **Bottom panel**: Output, Debugger, **Animation**… The Animation panel appears there when you
  select an AnimationPlayer.

Useful keys:

- **F6**: run the scene you have open (to test the cutscene alone).
- **F5**: run the whole game from the main menu.
- **Ctrl+S**: save the scene. Save often!
- **Ctrl+Z**: undo.
- In the viewport, **scroll the mouse wheel** to zoom, and **hold the middle mouse button (or Space) and drag** to move around.

**Positions:** every object has a **Position** (x, y) in the Inspector under
*Node2D → Transform*. **x grows to the right and y grows DOWNWARDS** (bigger y = lower on screen).
In this game the whiteboard is centred on (0, 0) and is about 1920 wide and 1164 tall:

- the left edge is at x = -960 and the right edge at x = 960
- the top is at y = -582 and the bottom at y = 582

The camera shows a little more than that, so anything placed between about x = -1150 and 1150 and
y = -850 and 730 is visible. **The ground of the village will be at y = 500.**

---

## 2. Open the cutscene scene

1. In the **FileSystem** dock, open `scenes` → `cutscenes`.
2. Double-click **`stage_1_village.tscn`**. A tab called *stage_1_village* opens.
3. In the **Scene** dock you'll see `Stage1Village` with `BoardCamera` under it. Don't touch the
   camera: it already shows the whiteboard.

## 3. Make groups to stay organised

Groups are empty **Node2D** nodes that hold other nodes, like folders.

1. Click **`Stage1Village`** in the Scene dock.
2. Press **Ctrl+A** (or click the **+** at the top of the Scene dock). A *Create New Node* window opens.
3. Type `Node2D` in the search box, select **Node2D** and click **Create**.
4. Rename it: double-click its name in the Scene dock (or press **F2**), type `Background` and press Enter.
5. Do steps 1 to 4 again to make three more groups: **`Village`**, **`Characters`** and **`Effects`**.
   Always click `Stage1Village` first so they're created at the same level.

Keep this order from top to bottom: `BoardCamera`, `Background`, `Village`, `Characters`, `Effects`.
(If one is in the wrong place, drag it up or down in the Scene dock.) That way the background is
drawn first and the effects end up on top of everything.

## 4. How to add a picture (you'll do this a lot)

1. In the Scene dock, **click the group** the picture should go into (for example `Background`).
2. In the FileSystem dock, find the picture (`.png`) and **drag it into the viewport**. This creates
   a **Sprite2D** (a node that shows a picture).
3. Look at the Scene dock: the new node should be **under** the group, slightly indented. If it
   isn't, drag it onto the group's name.
4. Rename it (F2) to something clear.
5. In the Inspector, under **Node2D → Transform**, type the **Position** (x and y) and the **Scale**
   (x and y). Typing exact numbers is easier than dragging.

To **copy** a node with all its settings: select it and press **Ctrl+D**.

To **mirror** a picture (make it face the other way): set its **Scale x** to a negative number, for
example `-0.6` instead of `0.6`.

## 5. The background

Put these in **`Background`** (pictures are in `sprites/environment/background/`):

| Name | Picture | Position | Scale |
|---|---|---|---|
| Cloud1 | `cloud_1.png` | (-600, -450) | (0.7, 0.7) |
| Cloud2 | `cloud_2.png` | (500, -500) | (0.6, 0.6) |
| Mountains | `mountains_with_giant_daven.tscn` (a **scene**, see below) | (0, 210) | (1.1, 1.1) |
| Ground | `sprites/environment/ground_line.png` | (0, 505) | (1.1, 1) |

**The mountains are a scene, not a picture**, because giant Daven lives inside them: drag
`sprites/environment/background/mountains_with_giant_daven.tscn` into the viewport like a picture.
It contains the mountain drawing, Daven hidden behind it, and two ready-made animations, **rise**
and **sink**. (If you already placed `mountain_range.png`, delete it: select it and press
**Delete**, then add this scene with the same Position and Scale.) Section 9.3 explains how the
hiding works.

## 6. The village

Put these in **`Village`** (`sprites/environment/...`):

| Name | Picture | Position | Scale |
|---|---|---|---|
| House1 | `buildings/house.png` | (-750, 305) | (1.6, 1.6) |
| House2 | (Ctrl+D on House1) | (-150, 305) | (1.6, 1.6) |
| House3 | (Ctrl+D on House1) | (550, 305) | (1.6, 1.6) |
| Fence | `props/fence_gate.png` | (180, 366) | (2, 2) |
| Tree | `props/tree/tree_full.png` | (-880, 243) | (0.35, 0.35) |

Now the destroyed versions, **hidden for now**. Put them in `Village` too, **below** the houses in
the list:

| Name | Picture | Position | Scale |
|---|---|---|---|
| HouseDestroyed1 | `buildings/house_broken_full.png` | (-750, 433) | (0.5, 0.5) |
| HouseDestroyed2 | (Ctrl+D) | (-150, 433) | (0.5, 0.5) |
| HouseDestroyed3 | (Ctrl+D) | (550, 433) | (0.5, 0.5) |

To hide a node: select it, and in the Inspector open **CanvasItem → Visibility** and **untick
Visible** (or click the **eye icon** next to its name in the Scene dock).

Press **F6** now to check: you should see the village on the whiteboard. Close the game window to
come back.

## 7. The characters

The characters are **scenes**, not single pictures. You add them the same way: drag the `.tscn` file
into the viewport while the group is selected.

Put these in **`Characters`**:

| Name | Scene | Position | Scale |
|---|---|---|---|
| Villager1 | `sprites/characters/orpheus/orpheus_rig.tscn` | (-560, 500) | (-0.5, 0.5) |
| Villager2 | (same scene) | (50, 500) | (0.5, 0.5) |
| Villager3 | (same scene) | (760, 500) | (-0.5, 0.5) |
| Orpheus | (same scene) | (-380, 500) | (0.6, 0.6) |

Each character's position is the point **between its feet**, which is why they all have y = 500 (the ground).
(Evil Daven isn't added here: he's already inside the mountains scene.)

**Seeing inside a character.** To change Orpheus's face later, you need to see his parts:

1. Right-click **Orpheus** in the Scene dock.
2. Tick **Editable Children**. His parts appear under him (`Body`, `Face`, `Eyes`, `Mouth`…).

## 8. Effects (hidden at the start)

Put these in **`Effects`** and **hide them all** (untick Visible):

| Name | Picture / scene | Position | Scale |
|---|---|---|---|
| Fireball1 | `sprites/projectiles/fireball/fireball_1_full.png` | (270, -130) | (0.15, 0.15) |
| Fireball2 | (Ctrl+D) | (270, -130) | (0.15, 0.15) |
| Fireball3 | (Ctrl+D) | (270, -130) | (0.15, 0.15) |
| Fire1 | `sprites/effects/fire/fire.tscn` (scene) | (-750, 470) | (0.6, 0.6) |
| Fire2 | (Ctrl+D) | (-150, 470) | (0.6, 0.6) |
| Fire3 | (Ctrl+D) | (550, 470) | (0.6, 0.6) |
| Smoke1 | `sprites/effects/smoke/smoke.tscn` (scene) | (-750, 280) | (1, 1) |
| Smoke2 | (Ctrl+D) | (-150, 280) | (1, 1) |
| Smoke3 | (Ctrl+D) | (550, 280) | (1, 1) |
| SpeechBubble | `sprites/ui/speech/speech_bubble_round.png` | (-300, 60) | (1, 1) |

The fire flickers and the smoke rises by themselves while they're visible. A fire's position is
the **bottom** of its flames. To use the other fire drawing, select the fire and drag `fire_2.png` onto
**Texture** in the Inspector.

**Text in the speech bubble:**

1. Click **SpeechBubble**, press **Ctrl+A**, search **Label** and create it. It appears under the bubble.
2. In the Inspector, type in **Text**: `I will avenge you all!`
3. Under **Theme Overrides → Colors**, tick **Font Color** and pick black.
4. Under **Theme Overrides → Font Sizes**, tick **Font Size** and set `60`.
5. Under **Layout → Transform**, set **Position** to (-230, -90) and **Size** to (460, 80).
6. Set **Horizontal Alignment** to **Center**.

## 9. The animation

An **AnimationPlayer** records how things change over time: you choose a moment, set a value, and
press a **key** icon to remember it. Godot fills in the movement between two keys.

### 9.1 Create it

1. Click **`Stage1Village`**, press **Ctrl+A**, search **AnimationPlayer**, and create it.
2. With the AnimationPlayer selected, the **Animation panel** opens at the bottom.
3. Click the **Animation** button in that panel → **New**, name it `cutscene` and click OK.
4. On the right of the panel there's a **length** box (with a little stopwatch icon) showing `1`.
   Change it to **`25`** (seconds).
5. Click the **Autoplay on Load** button next to the animation name. It's an icon with an "A" and
   an arrow. The cutscene will then play by itself when the scene starts.
6. Tip: at the bottom right of the panel, set the **snap** step to **0.1**, and zoom the timeline
   with the slider so you can see all 25 seconds.

### 9.2 How to add a key (the move you'll repeat)

1. **Pick the moment**: click on the time ruler at the top of the Animation panel, or type the time
   in the number box at its top left. The blue line (the playhead) moves there.
2. **Select the node** you want to animate in the Scene dock. The Animation panel stays open.
3. **Change the value** in the Inspector (for example Position).
4. **Click the key icon** that now appears just right of that property in the Inspector.
5. The first time, Godot asks *"Create new track … and insert key?"*: click **Create**.

A diamond appears on the timeline: that's your key. To fix a key, click the diamond and edit it in
the Inspector, or drag it left or right. To delete one, select it and press **Delete**.

> ⚠️ The most common mistake: changing a value and **forgetting to click the key**. Then nothing is
> recorded. Always click the key after changing something.

### 9.3 Giant Daven rises behind the mountains (5 → 9 s)

**How the hiding works.** The mountain drawing is only lines: its inside is see-through, so just
putting Daven "behind" it wouldn't hide him. Instead, the mountains scene has an invisible shape
called **SkyMask** that covers only the sky above the mountain ridge. Its **Clip Children** setting
is on, which means anything placed inside it is only drawn where the shape is. Daven is inside it,
so he only shows above the ridge, as if the mountains were in front of him. (`UndoScale` just keeps
Daven from being stretched when the mountains are.)

The rising is already animated inside that scene (**rise**: 4 s, **sink**: 3 s). Your cutscene only
has to start them:

1. Select your **AnimationPlayer**. In the Animation panel click **+ Add Track** → **Animation
   Playback Track**, and pick **Mountains** → `AnimationPlayer` (the one inside the mountains;
   tick **Editable Children** on Mountains first if you can't see it).
2. Move the playhead to **5.0**, right-click on the new track → **Insert Key**, and choose **rise**.

Press **F6**: at 5 s Daven comes up from behind the peaks. To change how high he comes up or how
big he is: right-click Mountains → Editable Children, then edit `SkyMask/UndoScale/GiantDaven`
(its Scale) or the **rise** animation inside `mountains_with_giant_daven.tscn`.

### 9.4 The three fireballs (8 → 12.5 s)

Fireball 1 hits House3 (it starts at Daven's raised hand):

- At **8.9**: Fireball1 → Visible **off** → key.
- At **9.0**: Visible **on** → key. Position (270, -130) → key. Rotation 0 → key.
- At **10.0**: Position (550, 305) → key. Rotation 720 → key (it spins twice). Visible **off** → key.

When it hits, at **10.0**, add keys for the house, the fire, the smoke and the villager:

- House3: Visible **off** → key.
- HouseDestroyed3: Visible **on** → key. Also add a key at **0.0** with Visible **off**.
- Fire3 and Smoke3: Visible **on** → key. Also add keys at **0.0** with Visible **off**.
- Villager3: Visible **off** → key. Also add a key at **0.0** with Visible **on**.

> Why the keys at 0.0? So that when the animation starts again, everything goes back to how it
> was at the beginning.

Do the same with:

- **Fireball2** from **10.5 to 11.5**, ending at (-150, 305), destroying **House2** / **Villager2**.
- **Fireball3** from **12.0 to 13.0**, ending at (-750, 305), destroying **House1** / **Villager1**.

For a bigger hit, add a little shake: put `Background` and `Village` (and `Characters`) inside one
more group called `World`. Key World's Position at 10.0: (0, 0), 10.05: (15, -10), 10.1: (-12, 8),
10.2: (0, 0). Copy the same keys around 11.5 and 13.0. Don't shake the camera itself: the camera
carries the classroom picture.

### 9.5 Daven sinks back down (13.5 → 16.5 s)

On the **Animation Playback Track** from 9.3, right-click at **13.5** → **Insert Key** → **sink**.

### 9.6 Orpheus is sad, then angry (16.5 → 24 s)

Open Orpheus's children (Editable Children, step 7): `Orpheus/Body/Face/Eyes`, `Mouth` and `Eyebrows`.

To key a **picture change**: select `Eyes`, then drag a picture from the FileSystem dock onto the
**Texture** box in the Inspector, then click the key next to Texture.

- At **0.0**: Eyes texture `orpheus_eyes_happy.png` → key. Mouth texture `orpheus_mouth_smile.png` → key.
- At **16.5**: Eyes `sprites/characters/orpheus/eyes/orpheus_eyes_teary.png` → key.
  Mouth `.../mouths/orpheus_mouth_frown.png` → key.
- At **0.0**: Eyebrows Visible **off** → key.
- At **19.0**: Eyebrows Texture `orpheus_eyebrows_angry.png` → key, Visible **on** → key.
  Eyes `orpheus_eyes_wavy.png` → key. Mouth `orpheus_mouth_zigzag.png` → key.
- SpeechBubble: Visible **off** at 0.0 and 18.9 → keys, **on** at 19.0 → key, **off** at 24.0 → key.

### 9.7 Go to Stage 2 at the end (25 s)

The animation needs to tell the game to change scene. That takes 3 lines of code.

1. Right-click **`Stage1Village`** → **Attach Script**. Keep the suggested path
   (`res://scenes/cutscenes/stage_1_village.gd`) and click **Create**.
2. The script editor opens. Replace everything in it with:

   ```gdscript
   extends Node2D

   ## Called by the cutscene animation at the very end.
   func go_to_training() -> void:
   	get_tree().change_scene_to_file("res://scenes/levels/stage_2_training.tscn")


   ## Press Enter or Space to skip the cutscene.
   func _unhandled_input(event: InputEvent) -> void:
   	if event.is_action_pressed("ui_accept"):
   		go_to_training()
   ```

   (The indented lines start with a **Tab**.) Press **Ctrl+S**, then click **2D** at the top to go back.
3. Select the **AnimationPlayer**. In the Animation panel click **+ Add Track** → **Call Method
   Track**, and pick **`Stage1Village`**.
4. Move the playhead to **25.0**, **right-click** on that new track at 25.0 → **Insert Key** → choose
   **`go_to_training`**.

### 9.8 Test

Press **Ctrl+S**, then **F5** (whole game): click **New game**, the camera zooms onto the board and
the cutscene plays, then Stage 2 opens (still empty for now). **Enter** skips the cutscene.

---

## 10. When something doesn't work

| Problem | Fix |
|---|---|
| A picture doesn't show | Is it Visible? Is it inside the board area (step 1)? Is another picture covering it (move it lower in the Scene dock)? |
| I can't find Orpheus's eyes / mouth | Right-click Orpheus → Editable Children. |
| My animation change didn't stay | You changed the value but didn't click the **key** icon. |
| Nothing moves when I press F6 | Autoplay on Load isn't turned on, or the animation length is still 1 s. |
| Something is huge or tiny | Check its **Scale** in the Inspector. |
| Everything is upside down or mirrored | A Scale is negative by mistake. |
| The red errors at the bottom talk about a path | A file was moved or renamed: drag the picture into the Texture box again. |

## 11. Swapping placeholders for drawings

If your scene still uses magenta placeholders, here's how to swap each one.

**A picture for a picture** (ground, destroyed houses):

1. Click the node (for example `PlaceholderGround`, or each `HouseDestroyed`).
2. Drag the drawing from the FileSystem dock onto its **Texture** in the Inspector:
   - ground → `sprites/environment/ground_line.png` (Position (0, 505), Scale (1.1, 1))
   - destroyed house → `sprites/environment/buildings/house_broken_full.png` (Scale (0.5, 0.5),
     Position y 433)
3. Rename the node if you like (F2). Its animation keys keep working.

**A picture for an animated scene** (fire, smoke): these drawings are animated scenes, so the old
node has to be replaced:

1. Note the old node's **name** and **Position**, then select it and press **Delete**.
2. With `Effects` selected, drag `sprites/effects/fire/fire.tscn` (or `smoke/smoke.tscn`) into the
   viewport, give it the **same name** and Position. Scale (0.6, 0.6) for fire.
3. Animation keys belong to a node name: if the name is the same, the old Visible keys work again.
   If the Animation panel shows a red track, delete it and add the Visible keys again.

When nothing uses a placeholder any more, delete its file in `sprites/placeholders/` and its row
in `sprites/placeholders/PLACEHOLDERS.md`.
