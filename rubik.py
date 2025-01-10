import bpy
import random
import math
from mathutils import Vector, Matrix, Quaternion
import kociemba

# A function that deletes all objects before creating the cube
def setup_scene():
    bpy.ops.object.mode_set(mode='OBJECT')
    # Select all objects in the scene
    bpy.ops.object.select_all(action='SELECT')
    # Delete all selected objects
    bpy.ops.object.delete()
    # delete meshes
    for item in bpy.data.meshes:
        bpy.data.meshes.remove(item)
    # Loop through all collections
    for collection in bpy.data.collections:
        # Make sure it's not the master scene collection or one that's needed
        if collection != bpy.context.scene.collection:
            bpy.data.collections.remove(collection)
    for material in bpy.data.materials:
        bpy.data.materials.remove(material)


def create_cubes(collection):
    for x in range(-1, 2):
        for y in range(-1, 2):
            for z in range(-1, 2):
                bpy.ops.mesh.primitive_cube_add(location=(x * 2, y * 2, z * 2))
                obj = bpy.context.active_object
                obj.name = f"{x} {y} {z}"
                collection.objects.link(obj)


# decorator function to apply an operation to all the cubes
def apply_all(func, collection):
    for obj in collection.all_objects:
        # Check if the object is a mesh and if it's a cube
        func(obj)


def create_color(name, color):
    material = bpy.data.materials.new(name=name)
    # Enable 'Use nodes' (the material will use the node system)
    material.use_nodes = True
    # Access the material's node tree
    nodes = material.node_tree.nodes

    bsdf = nodes.get('Principled BSDF')  # get_bsdf
    bsdf.inputs['Base Color'].default_value = color  # RGBA format (R, G, B, A)
    bsdf.inputs['Roughness'].default_value = 0.3
    return material


def add_materials(obj, materials):
    for material in materials:
        material_bpy = bpy.data.materials.get(material)
        obj.data.materials.append(material_bpy)


