@tool
extends Node2D
## Lava that scrolls from left to right and can rise.
## This node's position is the lava's surface: everything below it is lava.
##
## - scroll_speed: how fast it flows to the right (negative = to the left).
## - rise_speed: how fast it climbs, in units per second (0 = it stays put).
## - In code: $Lava.rise_to(-300, 8.0) makes it climb to y = -300 in 8 seconds,
##   $Lava.stop_rising() freezes it.

@export var scroll_speed := 120.0
@export var rise_speed := 0.0
@export var width := 6000.0:
	set(value):
		width = value
		if is_node_ready():
			_layout()
@export var depth := 3000.0:
	set(value):
		depth = value
		if is_node_ready():
			_layout()
## Light colour behind the dots, so the lava reads as one mass.
@export var fill_color := Color(0.85, 0.25, 0.2, 0.12):
	set(value):
		fill_color = value
		if is_node_ready():
			_layout()

@onready var fill: ColorRect = $Fill
@onready var surface: Sprite2D = $Surface
@onready var body: Sprite2D = $Body

var _flow := 0.0
var _tween: Tween


func _ready() -> void:
	_layout()


func _layout() -> void:
	var sh := surface.texture.get_height()
	for s: Sprite2D in [surface, body]:
		s.texture_repeat = CanvasItem.TEXTURE_REPEAT_ENABLED
		s.region_enabled = true
		s.centered = false
	surface.region_rect = Rect2(0, 0, width, sh)
	surface.position = Vector2(-width / 2.0, 0)
	body.region_rect = Rect2(0, 0, width, depth)
	body.position = Vector2(-width / 2.0, sh * 0.85)
	fill.color = fill_color
	fill.position = Vector2(-width / 2.0, sh * 0.15)
	fill.size = Vector2(width, depth + sh)


func _process(delta: float) -> void:
	if Engine.is_editor_hint():
		return
	_flow += scroll_speed * delta
	surface.region_rect.position.x = fposmod(-_flow, surface.texture.get_width())
	body.region_rect.position.x = fposmod(-_flow * 0.7, body.texture.get_width())
	if rise_speed != 0.0:
		position.y -= rise_speed * delta


## Smoothly move the surface to y = target_y over the given time.
func rise_to(target_y: float, seconds: float) -> void:
	stop_rising()
	_tween = create_tween().set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)
	_tween.tween_property(self, "position:y", target_y, seconds)


func stop_rising() -> void:
	rise_speed = 0.0
	if _tween:
		_tween.kill()
