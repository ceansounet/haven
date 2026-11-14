# Placeholder sprites

Every sprite that is still missing has a placeholder here: a **magenta dashed box** with
"PLACEHOLDER" and its name, so it's impossible to miss in the game. Use them in scenes while
the drawings aren't done. To replace one: draw it, save it in the right `sprites/` folder (same
name without `placeholder_`), then in each scene that uses it, drag the new drawing onto the
node's **Texture** in the Inspector. Once nothing uses a placeholder any more, delete it and its row.

Regenerate them all with `python tools/make_placeholders.py sprites`.

| Placeholder file | Size (px) | What it stands for |
|---|---|---|
| `sprites/placeholders/stage_1/placeholder_ground.png` | 1920 × 60 | Stage 1: village ground (a few marker lines) |
| `sprites/placeholders/stage_1/placeholder_house_destroyed.png` | 485 × 610 | Stage 1: destroyed / burning house (same size as house.png at scale 2.5) |
| `sprites/placeholders/stage_1/placeholder_fire.png` | 220 × 260 | Stage 1: fire on the ground |
| `sprites/placeholders/stage_1/placeholder_smoke.png` | 260 × 260 | Stage 1: smoke |
| `sprites/placeholders/stage_2/placeholder_scarecrow.png` | 380 × 620 | Stage 2: scarecrow boss |
| `sprites/placeholders/stage_2/placeholder_boots.png` | 140 × 110 | Stage 2: boots (double jump) |
| `sprites/placeholders/stage_2/placeholder_dash_effect.png` | 300 × 140 | Stage 2: dash effect |
| `sprites/placeholders/stage_2/placeholder_jump_puff.png` | 220 × 110 | Stage 2: jump / double-jump puff |
| `sprites/placeholders/stage_2/placeholder_tip_speech_bubble.png` | 600 × 300 | Stage 2: the old master's tip bubble |
| `sprites/placeholders/stage_3/placeholder_spike_trap.png` | 240 × 100 | Stage 3: spike trap |
| `sprites/placeholders/stage_3/placeholder_enemy.png` | 260 × 300 | Stage 3: bad guy |
| `sprites/placeholders/stage_4/placeholder_arena_background.png` | 1920 × 1164 | Stage 4: castle arena (inside walls), fills the board |
| `sprites/placeholders/stage_4/placeholder_ground_cracks.png` | 700 × 160 | Stage 4: cracks when Daven rises |
| `sprites/placeholders/stage_4/placeholder_dust.png` | 400 × 200 | Stage 4: dust when Daven rises |
| `sprites/placeholders/stage_4/placeholder_lava.png` | 1920 × 500 | Stage 4: rising lava |
| `sprites/placeholders/stage_4/placeholder_robot.png` | 260 × 360 | Stage 4: robot |
| `sprites/placeholders/stage_4/placeholder_ice_block.png` | 320 × 420 | Stage 4: frozen robot / ice block |
| `sprites/placeholders/stage_4/placeholder_speech_bubble.png` | 600 × 300 | Stage 4: speech bubbles ("waaaa", "what's that, I didn't sign for this!") |
| `sprites/placeholders/stage_4/placeholder_orpheus_eyes_closed.png` | 60 × 32 | Stage 4: Orpheus closed eyes (Orpheus face scale) |
| `sprites/placeholders/stage_4/placeholder_aura.png` | 600 × 700 | Stage 4: floating aura around Orpheus |
| `sprites/placeholders/stage_4/placeholder_orb.png` | 200 × 200 | Stage 4: powerful orb |
| `sprites/placeholders/stage_4/placeholder_daven_frozen.png` | 900 × 1000 | Stage 4: ice over Daven, frozen in place and time |
| `sprites/placeholders/stage_4/placeholder_explosion.png` | 900 × 900 | Stage 4: final explosion / blast |
| `sprites/placeholders/stage_4/placeholder_the_end.png` | 1920 × 1164 | "The end" screen, fills the board |
| `sprites/placeholders/ui/placeholder_button_main_menu.png` | 600 × 140 | Menu: "Main menu" button |
| `sprites/placeholders/ui/placeholder_button_new_game.png` | 600 × 140 | Menu: "New game" button |
| `sprites/placeholders/ui/placeholder_button_continue.png` | 600 × 140 | Menu: "Continue" button |
| `sprites/placeholders/ui/placeholder_button_continue_disabled.png` | 600 × 140 | Menu: "Continue" button, greyed out (no save) |
| `sprites/placeholders/ui/placeholder_button_settings.png` | 600 × 140 | Menu: "Settings" button |
| `sprites/placeholders/ui/placeholder_button_quit_game.png` | 600 × 140 | Menu: "Quit game" button |
| `sprites/placeholders/ui/placeholder_heart_full.png` | 120 × 110 | UI: player heart, full (x3) |
| `sprites/placeholders/ui/placeholder_heart_empty.png` | 120 × 110 | UI: player heart, empty |
| `sprites/placeholders/ui/placeholder_boss_health_bar_frame.png` | 1000 × 80 | UI: boss health bar frame |
| `sprites/placeholders/ui/placeholder_boss_health_bar_fill.png` | 980 × 60 | UI: boss health bar fill |
| `sprites/placeholders/intro/placeholder_classroom_pov.png` | 1920 × 1080 | Intro: classroom seen from a student's desk |
| `sprites/placeholders/intro/placeholder_whiteboard_frame.png` | 1600 × 900 | Intro: empty whiteboard frame |
| `sprites/placeholders/intro/placeholder_board_math.png` | 1200 × 600 | Intro: math written on the board |
| `sprites/placeholders/intro/placeholder_desk_and_arms.png` | 1920 × 500 | Intro: desk + the student's arms |
| `sprites/placeholders/intro/placeholder_eyelid_top.png` | 1920 × 600 | Intro: top eyelid closing |
| `sprites/placeholders/intro/placeholder_eyelid_bottom.png` | 1920 × 600 | Intro: bottom eyelid closing |

Also placeholders (made earlier, used in the main menu):
- the **New game / Continue / Quit game** buttons in `scenes/menus/main_menu.tscn` are drawn by
  Godot with `scenes/menus/placeholder_menu_theme.tres`
- `sprites/ui/placeholder_settings_wheel.png` (the gear in the menu)
