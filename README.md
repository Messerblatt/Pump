# Pump


Blender add-on to batch-export many objects one by one.

# Usage
![Screenshot of BatchExporter's Pie Menu](https://github.com/Messerblatt/BatchExporter/blob/main/BatchExporter_screenshot.png)

In Blender, select objects and press Shift+F. At least 1 target directory must be set in the addon settings to give Pump a direction. 

# Options
If you set Scene Sensitivity to True, Pump will export your objects into a subfolder inside your destination folder that is named after the scene in which the object is in. If set to False, Pump will just export into your destination folder.
    
**WARNING**: Pump uses a dirty workaround to solve common fbx-scaling issues. Before exporting objects, make sure that you have applied the scale of the objects by using
    `CTRL-A -> Apply scale`
    
Otherwise your objects will scale-up by x100

Written and tested on Blender 3.5.0.
