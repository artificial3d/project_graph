import bpy
from pathlib import Path
import sys

if '--' in sys.argv:
    argv = sys.argv[sys.argv.index('--') + 1:]

output = argv[0]

lines = []

for lib in bpy.data.libraries:
    lines.append(str(Path(bpy.path.abspath(lib.filepath)).resolve()) + "\n")

for img in bpy.data.images:
    lines.append(str(Path(bpy.path.abspath(img.filepath)).resolve()) + "\n")

with open(output, "w") as f:
    f.writelines(lines)