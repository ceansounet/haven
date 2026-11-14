extends Node2D
## Main menu, written on the whiteboard while the whole classroom is in view.
## New game zooms onto the board and starts stage 1.

const SAVE_PATH := "user://savegame.json"
const FIRST_SCENE := "res://scenes/cutscenes/stage_1_village.tscn"
const ZOOM_TIME := 1.2

@onready var camera: BoardCamera = $BoardCamera
@onready var menu: Control = $Menu
@onready var new_game_button: Button = $Menu/NewGame
@onready var continue_button: Button = $Menu/Continue
@onready var quit_button: Button = $Menu/Quit
@onready var settings_button: Button = $Menu/Settings


func _ready() -> void:
	continue_button.disabled = not has_save()  # greyed out when there is no save
	new_game_button.pressed.connect(_start.bind(FIRST_SCENE))
	continue_button.pressed.connect(_on_continue)
	quit_button.pressed.connect(get_tree().quit)
	settings_button.pressed.connect(_on_settings)


static func has_save() -> bool:
	return FileAccess.file_exists(SAVE_PATH)


func _on_continue() -> void:
	var scene := FIRST_SCENE
	var data = JSON.parse_string(FileAccess.get_file_as_string(SAVE_PATH))
	if data is Dictionary and ResourceLoader.exists(str(data.get("scene", ""))):
		scene = data["scene"]
	_start(scene)


func _on_settings() -> void:
	print("Settings: not made yet")  # TODO: settings screen (first thing to cut if time is short)


## Zoom from the classroom onto the whiteboard while the menu fades out, then load the scene.
func _start(scene: String) -> void:
	menu.mouse_filter = Control.MOUSE_FILTER_STOP
	for b in [new_game_button, continue_button, quit_button, settings_button]:
		b.disabled = true
	camera.show_board(ZOOM_TIME)
	create_tween().tween_property(menu, "modulate:a", 0.0, ZOOM_TIME * 0.6)
	await get_tree().create_timer(ZOOM_TIME).timeout
	get_tree().change_scene_to_file(scene)
