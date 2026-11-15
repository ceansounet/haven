@tool
extends Node2D
## Cancels the parent's stretching, so whatever is inside keeps its own proportions even if the
## mountains are stretched (non-uniform Scale). Put the giant Daven inside this node.


func _process(_delta: float) -> void:
	var s: Vector2 = (get_parent() as Node2D).get_global_transform().get_scale()
	if s.x != 0.0 and s.y != 0.0:
		scale = Vector2(1.0 / s.x, 1.0 / s.y)
