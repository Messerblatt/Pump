# BatchExporter
python script that exports every selected object as separate files. Press Shift + F to trigger the pie menu.

If you arrange your objects in scenes, BatchExporter will create subfolders according to the scene names
    

**WARNING**: BatchExporter uses a dirty workaround to solve common fbx-scaling issues. Before exporting objects, make sure that you have applied the scale of the objects by using
    `CTRL-A -> Apply scale`
    
Otherwise your objects will scale-up by x100

Written and tested on Blender 3.5.0.
