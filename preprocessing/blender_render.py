import bpy
import bpy_extras
from math import sin,cos,sqrt
from pathlib import Path
from mathutils import Quaternion, Vector, Matrix, Euler
from os import environ

# get the relevant data
def blender_to_opencv(cam):
    scene = bpy.context.scene
    # assume image is not scaled
    assert scene.render.resolution_percentage == 100
    # assume angles describe the horizontal field of view
    assert cam.sensor_fit != 'VERTICAL'

    f_in_mm = cam.lens
    sensor_width_in_mm = cam.sensor_width

    w = scene.render.resolution_x
    h = scene.render.resolution_y

    pixel_aspect = scene.render.pixel_aspect_y / scene.render.pixel_aspect_x

    f_x = f_in_mm / sensor_width_in_mm * w
    f_y = f_x * pixel_aspect

    # yes, shift_x is inverted. WTF blender?
    c_x = w * (0.5 - cam.shift_x)
    # and shift_y is still a percentage of width..
    c_y = h * 0.5 + w * cam.shift_y

    K = [[f_x, 0, c_x],
         [0, f_y, c_y],
         [0,   0,   1]]
    print(K)

def get_calibration_matrix_K_from_blender(camd):
    f_in_mm = camd.lens
    scene = bpy.context.scene
    resolution_x_in_px = scene.render.resolution_x
    resolution_y_in_px = scene.render.resolution_y
    scale = scene.render.resolution_percentage / 100
    sensor_width_in_mm = camd.sensor_width
    sensor_height_in_mm = camd.sensor_height
    pixel_aspect_ratio = scene.render.pixel_aspect_x / scene.render.pixel_aspect_y
    if (camd.sensor_fit == 'VERTICAL'):
        # the sensor height is fixed (sensor fit is horizontal), 
        # the sensor width is effectively changed with the pixel aspect ratio
        s_u = resolution_x_in_px * scale / sensor_width_in_mm / pixel_aspect_ratio 
        s_v = resolution_y_in_px * scale / sensor_height_in_mm
    else: # 'HORIZONTAL' and 'AUTO'
        # the sensor width is fixed (sensor fit is horizontal), 
        # the sensor height is effectively changed with the pixel aspect ratio
        pixel_aspect_ratio = scene.render.pixel_aspect_x / scene.render.pixel_aspect_y
        s_u = resolution_x_in_px * scale / sensor_width_in_mm
        s_v = resolution_y_in_px * scale * pixel_aspect_ratio / sensor_height_in_mm


    # Parameters of intrinsic calibration matrix K
    alpha_u = f_in_mm * s_u
    alpha_v = f_in_mm * s_v
    u_0 = resolution_x_in_px * scale / 2
    v_0 = resolution_y_in_px * scale / 2
    skew = 0 # only use rectangular pixels

    K = Matrix(
        ((alpha_u, skew,    u_0),
        (    0  , alpha_v, v_0),
        (    0  , 0,        1 )))
    return K

# Returns camera rotation and translation matrices from Blender.
# 
# There are 3 coordinate systems involved:
#    1. The World coordinates: "world"
#       - right-handed
#    2. The Blender camera coordinates: "bcam"
#       - x is horizontal
#       - y is up
#       - right-handed: negative z look-at direction
#    3. The desired computer vision camera coordinates: "cv"
#       - x is horizontal
#       - y is down (to align to the actual pixel coordinates 
#         used in digital images)
#       - right-handed: positive z look-at direction
def get_3x4_RT_matrix_from_blender(cam):
    # bcam stands for blender camera
    R_bcam2cv = Matrix(
        ((1, 0,  0),
         (0, -1, 0),
         (0, 0, -1)))

    # Transpose since the rotation is object rotation, 
    # and we want coordinate rotation
    # R_world2bcam = cam.rotation_euler.to_matrix().transposed()
    # T_world2bcam = -1*R_world2bcam * location
    #
    # Use matrix_world instead to account for all constraints
    location, rotation = cam.matrix_world.decompose()[0:2]
    R_world2bcam = rotation.to_matrix().transposed()

    # Convert camera location to translation vector used in coordinate changes
    # T_world2bcam = -1*R_world2bcam*cam.location
    # Use location from matrix_world to account for constraints:     
    T_world2bcam = -1*R_world2bcam @ location

    # Build the coordinate transform matrix from world to computer vision camera
    R_world2cv = R_bcam2cv@R_world2bcam
    T_world2cv = R_bcam2cv@T_world2bcam

    # put into 3x4 matrix
    RT = Matrix((
        R_world2cv[0][:] + (T_world2cv[0],),
        R_world2cv[1][:] + (T_world2cv[1],),
        R_world2cv[2][:] + (T_world2cv[2],)
         ))
    return RT

def get_3x4_P_matrix_from_blender(cam):
    K = get_calibration_matrix_K_from_blender(cam.data)
    RT = get_3x4_RT_matrix_from_blender(cam)
    return K@RT, K, RT

