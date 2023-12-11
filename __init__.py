import bpy
import os
from bpy.types import Operator, Menu, AddonPreferences
from bpy_extras.io_utils import ExportHelper
from bpy.props import StringProperty
from bpy.utils import register_class

bl_info = {
    'name': 'Pump',
    'category': 'All',
    'author': 'Markus Meyer',
    'version': (0, 0, 3),
    'blender': (3, 5, 0),
    'location': 'Pie Menu (SHIFT+F in Object mode, with objects selected)',
    'description': 'Batch exports selected Objects as separate files.'
}

# For storing hotkeys
addon_keymaps = []

def mkdir_if_necessary(path):
    if os.path.exists(path):
        return
    try:
        os.mkdir(path)
    except:
        raise Exception("Can't find path. Have you set your export path in addon settings?")

def get_objects():
    view_layer = bpy.context.view_layer
    obj_active = view_layer.objects.active
    selection = bpy.context.selected_objects
    scene = bpy.context.scene.name_full
    return {
        "view_layer": view_layer,
        "obj_active": obj_active,
        "selection": selection,
        "scene": scene
    }


def get_export_settings(prefix_only = False):
    user_settings = bpy.context.preferences.addons[__name__].preferences
    print("User Settings: ", user_settings)
    
    # Maybe deepcopy batch_export_path?
    batch_export_path = user_settings.active_folder
    
    if prefix_only:
        return user_settings.active_folder
    
    #if user_settings.scene_sensitivity:
    #   batch_export_path = os.path.join(batch_export_path, bpy.context.scene.name_full)
        
    return {
        "active_folder": user_settings.active_folder,
        "path_1": user_settings.path_1,
        "path_2": user_settings.path_2,
        "path_3": user_settings.path_3,
        "user_settings": user_settings,
        "scene_sensitivity" : user_settings.scene_sensitivity
    }
        

class FBX1(Operator):
    bl_idname = "view3d.fbx_1"
    bl_label = "FBX 1"

    def execute(self, context):
        layers = get_objects()
        
        if not layers["selection"]:
            raise Exception("No Mesh selected")

        export_settings = get_export_settings()
        batch_export_path = export_settings['active_folder']
        
        if export_settings['scene_sensitivity']:
            batch_export_path = os.path.join(batch_export_path, bpy.context.scene.name_full)
        bpy.ops.object.select_all(action='DESELECT')

        for obj in layers["selection"]:
            print("Inline batch export path: ", batch_export_path)
            obj.select_set(True)
            bpy.ops.object.transform_apply(scale=True, location=False, properties=False)
            obj.scale = [100, 100, 100]
            bpy.ops.object.transform_apply(scale=True, location=False, properties=False)
            obj.scale = [.01, .01, .01]
    
            mkdir_if_necessary(batch_export_path)
            
            bpy.ops.export_scene.fbx(
                filepath = os.path.join(batch_export_path, obj.name_full) + ".fbx",
                use_selection = True,
                object_types = {"MESH"},
                use_mesh_modifiers = True,
                use_mesh_modifiers_render = True,
                use_custom_props = False,
                axis_forward = '-Y',
                axis_up = 'Z',
                apply_unit_scale = False,
                use_space_transform = True,
                global_scale = 1,
                apply_scale_options = 'FBX_SCALE_ALL',
                mesh_smooth_type = 'OFF')

            bpy.ops.object.transform_apply(scale=True, location=False, properties=True)
            obj.select_set(False)
    
        layers["view_layer"].objects.active = layers["obj_active"]
        return {"FINISHED"}
    
class OBJ1(Operator):
    bl_idname = "view3d.obj_1"
    bl_label = "OBJ 1"

    def execute(self, context):
        layers = get_objects()
        export_settings = get_export_settings()
        
        if not layers["selection"]:
            raise Exception("No Mesh selected")
        bpy.ops.object.select_all(action='DESELECT')

        for obj in layers["selection"]:
            print("Inline batch export path: ", export_settings['active_folder'])
            obj.select_set(True)
    
            mkdir_if_necessary(export_settings['active_folder'])
            bpy.ops.export_scene.obj(
                filepath = os.path.join(export_settings['active_folder'], obj.name_full) + ".obj",
                use_selection = True,
                use_mesh_modifiers = True,
                axis_forward = '-Y',
                axis_up = 'Z',
                global_scale = 1,
                use_materials = False,
                use_vertex_groups = True,
                use_normals = True,
                use_uvs = True,
                use_smooth_groups = True,
                path_mode = "COPY",
            )

            bpy.ops.object.transform_apply(scale=True, location=False, properties=True)
            obj.select_set(False)
    
        layers["view_layer"].objects.active = layers["obj_active"]
        return {"FINISHED"}


class SetActiveTarget1(Operator):
    bl_idname = "test.set_active_target_1"
    bl_label = "Set the active destination folder"
    
    def invoke(self, context, event):
        bpy.context.preferences.addons[__name__].preferences.active_folder = get_export_settings()['path_1']
        return {'FINISHED'}

class SetActiveTarget2(Operator):
    bl_idname = "test.set_active_target_2"
    bl_label = "Set the active destination folder"
    
    def invoke(self, context, event):
        bpy.context.preferences.addons[__name__].preferences.active_folder = get_export_settings()['path_2']
        return {'FINISHED'}
        
