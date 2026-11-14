@tool
class_name BoardCamera
extends Camera2D
## Camera that carries the classroom picture with it, so the game always looks like it is
## happening on the whiteboard.
##
## CLASSROOM view: the whole classroom fills the screen (main menu, after the intro).
## BOARD view: zoomed in so only the whiteboard is in frame (all gameplay).
## Call show_board() / show_classroom() to zoom between the two.

enum View { CLASSROOM, BOARD }

## Which view the camera starts in.
@export var view: View = View.BOARD:
	set(value):
		view = value
		if is_node_ready():
			_snap()

## The whiteboard's writing area inside the background picture, in picture pixels.
## Update this if the classroom picture is replaced.
@export var board_rect := Rect2(91, 57, 259, 157):
	set(value):
		board_rect = value
		if is_node_ready():
			_snap()

## How wide the whiteboard is in world units. Level content is laid out at this scale:
## with the default 1920, the board is 1920 units wide.
@export var board_world_width := 1920.0:
	set(value):
		board_world_width = value
		if is_node_ready():
			_snap()

@onready var background: Sprite2D = $Background

var _tween: Tween


func _ready() -> void:
	if not Engine.is_editor_hint():
		get_viewport().size_changed.connect(_snap)
	_snap()


## Zoom in until only the whiteboard is in frame.
func show_board(duration := 1.0) -> void:
	_go(View.BOARD, duration)


## Zoom out to show the whole classroom.
func show_classroom(duration := 1.0) -> void:
	_go(View.CLASSROOM, duration)


func _go(target: View, duration: float) -> void:
	view = target
	if _tween:
		_tween.kill()
	if duration <= 0.0:
		_snap()
		return
	_tween = create_tween().set_parallel().set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)
	_tween.tween_property(self, "zoom", _zoom_for(target), duration)
	_tween.tween_property(background, "position", _background_offset(target), duration)


func _snap() -> void:
	if background == null or background.texture == null:
		return
	background.centered = true
	background.scale = Vector2.ONE * _picture_scale()
	background.position = _background_offset(view)
	zoom = _zoom_for(view)


func _picture_scale() -> float:
	return board_world_width / max(board_rect.size.x, 1.0)


func _screen_size() -> Vector2:
	if Engine.is_editor_hint():
		return Vector2(
			ProjectSettings.get_setting("display/window/size/viewport_width", 1152),
			ProjectSettings.get_setting("display/window/size/viewport_height", 648))
	return get_viewport_rect().size


## Zoom that makes the target fill the whole screen (cropping the edges rather than showing gaps).
func _zoom_for(target: View) -> Vector2:
	var s := _picture_scale()
	var area: Vector2 = board_rect.size * s if target == View.BOARD else background.texture.get_size() * s
	var screen := _screen_size()
	var z: float = max(screen.x / area.x, screen.y / area.y)
	return Vector2(z, z)


## Where the picture sits so the board (or the whole room) is centred on the camera.
func _background_offset(target: View) -> Vector2:
	var tex_size := background.texture.get_size()
	var focus: Vector2 = board_rect.get_center() if target == View.BOARD else tex_size / 2.0
	return -(focus - tex_size / 2.0) * _picture_scale()
