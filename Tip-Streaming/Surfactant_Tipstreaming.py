import bpy
import csv, os, bmesh, math
import mathutils
from scipy.io import loadmat
import numpy as np

#filename = 'pythontrial.txt'
filnamload = r'C:\Users\gaura\OneDrive\Documents\Blends_New\blendcodes\HighViscTipStr_Ca0.17_lmb0.1_N32_dt0.001_exten12_E0.2_invtau0.3_K0_bgamma10000'

path, dirs, files = next(os.walk(filnamload))
verts = []
edges = []
faces = []
for j in range(0,len(files)-2 ,5):
    #filepaths
    filepath = bpy.data.filepath
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    # create ligth datablock, set attributes
    light_data = bpy.data.lights.new(name="light_2.80", type='SUN')
    light_data.energy=100

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
    light_object.rotation_euler = mathutils.Euler((45*(np.pi / 180.0), 0.0, 0.0))
    
    # create camera
    cam_data = bpy.data.cameras.new('camera')
    cam=bpy.data.objects.new('camera', cam_data)
    bpy.context.collection.objects.link(cam)
    bpy.context.scene.camera = cam
    cam.data.lens=6
    cam.location = mathutils.Vector((-5, 5, 3))
    cam.rotation_euler = mathutils.Euler((90*(np.pi / 180.0), 0.0, 0.0))
    
    # bpy.ops.mesh.primitive_plane_add(size=200, enter_editmode=False, align='WORLD', location=(0, 0, -2))
    
    datafile = filnamload+'\data ('+str(j)+').mat'

    data = loadmat(datafile, squeeze_me=True)
    N = len(data['x'])-1
    
    x = data['x']
    y = data['r']
    z = np.zeros((N+1))
    t = np.zeros((N+1))
    tau = data['tau'].reshape(1, N+1)
    tt = (tau-np.min(tau[0,:]))/(np.max(tau[0,:])-np.min(tau[0,:]))
    vert = np.transpose([x, y, z])

    verti = np.transpose([x, y, z, t])
    
    for i in range(0, N+1):
        verts.append((float(vert[i, 0]), float(vert[i,1]), float(vert[i, 2])))
    name = 'drop'    

    obj = bpy.context.object

    #create mesh and object
    mesh = bpy.data.meshes.new("wave")
    object = bpy.data.objects.new("wave",mesh)

    if verts:
        # join vertices into one uninterrupted chain of edges.
        edges = [[i, i+1] for i in range(len(verts)-1)]

    for k in range(len(verts)-3):
        out1 = []
        out1 = [*verti[k], *verti[k+1], *verti[k+2]]
        # has one coordinate by default, we add one fewer than we need
        num_points_to_add = 2# len(verts) - 1
        curve = bpy.data.curves.new("path_name", type='CURVE')
        polyline = curve.splines.new(type='POLY')
        polyline.points.add(num_points_to_add)
        polyline.points.foreach_set('co', out1)
        
        obj = bpy.data.objects.new("obj_name", curve)
        # generate a random color
        red = tt[k] # creates a value from 0.0 to 1.0
        green = 0#random.random()
        blue = 1-tt[k]#random.random()
        
        color = (red, green, blue, 1.0)
        #print(i)
        # print(color)
        
        material = bpy.data.materials.new(name+"_material")
        material.diffuse_color=color
        curve.materials.append(material)
        curve.bevel_depth =0.2
        
        scene = bpy.context.collection
        scene.objects.link(obj)
        screw = obj.modifiers.new("Screw", 'SCREW')
        screw.axis ='X'

    bpy.context.scene.render.image_settings.file_format='PNG'
    bpy.context.scene.render.filepath=filnamload+'\figure ('+str(j)+').png'
    bpy.context.scene.render.resolution_x = 2480
    bpy.context.scene.render.resolution_y= 1920
    bpy.ops.render.render(use_viewport=True, write_still=True)
    