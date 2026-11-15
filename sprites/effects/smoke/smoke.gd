extends Node2D
## Rising smoke made from the separate smoke wisps you drew. Wisps keep appearing around this
## node's position, drift up, grow a little and fade out. Turn it on/off with "emitting".

@export var wisps: Array[Texture2D] = []
@export var emitting := true
## Seconds between two new wisps.
@export var spawn_every := 0.18
## How high a wisp rises before it disappears.
@export var rise := 420.0
@export var lifetime := 2.2
## How far left/right of the centre a wisp can start.
@export var spread := 70.0
@export var wisp_scale := 0.6

var _timer := 0.0


func _process(delta: float) -> void:
	if not emitting or wisps.is_empty():
		return
	_timer += delta
	while _timer >= spawn_every:
		_timer -= spawn_every
		_spawn()


func _spawn() -> void:
	var s := Sprite2D.new()
	s.texture = wisps.pick_random()
	s.position = Vector2(randf_range(-spread, spread), 0)
	s.scale = Vector2.ONE * wisp_scale * randf_range(0.7, 1.1)
	s.modulate.a = 0.0
	add_child(s)
	var move := create_tween().set_parallel().set_ease(Tween.EASE_OUT).set_trans(Tween.TRANS_SINE)
	move.tween_property(s, "position:y", -rise * randf_range(0.8, 1.2), lifetime)
	move.tween_property(s, "position:x", s.position.x + randf_range(-60.0, 60.0), lifetime)
	move.tween_property(s, "scale", s.scale * 1.4, lifetime)
	var fade := create_tween()
	fade.tween_property(s, "modulate:a", 1.0, lifetime * 0.2)
	fade.tween_property(s, "modulate:a", 0.0, lifetime * 0.8)
	fade.tween_callback(s.queue_free)
