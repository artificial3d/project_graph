import bpy
from pathlib import Path
output = "/Users/andy/dev/project_graph/tmp_bl_deps.txt"
    # todo: pass path automatically when launching blender

lines = []

for lib in bpy.data.libraries:
    lines.append(str(Path(bpy.path.abspath(lib.filepath)).resolve()))

with open(output, "w") as f:
    for line in lines:
        f.write(line + "\n")