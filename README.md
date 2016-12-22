#Pymoldmaker Tutorial

PyMoldmaker is a program designed to automatically generate woodworking "cut lists" from COLLADA 3d models. PyMoldmaker cutlists assist in the precise construction of inexpensive plaster-casting molds, for the hand-layup of carbon fiber parts.

##Overview
 - [3d model of part](#step-1-obtaining-3d-model)
 - [Cutlist](#step-2-generate-cutlist-with-pymoldmaker)
 - [Assembled blank or 'positive' of the part](#step-3-assemble-molding-positive)
 - [Plaster mold](#step-4-create-mold)
 - [Use the mold!](#step-5-use-the-mold)

##Step 1: Obtaining 3d model
Obtain a 3d model in COLLADA (.dae) file format, representing the actual size of the item to be molded.

![COLLADA model of part in SketchUp 2015](https://raw.githubusercontent.com/bjamesv/pymoldmaker/master/doc/COLLADA.png)

In my case, a model representing the desired object was created to mm scale in 'SketchUp 2015' using the Wine 1.7.34 Windows/Linux compatibility tool. The SketchUp model was then exported to a COLLADA file I named: `positive_for_mold.dae`

##Step 2: Generate cutlist with PyMoldmaker
Check out the latest PyMoldmaker source from GitHub

    $ git clone https://github.com/bjamesv/pymoldmaker

(Work In Progress - 2015-MAR, cutlist generation is in-progress)

Cutlist generation is not complete, however a COLLADA file with the outlines of the pieces to be cut superimposed over the original 3d model, can be generated via the PyMoldmaker script `vector.py`.

    $ python vector.py --input positive_for_mold.dae

By default output is saved to `out.dae`

![outlines of cut parts, overlaid on input model](https://raw.githubusercontent.com/bjamesv/pymoldmaker/master/doc/6mm_overlay.png)

By default a 6mm material thickness and 0.2mm cutting tool kerf width is used when generating cuts

Cutlists can also generated for materials of different thickness by use of the optional `--thickness_mm` parameter.

![outlines of cut parts for 3mm material, overlaid on input model](https://raw.githubusercontent.com/bjamesv/pymoldmaker/master/doc/3mm_overlay.png)

##Step 3: Assemble molding positive
The cutlist parts in `.eps` format are cut by CO2 laser or CNC mill, or can be cut by hand using human-readable cutlist output.

Parts are then glued or laminated back-to-back into sub-assemblies of appropriate thickness, and sub-assemblies are then assembled into the final shape to be molded.

##Step 4: Create mold
The assembled shape (or 'positive' image) to be molded is first prepared for casting by sanding or sealing with paint/wax.

Next a suitable container is filled with enough molding material (plaster) to cover all of the surface features of the shape to be molded, and shape is suspended in place while material cures.

After curing the shape is removed, leaving a 'negative' impression of the shape in the mold material.

#Step 5: Use the mold!
Now you can use your mold for all your neat projects!
