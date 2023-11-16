import bpy
import os

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


bl_info = \
    {
        "name" : "FastFBX",
        "author" : "Markus Meyer <messerblatt@protonmail.com>",
        "version" : (1, 0, 0),
        "blender" : (3, 5, 0),
        "location" : "In Object mode, select Objects, press Shift + F5 to trigger the pie menu",
        "description" :
        "Exports every selected object as separate .fbx files. Press Shift + F to trigger the pie menu.",
        "wiki_url" : "",
        "tracker_url" : "",
        "category" : "Import-Export",
    }

current_file_location = os.path.dirname(bpy.data.filepath)
fbx_folder = "fbx_assets"
export_path = os.path.join(current_file_location, fbx_folder)

def mkdir_if_necessary(path):
    if os.path.exists(path):
        return
    os.mkdir(path)
    
class BatchFBX(bpy.types.Operator):
    bl_idname = "mesh.batch_fbx_export"
    bl_label = "Batch Export FBX"
    
    def invoke(self, context, event):
        view_layer = bpy.context.view_layer
        obj_active = view_layer.objects.active
        selection = bpy.context.selected_objects
        scene = bpy.context.scene.name_full
        
        if not selection:
            raise Exception("No Mesh selected")

        bpy.ops.object.select_all(action='DESELECT')

        for obj in selection:
            full_path = os.path.join(export_path, scene)
            mkdir_if_necessary(full_path)
            self.export_routine(obj, scene)

        view_layer.objects.active = obj_active

        # for obj in selection:
        #    obj.select_set(False)        
        return {"FINISHED"}

    def export_routine(self, obj, scene):
        
        # Workaround for fbx.-scaling issues
        obj.select_set(True)
        bpy.ops.object.transform_apply(scale=True, location=False, properties=False)
        obj.scale = [100, 100, 100]
        bpy.ops.object.transform_apply(scale=True, location=False, properties=False)
        obj.scale = [.01, .01, .01]
    
        # some exporters only use the active object
        # view_layer.objects.active = obj
        
        fn = os.path.join(export_path, scene, obj.name_full)
        bpy.ops.export_scene.fbx(
            filepath=fn + ".fbx", 
            use_selection=True,
            object_types = {"MESH"},
            use_mesh_modifiers = True,
            use_mesh_modifiers_render = True,
            use_custom_props = False,
            axis_forward = 'Y',
            axis_up = 'Z',
            apply_unit_scale = False,
            use_space_transform = True,
            global_scale = 1,
            apply_scale_options = 'FBX_SCALE_ALL',
            mesh_smooth_type = 'OFF'
        )
    
        bpy.ops.object.transform_apply(scale=True, location=False, properties=True)
        obj.select_set(False)
        
class ExportMenu(bpy.types.Menu):
    bl_label = "Pie"
    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()
        pie.operator("mesh.batch_fbx_export", text="Batch Export FBX", icon="RIGHTARROW")

addon_keymaps = []

class TriggerPie(bpy.types.Operator):
    bl_idname = "collection.trigger_pie"
    bl_label = "Trigger"
    
    def invoke(self, context, event):
        bpy.ops.wm.call_menu_pie(name="ExportMenu")
        return {"FINISHED"}

def register():
    bpy.utils.register_class(BatchFBX)
    bpy.utils.register_class(ExportMenu)
    bpy.utils.register_class(TriggerPie)
#    bpy.ops.wm.call_menu_pie(name="ExportMenu")

    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon

    if kc:
        km = wm.keyconfigs.addon.keymaps.new(name='Object Mode')
        kmi = km.keymap_items.new(TriggerPie.bl_idname, 'F', 'PRESS', shift=True)

        addon_keymaps.append((km,kmi))

def unregister():
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()
    
    bpy.utils.unregister_class(BatchFBX)
    del bpy.types.Scene.fbxPath

if __name__ == "__main__" :
    try:
        unregister()
    except:
        pass
    register()

    mkdir_if_necessary(export_path)
