import bpy

def create_felt_material():
    # Create a new material
    material = bpy.data.materials.new(name="FeltMaterial")
    material.use_nodes = True
    nodes = material.node_tree.nodes
    links = material.node_tree.links

    # Clear existing nodes
    for node in nodes:
        nodes.remove(node)

    # Create necessary nodes
    tex_coord_node = nodes.new(type='ShaderNodeTexCoord')
    noise_texture_node = nodes.new(type='ShaderNodeTexNoise')
    color_ramp_node = nodes.new(type='ShaderNodeValToRGB')
    mix_shader_node = nodes.new(type='ShaderNodeMixRGB')
    principled_bsdf_node = nodes.new(type='ShaderNodeBsdfPrincipled')
    output_node = nodes.new(type='ShaderNodeOutputMaterial')

    # Arrange nodes
    tex_coord_node.location = (-600, 0)
    noise_texture_node.location = (-400, 0)
    color_ramp_node.location = (-200, 0)
    mix_shader_node.location = (0, 0)
    principled_bsdf_node.location = (200, 0)
    output_node.location = (400, 0)

    # Configure nodes
    noise_texture_node.inputs['Scale'].default_value = 12.0
    noise_texture_node.inputs['Detail'].default_value = 9.0
    noise_texture_node.inputs['Roughness'].default_value = 0.5
    noise_texture_node.inputs['Distortion'].default_value = 2.6
    color_ramp_node.color_ramp.interpolation = 'LINEAR'
    color_ramp_node.color_ramp.elements[0].position = 0.0
    color_ramp_node.color_ramp.elements[1].position = 0.373
    mix_shader_node.blend_type = 'MIX'
    principled_bsdf_node.inputs['Roughness'].default_value = 0.75

    # Connect nodes
    links.new(tex_coord_node.outputs['Generated'], noise_texture_node.inputs['Vector'])
    links.new(noise_texture_node.outputs['Fac'], color_ramp_node.inputs['Fac'])
    links.new(color_ramp_node.outputs['Color'], mix_shader_node.inputs['Color1'])
    links.new(mix_shader_node.outputs['Color'], principled_bsdf_node.inputs['Base Color'])
    links.new(principled_bsdf_node.outputs['BSDF'], output_node.inputs['Surface'])

    return material

def create_hair_particle_system(obj, material):
    # Add a particle system
    obj.modifiers.new(name="FeltHair", type='PARTICLE_SYSTEM')
    particle_system = obj.particle_systems[-1]
    settings = particle_system.settings

    # Configure the particle system
    settings.type = 'HAIR'
    settings.count = 700
    settings.hair_length = 0.08
    settings.use_advanced_hair = True
    settings.render_type = 'PATH'
    settings.material = len(obj.data.materials)  # Use the newly created material
    settings.child_type = 'INTERPOLATED'
    settings.child_nbr = 50
    settings.rendered_child_count = 60
    settings.use_clump_noise = True
    settings.clump_noise_size = 1.514
    settings.clump_noise_shape = 8.0

    # Assign the material
    if material.name not in obj.data.materials:
        obj.data.materials.append(material)

# Apply the material and particle system to the active object
if bpy.context.object:
    active_object = bpy.context.object
    felt_material = create_felt_material()
    create_hair_particle_system(active_object, felt_material)
else:
    print("No active object selected. Please select an object and run the script.")