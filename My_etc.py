# 3D Navigation_x TOOLBAR v1.2 - 3Dview Addon - Blender 2.5x
#
# THIS SCRIPT IS LICENSED UNDER GPL, 
# please read the license block.
#
# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

bl_info = {
    "name": "My_etc",
    "author": "bookyakuno",
    "version": (1),
    "location": "View3D > properties Shelf > My etc",
    "description": "I put  a well-used functions  in Properties Shelf.",
    "warning": "",
    "category": "3D View"}

# import the basic library
import bpy



        
        
class VIEW3D_PT_3dNavigation_xPanelx(bpy.types.Panel):


    bl_idname = "object.my_etc"


    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_label = "My etc_x"




    @classmethod
    def poll(cls, context):
        return (context.space_data and context.active_object)

    def draw(self, context):
        layout = self.layout

        ob = context.active_object
        row = layout.row()
        row.label(text="", icon='OBJECT_DATA')
        row.prop(ob, "name", text="")

        if ob.type == 'ARMATURE' and ob.mode in {'EDIT', 'POSE'}:
            bone = context.active_bone
            if bone:
                row = layout.row()
                row.label(text="", icon='BONE_DATA')
                row.prop(bone, "name", text="")
        
        
        
        
        col = layout.column(align=True)
        col.operator("view3d.view_persportho", text="View Persp/Ortho")  
        

        view = context.space_data
        scene = context.scene
        col.prop(view, "lock_camera")
        col.prop(view, "show_only_render")
        col.prop(view, "show_world")
        





#        play_hide
        if (bpy.context.screen.is_animation_playing == False):
            	col.operator("object.play_hide" , icon='PLAY')  
        
        else:
            	col.operator("object.play_hide" , icon='PAUSE')  



        
        layout.separator()
        col = layout.column(align=True)
        col.prop(view, "use_matcap")
        if view.use_matcap:
            col.template_icon_view(view, "matcap_icon")








        return {'FINISHED'}
        
        
           
"""
class VIEW3D_PT_3dNavigation_xPanelx_02(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_label = "My etc_02"

    @classmethod
    def poll(cls, context):
        return (context.space_data and context.active_object)

    def draw(self, context):
        layout = self.layout

        row = layout.row(align=True)

        op = row.operator(
            "super_grouper.change_selected_objects", text="", emboss=False, icon='WIRE')
        op.sg_objects_changer = 'WIRE_SHADE'

        op = row.operator(
            "super_grouper.change_selected_objects", text="", emboss=False, icon='SOLID')
        op.sg_objects_changer = 'MATERIAL_SHADE'

        op = row.operator(
            "super_grouper.change_selected_objects", text="", emboss=False, icon='RETOPO')
        op.sg_objects_changer = 'SHOW_WIRE'
        
        
"""





class DELETE_KEYFRAMES_RANGE(bpy.types.Operator):
    bl_idname = "pose.delete_keyframes"
    bl_label = "Delete Keyframes"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "Delete all keyframes for selected bones in a time range"

    @classmethod
    def poll(cls, context):
        obj = bpy.context.object
        return obj.type == 'ARMATURE' and obj.mode == 'POSE'

    def execute(self, context):
        wm = bpy.context.window_manager
        arm = bpy.context.object
        act = arm.animation_data.action
        delete = []

        # get selected bones names
        sel = [b.name for b in arm.data.bones if b.select]

        # get bone names from fcurve data_path
        for fcu in act.fcurves:
            name = fcu.data_path.split(sep='"', maxsplit=2)[1]

            # check if bone is selected and got keyframes in range
            if name in sel:
                for kp in fcu.keyframe_points:
                    if wm.del_range_start <= kp.co[0] <= wm.del_range_end:
                        delete.append((fcu.data_path, kp.co[0]))

        # delete keyframes
        for kp in delete:
            arm.keyframe_delete(kp[0], index=-1, frame=kp[1])

        context.scene.frame_set(context.scene.frame_current)
        return {'FINISHED'}









class play_hide(bpy.types.Operator):
    bl_idname = "object.play_hide"
    bl_label = "PLAY & HIDE"



    def execute(self, context):

        

        if (bpy.context.screen.is_animation_playing == False):
            	bpy.context.space_data.show_only_render = True
            	bpy.ops.screen.animation_play(reverse=False, sync=False)
        
        else:
            	bpy.context.space_data.show_only_render = False
            	bpy.ops.screen.animation_play(reverse=False, sync=False)

        

        return {'FINISHED'}





#        bpy.context.space_data.show_only_render = True
#        bpy.ops.screen.animation_play(reverse=False, sync=False)
        







# register the class
def register():
    bpy.utils.register_module(__name__)
 
    pass 

def unregister():
    bpy.utils.unregister_module(__name__)
 
    pass 

if __name__ == "__main__": 
    register()