def default_colors():
    # red-green-yellow
    bpy.ops.object.select_all(action='DESELECT')
    obj = bpy.data.objects.get("1 -1 1")
    add_materials(obj, ["red", "green", "yellow", "black"])
    obj.data.polygons[0].material_index = 3
    obj.data.polygons[1].material_index = 3
    obj.data.polygons[2].material_index = 1
    obj.data.polygons[3].material_index = 0
    obj.data.polygons[4].material_index = 3
    obj.data.polygons[5].material_index = 2
    # red-yellow
    bpy.ops.object.select_all(action='DESELECT')
    obj = bpy.data.objects.get("0 -1 1")
    add_materials(obj, ["red", "yellow", "black"])
    obj.data.polygons[0].material_index = 2
    obj.data.polygons[1].material_index = 2
    obj.data.polygons[2].material_index = 2
    obj.data.polygons[3].material_index = 0
    obj.data.polygons[4].material_index = 2
    obj.data.polygons[5].material_index = 1
    # pure red
    bpy.ops.object.select_all(action='DESELECT')
    obj = bpy.data.objects.get("0 -1 0")
    add_materials(obj, ["red", "black"])
    obj.data.polygons[0].material_index = 1
    obj.data.polygons[1].material_index = 1
    obj.data.polygons[2].material_index = 1
    obj.data.polygons[3].material_index = 0
    obj.data.polygons[4].material_index = 1
    obj.data.polygons[5].material_index = 1
    # red-green
    bpy.ops.object.select_all(action='DESELECT')
    obj = bpy.data.objects.get("1 -1 0")
    add_materials(obj, ["red", "green", "black"])
    obj.data.polygons[0].material_index = 2
    obj.data.polygons[1].material_index = 2
    obj.data.polygons[2].material_index = 1
    obj.data.polygons[3].material_index = 0
    obj.data.polygons[4].material_index = 2
    obj.data.polygons[5].material_index = 2
    # red-blue
    bpy.ops.object.select_all(action='DESELECT')
    obj = bpy.data.objects.get("-1 -1 0")
    add_materials(obj, ["red", "blue", "black"])
    obj.data.polygons[0].material_index = 1
    obj.data.polygons[1].material_index = 2
    obj.data.polygons[2].material_index = 2
    obj.data.polygons[3].material_index = 0
    obj.data.polygons[4].material_index = 2
    obj.data.polygons[5].material_index = 2
    # red-white
    bpy.ops.object.select_all(action='DESELECT')
    obj = bpy.data.objects.get("0 -1 -1")
    add_materials(obj, ["red", "white", "black"])
    obj.data.polygons[0].material_index = 2
    obj.data.polygons[1].material_index = 2
    obj.data.polygons[2].material_index = 2
    obj.data.polygons[3].material_index = 0
    obj.data.polygons[4].material_index = 1
    obj.data.polygons[5].material_index = 2
    # red-yellow-blue
    bpy.ops.object.select_all(action='DESELECT')
    obj = bpy.data.objects.get("-1 -1 1")
    add_materials(obj, ["red", "yellow", "blue", "black"])
    obj.data.polygons[0].material_index = 2
    obj.data.polygons[1].material_index = 3
    obj.data.polygons[2].material_index = 3
    obj.data.polygons[3].material_index = 0
    obj.data.polygons[4].material_index = 2
    obj.data.polygons[5].material_index = 1
    # red-blue-white
    bpy.ops.object.select_all(action='DESELECT')
    obj = bpy.data.objects.get("-1 -1 -1")
    add_materials(obj, ["red", "white", "blue", "black"])
    obj.data.polygons[0].material_index = 2
    obj.data.polygons[1].material_index = 3
    obj.data.polygons[2].material_index = 3
    obj.data.polygons[3].material_index = 0
    obj.data.polygons[4].material_index = 1
    obj.data.polygons[5].material_index = 3
    # red-green-white
    bpy.ops.object.select_all(action='DESELECT')
    obj = bpy.data.objects.get("1 -1 -1")
    add_materials(obj, ["red", "white", "green", "black"])
    obj.data.polygons[0].material_index = 3
    obj.data.polygons[1].material_index = 3
    obj.data.polygons[2].material_index = 2
    obj.data.polygons[3].material_index = 0
    obj.data.polygons[4].material_index = 1
    obj.data.polygons[5].material_index = 3
    # green
    bpy.ops.object.select_all(action='DESELECT')
    obj = bpy.data.objects.get("1 0 0")
    add_materials(obj, ["green", "black"])
    obj.data.polygons[0].material_index = 1
    obj.data.polygons[1].material_index = 1
    obj.data.polygons[2].material_index = 0
    obj.data.polygons[3].material_index = 1
    obj.data.polygons[4].material_index = 1
    obj.data.polygons[5].material_index = 1
    # green-white
    bpy.ops.object.select_all(action='DESELECT')
    obj = bpy.data.objects.get("1 0 -1")
    add_materials(obj, ["green", "white", "black"])
    obj.data.polygons[0].material_index = 2
    obj.data.polygons[1].material_index = 2
    obj.data.polygons[2].material_index = 0
    obj.data.polygons[3].material_index = 2
    obj.data.polygons[4].material_index = 1
    obj.data.polygons[5].material_index = 2
    # yellow-green
    bpy.ops.object.select_all(action='DESELECT')
    obj = bpy.data.objects.get("1 0 1")
    add_materials(obj, ["green", "yellow", "black"])
    obj.data.polygons[0].material_index = 2
    obj.data.polygons[1].material_index = 2
    obj.data.polygons[2].material_index = 0
    obj.data.polygons[3].material_index = 2
    obj.data.polygons[4].material_index = 2
    obj.data.polygons[5].material_index = 1
    # pure yellow
    bpy.ops.object.select_all(action='DESELECT')
    obj = bpy.data.objects.get("0 0 1")
    add_materials(obj, ["yellow", "black"])
    obj.data.polygons[0].material_index = 1
    obj.data.polygons[1].material_index = 1
    obj.data.polygons[2].material_index = 1
    obj.data.polygons[3].material_index = 1
    obj.data.polygons[4].material_index = 1
    obj.data.polygons[5].material_index = 0
    # green-yellow-orange
    bpy.ops.object.select_all(action='DESELECT')
    obj = bpy.data.objects.get("1 1 1")
    add_materials(obj, ["green", "yellow", "orange", "black"])
    obj.data.polygons[0].material_index = 3
    obj.data.polygons[1].material_index = 2
    obj.data.polygons[2].material_index = 0
    obj.data.polygons[3].material_index = 3
    obj.data.polygons[4].material_index = 3
    obj.data.polygons[5].material_index = 1
    # green-orange
    bpy.ops.object.select_all(action='DESELECT')
    obj = bpy.data.objects.get("1 1 0")
    add_materials(obj, ["green", "orange", "black"])
    obj.data.polygons[0].material_index = 2
    obj.data.polygons[1].material_index = 1
    obj.data.polygons[2].material_index = 0
    obj.data.polygons[3].material_index = 2
    obj.data.polygons[4].material_index = 2
    obj.data.polygons[5].material_index = 2
    # white-orange-green
    bpy.ops.object.select_all(action='DESELECT')
    obj = bpy.data.objects.get("1 1 -1")
    add_materials(obj, ["orange", "white", "green", "black"])
    obj.data.polygons[0].material_index = 3
    obj.data.polygons[1].material_index = 0
    obj.data.polygons[2].material_index = 2
    obj.data.polygons[3].material_index = 3
    obj.data.polygons[4].material_index = 1
    obj.data.polygons[5].material_index = 3
    # yellow-orange
    bpy.ops.object.select_all(action='DESELECT')
    obj = bpy.data.objects.get("0 1 1")
    add_materials(obj, ["orange", "yellow", "black"])
    obj.data.polygons[0].material_index = 2
    obj.data.polygons[1].material_index = 0
    obj.data.polygons[2].material_index = 2
    obj.data.polygons[3].material_index = 2
    obj.data.polygons[4].material_index = 2
    obj.data.polygons[5].material_index = 1
    # orange
    bpy.ops.object.select_all(action='DESELECT')
    obj = bpy.data.objects.get("0 1 0")
    add_materials(obj, ["orange", "black"])
    obj.data.polygons[0].material_index = 1
    obj.data.polygons[1].material_index = 0
    obj.data.polygons[2].material_index = 1
    obj.data.polygons[3].material_index = 1
    obj.data.polygons[4].material_index = 1
    obj.data.polygons[5].material_index = 1
    # orange-yellow-blue
    bpy.ops.object.select_all(action='DESELECT')
    obj = bpy.data.objects.get("-1 1 1")
    add_materials(obj, ["orange", "blue", "yellow", "black"])
    obj.data.polygons[0].material_index = 1
    obj.data.polygons[1].material_index = 0
    obj.data.polygons[2].material_index = 3
    obj.data.polygons[3].material_index = 3
    obj.data.polygons[4].material_index = 1
    obj.data.polygons[5].material_index = 2
    # yellow-blue
    bpy.ops.object.select_all(action='DESELECT')
    obj = bpy.data.objects.get("-1 0 1")
    add_materials(obj, ["blue", "yellow", "black"])
    obj.data.polygons[0].material_index = 0
    obj.data.polygons[1].material_index = 2
    obj.data.polygons[2].material_index = 2
    obj.data.polygons[3].material_index = 2
    obj.data.polygons[4].material_index = 2
    obj.data.polygons[5].material_index = 1
    # blue
    bpy.ops.object.select_all(action='DESELECT')
    obj = bpy.data.objects.get("-1 0 0")
    add_materials(obj, ["blue", "black"])
    obj.data.polygons[0].material_index = 0
    obj.data.polygons[1].material_index = 1
    obj.data.polygons[2].material_index = 1
    obj.data.polygons[3].material_index = 1
    obj.data.polygons[4].material_index = 1
    obj.data.polygons[5].material_index = 1
    # orange-blue
    bpy.ops.object.select_all(action='DESELECT')
    obj = bpy.data.objects.get("-1 1 0")
    add_materials(obj, ["blue", "orange", "black"])
    obj.data.polygons[0].material_index = 0
    obj.data.polygons[1].material_index = 1
    obj.data.polygons[2].material_index = 2
    obj.data.polygons[3].material_index = 2
    obj.data.polygons[4].material_index = 2
    obj.data.polygons[5].material_index = 2
    # white
    bpy.ops.object.select_all(action='DESELECT')
    obj = bpy.data.objects.get("0 0 -1")
    add_materials(obj, ["white", "black"])
    obj.data.polygons[0].material_index = 1
    obj.data.polygons[1].material_index = 1
    obj.data.polygons[2].material_index = 1
    obj.data.polygons[3].material_index = 1
    obj.data.polygons[4].material_index = 0
    obj.data.polygons[5].material_index = 1
    # white-blue
    bpy.ops.object.select_all(action='DESELECT')
    obj = bpy.data.objects.get("-1 0 -1")
    add_materials(obj, ["blue", "white", "black"])
    obj.data.polygons[0].material_index = 0
    obj.data.polygons[1].material_index = 2
    obj.data.polygons[2].material_index = 2
    obj.data.polygons[3].material_index = 2
    obj.data.polygons[4].material_index = 1
    obj.data.polygons[5].material_index = 2
    # orange-blue-white
    bpy.ops.object.select_all(action='DESELECT')
    obj = bpy.data.objects.get("-1 1 -1")
    add_materials(obj, ["orange", "white", "blue", "black"])
    obj.data.polygons[0].material_index = 2
    obj.data.polygons[1].material_index = 0
    obj.data.polygons[2].material_index = 3
    obj.data.polygons[3].material_index = 3
    obj.data.polygons[4].material_index = 1
    obj.data.polygons[5].material_index = 3
    # orange-white
    bpy.ops.object.select_all(action='DESELECT')
    obj = bpy.data.objects.get("0 1 -1")
    add_materials(obj, ["orange", "white", "black"])
    obj.data.polygons[0].material_index = 2
    obj.data.polygons[1].material_index = 0
    obj.data.polygons[2].material_index = 2
    obj.data.polygons[3].material_index = 2
    obj.data.polygons[4].material_index = 1
    obj.data.polygons[5].material_index = 2