class SetActiveTarget3(Operator):
    bl_idname = "test.set_active_target_3"
    bl_label = "Set the active destination folder"
    
    def invoke(self, context, event):
        bpy.context.preferences.addons[__name__].preferences.active_folder = get_export_settings()['path_3']
        return {'FINISHED'}


class ExportMenu(Menu):
    bl_label = "Batch Export"
    #user_settings = get_export_settings()

    
    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()
        pie.operator("view3d.fbx_1", text="FBX 1", icon="RIGHTARROW")
        pie.operator("view3d.obj_1", text="OBJ 1", icon="RIGHTARROW")
        col = pie.column()
        col.operator("test.set_active_target_1", text = "Main")
        col.operator("test.set_active_target_2", text = "Minimal")
        col.operator("test.set_active_target_3", text = "Sandbox")
        
class TriggerPie(Operator):
    bl_idname = "collection.trigger_pie"
    bl_label = "Trigger"
    
    def invoke(self, context, event):
        bpy.ops.wm.call_menu_pie(name = "ExportMenu")
        return {"FINISHED"}
    

class UserSettings(AddonPreferences):
    bl_idname = __name__
 
    path_1: bpy.props.StringProperty(name="String Value1")
    path_2: bpy.props.StringProperty(name="String Value2")
    path_3: bpy.props.StringProperty(name="String Value3")
    active_folder: bpy.props.StringProperty(name="String Value4", default = "...")
    
    scene_sensitivity: bpy.props.BoolProperty(
        name = "Consider Scenes",
        description = "If True, BatchExporter will export your objects into a subfolder inside your destination folder that is named after the scene in which the object is located. If set to False, BatchExporter will ignore scenes and just exports into your destination folder.",
        default = True
    )
    
    
    def draw(self, context):
        layout = self.layout
        layout.label(text='Destination folder')
        
        row = layout.row()
        row.label(text="Main")
        row.label(text = self.path_1)
        row.operator("test.select_target_path_1", icon="FILEBROWSER", text="Choose path")
        
        row2 = layout.row()
        row2.label(text="Minimal")
        row2.label(text = self.path_2)
        row2.operator("test.select_target_path_2", icon="FILEBROWSER", text="Choose path")
        
        row3 = layout.row()
        row3.label(text="Sandbox")
        row3.label(text = self.path_3)
        row3.operator("test.select_target_path_3", icon="FILEBROWSER", text="Choose path")
        
        layout.separator()
        
        row_scene = layout.row()
        row_scene.prop(self, 'scene_sensitivity', expand=True)


class SelectTargetPath1(Operator, ExportHelper):
    bl_idname = "test.select_target_path_1" 
    bl_label = "Select the target path before triggering DestinationFolderModal"
    
    filepath = '.'
    filename_ext = ''
    #filter_glob: bpy.props.StringProperty(default = 'herethere', options = {} )
    
    def execute(self, context):
        bpy.context.preferences.addons[__name__].preferences.path_1 = self.filepath
        bpy.context.preferences.addons[__name__].preferences.active_folder = self.filepath
        return {'FINISHED'}

class SelectTargetPath2(Operator, ExportHelper):
    bl_idname = "test.select_target_path_2" 
    bl_label = "Select the target path before triggering DestinationFolderModal"
    
    filepath = '.'
    filename_ext = ''
    #filter_glob: bpy.props.StringProperty(default = 'herethere', options = {} )
    
    def execute(self, context):
        bpy.context.preferences.addons[__name__].preferences.path_2 = self.filepath
        return {'FINISHED'}
        
        
class SelectTargetPath3(Operator, ExportHelper):
    bl_idname = "test.select_target_path_3" 
    bl_label = "Select the target path before triggering DestinationFolderModal"
    
    filepath = '.'
    filename_ext = ''
    #filter_glob: bpy.props.StringProperty(default = 'herethere', options = {})
    
    def execute(self, context):
        bpy.context.preferences.addons[__name__].preferences.path_3 = self.filepath
        return {'FINISHED'}


def register():
    bpy.utils.register_class(UserSettings)
    bpy.utils.register_class(SelectTargetPath1)
    bpy.utils.register_class(SelectTargetPath2)
    bpy.utils.register_class(SelectTargetPath3)
    bpy.utils.register_class(SetActiveTarget1)
    bpy.utils.register_class(SetActiveTarget2)
    bpy.utils.register_class(SetActiveTarget3)
    bpy.utils.register_class(TriggerPie)
    bpy.utils.register_class(ExportMenu)
    bpy.utils.register_class(FBX1)
    bpy.utils.register_class(OBJ1)
    
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
    
    bpy.utils.unregister_class(UserSettings)
    bpy.utils.unregister_class(ExportMenu)
    bpy.utils.unregister_class(TriggerPie)
    bpy.utils.unregister_class(SelectTargetPath1)
    bpy.utils.unregister_class(SelectTargetPath2)
    bpy.utils.unregister_class(SelectTargetPath3)
    bpy.utils.unregister_class(SetActiveTarget1)
    bpy.utils.unregister_class(SetActiveTarget2)
    bpy.utils.unregister_class(SetActiveTarget3)
    bpy.utils.unregister_class(FBX1)
    bpy.utils.unregister_class(OBJ1)
    
    #del bpy.types.Scene.active_folder
    #del bpy.types.Scene.path_1
    #del bpy.types.Scene.path_2
    #del bpy.types.Scene.path_3

if __name__ == "__main__" :
    try:
        unregister()
    except:
        pass
    register()
