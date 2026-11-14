# Haven scenes

Every scene is empty for now except for the **BoardCamera**, which makes the game look like it
happens on the classroom whiteboard.

| Scene | Storyboard part | Camera view |
|---|---|---|
| `intro/intro.tscn` | classroom intro (whiteboard turns into the menu) | classroom |
| `menus/main_menu.tscn` | main menu, the whole classroom in view | classroom |
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

- **View** in the Inspector: `CLASSROOM` shows the whole room (main menu), `BOARD` zooms in until
  only the whiteboard is in frame (gameplay).
- **Board Rect**: where the whiteboard is inside the picture, in picture pixels. Update it if you
  replace the classroom picture.
- **Board World Width**: how wide the whiteboard is in world units (1920 by default). Lay out
  levels at that scale.
- In code: `$BoardCamera.show_board(1.0)` zooms from the classroom onto the board over 1 second,
  for example when "New game" is pressed. `show_classroom()` zooms back out.