def get_bounding_box_location(obj):
    bbox_corners = [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]
    geometry_center = sum(bbox_corners, Vector()) / len(bbox_corners)
    return geometry_center

def get_face(collection, axis, value):
    epsilon = 0.1
    cubes = []
    for obj in collection.objects:
        abs_loc = get_bounding_box_location(obj)[axis]
        if abs(abs_loc - value) < epsilon:
            cubes.append(obj)
    return cubes

def select_all(object_list):
    # Deselect all objects first
    bpy.ops.object.select_all(action='DESELECT')
    # Select each object in the list
    for obj in object_list:
        obj.select_set(True)


def rotate_selected (axis, angle):
    angle_in_radians = math.radians(angle)
    bpy.ops.transform.rotate(value=angle_in_radians, orient_axis=axis.upper())


def rotate(collection, rotation):
    bpy.ops.object.select_all(action='DESELECT')
    #'F', 'R', 'U', 'B', 'L', 'D', "F'", "R'", "B'", "L'", "D'"
    axis_dict = {'F':'y', "F'": 'y', 'B': 'y', "B'": 'y', 'L': 'x', "L'":'x', "R": 'x', "R'": "x",
                 "U": "z", "U'": "z", "D": 'z', "D'": "z"}
    angle_dict = {'F': -90, 'R': 90, 'U': 90, 'B': 90, 'L': -90, 'D': -90,
                  "F'": 90, "R'": -90, "U'": -90, "B'": -90, "L'": 90, "D'": 90}
    axis_to_num = {"x": 0, "y": 1, "z": 2}
    values_dict = {'F':-2, "F'": -2, 'B': 2, "B'": 2, 'L': -2, "L'":-2, "R": 2, "R'": 2,
                 "U": 2, "U'": 2, "D": -2, "D'": -2}
    value = values_dict[rotation]
    axis = axis_dict[rotation] #X
    angle = angle_dict[rotation] #90
    axis_num = axis_to_num[axis]
    cubes = get_face(collection, axis_num, value)
    select_all(cubes)
    rotate_selected(axis, angle)
    selected_objects = [obj for obj in bpy.context.selected_objects]
    return selected_objects
    #bpy.ops.object.transform_apply(rotation=True, scale=False, location=False)

