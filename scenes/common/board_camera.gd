@tool
class_name BoardCamera
extends Camera2D
## Camera that carries the classroom picture with it, so the game always looks like it is
## happening on the whiteboard.
##
## CLASSROOM view: the whole classroom fills the screen (main menu, after the intro).
## BOARD view: zoomed in on board_view_rect, so the whiteboard fills the screen (all gameplay).
## Call show_board() / show_classroom() to zoom between the two.
##
## The whiteboard is centred on the camera's position and is board_world_width units wide:
## put anything that is written on the board around (0, 0) of the camera.

enum View { CLASSROOM, BOARD }

## Which view the camera starts in.
@export var view: View = View.BOARD:
	set(value):
		view = value
		if is_node_ready() and not _moving:
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

## What the BOARD view shows, in world units around the camera's position (the board's centre).
## The whole rectangle is always kept on screen.
@export var board_view_rect := Rect2(-1158.5, -816.5, 2313, 1553):
	set(value):
		board_view_rect = value
		if is_node_ready():
			_snap()

@onready var background: Sprite2D = $Background

var _tween: Tween
var _moving := false
var _from_zoom: float
var _from_offset: Vector2
var _to_zoom: float
var _to_offset: Vector2


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
	if _tween:
		_tween.kill()
	if duration <= 0.0:
		_moving = false
		view = target
		return
	# Start from wherever the camera is right now, so the move is smooth (never a cut).
	_moving = true
	_from_zoom = zoom.x
	_from_offset = offset
	_to_zoom = _zoom_for(target).x
	_to_offset = _view_offset(target)
	view = target
	_tween = create_tween().set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)
	_tween.tween_method(_blend, 0.0, 1.0, duration)
	_tween.finished.connect(func(): _moving = false)


## t goes 0 -> 1. Zoom is blended on a log scale so zooming in feels even (no sudden rush at the
## end), and the offset follows the visible size so the board grows steadily towards the centre.
func _blend(t: float) -> void:
	var z := exp(lerpf(log(_from_zoom), log(_to_zoom), t))
	zoom = Vector2(z, z)
	var k := 1.0
	if not is_equal_approx(_to_zoom, _from_zoom):
		k = (1.0 / z - 1.0 / _from_zoom) / (1.0 / _to_zoom - 1.0 / _from_zoom)
	offset = _from_offset.lerp(_to_offset, clampf(k, 0.0, 1.0))


func _snap() -> void:
	if background == null or background.texture == null or _moving:
		return
	background.centered = true
	background.scale = Vector2.ONE * _picture_scale()
	# The whiteboard's centre always sits on the camera's position, in both views, so anything
	# placed on the board stays on the board while zooming. Only the view (offset + zoom) changes.
	background.position = -(board_rect.get_center() - background.texture.get_size() / 2.0) * _picture_scale()
	offset = _view_offset(view)
	zoom = _zoom_for(view)


func _picture_scale() -> float:
	return board_world_width / max(board_rect.size.x, 1.0)


func _screen_size() -> Vector2:
	if Engine.is_editor_hint():
		return Vector2(
			ProjectSettings.get_setting("display/window/size/viewport_width", 1152),
			ProjectSettings.get_setting("display/window/size/viewport_height", 648))
	return get_viewport_rect().size


## BOARD: the whole board_view_rect fits on screen.
## CLASSROOM: the picture fills the whole screen (cropping its edges rather than showing gaps).
func _zoom_for(target: View) -> Vector2:
	var screen := _screen_size()
	var z: float
	if target == View.BOARD:
		z = min(screen.x / board_view_rect.size.x, screen.y / board_view_rect.size.y)
	else:
		var area: Vector2 = background.texture.get_size() * _picture_scale()
		z = max(screen.x / area.x, screen.y / area.y)
	return Vector2(z, z)


## Where the view is centred, relative to the board's centre: on the board, or on the whole room.
func _view_offset(target: View) -> Vector2:
	if target == View.BOARD:
		return board_view_rect.get_center()
	return -(board_rect.get_center() - background.texture.get_size() / 2.0) * _picture_scale()
