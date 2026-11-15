extends Node2D
## Stage 1 cutscene: the village is destroyed. Everything happens in AnimationPlayer "cutscene",
## which plays by itself and calls go_to_training() at the end.

const NEXT_SCENE := "res://scenes/levels/stage_2_training.tscn"


## Called by the cutscene animation at the very end.
func go_to_training() -> void:
	get_tree().change_scene_to_file(NEXT_SCENE)


## Press Enter or Space to skip the cutscene.
func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("ui_accept"):
		go_to_training()