def adapt_for_kociemba(color_string):
    color_string2 = color_string.replace("r", "F").replace("w", "D").replace("y", "U").replace("b", "L").replace("g", "R").replace("o", "B")
    return color_string2

def get_highest_face(obj):
    mesh = obj.data
    highest_z = -10
    highest_face = None
    for face in mesh.polygons:
        # Get the world coordinates of the vertices in the face
        world_coords = [obj.matrix_world @ mesh.vertices[i].co for i in face.vertices]
        # Find the maximum Z coordinate for this face
        max_z = sum(v[2] for v in world_coords)/len(world_coords)

        # If this Z is higher than the current highest, update the highest face
        if max_z > highest_z:
            highest_z = max_z
            highest_face = face
    return highest_face

def get_bottom_face(obj):
    mesh = obj.data
    lowest_z = 10
    highest_face = None
    for face in mesh.polygons:
        # Get the world coordinates of the vertices in the face
        world_coords = [obj.matrix_world @ mesh.vertices[i].co for i in face.vertices]
        # Find the maximum Z coordinate for this face
        min_z = sum(v[2] for v in world_coords)/len(world_coords)

        # If this Z is higher than the current highest, update the highest face
        if min_z < lowest_z:
            lowest_z = min_z
            highest_face = face
    return highest_face

