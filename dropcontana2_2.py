import bpy
import csv, os, bmesh, math
import mathutils
from scipy.io import loadmat
import numpy as np

filnamload = r'C:\Users\gaura\OneDrive\Documents\Blends\ABinWATER_50'

path, dirs, files = next(os.walk(filnamload))

for j in range(900, 2820, 5):
    vertsd = []
    edgesd = []
    facesd = []

    vertsw = []
    edgesw = []
    facesw = []

    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)

    light_data = bpy.data.lights.new(name="light_2.80", type='SUN')
    light_data.energy=2

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
    light_object.location = mathutils.Vector((0.0, -10.0, 0))
    light_object.rotation_euler = mathutils.Euler((0.0, 0.0, 0.0))
    # update scene if needed
    # dg = bpy.context.evaluated_depsgraph_get()
    # dg.update()


    # create camera
    cam_data = bpy.data.cameras.new('camera')
    cam=bpy.data.objects.new('camera', cam_data)
    bpy.context.collection.objects.link(cam)
    bpy.context.scene.camera = cam
    cam.data.lens=40
    cam.location = mathutils.Vector((0, -7.0, 0))
    cam.rotation_euler = mathutils.Euler((1.57, 1.57, 0.0))

    # bpy.ops.mesh.primitive_plane_add(size=200, enter_editmode=False, align='WORLD', location=(0, 0, -2))

    datafile = filnamload+'\data ('+str(j)+').mat'

    data = loadmat(datafile, squeeze_me=True)
    Nd = data['Nd']
    Nw = data['Nw']

    xd = data['xd']
    yd = data['rd']
    xw = data['xw']
    yw = data['rw']

    xd = np.append(xd, xd)# data['xd']+data['xd']
    yd = np.append(yd, -1*yd)# data['rd']+(-1)*data['rd']
    # xw = np.append(xw, xw)# data['xw']+data['xw']
    # yw = np.append(yw, -1*yw)# data['rw']+(-1)*data['rw']

    zd = np.zeros((2*Nd+2))
    zw = np.zeros((Nw+1))

    vertd = np.transpose([xd, yd, zd])
    vertw = np.transpose([xw, yw, zw])

    for i in range(0, 2*Nd+2):
        vertsd.append((float(vertd[i, 0]), float(vertd[i,1]), float(vertd[i, 2])))
        
    for i in range(0, Nw+1):
        vertsw.append((float(vertw[i, 0]), float(vertw[i,1]), float(vertw[i, 2])))
            
    obj = bpy.context.object

    mesh = bpy.data.meshes.new("wave")
    object = bpy.data.objects.new("wave",mesh)

    if vertsd:
            # join vertices into one uninterrupted chain of edges.
        edgesd = [[i, i+1] for i in range(len(vertsd)-1)]

    if vertsw:
            # join vertices into one uninterrupted chain of edges.
        edgesw = [[i, i+1] for i in range(len(vertsw)-1)]
        
        
     
    if vertsd:
        # curve coordinates require a 4th 'W'(weight) component,
        # the +[0.0] adds that for us
        out1 = []
        [out1.extend(list(i)+[0.0]) for i in vertsd] 

        # has one coordinate by default, we add one fewer than we need
        num_points_to_add1 = len(vertsd) - 1
        curve = bpy.data.curves.new("path_name1", type='CURVE')
        polyline = curve.splines.new(type='POLY')
        polyline.points.add(num_points_to_add1)
        polyline.points.foreach_set('co', out1)
        
        obj = bpy.data.objects.new("drop", curve)
        scene = bpy.context.collection
        scene.objects.link(obj)
        screw = obj.modifiers.new("Screw", 'SCREW')
        screw.axis ='X'
        


        
    obd = bpy.data.objects['drop']
    matd=bpy.data.materials.new(name="dropmaterial")
    obd.data.materials.append(matd)
    matd.diffuse_color = (0.0, 1.0, 0.0, 0.8)
    matd.metallic=1
        
    if vertsw:
        # curve coordinates require a 4th 'W'(weight) component,
        # the +[0.0] adds that for us
        out2 = []
        [out2.extend(list(i)+[0.0]) for i in vertsw] 

        # has one coordinate by default, we add one fewer than we need
        num_points_to_add2 = len(vertsw) - 1
        curve = bpy.data.curves.new("path_name2", type='CURVE')
        polyline = curve.splines.new(type='POLY')
        polyline.points.add(num_points_to_add2)
        polyline.points.foreach_set('co', out2)
        
        obj = bpy.data.objects.new("cont", curve)
        scene = bpy.context.collection
        scene.objects.link(obj)
        screw = obj.modifiers.new("Screw", 'SCREW')
        screw.axis ='Y'

    obw = bpy.data.objects['cont']
    matw=bpy.data.materials.new(name="contmaterial")
    obw.data.materials.append(matw)
    matw.diffuse_color = (0.5, 1.0, 1.0, 0.001)
    matw.metallic=0
    # matw.use_transparency = True #  renders trans
    obw.show_transparent = True





    bpy.context.scene.render.image_settings.file_format='PNG'
    bpy.context.scene.render.filepath=filnamload+'\datat ('+str(j)+').png'
    bpy.context.scene.render.resolution_x = 2480
    bpy.context.scene.render.resolution_y= 1920
    bpy.context.scene.render.image_settings.color_mode = 'RGBA'
    bpy.context.scene.render.film_transparent = True
    bpy.ops.render.render(use_viewport=True, write_still=True)