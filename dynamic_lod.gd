extends Spatial

var loader
var time_max = 100 # msec
var current_scene
var current_lod

export (Array, String, FILE, "*.gltf") var lod_resources
export (Array, float) var lod_distances
var last_distance = -1


# Called when the node enters the scene tree for the first time.
func _ready():
	var root = get_node('.')
	current_scene = root  #.get_child(root.get_child_count() -1)
	var placeholder = get_node("placeholder")
	if placeholder:
		placeholder.queue_free()


func load_scene(path): # Game requests to switch to this scene.
	loader = ResourceLoader.load_interactive(path)
	if loader == null: # Check for errors.
		print('error loading resource')


func _process(_delta):
	if loader == null:
		return
	
	var t = OS.get_ticks_msec()
	# Use "time_max" to control for how long we block this thread.
	while OS.get_ticks_msec() < t + time_max:
		# Poll your loader.
		var err = loader.poll()

		if err == ERR_FILE_EOF: # Finished loading.
			var resource = loader.get_resource()
			loader = null
			set_new_scene(resource)
			break
		elif err == OK:
			pass
		else: # Error during loading.
			pass
			loader = null
			break


func _physics_process(_delta):
	# don't try loading a new scene if the loader is currently loading a LOD
	if loader != null:
		return
	
	var camera := get_viewport().get_camera()
	if camera == null:
		return
	var distance := camera.global_transform.origin.distance_to(global_transform.origin)
	update_distance(distance)


func set_new_scene(scene_resource):
	var last_lod = current_lod
	current_lod = scene_resource.instance()
	current_scene.add_child(current_lod)
	if last_lod:
		last_lod.queue_free()


func update_distance(distance):
	for i in range(len(lod_distances)):
		if distance < lod_distances[i]:
			if last_distance != i:
				load_scene(lod_resources[i])
				last_distance = i
			return
	
	# we ran out of LOD levels, unload
	if current_lod:
		current_lod.queue_free()


func _on_VisibilityEnabler_camera_exited(_camera):
	# if this scene is no longer visible, unload
	if current_lod:
		current_lod.queue_free()
	last_distance = -1
	set_physics_process(false)


func _on_VisibilityEnabler_camera_entered(_camera):
	set_physics_process(true)