def get_front_face(obj):
    mesh = obj.data
    smallest_y = 10
    front_face = None
    for face in mesh.polygons:
        # Get the world coordinates of the vertices in the face
        world_coords = [obj.matrix_world @ mesh.vertices[i].co for i in face.vertices]

        # Find the maximum Z coordinate for this face
        min_y = sum(v[1] for v in world_coords)/len(world_coords)

        # If this Z is higher than the current highest, update the highest face
        if min_y < smallest_y:
            smallest_y = min_y
            front_face = face
    return front_face


def get_back_face(obj):
    mesh = obj.data
    biggest_y = -10
    back_face = None
    for face in mesh.polygons:
        # Get the world coordinates of the vertices in the face
        world_coords = [obj.matrix_world @ mesh.vertices[i].co for i in face.vertices]

        # Find the maximum Z coordinate for this face
        max_y = sum(v[1] for v in world_coords)/len(world_coords)

        # If this Z is higher than the current highest, update the highest face
        if max_y > biggest_y:
            biggest_y = max_y
            back_face = face
    return back_face

def get_right_face(obj):
    mesh = obj.data
    biggest_x = -10
    front_face = None
    for face in mesh.polygons:
        # Get the world coordinates of the vertices in the face
        world_coords = [obj.matrix_world @ mesh.vertices[i].co for i in face.vertices]

        # Find the maximum Z coordinate for this face
        max_x = sum(v[0] for v in world_coords)/len(world_coords)

        # If this Z is higher than the current highest, update the highest face
        if max_x > biggest_x:
            biggest_x = max_x
            front_face = face
    return front_face


