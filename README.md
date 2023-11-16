# FastFBX
Blender add-on that exports every selected object as separate .fbx files. Press Shift + F to trigger the pie menu.

The location of the saved files is:
    `yourBlenderFile.blend/fbx_assets/`
    
If you arrange your objects in scenes, fast-fbx will create subfolders according to the name of the scenes:
    `yourBlenderFile.blend/fbx_assets/scene/nameOfObject.fbx`
    
As of now you can only change the target folder by changing the dirs in the source code."

**WARNING**: "Fast-fbx uses a dirty workaround to solve common fbx-scaling issues. Before exporting objects, make sure that you have applied the scale of the objects by using
    `CTRL-A -> Apply scale`
    
Otherwise your objects will scale-up by x100


Written and tested on blender 3.5.0.
