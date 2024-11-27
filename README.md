This is a small utility to generate .dot files from a repository which can be fed into Graphviz.

### Usage
To plot only the directory structure with all the files:

`python ./project_graph.py <path to project>`

To print all dependencies inside a .blend file we need to specify which executable to use for opening the files.

`python ./project_graph.py -b <path to blender executable> <path to project>`

To plot out the data to an svg in Graphviz, run:

`dot -Tsvg ./graph.dot -o graph.svg`

### To-dos
- Properly sort all the dependencies inside .blend files so the graph is nicer to look at
- General formatting of the graph to make it easier to read
- Separating the paths within the directory from outside dependencies and making that clearer in the Graph.
- More .blend deps. Right now it only tracks images and libraries.