def get_left_face(obj):
    mesh = obj.data
    smallest_x = 10
    front_face = None
    for face in mesh.polygons:
        # Get the world coordinates of the vertices in the face
        world_coords = [obj.matrix_world @ mesh.vertices[i].co for i in face.vertices]

        # Find the maximum Z coordinate for this face
        min_x = sum(v[0] for v in world_coords)/len(world_coords)

        # If this Z is higher than the current highest, update the highest face
        if min_x < smallest_x:
            smallest_x = min_x
            front_face = face
    return front_face

def get_color_string(collection):
    faces = ""
    upper_face = ""
    lower_face = ""
    left_face = ""
    right_face = ""
    front_face = ""
    back_face = ""
    #get the top face
    top_cubes = get_face(collection, 2, 2)
    # Sort cubes by y-coordinate first (row by row)
    #top_cubes.sort(key=lambda o: -o.location.y)
    #top_cubes.sort(key=lambda o: o.location.x)
    top_cubes_sorted = sorted(top_cubes, key=lambda obj: (-round(obj.location.y, 2), round(obj.location.x, 2)))
    for cube in top_cubes_sorted:
        top_face = get_highest_face(cube)
        face_color_idx = top_face.material_index
        material_name = cube.material_slots[face_color_idx].material.name
        upper_face += material_name[0]
    #print("top:",upper_face)

    #get the bottom face
    bottom_cubes = get_face(collection, 2, -2)
    right_cubes_sorted = sorted(bottom_cubes, key=lambda obj: (round(obj.location.y, 2), round(obj.location.x, 2)))
    for cube in right_cubes_sorted:
        bottom_polygon = get_bottom_face(cube)
        face_color_idx = bottom_polygon.material_index
        material_name = cube.material_slots[face_color_idx].material.name
        lower_face += material_name[0]
    #print("bottom:", lower_face)

    #get the left face
    left_cubes = get_face(collection, 0, -2)
    left_cubes_sorted = sorted(left_cubes, key=lambda obj: (-round(obj.location.z, 2), -round(obj.location.y, 2)))
    for cube in left_cubes_sorted:
        left_polygon = get_left_face(cube)
        face_color_idx = left_polygon.material_index
        material_name = cube.material_slots[face_color_idx].material.name
        left_face += material_name[0]
    #print("left:", left_face)

    #get the right face
    right_cubes = get_face(collection, 0, 2)
    right_cubes_sorted = sorted(right_cubes, key=lambda obj: (-round(obj.location.z, 2), round(obj.location.y, 2)))
    for cube in right_cubes_sorted:
        right_polygon = get_right_face(cube)
        face_color_idx = right_polygon.material_index
        material_name = cube.material_slots[face_color_idx].material.name
        right_face += material_name[0]
    #print("right:", right_face)

    #get the front face
    front_cubes = get_face(collection, 1, -2)
    front_cubes_sorted = sorted(front_cubes, key=lambda obj: (-round(obj.location.z, 2), round(obj.location.x, 2)))
    for cube in front_cubes_sorted:
        front_polygon = get_front_face(cube)
        face_color_idx = front_polygon.material_index
        material_name = cube.material_slots[face_color_idx].material.name
        front_face += material_name[0]
    #print("front:", front_face)

    #get the back face
    back_cubes = get_face(collection, 1, 2)
    back_cubes_sorted = sorted(back_cubes, key=lambda obj: (-round(obj.location.z, 2), -round(obj.location.x, 2)))
    for cube in back_cubes_sorted:
        back_polygon = get_back_face(cube)
        face_color_idx = back_polygon.material_index
        material_name = cube.material_slots[face_color_idx].material.name
        back_face += material_name[0]
    #print("back:", back_face)
    #concatenate
    faces = upper_face + right_face + front_face + lower_face + left_face + back_face
    return faces


# MAIN PROGRAM

# setup scene
setup_scene()

# setup collection for cube
collection = bpy.data.collections.new("cube")
bpy.context.scene.collection.children.link(collection)

# create_cubes
create_cubes(collection)


