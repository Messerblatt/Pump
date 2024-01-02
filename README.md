# Pump

![Screenshot of BatchExporter's Pie Menu](https://github.com/Messerblatt/Pump/blob/main/Screenhot_lightingOnly.png)

Blender add-on to batch-export many objects one by one.



# Usage
![Screenshot of BatchExporter's Pie Menu](https://github.com/Messerblatt/BatchExporter/blob/main/BatchExporter_screenshot.png)

In Blender, select objects and press Shift+F. At least 1 target directory must be set in the addon settings to give Pump a direction. 

# Options
If you set Scene Sensitivity to True, Pump will mirror your blender-scenes inside your destination folder. This can simplify the asset management of your entire project. If set to False, Pump will just batch-export into your destination folder without considering scenes.
    
**WARNING**: Pump uses a dirty workaround to solve common fbx-scaling issues. Before exporting objects, make sure that you have applied the scale of the objects:
    `CTRL-A -> Apply scale`
    
Otherwise your objects will scale-up by x100

Written and tested on Blender 3.5.0.
