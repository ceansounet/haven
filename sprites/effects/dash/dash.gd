extends Node2D
## Speed lines for the dash. Each line you drew is a child Sprite2D. Call burst() when the
## player dashes: the lines shoot backwards (to the left) and fade out.
## For a dash to the left, set this node's Scale x to -1.

## Play once as soon as it appears (handy: spawn it at the player, it plays by itself).
@export var play_on_start := true
## Keep repeating (only for previewing it).
@export var loop := false
@export var distance := 220.0
@export var duration := 0.35

var _home := {}


func _ready() -> void:
	for c in get_children():
		if c is Sprite2D:
			_home[c] = c.position
			c.modulate.a = 0.0
	if play_on_start:
		burst()


func burst() -> void:
	for c in _home:
		c.position = _home[c]
		c.modulate.a = 1.0
		var tw := create_tween().set_parallel().set_ease(Tween.EASE_OUT)
		tw.tween_property(c, "position:x", _home[c].x - distance * randf_range(0.6, 1.4), duration)
		tw.tween_property(c, "modulate:a", 0.0, duration)
	if loop:
		get_tree().create_timer(duration + 0.25).timeout.connect(burst)
