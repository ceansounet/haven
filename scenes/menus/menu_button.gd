extends BaseButton
## Menu button: grows a little while the mouse is over it (the red hover picture is set on the
## TextureButton itself).

@export var hover_scale := 1.08


func _ready() -> void:
	resized.connect(_center_pivot)
	_center_pivot()
	mouse_entered.connect(_set_hovered.bind(true))
	mouse_exited.connect(_set_hovered.bind(false))


func _center_pivot() -> void:
	pivot_offset = size / 2.0


func _set_hovered(on: bool) -> void:
	if on and disabled:
		return
	create_tween().tween_property(self, "scale", Vector2.ONE * (hover_scale if on else 1.0), 0.12)
