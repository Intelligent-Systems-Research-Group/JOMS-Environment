bl_info = {
    "name": "Move X Axis",
    "category": "Object",
    "blender": (2, 80, 0)
}

import bpy
import fnmatch
import mathutils
from bpy.app.handlers import persistent

in_g = False

@persistent
def handler(scene):
    global in_g
    if in_g:
        return
    #if last(bpy.data.objects,"joints*").data.is_updated:
    g()

def last(objects, regex):
    result = [obj for obj in objects if fnmatch.fnmatchcase(obj.name, regex)]
    return sorted(result,key=lambda x:x.name)[-1]
def f():
    import mathutils
    from math import radians
    def M(x,y,z,i):
        R = mathutils.Euler((x,y,z),'XYZ')
        M = R.to_matrix()
        v = M[i//3][i%3]
        #v = M[i%3][i//3]
        v = v - 1 if i % 4 == 0 else v    
        return v

    bpy.app.driver_namespace['M'] = M
    
    jointnames = [
        "m_root",
        "m_chest",
        "m_neck",
        
        "m_chest.001",
        "m_rupperarm",
        "m_rlowerarm",
        "m_rhand",
        "m_rthumb",
        "m_rthumb-proximal",
        "m_rhand.001",
        "m_rfist",
        "m_rfist.001",
        "m_rfist.002",
        "m_rfist.003",
        
        "m_chest.002",
        "m_lupperarm",
        "m_llowerarm",
        "m_lhand",
        "m_lthumb",
        "m_lthumb-proximal",
        "m_lhand.001",
        "m_lfist",
        "m_lfist.001",
        "m_lfist.002",
        "m_lfist.003",
        
        
        "m_chest.003",
        "m_hip",
        "m_pelvis",
        "m_rupperleg",
        "m_rlowerleg",
        "m_pelvis.001",
        "m_lupperleg",
        "m_llowerleg"]
        
    #{ "m_pelvis","m_hip",-1 },

    #{ "m_rupperleg","m_pelvis",7 },
    #{ "m_rlowerleg","m_rupperleg",8 },
    #{ "m_rfoot","m_rlowerleg",9 },

    #{ "m_lupperleg","m_pelvis",10 },
    #{ "m_llowerleg","m_lupperleg",11 },
    #{ "m_lfoot","m_llowerleg",12 },
        
    
    scene = bpy.context.scene

    armature = last(bpy.data.armatures, "proxy*")
    mesh = last(bpy.data.objects, "test*")
    joints = last(bpy.data.objects, "joints*")

    if len(mesh.modifiers) == 1: 
        mesh.modifiers.new("subsurf","SUBSURF")
        mesh.modifiers["subsurf"].levels = 3
    #print(mesh)
    #armature = bpy.data.armatures["proxy"]
    
        
    start = 9 #0
    stop = 9*len(jointnames)-9

    #skeleton = bpy.data.objects["proxy"] #.pose.bones[bonename].rotation_euler
    skeleton = last(bpy.data.objects,"proxy*")
    mesh = last(bpy.data.objects,"test*")
    
    names = [x.name for x in bpy.data.shape_keys]
    shapekeys = mesh.data.shape_keys
    jointkeys = joints.data.shape_keys
    print(dir(shapekeys)) 
    
    dcount = 0
    for i in range(0,stop): 
        name = "pose"+format(i+9,'05')
        keys = shapekeys #last(bpy.data.shape_keys,"Key*")
        shapekey = keys.key_blocks[name]
        shapekey.slider_min = -1
        shapekey.value = 0
        if not keys.animation_data is None:
            dcount += len(keys.animation_data.drivers)
        shapekey.driver_remove("value", -1)
    #old_drivers = mesh.animation_data.drivers
    state = dcount > 0
    #state = True
    if not state:
        for j in range(20):
            i = j // 2
            name = "shape"+format(i,'05')
            if j % 2 == 1:
                name = f"{name}.001"
            keys = jointkeys
            print (name)
            jointkey = keys.key_blocks[name]
            shapekey = jointkeys.key_blocks[name]
            shapekey.slider_min = -.3
            shapekey.slider_max = .3
            
            shapeblend = mesh.data.shape_keys.key_blocks[name]
            shapeblend.slider_min = -.3
            shapeblend.slider_max = .3
            
            driver = jointkey.driver_add ("value").driver
            driver.type = 'SCRIPTED'
            x = driver.variables.new()
            x.type = "SINGLE_PROP"
            x.name = "x"
            x.targets[0].id_type = "MESH"   
            x.targets[0].id = mesh.data 
            x.targets[0].data_path = 'shape_keys.key_blocks["' + name + '"].value'
            driver.expression = "x"
        
    if not state:
        for i in range(start,stop): #144
            name = "pose"+format(i+9,'05')
            shapekey = shapekeys.key_blocks[name] #last(shapekeys,"Key*")
            shapekey.slider_min = -1
            shapekey.value = 0
            driver = shapekey.driver_add("value").driver
            driver.type = 'SCRIPTED'
            jointId = i // 9
            bonename = "Skeleton_" + jointnames[jointId]
            #bone = skeleton.pose.bones[bonename]
            
            x = driver.variables.new()
            x.type = "TRANSFORMS"
            x.name = "x"
            x.targets[0].id = skeleton.id_data   
            x.targets[0].bone_target = bonename 
            x.targets[0].transform_type = "ROT_X" 
            x.targets[0].transform_space = "LOCAL_SPACE" 
            x.targets[0].data_path = "pose.bones[" + bonename + "].rotation_euler[0]"
            
            y = driver.variables.new()
            y.type = "TRANSFORMS"
            y.name = "y"
            y.targets[0].id = skeleton.id_data    
            y.targets[0].bone_target = bonename 
            y.targets[0].transform_type = "ROT_Y" 
            y.targets[0].transform_space = "LOCAL_SPACE" 
            y.targets[0].data_path = "pose.bones[" + bonename + "].rotation_euler[1]"
            
            z = driver.variables.new()
            z.type = "TRANSFORMS"
            z.name = "z"
            z.targets[0].id = skeleton.id_data    
            z.targets[0].bone_target = bonename 
            z.targets[0].transform_type = "ROT_Z" 
            z.targets[0].transform_space = "LOCAL_SPACE" 
            z.targets[0].data_path = "pose.bones[" + bonename + "].rotation_euler[2]"
            
            driver.expression = "M(x,y,z,"+ str(i%9) + ")"
            
        
    #bpy.app.handlers.depsgraph_update_post.append(handler)
     
            
def g():
    global in_g
    in_g = True
    jointnames = [
        "m_root",
        "m_chest",
        "m_neck",
        
        "m_chest.001",
        "m_rupperarm",
        "m_rlowerarm",
        "m_rhand",
        "m_rthumb",
        "m_rthumb-proximal",
        "m_rhand.001",
        "m_rfist",
        "m_rfist.001",
        "m_rfist.002",
        "m_rfist.003",
        
        "m_chest.002",
        "m_lupperarm",
        "m_llowerarm",
        "m_lhand",
        "m_lthumb",
        "m_lthumb-proximal",
        "m_lhand.001",
        "m_lfist",
        "m_lfist.001",
        "m_lfist.002",
        "m_lfist.003",
        
        
        "m_chest.003",
        "m_hip",
        "m_pelvis",
        "m_rupperleg",
        "m_rlowerleg",
        "m_pelvis.001",
        "m_lupperleg",
        "m_llowerleg"]
        
    #hide = [
    #    "m_root",
    #    "m_chest",
    #    "m_chest.001",
    #    "m_chest.002",
    #    "m_chest.003",
    #]
    hide=[]
    
    temp = bpy.context.view_layer.objects.active
    pos = []
    obj = last(bpy.data.objects,"joints*")
    #bpy.context.view_layer.objects.active = obj
    #bpy.ops.object.mode_set(mode='EDIT')
    for i in range(len(jointnames)):
        #v = obj.data.vertices[i]
        dg = bpy.context.evaluated_depsgraph_get()
        #me = obj.to_mesh(depsgraph=dg,preserve_all_data_layers=True)
        active_eval = obj.evaluated_get(dg)
        me = bpy.data.meshes.new_from_object(active_eval)
        v = me.vertices[i]
        p = v.co
        print(f"{i} {p.xyz}")
        pos.append(p.xyz)
        bpy.data.meshes.remove(me)
    #bpy.ops.object.mode_set(mode='OBJECT')
    #bpy.context.view_layer.objects.active = temp
    
    temp = bpy.context.view_layer.objects.active
    skeleton = last(bpy.data.objects,"proxy*")
    #print(dir(skeleton))
    bpy.context.view_layer.objects.active = skeleton
    bpy.ops.object.mode_set(mode='EDIT')
    for i in range(len(jointnames)):
        jointname = "Skeleton_" + jointnames[i]
        armature = last(bpy.data.armatures,"proxy*")
        if jointnames[i] in hide:
            armature.bones[jointname].hide = True
        #skeleton.show_x_ray = True
        
        #armature.draw_type = 'STICK'
        bones = armature.edit_bones
        joint = bones[jointname]
        
        scene = bpy.context.scene
        
        dg = bpy.context.evaluated_depsgraph_get()
        
        p = pos[i]
            
        #print(dir(p))
        #print(p) 
        #print(joint.head.xyz) 
        print(p.xyz)
        joint.head.xyz = p.xyz 
        joint.tail.xyz = p.xyz
        joint.tail.y = p.y + .1#.00002
        #print(joint.head.xyz) 
        #obj.to_mesh_clear()
        #bpy.data.meshes.remove(me)
    dg = bpy.context.evaluated_depsgraph_get().update()
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.context.view_layer.objects.active = temp
        #bpy.
    
    in_g = False
    
class ObjectMoveX(bpy.types.Operator): 
    """My Object Moving Script"""      # blender will use this as a tooltip for menu items and buttons.
    bl_idname = "object.move_x"        # unique identifier for buttons and menu items to reference.
    bl_label = "Muscle"         # display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # enable undo for the operator.

    def execute(self, context):        # execute() is called by blender when running the operator.

        f()

        return {'FINISHED'}            # this lets blender know the operator finished successfully.

class ChangeJoints(bpy.types.Operator):
    bl_idname = "object.changejoints"        # unique identifier for buttons and menu items to reference.
    bl_label = "ChangeJoints"         # display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # enable undo for the operator.

    def execute(self, context):        # execute() is called by blender when running the operator.
        
        g()

        return {'FINISHED'}            # this lets blender know the operator finished successfully.

class Dump(bpy.types.Operator):
    bl_idname = "object.dump"        # unique identifier for buttons and menu items to reference.
    bl_label = "Dump"         # display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # enable undo for the operator.

    def execute(self, context):        # execute() is called by blender when running the operator.
        jointnames = [
        "m_root",
        "m_chest",
        "m_neck",
        
        "m_chest.001",
        "m_rupperarm",
        "m_rlowerarm",
        "m_rhand",
        "m_rthumb",
        "m_rthumb-proximal",
        "m_rhand.001",
        "m_rfist",
        "m_rfist.001",
        "m_rfist.002",
        "m_rfist.003",
        
        "m_chest.002",
        "m_lupperarm",
        "m_llowerarm",
        "m_lhand",
        "m_lthumb",
        "m_lthumb-proximal",
        "m_lhand.001",
        "m_lfist",
        "m_lfist.001",
        "m_lfist.002",
        "m_lfist.003",
        
        
        "m_chest.003",
        "m_hip",
        "m_pelvis",
        "m_rupperleg",
        "m_rlowerleg",
        "m_pelvis.001",
        "m_lupperleg",
        "m_llowerleg"]
        f = open('pose.csv','w+')
        #g= open('shape.csv','w+')
        
        for i in range(10):
            bpy.ops.import_scene.fbx(filepath="/media/dl/Volume/out_scaled_comp/p%d_261binZYX.fbx" % i,
                global_scale = 100)            
            bpy.ops.object.move_x()
            bpy.ops.object.changejoints()
            
            for t in range(2,51):
                bpy.context.scene.frame_set(t)
                for x in jointnames:
                    jointname = "Skeleton_%s" % x
                    skeleton = last(bpy.data.objects,"proxy*")
                    rot = skeleton.pose.bones[jointname].rotation_quaternion
                    loc = skeleton.pose.bones[jointname].location
                    if x == "Skeleton_m_root":
                        f.write("%f,%f,%f," % (loc.x, loc.y, loc.z))
                    f.write("%f,%f,%f,%f," % (rot.w, rot.x, rot.y, rot.z))
                    print(rot)
                f.write('\n')
            
            base = last(bpy.data.objects,"base*") 
            base.select_set(state = True)
            for c in base.children:
                c.select_set(state = True)
            bpy.ops.object.delete()
            
        f.close()
        return {'FINISHED'}            # this lets blender know the operator finished successfully.

class Sample(bpy.types.Operator):
    bl_idname = "object.sample"        # unique identifier for buttons and menu items to reference.
    bl_label = "Sample"         # display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # enable undo for the operator.

    def execute(self, context):        # execute() is called by blender when running the operator.
        jointnames = [
        "m_root",
        "m_chest",
        "m_neck",
        
        "m_chest.001",
        "m_rupperarm",
        "m_rlowerarm",
        "m_rhand",
        "m_rthumb",
        "m_rthumb-proximal",
        "m_rhand.001",
        "m_rfist",
        "m_rfist.001",
        "m_rfist.002",
        "m_rfist.003",
        
        "m_chest.002",
        "m_lupperarm",
        "m_llowerarm",
        "m_lhand",
        "m_lthumb",
        "m_lthumb-proximal",
        "m_lhand.001",
        "m_lfist",
        "m_lfist.001",
        "m_lfist.002",
        "m_lfist.003",
        
        
        "m_chest.003",
        "m_hip",
        "m_pelvis",
        "m_rupperleg",
        "m_rlowerleg",
        "m_pelvis.001",
        "m_lupperleg",
        "m_llowerleg"]
        f = open('pose.csv','r')
        #g= open('shape.csv','w+')
        
        for i in range(1):
            #bpy.ops.import_scene.fbx(filepath="/media/dl/Volume/out_scaled_comp/p%d_261binZYX.fbx" % i,
            #    global_scale = 100)            
            #bpy.ops.object.move_x()
            #bpy.ops.object.changejoints()
            
            for t in range(500):
                frame = [float(x) for x in f.readline()[:-2].split(',')]
                print (t)
                print (frame)
                #bpy.context.scene.frame_set(t)
                #bpy.ops.object.mode_set(mode='POSE')
                for j,x in enumerate(jointnames):
                    jointname = "Skeleton_%s" % x
                    skeleton = last(bpy.data.objects,"proxy*")
                    print([x.name for x in bpy.data.objects])
                    skeleton.pose.bones[jointname].rotation_mode = "QUATERNION"
                    skeleton.pose.bones[jointname].rotation_quaternion = mathutils.Quaternion(
                        (frame[4*j+0],frame[4*j+1],frame[4*j+2],frame[4*j+3])
                    )
                    #print(skeleton.pose.bones[jointname].rotation_quaternion)
                    #skeleton.pose.bones[jointname].rotation_quaternion = mathutils.Quaternion(
                    #    (1,0,0,0)
                    #)
                #skeleton.pose.update()
                bpy.context.scene.update()
                bpy.data.scenes['Scene'].render.filepath = '/media/dl/DATA/renders/%06d' % t
                bpy.ops.render.render(write_still=True)
        
        f.close()
        return {'FINISHED'}   
        base = last(bpy.data.objects,"base*") 
        base.select_set(state = True)
        for c in base.children:
            c.select_set(state = True)
        bpy.ops.object.delete()
        return {'FINISHED'}            # this lets blender know the operator finished successfully.


def register():
    bpy.utils.register_class(ObjectMoveX)
    bpy.utils.register_class(ChangeJoints)
    bpy.utils.register_class(Dump)
    bpy.utils.register_class(Sample)


def unregister():
    bpy.utils.unregister_class(ObjectMoveX)
    bpy.utils.unregister_class(ChangeJoints)
    bpy.utils.unregister_class(Dump)
    bpy.utils.register_class(Sample)


# This allows you to run the script directly from blenders text editor
# to test the addon without having to install it.
if __name__ == "__main__":
    register()

 
