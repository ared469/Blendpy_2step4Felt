import bpy

def create_shading_nodes():
    # Ensure there is an active object
    obj = bpy.context.object
    if obj is None or obj.type != 'MESH':
        print("Please select a mesh object to apply the shader.")
        return

    # Create a new material or get the existing one
    material_name = "FeltMaterial"
    if material_name in bpy.data.materials:
        material = bpy.data.materials[material_name]
    else:
        material = bpy.data.materials.new(name=material_name)

    material.use_nodes = True
    nodes = material.node_tree.nodes
    links = material.node_tree.links

    # Clear existing nodes
    for node in nodes:
        nodes.remove(node)

    # Create nodes
    tex_coord_node = nodes.new(type='ShaderNodeTexCoord')
    noise_texture_node = nodes.new(type='ShaderNodeTexNoise')
    color_ramp_node = nodes.new(type='ShaderNodeValToRGB')
    mix_rgb_node = nodes.new(type='ShaderNodeMixRGB')
    principled_bsdf_node = nodes.new(type='ShaderNodeBsdfPrincipled')
    material_output_node = nodes.new(type='ShaderNodeOutputMaterial')

    # Arrange nodes
    tex_coord_node.location = (-800, 0)
    noise_texture_node.location = (-600, 0)
    color_ramp_node.location = (-400, 0)
    mix_rgb_node.location = (-200, 0)
    principled_bsdf_node.location = (0, 0)
    material_output_node.location = (200, 0)

    # Configure the nodes
    noise_texture_node.noise_dimensions = '3D'
    noise_texture_node.inputs['Scale'].default_value = 12.0
    noise_texture_node.inputs['Detail'].default_value = 9.0
    noise_texture_node.inputs['Roughness'].default_value = 0.5
    noise_texture_node.inputs['Distortion'].default_value = 2.6

    color_ramp_node.color_ramp.interpolation = 'LINEAR'
    color_ramp_node.color_ramp.elements[0].position = 0.0
    color_ramp_node.color_ramp.elements[1].position = 0.373
    color_ramp_node.color_ramp.elements[0].color = (0, 0, 0, 1)  # Black
    color_ramp_node.color_ramp.elements[1].color = (1, 1, 1, 1)  # White

    mix_rgb_node.blend_type = 'MIX'
    mix_rgb_node.inputs['Fac'].default_value = 0.5
    mix_rgb_node.inputs['Color2'].default_value = (0.8, 0.6, 0.2, 1)  # Light brown

    principled_bsdf_node.inputs['Metallic'].default_value = 0.0
    principled_bsdf_node.inputs['Roughness'].default_value = 0.75
    principled_bsdf_node.inputs['IOR'].default_value = 1.5
    principled_bsdf_node.inputs['Alpha'].default_value = 1.0

    # Connect the nodes
    links.new(tex_coord_node.outputs['Generated'], noise_texture_node.inputs['Vector'])
    links.new(noise_texture_node.outputs['Fac'], color_ramp_node.inputs['Fac'])
    links.new(color_ramp_node.outputs['Color'], mix_rgb_node.inputs['Color1'])
    links.new(mix_rgb_node.outputs['Color'], principled_bsdf_node.inputs['Base Color'])
    links.new(principled_bsdf_node.outputs['BSDF'], material_output_node.inputs['Surface'])

    # Assign the material to the object
    if material.name not in obj.data.materials:
        obj.data.materials.append(material)
    obj.active_material = material

# Run the function to create the shading nodes
create_shading_nodes()