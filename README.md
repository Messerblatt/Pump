# FastFBX
python script that exports every selected object as separate .fbx files. Press Shift + F to trigger the pie menu.

If you arrange your objects in scenes, FastFBX will create subfolders according to the scene names
    
As of now you can only change the target folder by changing the dirs in the source code.

**WARNING**: FastFBX uses a dirty workaround to solve common fbx-scaling issues. Before exporting objects, make sure that you have applied the scale of the objects by using
    `CTRL-A -> Apply scale`
    
Otherwise your objects will scale-up by x100

Written and tested on blender 3.5.0.
