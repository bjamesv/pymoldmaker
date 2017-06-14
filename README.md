# Pymoldmaker Tutorial

PyMoldmaker is a program designed to automatically generate woodworking "cut lists" from COLLADA 3d models. PyMoldmaker cutlists assist in the precise construction of inexpensive plaster-casting molds, for the hand-layup of carbon fiber parts.

## Overview
 - [3d model of part](#step-1-obtain-3d-model)
 - [Desired cuts](#step-2-describe-parts)
 - [Cutlist](#step-3-generate-cutlist-with-pymoldmaker)
 - [Assembled blank or 'positive' of the part](#step-4-assemble-molding-positive)
 - [Plaster mold](#step-5-create-mold)
 - [Use the mold!](#step-6-use-the-mold)

## Step 1: Obtain 3d model
Obtain a 3d model in COLLADA (.dae) file format, representing the actual size of the item to be molded.

![COLLADA model of part in SketchUp 2015](https://raw.githubusercontent.com/bjamesv/pymoldmaker/master/doc/COLLADA.png)

In my case, a model representing the desired object was created to mm scale in 'SketchUp 2015' using Wine 1.7.34 Windows/Linux compatibility tool. The model was then exported from SketchUp to a COLLADA file, which I named: `positive_for_mold.dae`

## Step 2: Describe parts
Next, create a simple Python module defining a minimal list of parts for PyMoldmaker to generate cutlist for. This minimal description of edges, part orientation & shrink indicators provides the basic details PyMoldmaker needs in order to begin calculating a detailed cutlist.

Example parts description:
```
[ ##List of parts, in the format of strings of "friendly names" paired into
  ## tuples with dicts of arguments for calculator.make_part 
    ("Bottom", { "start_edge": ([-1,1,1],[-1,1,-1])
                ,"end_edge": ([-1,-1,1],[-1,-1,-1])
                ,"part_plane": (1,2) # oriented along Y Z plane
                ,"shrink_edges": {"left", "right"}
                ,"shrink_axis": 1 # shrink along Y axis
                ,"thickness_direction_negative": False #model_center_along_negative_x_axis_from_part
                })
    ,("Left", { "start_edge": ([-1,1,1],[-1,1,-1])
               ,"end_edge": ([1,1,1],[1,1,-1])
               ,"part_plane": (0,2) #oriented along X Z plane
               })
    ,("Right-i", { "start_edge": ([-1,-1,1],[-1,-1,-1])
                  ,"end_edge": ([1,-1,1],[1,-1,-1])
                  ,"part_plane": (0,2) #oriented along X Z plane
                  ,"shrink_edges": {'right': 145.8} #room for other Right parts
                  ,"shrink_axis": 0 # shrink along X axis
                  ,"thickness_direction_negative": False
                  })
]
```

I named my file: `positive_for_mold.py`

## Step 3: Generate cutlist with PyMoldmaker
Check out the latest PyMoldmaker source from GitHub

    $ git clone https://github.com/bjamesv/pymoldmaker

A COLLADA file with the outlines of the pieces to be cut superimposed over the original 3d model, can be generated via the PyMoldmaker script `vector.py`.

    $ python vector.py --input positive_for_mold.dae

By default output is saved to `out.dae`

![outlines of cut parts, overlaid on input model](https://raw.githubusercontent.com/bjamesv/pymoldmaker/master/doc/6mm_overlay.png)

By default a 6mm material thickness and 0.2mm cutting tool kerf width is used when generating cuts

Cutlists can also generated for materials of different thickness by use of the optional `--thickness_mm` parameter.

![outlines of cut parts for 3mm material, overlaid on input model](https://raw.githubusercontent.com/bjamesv/pymoldmaker/master/doc/3mm_overlay.png)

## Step 4: Assemble molding positive
The cutlist parts in `.eps` format are cut by CO2 laser or CNC mill, or can be cut by hand using human-readable cutlist output.

Parts are then glued or laminated back-to-back into sub-assemblies of appropriate thickness, and sub-assemblies are then assembled into the final shape to be molded.

## Step 5: Create mold
The assembled shape (or 'positive' image) to be molded is first prepared for casting by sanding or sealing with paint/wax.

Next a suitable container is filled with enough molding material (plaster) to cover all of the surface features of the shape to be molded, and shape is suspended in place while material cures.

After curing the shape is removed, leaving a 'negative' impression of the shape in the mold material.

## Step 6: Use the mold!
Now you have a plaster mold, for your neat project!
