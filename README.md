# BatchExporter
Blender addon to accelerate the export-import pipeline to Game engines. 

# Installation
Git clone this repo and install the .zip file, or just download the .zip file from this repo and install

# Usage
In Blender, select objects and press Shift+F

# Options
If you set Scene Sensitivity to True, BatchExporter will export your objects into a subfolder inside your destination folder that is named after the scene in which the object is in. If set to False, BatchExporter just exports into your destination folder.",
    
**WARNING**: BatchExporter uses a dirty workaround to solve common fbx-scaling issues. Before exporting objects, make sure that you have applied the scale of the objects by using
    `CTRL-A -> Apply scale`
    
Otherwise your objects will scale-up by x100

Written and tested on Blender 3.5.0.
