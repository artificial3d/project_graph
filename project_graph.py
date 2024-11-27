import os
import uuid
import argparse
import subprocess
import sys
from pathlib import Path

script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))

blender_print_deps = f"{script_directory}/blender_print_deps.py"
blender_tmp = f"{script_directory}/tmp_bl_deps.txt"

currentdir = os.getcwd()
dotfile = "graph.dot"

dotheader = """digraph {
rankdir = "RL"
splines = "spline"
outputorder = "edgesfirst"
"""

uuid_namespace = uuid.uuid1()

parser = argparse.ArgumentParser()
parser.add_argument(
    "path",
    help="Path to files to create a graph from.",
)

parser.add_argument(
    "-b",
    "--blend",
    help="Plot .blend file dependencies. Warning: Depending on the number of .blend files this may take a long time.",
    required=False,
    nargs='?',
)

def get_parentdir(path):
    return os.path.dirname(path)

def get_uuid(path):
    return uuid.uuid3(uuid_namespace, path).int

def print_file_node(root, name, shape: str):
    """Returns a .dot formatted Node for relationships between files."""
    id = get_uuid(os.path.join(root,name))
    node = f'{id} [label = "{name}" shape = "{shape}" style = "filled" fillcolor="white"];\n'
    return node

def print_file_relation(root, name):
    """Returns a .dot formatted Edge for connecting file nodes."""
    parentdir = get_parentdir(os.path.join(root,name))
    id = get_uuid(os.path.join(root,name))
    parent_id = get_uuid(parentdir)
    relation = f'{id} -> {parent_id} [arrowsize=0.5 penwidth=5.0 color="grey" dir=back];\n'
    return relation

def get_blend_relations(root, name, blender_exec):
    """Return relations inside a blend file by calling the blender executable."""
    relations = []
    blendpath = os.path.join(root, name)
    blender_cmd = [blender_exec, blendpath, "--background", "--python", blender_print_deps, "--", blender_tmp]
    subprocess.run(blender_cmd, shell=False)
    with open(blender_tmp, "r") as file:
        relations = file.readlines()
    return relations

def cancel_program(message: str) -> None:
    """Cancel Execution of this file"""
    print(message)
    sys.exit(0)


def main():
    """Plots a graph of a given directory with all the dependencies of .blend files (optional)."""
    nodes, edges, blendnodes = [], [], []

    args = parser.parse_args()
    project_path = os.path.abspath(args.path)

    if not os.path.exists(project_path):
        cancel_program("Provided project path does not exist")

    if args.blend:
        blender_exec = os.path.abspath(args.blend)

        if not os.path.exists(blender_exec):
            cancel_program("Provided executable path does not exist")

    print_blend_deps = args.blend

    # print directory root as first node so others can connect to it.
    basename = os.path.basename(project_path)
    root = get_parentdir(project_path)
    nodes.append(print_file_node(root, basename, shape="folder"))

    for root, dirs, files in os.walk(project_path):
        for name in files:
            nodes.append(print_file_node(root, name, shape="box"))
            edges.append(print_file_relation(root, name))
            if name.endswith(".blend") and print_blend_deps:
                blend_relations = get_blend_relations(root, name, blender_exec)
                for rel in blend_relations:
                    blendnodes.append(f'{get_uuid(rel + "x")} [label = "{os.path.basename(rel)}" shape = "box" style = "rounded" color = "orange"];')
                    edges.append(f'{get_uuid(rel + "x")} -> {get_uuid(os.path.join(root,name))} [arrowsize = 0.5 color = "orange" style = "dashed"];')
        for name in dirs:
            nodes.append(print_file_node(root, name, shape="folder"))
            edges.append(print_file_relation(root, name))

    with open(os.path.join(currentdir, dotfile), "w") as file:
        file.write(dotheader)
        file.writelines(nodes + blendnodes + edges)
        # close the arguments
        file.write("}")

    print(f'\n Done creating dot file! You may now run Graphviz to turn it into an image. \n For example: dot -Tpng ./graph.dot -o graph.png')

if __name__ == "__main__":
    main()