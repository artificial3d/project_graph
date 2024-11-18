import os
import uuid
import subprocess
import sys

script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))

blender_exec = "/Applications/Blender.app/Contents/MacOS/blender"
blender_print_deps = f"{script_directory}/blender_print_deps.py"
blender_tmp = f"{script_directory}/tmp_bl_deps.txt"

directory = "/Users/andy/Downloads/wing-it.packed/pro/"
currentdir = os.getcwd()
dotfile = "graph.dot"

dotheader = """digraph {
rankdir = "RL"
splines = "spline"
outputorder = "edgesfirst"
"""

uuid_namespace = uuid.uuid1()

def get_parentdir(path):
    return os.path.dirname(path)

def get_uuid(path):
    return uuid.uuid3(uuid_namespace, path).int

def print_file_node(root, name, shape: str):
    id = get_uuid(os.path.join(root,name))
    node = f'{id} [label = "{name}" shape = "{shape}" style = "filled" fillcolor="white"];'
    return node

def print_file_relation(root, name):
    parentdir = get_parentdir(os.path.join(root,name))
    id = get_uuid(os.path.join(root,name))
    parent_id = get_uuid(parentdir)
    relation = f'{id} -> {parent_id} [arrowsize=0.5 penwidth=5.0 color="grey" dir=back];'
    return relation

def get_blend_relations(root, name):
    relations = []
    blendpath = os.path.join(root, name)
    subprocess.run([blender_exec, blendpath, "--background", "--python", blender_print_deps], shell=False)
    with open(blender_tmp, "r") as file:
        for line in file:
            relations.append(line)
    return relations

def main():
    nodes, edges, blendnodes = [], [], []

    # print directory root as first node so others can connect to it.
    basename = os.path.basename(os.path.abspath(directory))
    root = get_parentdir(os.path.abspath(directory))
    nodes.append(print_file_node(root, basename, shape="folder"))

    for root, dirs, files in os.walk(directory):
        for name in files:
            nodes.append(print_file_node(root, name, shape="box"))
            edges.append(print_file_relation(root, name))
            #if name.endswith(".blend"):
            #    blend_relations = get_blend_relations(root, name)
            #    for rel in blend_relations:
            #        blendnodes.append(f'{get_uuid(rel + "x")} [label = "{os.path.basename(rel)}" shape = "box" style = "rounded" color = "orange"];')
            #        edges.append(f'{get_uuid(os.path.join(root,name))} -> {get_uuid(rel + "x")} [arrowsize = 0.5 color = "orange" style = "dashed"];')
        for name in dirs:
            if name.startswith("."):
                continue
            nodes.append(print_file_node(root, name, shape="folder"))
            edges.append(print_file_relation(root, name))

    with open(os.path.join(currentdir,dotfile), "w") as file:
        file.write(dotheader)
        for line in nodes:
            file.write(line + "\n")
        for line in blendnodes:
            file.write(line + "\n")
        for line in edges:
            file.write(line + "\n")
        file.write("}")

if __name__ == "__main__":
    main()