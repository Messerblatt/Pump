import bpy
from bpy.types import Operator, Menu, AddonPreferences
from bpy_extras.io_utils import ExportHelper
from bpy.props import StringProperty
from bpy.utils import register_class
import os
 
bl_info = {
    'name': 'BatchExporter',
    'category': 'All',
    'author': 'Markus Meyer',
    'version': (0, 0, 2),
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
        raise Exception("Can't find path. Have your export path in addon settings?")

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
    
def get_user_path():
    return {"export_path_1" : bpy.context.preferences.addons['BatchExporter'].preferences.batch_export_path}
    
def export_routine(obj, export_path, settings): # settings not implemented yet
    # Workaround for fbx.-scaling issues:
    obj.select_set(True)
    bpy.ops.object.transform_apply(scale=True, location=False, properties=False)
    obj.scale = [100, 100, 100]
    bpy.ops.object.transform_apply(scale=True, location=False, properties=False)
    obj.scale = [.01, .01, .01]

    # some exporters only use the active object
    # view_layer.objects.active = obj
    fn = os.path.join(export_path, obj.name_full)
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
        
class BatchExporter(Operator):
    bl_idname = "mesh.batch_exporter"
    bl_label = "Batch Exporter"
    
    def invoke(self, context, event):
        layers = get_objects()
        export_settings = "..." # Not implemented yet
        batch_export_path_ = get_user_path()['export_path_1']
        
        if not layers["selection"]:
            raise Exception("No Mesh selected")

        bpy.ops.object.select_all(action='DESELECT')

        for obj in layers["selection"]:
            
            # TODO: Enable disable scene-sensitivity in user-settings
            scene_sensitivity = context.preferences.addons['BatchExporter'].preferences.scene_sensitive
            if scene_sensitivity:
                batch_export_path_ = os.path.join(batch_export_path_, layers["scene"])
            mkdir_if_necessary(batch_export_path_)
            export_routine(obj, batch_export_path_, export_settings)

        layers["view_layer"].objects.active = layers["obj_active"]
        return {"FINISHED"}
        
class ExportMenu(Menu):
    bl_label = "Batch Export"
    
    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()
        pie.operator("mesh.batch_exporter", text="Batch Export FBX", icon="RIGHTARROW")


# Triggers ExportMenu, because ExportMenu 
# apperantly can't trigger itself
class TriggerPie(Operator):
    bl_idname = "collection.trigger_pie"
    bl_label = "Trigger"
    
    def invoke(self, context, event):
        bpy.ops.wm.call_menu_pie(name = "ExportMenu")
        return {"FINISHED"}
    
class UserSettings(AddonPreferences):
    bl_idname = __name__

    batch_export_path: bpy.props.StringProperty(
        name = "batch_export_path",
        description = "Where user set the exports files",
        default = "Path not set"
    )
    
    scene_sensitive: bpy.props.BoolProperty(
        name = "Consider Scenes",
        description = "If True, BatchExporter will export your objects into a subfolder inside your destination folder that is named after the scene in which the object is in. If set to False, BatchExporter just exports into your destination folder.",
        default = True
    )
    
    def draw(self, context):
        layout = self.layout
        layout.label(text='Destination folder')
        row = layout.row()
        row.label(text=get_user_path()["export_path_1"])
        row.operator("test.folder_pref", icon="FILEBROWSER", text="Choose path")
        row2 = layout.row()
        row2.prop(self, 'scene_sensitive', expand=True)


class DestinationFolderModal(Operator, ExportHelper):
    bl_idname = 'test.folder_pref'
    bl_label = 'Accept'
    bl_options = {'PRESET', 'UNDO'}
 
    filepath = '.'
    filename_ext = ''
    
    filter_glob: StringProperty(
        default='herethere',
        options={}
    )
 
    def execute(self, context):
        bpy.context.preferences.addons['BatchExporter'].preferences.batch_export_path = self.filepath
        print('exported file: ', self.filepath)
        return {'FINISHED'}

def register():
    bpy.utils.register_class(BatchExporter)
    bpy.utils.register_class(UserSettings)
    bpy.utils.register_class(TriggerPie)
    bpy.utils.register_class(ExportMenu)

    bpy.utils.register_class(DestinationFolderModal)
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
    
    bpy.utils.unregister_class(BatchExporter)
    bpy.utils.unregister_class(UserSettings)
    bpy.utils.register_class(ExportMenu)
    bpy.utils.register_class(TriggerPie)
    bpy.utils.unregister_class(DestinationFolderModal)
    
    del bpy.types.Scene.batch_export_path

if __name__ == "__main__" :
    try:
        unregister()
    except:
        pass
    register()
