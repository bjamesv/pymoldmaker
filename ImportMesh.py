#!/usr/bin/python3
"""
this file is a part of pymoldmaker

Copyright (C) 2015 Brandon J. Van Vaerenbergh

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
from collada import Collada
from collada.lineset import LineSet
from collada.source import InputList
from collada.source import FloatSource
import numpy

from collada import material
from collada.geometry import Geometry
from collada.scene import MaterialNode
from collada.scene import GeometryNode
from collada.scene import Node
from collada.scene import Scene

class Mesh:
    def __init__(self, file_path):
        self.mesh = Collada( file_path)
        
    def geometry(self):
        """ returns data contained in the COLLADA <geometry/> tag 
        per:
        pycollada.github.io/reference/generated/collada.geometry.Geometry.html
        """
        return self.mesh.geometries[0]
        
    def visual_scene(self):
        """ returns data contained in the COLLADA <visual_sceen/> tag 
        per:
        pycollada.github.io/reference/generated/collada.scene.Scene.html
        """
        return self.mesh.scene
        
    def primitives(self):
        """ returns a list of primitive sets specified in the <geometry/>
        per:
        pycollada.github.io/reference/generated/collada.primitive.Primitive.html
        """
        return self.geometry().primitives
    
    def lines(self):
        """
        returns a primitive set of the shape we are importing
        ##TODO: work out a meaningful way to extract shape's dimensions
        # (Polylist may be better than LineSet)
        # per: http://pycollada.github.io/structure.html#structure
        """
        for primative_list in self.primitives():
            if type(primative_list) is LineSet:
                vertex_i = primative_list.vertex_index
                return primative_list.vertex[vertex_i][0]
        else:
            ## list of mesh geometries was exhausted, without finding a LineSet
            raise Exception("No LineSet found in the list of mesh geometries!")
            
    def sections(self):
        """
        Returns the coordinates of the first face of the cube/model
        ##TODO: provide prototype implementation for the model slicing function
        """
        pass
        
    def create_lines(self):
        """ returns a new Node representing a geometry that will add some lines
         to the COLLADA scene """
        vert_floats = [-50,50,50
                      ,50,50,50
                      ,-50,-50,50
                      ,50,-50,50]
        print("verts: {}".format(len(vert_floats)))
        normal_floats = [0,0,1,0,0,1,0,0,1,0,0,1,0,1,0,
            0,1,0,0,1,0,0,1,0,0,-1,0,0,-1,0,0,-1,0,0,-1,0,-1,0,0,
            -1,0,0,-1,0,0,-1,0,0,1,0,0,1,0,0,1,0,0,1,0,0,0,0,-1,
            0,0,-1,0,0,-1,0,0,-1]
        print("normals:"+str(len(normal_floats)))
        vert_src = FloatSource("cubeverts-array", numpy.array(vert_floats), ('X', 'Y', 'Z'))
        normal_src = FloatSource("cubenormals-array", numpy.array(normal_floats), ('X', 'Y', 'Z'))
        geom = Geometry(self.mesh, "geometry0", "mycube", [vert_src, normal_src])
        # InputList will consist of one item, a set of vertices
        input_list = InputList()
        input_list.addInput(0, 'VERTEX', "#cubeverts-array")
        # since line vertex do not need to be paired with normals
        # indices list is just the indise of our vertex source
        indices_list = range(0, len(vert_src))
        # lines are formed by connecting every odd vertex triplet 
        # to the X,Y,Z triplet declared immediately after it.
        indices = numpy.array( indices_list)
        lineset = geom.createLineSet( indices, input_list, "materialref")
        geom.primitives.append( lineset)
        self.mesh.geometries.append(geom)
        mat_list = []
        geomnode = GeometryNode(geom, mat_list) #matnode])
        node = Node("node0", children=[geomnode])
        #myscene = Scene("myscene", [node])
        #self.mesh.scenes.append(myscene)
        # add Node to existing visual_scene
        self.mesh.scene.nodes.append( node)
        """geom = self.geometry()
    	indices_for_inputlist = numpy.array([0,1])
        inputlist = InputList()
        # define a source of coordinates for line endpoints
        vert_floats = [-50,50,50,50,50,50]
        vert_array = numpy.array(vert_floats)
        vert_src_id = "lineverts-array"
        vert_src = FloatSource( vert_src_id, vert_array, ('X', 'Y', 'Z'))
        # specifiy VERTEX contents, per:
        # pycollada.github.io/reference/generated/collada.source.InputList.html
        offset = 0 # index starts & stays at 0, b/c we only add 1x source
        inputlist.addInput( offset, 'VERTEX','#'+vert_src_id)
        materialid = None
        geom.createLineSet( indices_for_inputlist, inputlist, materialid)"""
        
    def save_lines(self, file_path):
        """ Adds a line_set to the current model & saves the resulting COLLADA
        scene as a new file.
        """
        line_set = self.create_lines()
        self.mesh.write(file_path)
