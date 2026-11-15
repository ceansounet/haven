@tool
extends Node2D
## A flickering fire. Pick the drawing with "Texture" in the Inspector (fire_1 or fire_2).
## The flicker (AnimationPlayer "flicker") squashes and leans the flame around its base,
## so you can still scale and move this node freely.

@export var texture: Texture2D:
	set(value):
		texture = value
		if is_node_ready():
			_apply()


func _ready() -> void:
	_apply()


func _apply() -> void:
	var flame: Sprite2D = $Flame
	flame.texture = texture
	if texture:
		flame.offset = Vector2(0, -texture.get_height() / 2.0)  # grow from the bottom
