extends Node2D
## An Orpheus-style villager (also used for Orpheus in cutscenes).
## Plays "idle" (hanging around) by itself. Other moves, callable from a cutscene's
## Call Method Track:
##   set_mood("happy" / "scared" / "sad")  - changes the face
##   die()                                 - falls over and fades away
##   look_around()                         - turns left and right, then becomes sad
##   be_sad()                              - sad face, arm down, slumped

## Shifts this villager's idle loop (0 to 1) so they don't all move in sync.
@export var idle_phase := 0.0

const FACES := {
	"happy": ["orpheus_eyes_happy", "orpheus_mouth_smile", ""],
	"scared": ["orpheus_eyes_wavy", "orpheus_mouth_open", "orpheus_eyebrows_worried"],
	"sad": ["orpheus_eyes_teary", "orpheus_mouth_frown", "orpheus_eyebrows_worried"],
}
const DIR := "res://sprites/characters/orpheus/"

@onready var anim: AnimationPlayer = $AnimationPlayer
@onready var eyes: Sprite2D = $Rig/Body/Face/Eyes
@onready var mouth: Sprite2D = $Rig/Body/Face/Mouth
@onready var eyebrows: Sprite2D = $Rig/Body/Face/Eyebrows


func _ready() -> void:
	anim.play("idle")
	anim.seek(idle_phase * anim.current_animation_length, true)


func set_mood(mood: String) -> void:
	var f: Array = FACES.get(mood, FACES["happy"])
	eyes.texture = load(DIR + "eyes/" + f[0] + ".png")
	mouth.texture = load(DIR + "mouths/" + f[1] + ".png")
	eyebrows.visible = f[2] != ""
	if f[2] != "":
		eyebrows.texture = load(DIR + "eyes/" + f[2] + ".png")


func die() -> void:
	set_mood("scared")
	anim.play("die")


func look_around() -> void:
	set_mood("scared")
	anim.play("look_around")
	anim.queue("sad")
	await anim.animation_changed
	set_mood("sad")


func be_sad() -> void:
	set_mood("sad")
	anim.play("sad")
