import bpy
import bmesh
import math

#delete all existing meshes
# select objects by type
for o in bpy.data.objects:
    if o.type == 'MESH':
        o.select = True
    else:
        o.select = False

# call the operator once
bpy.ops.object.delete()

#create a list of vertices
verts = \
    [
        (0, -1 / math.sqrt(3),0),
        (0.5, 1 / (2 * math.sqrt(3)), 0),
        (-0.5, 1 / (2 * math.sqrt(3)), 0),
        (0, 0, math.sqrt(2 / 3)),
    ]  # 2 verts made with XYZ coords

#create list of faces
faces = [[0, 1, 2], [0, 1, 3], [1, 2, 3], [2, 0, 3]]

mesh = bpy.data.meshes.new("mesh")  # add a new mesh
obj = bpy.data.objects.new("MyObject", mesh)  # add a new object using the mesh

scene = bpy.context.scene
scene.objects.link(obj)  # put the object into the scene (link)
scene.objects.active = obj  # set as the active object in the scene
obj.select = True  # select object

#make new mesh
mesh = bpy.context.object.data
bm = bmesh.new()

#add vertices and faces
for v in verts:
    bm.verts.new(v)  # add a new vert
    
bm.verts.ensure_lookup_table()

for f in faces:
    newface = set(bm.verts[i] for i in f)
    bm.faces.new(newface)

# make the bmesh the object's mesh
bm.to_mesh(mesh)  
bm.free()  # always do this when finished