# ----------------------------------------------------------
# Alternate 3D coordinates to 2D pixel coordinate projection code
# adapted from https://blender.stackexchange.com/questions/882/how-to-find-image-coordinates-of-the-rendered-vertex?lq=1
# to have the y axes pointing up and origin at the top-left corner
def project_by_object_utils(cam, point):
    scene = bpy.context.scene
    co_2d = bpy_extras.object_utils.world_to_camera_view(scene, cam, point)
    render_scale = scene.render.resolution_percentage / 100
    render_size = (
            int(scene.render.resolution_x * render_scale),
            int(scene.render.resolution_y * render_scale),
            )
    return Vector((co_2d.x * render_size[0], render_size[1] - co_2d.y * render_size[1]))

#folder = "/media/dl/DATA/EHF"
#folder= "/media/dl/DATA/MPI-FAUST/scans/Faust0"
#folder="/media/dl/Volume/dfaust_full/scans_raw/"
#folder="/media/dl/Volume/dfaust_full/scans/"

import json
Json = None
with open(environ['CAM'],'r') as f:
    Json = json.load(f)
folder="/input"
outfolder = "/output"

p = Path(folder)
cameras = Json['setup']
#bpy.data.objects.remove(bpy.data.objects["Cube"],do_unlink=True)
#bpy.context.scene.cycles.device = 'GPU'
bpy.context.preferences.addons['cycles'].preferences.get_devices()
bpy.context.preferences.addons['cycles'].preferences.compute_device_type = 'CUDA'
bpy.context.preferences.addons['cycles'].preferences.devices[0].use = True
bpy.context.scene.cycles.device = 'GPU'
bpy.context.scene.cycles.samples = 1

for path in p.glob("**/*.ply"): # REVERT TO PLY
    rel = path.parent.relative_to(folder)
    #print(str(f))
    print(rel)
    impath = folder + "/" + str(path.stem)
    
    imagename = Path(f"{str(path.stem)}_{0}.png")
    outpath = Path(outfolder,rel,imagename)
    
    bpy.ops.import_mesh.ply(filepath=str(path))
    #bpy.ops.import_scene.obj(filepath=str(path))

    obj = bpy.data.objects[str(path.stem)]
    #obj = bpy.data.objects["m_mosh_cmu88_Mesh"]
    #obj = bpy.data.objects["f_mosh_cmu05_Mesh"] #75_Mesh.001
    #print(bpy.data.materials.get("Material"))
    #obj.data.materials.append( bpy.data.materials.get("Material") )
    #obj.active_material_index = 0
    #obj.active_material.name="Material"
    mat = bpy.data.materials.get("Material")
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.material_slot_add()
    obj.material_slots[0].material = mat
    obj.active_material_index = 0
    obj.rotation_euler = [0,0,0]
    
    layer = bpy.context.view_layer
    #layer.update()

    PI = 3.141592
    PH = PI/2
    PQ = PI/4
    distance = 2.5

    s = 1
    w = 1600//s
    h = 1200//s
    cx = 790.263706/s
    cy = 578.90334/s
    fx = 1498.2242623/s
    fy = 1498.22426253/s
    
    
    cam = bpy.data.cameras["Camera"]
    scene = bpy.data.scenes["Scene"]
    scene.render.resolution_x = w
    scene.render.resolution_y = h
    cam.shift_x = -(cx/w - .5)
    cam.shift_y = -(cy - .5*h)/w
    print(fx/w)
    cam.lens = fx / w
    pixel_aspect = fy/fx
    scene.render.pixel_aspect_x = 1.0
    scene.render.pixel_aspect_y = pixel_aspect
    cam.sensor_width = 1
    
    camera = bpy.data.objects["Camera"]
    #blender_to_opencv(camera.data)
    
    for i,jsonCam in enumerate(cameras[0:8]): #4:5
        #print(jsonCam)
        m = jsonCam['R']
        p = Matrix([[0,0,0],[0,0,0],[0,0,0]])
        for j in range(9):
            p[j//3][j%3] = m[j]
        print(p)
        mat = p @ Euler((PI,0,0)).to_matrix()
        
        #camera.location = [distance*sin(angle),-.3,distance*cos(angle)]
        ax,ang=mat.to_quaternion().to_axis_angle() 
        camera.location = Vector(jsonCam['t'])
        camera.rotation_mode = 'AXIS_ANGLE'
        camera.rotation_axis_angle = [ang,ax[0],ax[1],ax[2]]
        #camera.location = p @ (-Vector(jsonCam['t']))
        print(camera.location)
        print(mat)
        print(mat.to_quaternion().to_axis_angle())
        
        layer.update()
        P, K, RT = get_3x4_P_matrix_from_blender(camera)
    
        imagename = Path(f"{str(path.stem)}_{i}.png")
        outpath = Path(outfolder,rel,imagename)
        bpy.context.scene.render.filepath=str(outpath)
        bpy.ops.render.render(write_still=True, use_viewport=False) #True
    
    bpy.data.objects.remove(obj,do_unlink=True)
    
    for block in bpy.data.meshes:
        if block.users == 0:
            bpy.data.meshes.remove(block)

    for block in bpy.data.materials:
        if block.users == 0:
            bpy.data.materials.remove(block)

    for block in bpy.data.textures:
        if block.users == 0:
            bpy.data.textures.remove(block)

    for block in bpy.data.images:
        if block.users == 0:
            bpy.data.images.remove(block)
    
