import bpy
from math import radians

def update_legend( scene ):
    C = bpy.context

    ## Get global height coordinates of terrain vertices
    obj = bpy.data.objects['Plane'] # Reference terrain object
    m = obj.to_mesh( C.scene, True, 'RENDER' )

    offset  = 0.5 # The value placed in the math.add node
    heights = [ v.co.z + offset for v in m.vertices ]

    minZ = min( heights )
    maxZ = max( heights )

    ## Generate legend color bar

    legendPlane = None
    if 'legend' in bpy.data.objects:
        legendPlane = bpy.data.objects[ 'legend' ]
    else:
        # Add legened plane on layer 2
        bpy.ops.mesh.primitive_plane_add( layers = [ i == 1 for i in range(20) ] )

        legendPlane = bpy.data.objects[ C.object.name ]
        legendPlane.name = 'legend'
        legendPlane.dimensions.y = 20

        bpy.ops.object.transform_apply( scale = True ) # Apply scale (dim change)

        # Setup legend material
        cr = obj.active_material.node_tree.nodes['ColorRamp']

        legendMat = None
        if "legend" not in bpy.data.materials:
            legendMat = bpy.data.materials.new("legend")

            legendMat.use_nodes = True
            t = legendMat.node_tree

            t.nodes.remove( t.nodes['Diffuse BSDF'] )

            emit = t.nodes.new( 'ShaderNodeEmission' )
            mo   = t.nodes['Material Output']

            # Link Emission to Material Output
            t.links.new( emit.outputs['Emission'], mo.inputs['Surface'] )

            # Generate new color ramp and link to Emission node
            colorRamp = t.nodes.new( 'ShaderNodeValToRGB' )
            t.links.new( emit.inputs['Color'], colorRamp.outputs['Color'] )

            # Add another color swatch in the middle of the ramp
            colorRamp.color_ramp.elements.new( 0.5 )

            # Set color ramp colors
            originalRampColors = obj.active_material.node_tree.nodes['ColorRamp'].color_ramp.elements[:]
            for i, c in enumerate( originalRampColors ):
                color = c.color[:]
                colorRamp.color_ramp.elements[i].color = color

            # Add Texture coordiantes and Mapping nodes
            mapp  = t.nodes.new( 'ShaderNodeMapping'  )
            texco = t.nodes.new( 'ShaderNodeTexCoord' )

            # Set up texture coordiantes Y rotation
            mapp.rotation[1] = radians( 45 )

            # Set up links
            t.links.new( mapp.inputs['Vector'],   texco.outputs['Object'] )
            t.links.new( colorRamp.inputs['Fac'], mapp.outputs['Vector'] )

        else:
            legendMat = bpy.data.materials["legend"]

        legendPlane.active_material = legendMat

    ## Generate legend text

    legendTextMat = None
    if 'legendText' in bpy.data.materials:
        legendTextMat = bpy.data.materials["legendText"]
    else:
        # Generate a material for the text
        legendTextMat = bpy.data.materials.new( "legendText" )

        legendTextMat.use_nodes = True
        t = legendTextMat.node_tree
        if 'Diffuse BSDF' in t.nodes: 
            t.nodes.remove( t.nodes['Diffuse BSDF'] )

        emit = t.nodes.new( 'ShaderNodeEmission' )
        mo   = t.nodes['Material Output'] if 'Material Output' in t.nodes else t.nodes.new( 'ShaderNodeOutputMaterial' )
        t.links.new( emit.outputs['Emission'], mo.inputs['Surface'] )
        emit.inputs['Color'].default_value = (0,0,0,1) # Set color to black

    # Calculate text positions
    heightRange = maxZ - minZ
    rungs       = 7
    interval    = heightRange / rungs

    ladderText = [ str( round( minZ + i * interval - offset, 2 ) ) for i in range(2, rungs) ]
    ladderText = [ str( round( minZ - offset, 2 ) ) ] + ladderText + [ str( round( maxZ - offset, 2 ) ) ] # Add min and max Z values

    legendGlobCoo = [ legendPlane.matrix_world * v.co for v in legendPlane.data.vertices ]
    legendY = [ co.y for co in legendGlobCoo ]

    minY, maxY = ( min( legendY ), max( legendY ) )
    yInterval  = ( maxY - minY ) / rungs
    yPositions = [ minY + i * yInterval for i in range( rungs ) ]

    # Set X position as legend plane's maximum X + a space of 0.5 blender units
    xPos = max([ co.x for co in legendGlobCoo ]) + 0.5

    for i, yPos, text in zip( range(rungs), yPositions, ladderText ):
        name = "rung%s" % i

        o = None
        if name in bpy.data.objects:
            o = bpy.data.objects[ name ]
        else:
            bpy.ops.object.text_add( location = ( xPos, yPos, 0 ), layers = [ i == 1 for i in range(20) ] )
            o = bpy.data.objects[ bpy.context.object.name ]
            o.name = name
            o.location.y += i * ( o.dimensions.y / 2 )

        o.data.body = text

        o.active_material = legendTextMat

bpy.app.handlers.frame_change_pre.append( update_legend )