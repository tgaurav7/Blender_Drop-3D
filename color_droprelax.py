#import csv
#import os
#import bpy


#filename = 'pythontrial.txt'
#directory = r'C:\Users\gaura\OneDrive\Documents\Blends'  # <-- if you have linux or osx
## directory = r'c:\some\directory'  # <-- if windows, the r is important
## directory = 'c:/some/directory'  # <-- if windows (alternative)

#fullpath = os.path.join(directory, filename)

#with open(fullpath, 'r', newline='') as csvfile:
#    ofile = csv.reader(csvfile, delimiter=',')
#    # next(ofile) # <-- skip the x,y,z header

#    # this makes a generator of the remaining non-empty lines
#    rows = (r for r in ofile if r)

#    # this converts the string representation of each line
#    # to an x,y,z list, and stores it in the verts list.
#    verts = [[float(i) for i in r] for r in rows]

#if verts:
#    # curve coordinates require a 4th 'W'(weight) component,
#    # the +[0.0] adds that for us
#    out2 = []
#    [out2.extend(list(i)+[0.0]) for i in verts] 

#    # has one coordinate by default, we add one fewer than we need
#    num_points_to_add = len(verts) - 1
#    curve = bpy.data.curves.new("path_name", type='CURVE')
#    polyline = curve.splines.new(type='POLY')
#    polyline.points.add(num_points_to_add)
#    polyline.points.foreach_set('co', out2)

#    obj = bpy.data.objects.new("obj_name", curve)
#    scene = bpy.context.scene
#    scene.objects.link(obj)


#with open(fullpath, 'r', newline='') as csvfile:
#    ofile = csv.reader(csvfile, delimiter=',')
#    next(ofile) # <-- skip the x,y,z header

#    # this makes a generator of the remaining non-empty lines
#    rows = (r for r in ofile if r)

#    # this converts the string representation of each line
#    # to an x,y,z list, and stores it in the verts list.
#    verts = [[float(i) for i in r] for r in rows]

#if verts:
#    # join vertices into one uninterrupted chain of edges.
#    edges = [[i, i+1] for i in range(len(verts)-1)]

#    mesh = bpy.data.meshes.new("mesh_name")
#    mesh.from_pydata(verts, edges, faces=[])
#    mesh.update()

#    obj = bpy.data.objects.new("obj_name", mesh)

#    scene = bpy.context.scene
#    scene.objects.link(obj)

import bpy
import csv, os, bmesh, math
import mathutils
from scipy.io import loadmat
import numpy as np
#filepaths
# filepath = bpy.data.filepath
#directory = os.path.dirname(filepath)


#filename = 'pythontrial.txt'
filnamload = r'C:\Users\gaura\OneDrive\Documents\Blends\Stretch_2_Ca0.3827_lmb0.056_N32_dt0.001_exten6.93'

path, dirs, files = next(os.walk(filnamload))
  
# create the light
# light_data = bpy.data.lamps.new('light', type='POINT')
# light=bpy.data.objects.new('light', light_data)
# scene.objects.link(light)
# light.location=mathutils.Vector((3, -4.2, 5))  

# create ligth datablock, set attributes
#light_data = bpy.data.lights.new(name="light_2.80", type='SPOT')
#light_data.energy=5000

## create new object with our light datablock
#light_object = bpy.data.objects.new(name="light_2.80", object_data=light_data)
## set color
#light_object.data.color = (0.05, 1.0, 0.0)
#light_object.data.use_shadow = False

## link light object
#bpy.context.collection.objects.link(light_object)
## make it active
#bpy.context.view_layer.objects.active = light_object

## change location
## light_object.location = (5, 5, 5)
#light_object.location = mathutils.Vector((0, -10, 15))
#light_object.rotation_euler = mathutils.Euler((0.5, 0.0, 0.0))
## update scene if needed
## dg = bpy.context.evaluated_depsgraph_get()
## dg.update()


## create camera
#cam_data = bpy.data.cameras.new('camera')
#cam=bpy.data.objects.new('camera', cam_data)
#bpy.context.collection.objects.link(cam)
#bpy.context.scene.camera = cam
#cam.data.lens=6
#cam.location = mathutils.Vector((-0.25, 5, 3.5))
#cam.rotation_euler = mathutils.Euler((-0.95, 0.0, 0.0))


