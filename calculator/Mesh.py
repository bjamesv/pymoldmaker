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
import math

from collada import material
from collada.geometry import Geometry
from collada.scene import MaterialNode
from collada.scene import GeometryNode
from collada.scene import Node
from collada.scene import Scene, MatrixTransform

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

    def ratio_mm_per_unit(self):
        """ returns the number of millimeters per COLLADA unit, in this Mesh

        per:
        http://pycollada.github.io/reference/generated/collada.Collada.html#collada.Collada.assetInfo
        http://pycollada.github.io/reference/generated/collada.asset.Asset.html#collada.asset.Asset

        >>> t = Mesh('test/cube.dae')
        >>> t.ratio_mm_per_unit()
        25.4
        """
        mm_per_meter = 1000
        meter_per_unit= self.mesh.assetInfo.unitmeter#SI meter per COLLADA unit
        return meter_per_unit * mm_per_meter

    def getFirstTransformOfFirstScene(self):
        """ returns 4x4 numpy array,representing transform of first scene

        >>> t = Mesh('test/cube.dae').getFirstTransformOfFirstScene()
        >>> t.matrix
        array([[1., 0., 0., 0.],
               [0., 1., 0., 0.],
               [0., 0., 1., 0.],
               [0., 0., 0., 1.]])
        >>> import numpy as np
        >>> np.set_printoptions(6)
        >>> t = Mesh('test/cube_flipped.dae').getFirstTransformOfFirstScene()
        >>> t.matrix
        array([[ 1.000000e+00,  0.000000e+00,  0.000000e+00, -4.373134e-01],
               [ 0.000000e+00, -1.000000e+00, -8.187895e-16, -1.090898e+01],
               [ 0.000000e+00,  8.187895e-16, -1.000000e+00,  4.659263e+00],
               [ 0.000000e+00,  0.000000e+00,  0.000000e+00,  1.000000e+00]],
              dtype=float32)
        """
        geometry_node_of_scene = self.visual_scene().nodes[0].children[0]
        if isinstance(geometry_node_of_scene, Node):
            return geometry_node_of_scene.transforms[0]
        #else, no transform: generate an Identity MatrixTransform
        matrix_4x4 = numpy.identity(4)
        return MatrixTransform(numpy.ravel( matrix_4x4))
        
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

    def dist_between( self, vert1, vert2):
        """ simple calculation of the distance between two vertices
        """
        xd = vert1[0] - vert2[0]
        yd = vert1[1] - vert2[1]
        zd = vert1[2] - vert2[2]
        xy_hypotenuse = math.sqrt( xd**xd + yd**yd)
        return math.sqrt( xy_hypotenuse**xy_hypotenuse + zd**zd)
            
    def sections(self, material_thickness_mm=6):
        """
        Returns a list of vertex coodinates of the form [ x1, y1,z1, x2, y2, z2
        , ...] representing a set of line segments, defining the geometry of a 
        slice of final plaster mould blank.
        ##TODO: deprecated - see ImportMesh.VectorMesh
        ##TODO: provide prototype implementation for the model slicing function
        """
        list_ret = []
        scale = 25.38 # TODO: is this correct? ..how is 4.23 * 6 units per derived?
        # define a rectangle for the left side
        corner_top_NW = self.get_corner( [-1,1,1])
        corner_bot_NW = self.get_corner( [-1,1,-1])
        list_ret.append( corner_top_NW)
        # list_ret.append ([50,50,-50])
        list_ret.append( corner_bot_NW)
        # list_ret.append ([50,50,50])
        # line segment2
        list_ret.append( corner_bot_NW)
        list_ret.append( self.get_corner( [-1,-1,-1]))
        # line segment3
        list_ret.append( self.get_corner( [-1,-1,-1]))
        list_ret.append( self.get_corner( [-1,-1,1]))
        # line segment4
        list_ret.append( self.get_corner( [-1,-1,1]))
        list_ret.append( self.get_corner( corner_top_NW))
        # insert another set of lines, shifted material_thickness_mm to the Right
        l2 = list( list_ret)
        #inspect = l2
        #print( type( inspect))
        #print( inspect)
        #print( dir( inspect))    
        for vert in l2:
            list_ret.append( [ vert[0]+(material_thickness_mm/scale), vert[1], vert[2] ])
        return list_ret
        
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
        # Add lines to COLLADA scene as a transformed Node /w geometry
        existing_scene_transforms = self.mesh.scene.nodes[0].children[0].transforms
        self.mesh.scene.nodes[0].children[0].transforms = []
        # build + add no
        mat_list = []
        geomnode = GeometryNode(geom, mat_list)
        node = Node("node0", children=[geomnode])
        #node.transforms.append(existing_scene_transforms[0])
        self.mesh.scene.nodes.append( node)
        pass

    def get_corner(self, list_directional):
        """ returns one of the six vertices of a rectangular poly that encloses
         the imported model. Which vertex is determined by parameter 
        list_directional
        list_directional a 3D coordinate tuple, representing the endpoint of a 
            directional vector extending from the origin. (eg: [-1,-1, ] 
            indicates the top-most, vertex in the south-west quadrant should be
            returned.
        """
        tri_set = self.primitives()[0]
        np_array  = tri_set.vertex
        x = []
        y = []
        z = []
        #Sort all vertex values
        # TODO: can numpy array be turned sideways? to eliminate need to
        for three_tuple in np_array:
            x.append( three_tuple[0])
            y.append( three_tuple[1])
            z.append( three_tuple[2])
        x.sort() 
        y.sort()
        z.sort()
        # determine vertex coordinates of a rectangular poly that encloses the 
        # imported model
        direction_x = list_directional[0]
        direction_y = list_directional[1]
        direction_z = list_directional[2]
        if direction_x > 0:
            # the smallest x coordinate value is not wanted,
            # reverse the list, so the largest vertex x-value is returned
            x.reverse()
        if direction_y > 0:
            # the smallest y coordinate value is not wanted,
            # reverse the list, so the largest vertex y-value is returned
            y.reverse()
        if direction_z > 0:
            # the smallest z coordinate value is not wanted,
            # reverse the list, so the largest vertex z-value is returned
            z.reverse()
        return [ x[0], y[0], z[0]]
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
