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
import uuid

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
        
    def create_lines(self, list_vert_floats):
        """ adds a new Node representing the geometry of a line to the COLLADA 
        scene """
        node_uuid = uuid.uuid1()
        vert_src = FloatSource("cubeverts-array", numpy.array(list_vert_floats)
                                                , ('X', 'Y', 'Z'))
        geom = Geometry(self.mesh, "geometry0", "line", [vert_src])
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
        geomnode = GeometryNode(geom, mat_list)
        node = Node("node0", children=[geomnode])
        self.mesh.scene.nodes.append( node)

    def get_corner(self):
        """ locate a feature of the model, the top south-west corner
        """
        tri_set = self.primitives()[0]
        np_array  = tri_set.vertex
        x = []
        y = []
        z = []
        # can numpy array be turned sideways?
        for three_tuple in np_array:
            x.append( three_tuple[0])
            y.append( three_tuple[1])
            z.append( three_tuple[2])
        x.sort()
        x_asc = x 
        y.sort()
        y_asc = y
        z.sort()
        #z.reverse()
        z_dec = z
        return [ x_asc[0], y_asc[0], z_dec[0]]
        #inspect = ret
        #print( type( inspect))
        #print( inspect)
        #print( dir( inspect))
    
        
    def save_lines(self, file_path, list_vert_floats):
        """ Adds a line_set to the current model & saves the resulting COLLADA
        scene as a new file.
        """
        line_set = self.create_lines( list_vert_floats)
        self.mesh.write(file_path)