for j in range(4678,4678 ,5):# len(files)-2):
    verts = []
    edges = []
    faces = []
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
      
    # create the light
    # light_data = bpy.data.lamps.new('light', type='POINT')
    # light=bpy.data.objects.new('light', light_data)
    # scene.objects.link(light)
    # light.location=mathutils.Vector((3, -4.2, 5))  

    # create ligth datablock, set attributes
    light_data = bpy.data.lights.new(name="light_2.80", type='SUN')
    light_data.energy=5

    # create new object with our light datablock
    light_object = bpy.data.objects.new(name="light_2.80", object_data=light_data)
    # set color
    light_object.data.color = (1.0, 1.0, 1.0)
    light_object.data.use_shadow = False

    # link light object
    bpy.context.collection.objects.link(light_object)
    # make it active
    bpy.context.view_layer.objects.active = light_object

    # change location
    # light_object.location = (5, 5, 5)
    light_object.location = mathutils.Vector((0, 20, 10))
    light_object.rotation_euler = mathutils.Euler((0, 0.0, 0.0))
    # update scene if needed
    # dg = bpy.context.evaluated_depsgraph_get()
    # dg.update()


    # create camera
    cam_data = bpy.data.cameras.new('camera')
    cam=bpy.data.objects.new('camera', cam_data)
    bpy.context.collection.objects.link(cam)
    bpy.context.scene.camera = cam
    cam.data.lens=6
    cam.location = mathutils.Vector((-0.25, 7, 5))
    cam.rotation_euler = mathutils.Euler((-0.95, 0.0, 0.0))
    
    # bpy.ops.mesh.primitive_plane_add(size=200, enter_editmode=False, align='WORLD', location=(0, 0, -2))
    
    datafile = filnamload+'\data ('+str(j)+').mat'

    data = loadmat(datafile, squeeze_me=True)
    N = len(data['x'])-1

    #pointsReader = csv.reader(open(csvpoints, newline=''), delimiter=',')   

    #with open(csvpoints, 'rt', encoding="utf8") as csvfile:
    #    pointsReader = csv.reader(csvfile, delimiter=',', quotechar='|')
    #    for idx, row in enumerate(pointsReader):
    #        if (idx > 0):
    #            vert = (float(row[0]), float(row[1]), float(row[2])) 
    #            verts.append(vert)
    x = data['x']
    y = data['r']
    z = np.zeros((N+1))
    vert = np.transpose([x, y, z])


    for i in range(0, N+1):
        verts.append((float(vert[i, 0]), float(vert[i,1]), float(vert[i, 2])))
        

    obj = bpy.context.object

    #create mesh and object
    mesh = bpy.data.meshes.new("wave")
    object = bpy.data.objects.new("wave",mesh)

    if verts:
        # join vertices into one uninterrupted chain of edges.
        edges = [[i, i+1] for i in range(len(verts)-1)]

    #create mesh from python data
    #mesh.from_pydata(verts,edges,[])
    #mesh.update(calc_edges=True)

    if verts:
        # curve coordinates require a 4th 'W'(weight) component,
        # the +[0.0] adds that for us
        out2 = []
        [out2.extend(list(i)+[0.0]) for i in verts] 

        # has one coordinate by default, we add one fewer than we need
        num_points_to_add = len(verts) - 1
        curve = bpy.data.curves.new("path_name", type='CURVE')
        polyline = curve.splines.new(type='POLY')
        polyline.points.add(num_points_to_add)
        polyline.points.foreach_set('co', out2)
        mesh_obj = bpy.ops.object.convert(target='MESH')
        obj = bpy.data.objects.new("obj_name", curve)
        scene = bpy.context.collection
        scene.objects.link(obj)
        screw = obj.modifiers.new("Screw", 'SCREW')
        screw.axis ='X'
        

    # bpy.context.space_data.context = 'MATERIAL'
#    mat=bpy.ops.material.new(name="MaterialName")
#    bpy.context.object.active_material
#    mat.use_nodes=False
#    # bpy.context.object.active_material.type='DD'
#    # mat.node_tree.nodes["Glossy BSDF"].inputs[0].default_value = (0, 0, 0, 1)
#    mat.diffuse_color = (0, 0, 1)
#    mat.matallic=1
#    obj.active_material =  mat   
    # ob = bpy.context.scene.objects["obj_name"]
    ob = bpy.data.objects['obj_name']
    # activeObject = bpy.context.active_object
    
    mat=bpy.data.materials.new(name="MaterialName")
    
    # bpy.context.object.active_material.diffuse_color=(1, 0, 0, 1)
    
    ob.data.materials.append(mat)
    mat.diffuse_color = (0.0, 0.5, 1.0, 1)
    mat.metallic=1
    
    bpy.context.scene.render.image_settings.file_format='PNG'
    bpy.context.scene.render.filepath=filnamload+'\data ('+str(j)+').png'
    bpy.context.scene.render.resolution_x = 2480
    bpy.context.scene.render.resolution_y= 1920
    bpy.ops.render.render(use_viewport=True, write_still=True)

    # Delete the object
    # bpy.data.objects.remove( obj )

  
    ##set mesh location
    #object.location = bpy.context.scene.cursor.location
    #bpy.context.collection.objects.link(object)

#    r,g, b = (0.5, 1, 1)
#    
#    # iterating over the selected objets
#    for o in bpy.context.selected_objects:
#        o.active_material.diffuse_color=(r, g, b)