# make cubes slightly smaller
def resize_cube(cube):
    cube.scale *= 0.99

apply_all(resize_cube, collection)


# create colors
color_tuple = ("w", "g", "o", "y", "b", "r")
color_set = ["w"] * 9 + ["g"] * 9 + ["o"] * 9 + ["y"] * 9 + ["b"] * 9 + ["r"] * 9
create_color("white", (1, 1, 1, 1))
create_color("green", (0, 1, 0, 1))
create_color("orange", (1, 0.27, 0, 1))
create_color("yellow", (1, 1, 0, 1))
create_color("blue", (0, 0, 1, 1))
create_color("red", (1, 0, 0, 1))
create_color("black", (0, 0, 0, 1))

# create the correct cube
default_colors()

# rotate it randomly for N times
rotations = ('F', 'R', 'U', 'B', 'L', 'D', "F'", "R'", "B'", "L'", "D'")
N_ROTATIONS = 300

for i in range(0, N_ROTATIONS):
    rotation = random.sample(rotations, 1)[0]
    rotate(collection, rotation)

# create color string for animation
color_string = get_color_string(collection)
color_string = adapt_for_kociemba(color_string)
solution = kociemba.solve(color_string.upper())
solution_moves = solution.split()
print(color_string)
print("solution", solution)


#bevel all cubes
bpy.ops.object.select_all(action='DESELECT')
# Loop through all objects in the collection and select them
for obj in collection.objects:
    obj.select_set(True)  # Select the object

bpy.ops.object.mode_set(mode='EDIT')  # Switch to edit mode
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.mesh.bevel(offset=0.148376, offset_pct=0, segments=2, affect='EDGES')
bpy.ops.object.mode_set(mode='OBJECT')
bpy.ops.object.shade_smooth()
bpy.ops.object.select_all(action='DESELECT')


#set origin to cursor
for obj in collection.objects:
    obj.select_set(True)
    obj.rotation_mode = "QUATERNION"
bpy.ops.object.origin_set(type='ORIGIN_CURSOR')

#animate
bpy.context.preferences.edit.keyframe_new_interpolation_type = 'LINEAR'
frame_start = 1
frame_duration = 10  # Number of frames for each move
current_frame = 10
idx = 0

for obj in collection.objects:
    obj.keyframe_insert(data_path="rotation_quaternion", frame=current_frame)

for move in solution_moves:
    selected = []
    if "2" in move:
        for i in range(0, 2):
            idx += 1
            current_frame = current_frame + frame_duration
            short_move = move.replace("2", "")
            selected = rotate(collection, short_move)
            for obj in collection.objects:
                obj.keyframe_insert(data_path="rotation_quaternion", frame=current_frame)
                #obj.keyframe_insert(data_path="location", frame=current_frame)
            #idx += 1
            #pause
        current_frame += 5
        for obj in collection.objects:
            obj.keyframe_insert(data_path="rotation_quaternion", frame=current_frame)

    else:
        idx += 1
        current_frame = current_frame + frame_duration
        selected = rotate(collection, move)
        for obj in collection.objects: #selected
            obj.keyframe_insert(data_path="rotation_quaternion", frame=current_frame)
        #pause
        current_frame += 5
        for obj in collection.objects:
            obj.keyframe_insert(data_path="rotation_quaternion", frame=current_frame)
            # obj.keyframe_insert(data_path="location", frame=current_frame)
        # idx += 1

bpy.context.scene.frame_end = current_frame + 30

#add a camera
bpy.ops.object.camera_add(enter_editmode=False, align='VIEW',
                          location=(-7.72653e-08, 1.32455e-08, -7.17463e-09),
                          rotation=(1.20777, -2.8053e-06, 0.637628), scale=(1, 1, 1))
camera = bpy.data.objects.get("Camera")
camera.rotation_euler = (math.radians(69.2), math.radians(-0.000162), math.radians(36.5334))
camera.location = (15.7829, -21.1545, 10.2568)
