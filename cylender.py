import bpy
import bmesh
import math
from math import pi, sin, cos
from numpy import linspace

pointsInSlice = 30 #number of vertices in a given slice
modelHeight = 1 #space between slices
numSlices = 2 #total height of object in slices

def deletMeshes():
  #delete all existing meshes
  # select objects by type
  for o in bpy.data.objects:
      if o.type == 'MESH':
          o.select = True
      else:
          o.select = False

  # call the operator once
  bpy.ops.object.delete()

def createVerts():
  #create a list of vertices
  verts = []
  currentSlice = 0

  #create a circle
  for z in linspace(0,modelHeight, numSlices):
    for theta in linspace(0,2*pi,pointsInSlice):
      verts.append([sin(theta),cos(theta),z])


  return verts

def createFaces():
  #create list of faces
  faces = [];

  #the cylender defines a 2 dimensional manifold linked on 2 edges
  #the heights are zero indexed (hence numSlices - 1)
  #the faces are added "above" the current slice, as well as "bellow" the next slice
  #hence (numSlices -1) - 1
  for h in linspace(0,numSlices-2,numSlices-1): #iterate over height slices.
    for r in range(0,pointsInSlice-1): #iterate over each point in slice
      if(r == pointsInSlice-1):
        #handle linking ends of manifold together
        faces.append([r,r+pointsInSlice,pointsInSlice*h])
        faces.append([r+pointsInSlice,pointsInSlice*h,pointsInSlice*(h+1)])
      else:
        #handle rest of manifold
        faces.append([r,r+pointsInSlice,r+1])
        faces.append([r+pointsInSlice,r+1,r+1+pointsInSlice])

  return faces

def createMesh(verts,faces):
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

deletMeshes()
verts = createVerts()
faces = createFaces()
print(faces)
createMesh(verts,faces)