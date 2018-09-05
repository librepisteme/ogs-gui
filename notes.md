General notes for ogs-gui
========================
## Open source scientific simulation frontend that's actually usable without feeding punchcards into your floppy drive.

## The Plan: 
Create GUI for opengeosys and other open source scientific computing/analysis tools that are lacking in frontends and/or standardization.

### What's working: 

 - rudimentary xml project file import using ugly code
 - tree view showing xml structure
 - active element selection via tree view

### What's not working: 

 - Everything elese

31.08.
------
 - [x ] Find a way to automate python-qt launch on vim save and send it to certain bspc workspace
   - Add to vim during at vim runtime:
```vimrc
autocmd FileWritePost *.py exec [command] shellescape(@%, 1)
``` 
   - Use something like [embear/vimlocalvimrc](https://github.com/embear/vimlocalvimrc)  so it's persistent per project
   - In `~/.vimrc`: 
```vimrc
autocmd FileType python call AutoCmd_python()

fun! AutoCmd_python()
    # various python related stuff
    nnoremap <buffer> <F9> :exec '[command]' shellescape(@%, 1)<cr>
endf
```     
   - Might make this filetype-agnostic or at least expand to most source files and use a makefile.

05.09.
-----
Try to create python bindings using SWIG

[wip] Clean up the god damn xml mess
So it's difficult to create a Model from arbitrary nested XML.
Luckily I don't actually need to do that. My options are:
 - Create a Model in python using the qt XmlStreamReader/XmlStreamWriter. Read the important parts from that and then create submodels.
 - Create a Model in QML and then find a way to import that into python to use.

Pros of using QML are the portability should I choose to create other apps entirely in QML.
Cons are obviously adding another layer to this Cronenberg abomination of frameworks.

So the next step is to create a simple XML Model in python, use that for the regular app and if I want to create a QML app later I can either: 
 1. Find a way to convert a PyQt model to QML
 2. Just rewrite the thing
 3. (The best one): Slap myself for wanting to do something in QML

### Current Task: Create ogs xml PyQt model.


03.09. - 01.10.
-----
 - [ ] Think about persistence (but not too much, just mark unsure areas)
 - [ ] Create input fields for a few input xml tags
 - [ ] Try to get vtk working inside the pyqt window
 - [ ] Create one pipeline to start ogs directly from gui

Future
------
 - [ ] Data import from open databases for easy dataset generation
 - [ ] Standardize the everliving fuck out of the various toolset formats

Manic Feaver Dreams
------
 - [ ] Use Machine Learning hyperparameter optimization to improve on model generation
 - [ ] Create *OPT-IN* data sharing for data analysis and modellation improvements using AI.


### Resources:

Primary:
========

- OGS
    Needs geometry (points, lines, surfaces) and mesh (meshed geometry with properties(?).
    Has visualizer (DataExplorer) with some conversion but basically needs 
    command line tools to work. 
    Outputs `*.vtu` files (meshes with properties) and `*.pvd` files (contains info about timestepped meshes). 


- Paraview
    Can visualize a lot of finite element stuff. Also has libraries for python - worth checking out

Secondary:
----------
- Grass GIS
    Geospatial data management. Might be pretty cool for advanced pipelines.

- OpenFOAM
    Open source Computational Fluid Dynamics.
    Seems mighty powerful, the Open Source version is CLI only.
    Need to check out what file formats are used

- QGIS, GIS
    Seems they both do the same? Definitely need to investigate.

Honorary mentions:
------------------

- Elmer
    Open source multiphysical simulation.


Hey, at least you tried Tier:
-----------------------------

- Visual-CFD
    GUI Interface for OpenFOAM. Thought this was open source too, it very very much is not.
    Maybe check out some screenshots and instructional videos for UX inspiration


- GMSH
    Finite-element mesh-creator with GUI (gmsh.info)
    Absolutely disastrous to use via GUI. Might have some interesting cli tools

- GetDP
    Finite Element Solver
     - Only tried in combination with GMSH, need to check out CLI tools.
       Though, it leans more on the script side of things and might be overkill to implement.

# Onelab
    Frontend combining GMSH and GetDP
     - Doesn't seem to be in active development, can be disregarded.
