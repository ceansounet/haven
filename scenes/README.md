# Haven scenes

Every scene is empty for now except for the **BoardCamera**, which makes the game look like it
happens on the classroom whiteboard, and the main menu's placeholder buttons.

| Scene | Storyboard part | Camera view |
|---|---|---|
| `intro/intro.tscn` | classroom intro (whiteboard turns into the menu) | classroom |
| `menus/main_menu.tscn` | main menu on the whiteboard, the whole classroom in view (see below) | classroom |
| `cutscenes/stage_1_village.tscn` | stage 1: Orpheus's village is destroyed | board |
| `levels/stage_2_training.tscn` | stage 2: training + scarecrow, old master on his cloud | board |
| `levels/stage_3_travel_1.tscn` | stage 3: first travel level | board |
| `levels/stage_3_travel_2.tscn` | stage 3: second travel level, arriving at the castle in the storm | board |
| `levels/stage_4_boss_fight.tscn` | stage 4: arena reveal and the Evil Daven fight | board |
| `menus/the_end.tscn` | "the end" | board |

## BoardCamera (`common/board_camera.tscn`)
A Camera2D that carries the classroom picture (`sprites/classroom/classroom_background.png`) as
its child, so the picture always follows the camera. When the camera moves through a level, the
whiteboard stays still on screen and the level scrolls across it.

- **View** in the Inspector: `CLASSROOM` shows the whole room (main menu), `BOARD` zooms onto the
  whiteboard (gameplay).
- **Board View Rect**: exactly what the `BOARD` view shows, in world units around the board's centre
  (currently 2313 × 1553, centred at (-2, -40)). The whole rectangle always stays on screen.
- **Board Rect**: where the whiteboard is inside the picture, in picture pixels. Update it if you
  replace the classroom picture.
- **Board World Width**: how wide the whiteboard is in world units (1920 by default). Lay out
  levels at that scale.
- In code: `$BoardCamera.show_board(1.0)` zooms from the classroom onto the board over 1 second,
  for example when "New game" is pressed. `show_classroom()` zooms back out.

## Main menu (`menus/main_menu.tscn`)
**Placeholders:** the buttons and the gear are temporary and must be replaced by the drawings
(tracked in `MISSING_SPRITES.md`).
- **New game**, **Continue** and **Quit game** sit in the middle of the board, and the **settings
  wheel** sits in its bottom-left corner. Move them freely in the editor: the `Menu` node covers the
  whole board.
- **Hover:** the button turns red with a light red tint and grows a little (`menu_button.gd` +
  `placeholder_menu_theme.tres`).
- **Continue** is greyed out and can't be clicked when there's no save file
  (`user://savegame.json`). When there is one, it loads the scene stored in it as `{"scene": "res://..."}`.
- **New game** zooms from the classroom onto the whiteboard while the menu fades, then opens stage 1.
- **Quit game** closes the game. The **settings wheel** only prints a message for now (no settings screen yet).
- Anything placed on the board stays on the board during the zoom: the board's centre is always
  at the camera's position.

## Guides
- [Making the Stage 1 village cutscene](../docs/stage_1_village_cutscene_guide.md): step-by-step, for someone new to Godot.

## Stage 1 cutscene (`cutscenes/stage_1_village.tscn`)
Built on your village layout. Everything is driven by one animation, **cutscene** (AnimationPlayer,
plays by itself, 25 s). Enter or Space skips it. At the end it opens stage 2.

| Time | What happens |
|---|---|
| 0 → 3 s | Orpheus and his 5 mates hang around (each mate idles on its own) |
| 3 → 7 s | the ground rumbles and giant Daven rises behind the mountains; at 4 s everyone looks scared |
| 8 → 12 s | 6 fireballs fall from the sky, one per house: House3 at 8.0 s, House5 at 8.8, House1 at 9.6, House6 at 10.4, House2 at 11.2, House4 at 12.0 |
| on each hit | **HouseN** disappears and **HouseBroken…N** appears, **FireN** lights up, **SmokeN** starts, **MateN** dies (falls and fades), and the screen jolts |
| 13.5 → 16.5 s | Daven sinks back behind the mountains |
| 17 → 20 s | Orpheus looks left and right, then turns sad (teary eyes, frown, arm down) |
| 25 s | `go_to_training()` opens stage 2 |

**Numbers match:** House N ↔ HouseBroken…N ↔ Fire N ↔ Smoke N ↔ Fireball N ↔ Mate N. House 1 has no
mate. Your fires and smokes were renamed to match: Fire3 → Fire5, Fire2 → Fire3, Fire → Fire2,
Smoke → Smoke3, Smoke2 → Smoke5, Smoke3 → Smoke2. Fire/Smoke 1, 4 and 6 are new.

**Villagers** (`sprites/characters/orpheus/villager.tscn`) are Orpheus look-alikes with their own
animations (idle, die, look_around, sad). The cutscene calls `set_mood("scared")`, `die()` and
`look_around()` on them. Orpheus himself is one too.

**Changing it:** select the AnimationPlayer and drag keys left or right in the Animation panel to
change the timing. Move houses, mates and fires in the viewport as usual. The fireball tracks fly
to each house's position, so if you move a house, update the last key of its `FireballN:position`
track.
