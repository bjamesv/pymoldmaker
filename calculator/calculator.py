#
"""
this file is a part of pymoldmaker

Copyright (C) 2015-2016 Brandon J. Van Vaerenbergh

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
from collections import OrderedDict
from copy import deepcopy
import math
from ast import literal_eval

import numpy

from calculator.Mesh import Mesh
from calculator.Part import Part
from calculator.PartSection import PartSection
from . import kerf

class Calculator(Mesh):
    # object representing COLLADA mesh of a positive for mold-making, 
    # supplemented with additional generated sets of lines representing the 
    # inventory of pieces of material (wood, plastic, etc.) needed to assemble
    # the mold-making positive

    material = { 'thickness_mm': 6, 'kerf_mm': 0.4}
    # dictionary of characteristics, possessed by the material the mold-making 
    # positive will be fabricated from

    bottom_parts = []
    # list representing x,y,z coordinate outlines of the pieces 
    # needed to assemble/build up the 'base'/bottom side of the molding 
    # positive

    depth_xy_corner_cut = 11. #TODO: lookup/detect actual depth
    """ depth in mm of the 45deg corner cuts that bisect the XY plane of the 
        flat positive being molded"""

    def __init__(self, mesh_path):
        """
        Construct Calculator for COLLADA mesh & part description files
        """
        Mesh.__init__(self, mesh_path)

        #fetch mold part descriptions
        # assume COLLADA mesh file has .dae extension
        extension_length = 4 # ".dae", ".DAE", etc.
        # .. and assume part descriptions .py file is in same directory
        directions_path = mesh_path[:-1*extension_length] + ".py"
        # fetch the Python 'parts' list from directions file
        try:
            self.directions = self.get_directions_from_module_file(directions_path)
        except FileNotFoundError:
            self.directions = [] #default: no directions

    def get_directions_from_module_file(self, directions_path):
        """
        Returns directions for mold subparts from referenced .py file

        .py module file is expected to define a single, anonymous list

        >>> from tempfile import NamedTemporaryFile
        >>> # test file with empty list
        >>> with NamedTemporaryFile() as directions:
        ...   directions.write("[]".encode('utf-8')) #prints '2' to stdout
        ...   directions.seek(0) #prints '0' to stdout
        ...   test_maker = Calculator('test/cube.dae')
        ...   test_maker.get_directions_from_module_file(directions.name)
        2
        0
        []
        >>> # test file with bad list
        >>> with NamedTemporaryFile() as directions:
        ...   directions.write("invalid = []".encode('utf-8'))
        ...   directions.seek(0)
        ...   test_maker = Calculator('test/cube.dae')
        ...   test_maker.get_directions_from_module_file(directions.name)
        Traceback (most recent call last):
           ...
        SyntaxError: invalid syntax
        """
        with open(directions_path) as parts_file:
            return literal_eval(parts_file.read())

    def save(self, file_path):
        """ save mesh and supplemental PartSections out to a COLLADA file.
        """
        print(self.parts_to_string()) #print human-readable output to console

        #TODO: eliminate below code duplicated in 'parts_to_string'
        # get Parts (... and their component PartSections)
        parts = self.generateParts()

        # convert mold-making PartSections into list of 3d-coord pairs("lines")
        list_line_segment_endpoints_xyz = list()
        for keyPartName in parts.keys():
            part = parts[keyPartName] #get part
            #collect the line segment endpoints, for this Part's sections
            list_line_segment_endpoints_xyz.extend(part.getAsLineSegments())

        # overlay a visualization of this part, onto original COLLADA model,and
        # save original mesh+ these lines to the specified file
        self.save_lines( file_path, list_line_segment_endpoints_xyz)
        return

    def parts_to_string(self):
        """
        Returns String, representing a human-readable cutlist for parts

        >>> from pprint import pprint
        >>> from tempfile import NamedTemporaryFile
        >>> import os
        >>> # prepare fake geometry & real part design files
        >>> with NamedTemporaryFile() as fake_mesh, NamedTemporaryFile() as part_design, open('test/cube.dae') as real_mesh:
        ...    # make part_design filename look related to fake_mesh filename
        ...    orig_fullpath = part_design.name
        ...    orig_dir = os.path.dirname(part_design.name)
        ...    mesh_filename = os.path.basename(fake_mesh.name)
        ...    new_filename = mesh_filename[:-4]+'.py'
        ...    new_fullpath = os.path.join(orig_dir, new_filename)
        ...    os.rename(part_design.name, new_fullpath)
        ...    part_design.name = new_fullpath
        ...    part_design.write('''# Simple Python module defining an anonymous list of mold parts
        ... [##List of parts (e.g.: friendly names + arguments for calculator.make_part)
        ...    ("Bottom", { "start_edge": ([-1,1,1],[-1,1,-1])
        ...                ,"end_edge": ([-1,-1,1],[-1,-1,-1])
        ...                ,"part_plane": (1,2) # oriented along Y Z plane
        ...                ,"shrink_edges": {"left", "right"}
        ...                ,"shrink_axis": 1 # shrink along Y axis
        ...                ,"thickness_direction_negative": False #model_center_along_negative_x_axis_from_part
        ...                })
        ...    ,("Left", { "start_edge": ([-1,1,1],[-1,1,-1])
        ...               ,"end_edge": ([1,1,1],[1,1,-1])
        ...               ,"part_plane": (0,2) #oriented along X Z plane
        ...               })
        ...    ,("Right-i", { "start_edge": ([-1,-1,1],[-1,-1,-1])
        ...                  ,"end_edge": ([1,-1,1],[1,-1,-1])
        ...                  ,"part_plane": (0,2) #oriented along X Z plane
        ...                  ,"shrink_edges": {'right': 145.8} #room for other Right parts
        ...                  ,"shrink_axis": 0 # shrink along X axis
        ...                  ,"thickness_direction_negative": False
        ...                  })
        ...    ,("Right-ii", { "start_edge": ([-1,-1,1],[-1,-1,-1])
        ...                   ,"end_edge": ([1,-1,1],[1,-1,-1])
        ...                   ,"part_plane": (0,2) #oriented along X Z plane
        ...                   ,"shrink_edges": {'left': 106.3, 'right': 129.4}#room for other Right parts
        ...                   ,"shrink_axis": 0 # shrink along X axis
        ...                   ,"thickness_direction_negative": False
        ...                   })
        ...    ,("Right-iii", { "start_edge": ([-1,-1,1],[-1,-1,-1])
        ...                    ,"end_edge": ([1,-1,1],[1,-1,-1])
        ...                    ,"part_plane": (0,2) #oriented along X Z plane
        ...                    ,"shrink_edges": {'left': 122.7, 'right': 123.5}#room for other Right parts
        ...                    ,"shrink_axis": 0 # shrink along X axis
        ...                    ,"thickness_direction_negative": False
        ...                    })
        ...    ,("Right-iv", { "start_edge": ([-1,-1,1],[-1,-1,-1])
        ...                   ,"end_edge": ([1,-1,1],[1,-1,-1])
        ...                   ,"part_plane": (0,2) #oriented along X Z plane
        ...                   ,"shrink_edges": {'left': 128.6, 'right': 50.7}#room for other Right parts
        ...                   ,"shrink_axis": 0 # shrink along X axis
        ...                   ,"thickness_direction_negative": False
        ...                   })
        ...    ,("Right-v", { "start_edge": ([-1,-1,1],[-1,-1,-1])
        ...                  ,"end_edge": ([1,-1,1],[1,-1,-1])
        ...                  ,"part_plane": (0,2) #oriented along X Z plane
        ...                  ,"shrink_edges": {'left': 50.7}#room for other Right parts
        ...                  ,"shrink_axis": 0 # shrink along X axis
        ...                  ,"thickness_direction_negative": False
        ...                  })
        ... ]'''.encode('utf-8'))
        ...    part_design.seek(0)
        ...    # prepare a random geometry file
        ...    fake_mesh.write(real_mesh.read().encode('utf-8'))
        ...    fake_mesh.seek(0)
        ...    # Test!
        ...    mold_maker = Calculator(fake_mesh.name)
        ...    pprint(mold_maker.parts_to_string())
        ...    # post-test, restore temp filename
        ...    os.rename(part_design.name, orig_fullpath)
        ...    part_design.name = orig_fullpath
        2680
        0
        5183
        0
        ('# Cutlist\\n'
         '## Bottom Part\\n'
         ' * (112.5 mm, 248.0 mm) section\\n'
         ' * (112.5 mm, 248.0 mm) section\\n'
         '## Left Part\\n'
         ' * (112.5 mm, 577.4 mm) section\\n'
         ' * (112.5 mm, 577.4 mm) section\\n'
         '## Right-i Part\\n'
         ' * (112.5 mm, 431.6 mm) section\\n'
         ' * (112.5 mm, 431.6 mm) section\\n'
         '## Right-ii Part\\n'
         ' * (112.5 mm, 341.7 mm) section\\n'
         ' * (112.5 mm, 341.7 mm) section\\n'
         '## Right-iii Part\\n'
         ' * (112.5 mm, 331.2 mm) section\\n'
         ' * (112.5 mm, 331.2 mm) section\\n'
         '## Right-iv Part\\n'
         ' * (112.5 mm, 398.1 mm) section\\n'
         ' * (112.5 mm, 398.1 mm) section\\n'
         '## Right-v Part\\n'
         ' * (112.5 mm, 526.7 mm) section\\n'
         ' * (112.5 mm, 526.7 mm) section')
        """
        # get Parts (... and their component PartSections)
        dictParts = self.generateParts()

        # convert mold-making PartSections into list of 3d-coord pairs("lines")
        list_line_segment_endpoints_xyz = list()
        # ..and while we convert, also print human-readable cutlist
        output = "# Cutlist"
        for keyPartName in dictParts.keys():
            part = dictParts[keyPartName] #get part, print its name
            output += '\n' + "## {} Part".format(keyPartName)
            for partSection in part: #print its component PartSections
                output += '\n' + " * {} section".format(partSection)
        return output

    def generateParts(self):
        """
        generates the inventory of Parts needed to assemble the mold positive.

        Returns: Dict of Parts needed,indexed by human-readable part name
        """
        ## generation strategy: start by determining size of bottom edge,then
        # side edges. Then, assuming the mold positive needs an exhaust on the
        # top edge, determine sizes for the three parts for the top edge.
        # Finally calculate dimensions of the mold positive's top face.
        parts_generator = ((name, self.make_part(**args)) #name/part tuples
                           for name,args
                           in self.directions)
        dictParts = OrderedDict(parts_generator)

        #TODO: generate top edge, and top face.
        return dictParts

    def isCompleteBottom(self):
        """ returns True if bottom_parts has been fully populated """
        return self.isCompleteXyPlane(self.bottom_parts)
        
    def isCompleteXyPlane( self, parts):
        """ returns true, if 'parts' is thick enough to make one of the 45deg 
        corner cuts, that bisect the XY plane, of the flat positive being 
        molded """
        # is combined thickness of parts sufficient?
        part_thickness = len(parts)*self.material['thickness_mm']
        if part_thickness >= self.depth_xy_corner_cut:
            return True
        return False

    def sectionsNeededToCompleteXyPlaneCut( self):
        """ returns an integer, representing how many full slices of material 
        are needed to make one of the 45deg corner cuts, that bisect the XY 
        plane of the flat positive being molded """
        sections = self.depth_xy_corner_cut/self.material['thickness_mm']
        return math.ceil( sections) # whole sections required

    def getMaterialHalfKerf(self):
        """
        Returns 1/2 the # mm of material the configured tool destroys, per cut
        """
        return 0.5 * self.material['kerf_mm']

    def make_part(self, start_edge, end_edge, part_plane, shrink_edges=[], shrink_axis=0
            ,thickness_direction_negative=True):
        """
        Returns a Part representing a full edge of the molding positive

        Keyword Arguments:
        start_edge  -- list of two unit-square tuples
        end_edge  -- list of two unit-square tuples
        part_plane  -- integer 2tuple, values 0-2, representing the pair of axis
          parallel to the plane part is majorly oriented along (TODO: should be
          derived from start_edge + end_edge but parameterizing is simple)
        shrink_edges -- collection of string keys representing which
         sides (top,right,bottom,left) of the part must be translated in
         toward the center to accommodate a butt joint with another part
         ,on that side. OR a dictionary of string keys with values
         specifying a number of mm part edge is to be translated.
        shrink_axis -- integer, values 0-2 representing axis part is to shrink
          along
        thickness_direction_negative  -- boolean, indicating if part should be
          grown more thick (to permit corner-cuts) negatively along axis or
          positively

        >>> vect = Calculator('test/cube_flipped.dae') #112.1 x 577.0mm face
        >>> start_edge, end_edge = ([-1,1,1],[-1,1,-1]), ([1,1,1],[1,1,-1])
        >>> part_plane = (0, 2) # X & Z-axis (perpendicular to Y)
        >>> left_side = vect.make_part(start_edge, end_edge, part_plane)
        >>> len(left_side.sections)
        2
        >>> #(112.1+.4/2+.4/2, 577.0+.4/2+.4/2)
        >>> [ round(x, 1) for x in left_side[0].dimensions_mm ] #FIXME: precision finer than 0.1mm should be possible
        [112.5, 577.4]
        >>> start_edge, end_edge =([-1,1,1],[-1,1,-1]), ([-1,-1,1],[-1,-1,-1])
        >>> part_plane = (1, 2) # Y & Z-axis (perpendicular to X-axis)
        >>> shrink_sides = {'left','right'}
        >>> shrink_axis = 1 # Y-axis
        >>> negative_x_is_toward_center = False
        >>> bottom = vect.make_part(start_edge, end_edge, part_plane, shrink_sides, shrink_axis, negative_x_is_toward_center)
        >>> len(bottom.sections)
        2
        >>> #(112.1+.4/2+.4/2, 271.6+.4/2+.4/2-2*6-2*6)
        >>> [ round(x, 1) for x in bottom[0].dimensions_mm ] #FIXME: precision finer than 0.1mm should be possible
        [112.5, 248.0]
        >>> shrink_sides = {'left': 'default', 'right': 70}
        >>> partial_bottom = vect.make_part(start_edge, end_edge, part_plane, shrink_sides, shrink_axis, negative_x_is_toward_center)
        >>> len(partial_bottom.sections)
        2
        >>> #(112.1+.4/2+.4/2, 271.6+.4/2+.4/2-2*6-70)
        >>> [ round(x, 1) for x in partial_bottom[0].dimensions_mm ] #FIXME: precision finer than 0.1mm should be possible
        [112.5, 190.0]
        >>> # Check a part, oriented along X/Y plane
        >>> start_edge, end_edge =([1,-1,-1],[-1,-1,-1]), ([1,1,-1],[-1,1,-1])
        >>> part_plane = (0, 1) # X & Y-axis (perpendicular to Z-axis)
        >>> shrink_sides = {'left'}
        >>> shrink_axis = 1 # Y-axis
        >>> negative_x_is_toward_center = False
        >>> bottom = vect.make_part(start_edge, end_edge, part_plane, shrink_sides, shrink_axis, negative_x_is_toward_center)
        >>> len(bottom.sections)
        2
        >>> #(557.0+.4/2+.4/2, 271.6+.4/2+.4/2-2*6)
        >>> [ round(x, 1) for x in bottom[0].dimensions_mm ] #FIXME: precision finer than 0.1mm should be possible
        [577.4, 260.0]
        """
        part_side = Part()
        # part is built up from one or more layers laminated together.
        list_section_poly_outline = [] # polygon, outlining the first layer of the part
        material_thickness_mm = self.material['thickness_mm']
        material_half_kerf_mm = self.getMaterialHalfKerf()
        sections_needed = self.sectionsNeededToCompleteXyPlaneCut()
        part_thickness_mm = sections_needed*material_thickness_mm
        # define a rectangle for the left side
        top_vert, bottom_vert = start_edge
        corner_top_NW = self.get_corner( top_vert)
        corner_bot_NW = self.get_corner( bottom_vert)
        scale = self.ratio_mm_per_unit() #TODO: use both the unit ratio AND geometry transform matrix
        adjust_direction = kerf.adjustment_direction(start_edge, end_edge, shrink_axis)
        # raise error, if any unrecognized shrink directions are specified
        supported_shrinks = {'left', 'right', 'bottom', 'top'}
        unsupported_shrink_keys = set(shrink_edges) - supported_shrinks
        if any(unsupported_shrink_keys):
            raise TypeError('Unsupported shrink edges: {}'.format(unsupported_shrink_keys))
        # shrink dimensions
        if 'left' in shrink_edges:
            plane = shrink_axis #FIXME: detect which plane the part is oriented on
            try:
                translate_distance_mm = float(shrink_edges['left'])
            except (TypeError, ValueError) as e: #default to thickness
                translate_distance_mm = part_thickness_mm
            corner_top_NW[plane] -= translate_distance_mm/scale * adjust_direction
            corner_bot_NW[plane] -= translate_distance_mm/scale * adjust_direction
        if 'bottom' in shrink_edges:
            plane = (set(part_plane)-{shrink_axis}).pop()
            adjust_direction = kerf.adjustment_direction(start_edge, end_edge, plane)
            try:
                translate_distance_mm = float(shrink_edges['bottom'])
            except (TypeError, ValueError) as e: #default to thickness
                translate_distance_mm = part_thickness_mm
            corner_bot_NW[plane] += translate_distance_mm/scale * adjust_direction
        if 'top' in shrink_edges:
            plane = (set(part_plane)-{shrink_axis}).pop()
            adjust_direction = kerf.adjustment_direction(start_edge, end_edge, plane)
            try:
                translate_distance_mm = float(shrink_edges['top'])
            except (TypeError, ValueError) as e: #default to thickness
                translate_distance_mm = part_thickness_mm
            corner_top_NW[plane] -= translate_distance_mm/scale * adjust_direction
        ''' adjust for half of the cutting tool's kerf (other half of kerf lies
            outside our cut line & for the part dimensions can be ignored)'''
        top_vert, bottom_vert = end_edge
        corner_bot_SW = self.get_corner( bottom_vert)
        corner_top_SW = self.get_corner( top_vert)

        part_corners = ((corner, axis) for corner in (corner_top_NW, corner_bot_NW) for axis in part_plane)
        adjust_directions = ((c,a, kerf.adjustment_axis_directions((corner_top_NW, corner_bot_NW), (corner_top_SW, corner_bot_SW), shrink_axis, part_plane, c))
                             for c,a in part_corners)

        for corner, axis, adjust_direction in adjust_directions:
            corner[axis] += material_half_kerf_mm/scale * adjust_direction[axis]
        list_section_poly_outline.append( corner_top_NW)
        list_section_poly_outline.append( corner_bot_NW)
        # compute final height of north edge #TODO:refactor this into PartSection
        length_north_edge = self.get_mm_dist( corner_bot_NW, corner_top_NW)

        # line segment2
        #make copies of vertici already used
        #FIXME: does not need to translate (also, translate the south edge out, to make room for that side's part)
        if 'right' in shrink_edges:
            plane = shrink_axis #FIXME: detect which plane the part is oriented on
            adjust_direction = kerf.adjustment_direction(start_edge, end_edge, shrink_axis)#TODO: refactor this terrible, duplicative code
            try: #TODO: eliminate below code duplication
                translate_distance_mm = float(shrink_edges['right'])
            except (TypeError, ValueError) as e: #default to thickness
                translate_distance_mm = part_thickness_mm
            corner_bot_SW[plane] += translate_distance_mm/scale * adjust_direction
            corner_top_SW[plane] += translate_distance_mm/scale * adjust_direction
        if 'bottom' in shrink_edges:
            plane = (set(part_plane)-{shrink_axis}).pop()
            adjust_direction = kerf.adjustment_direction(start_edge, end_edge, plane)
            try:
                translate_distance_mm = float(shrink_edges['bottom'])
            except (TypeError, ValueError) as e: #default to thickness
                translate_distance_mm = part_thickness_mm
            corner_bot_SW[plane] += translate_distance_mm/scale * adjust_direction
        if 'top' in shrink_edges:
            plane = (set(part_plane)-{shrink_axis}).pop()
            adjust_direction = kerf.adjustment_direction(start_edge, end_edge, plane)
            try:
                translate_distance_mm = float(shrink_edges['top'])
            except (TypeError, ValueError) as e: #default to thickness
                translate_distance_mm = part_thickness_mm
            corner_top_SW[plane] -= translate_distance_mm/scale * adjust_direction
        # adjust for 1/2 of the cutting tool's kerf width

        part_corners = ((corner, axis) for corner in (corner_top_SW, corner_bot_SW) for axis in part_plane)
        adjust_directions = ((c,a, kerf.adjustment_axis_directions((corner_top_NW, corner_bot_NW), (corner_top_SW, corner_bot_SW), shrink_axis, part_plane, c))
                             for c,a in part_corners)
        for corner, axis, adjust_direction in adjust_directions:
            corner[axis] += material_half_kerf_mm/scale * adjust_direction[axis]

        list_section_poly_outline.append( corner_bot_SW )
        # compute final length of west face
        length_west_face = self.get_mm_dist( corner_bot_NW, corner_bot_SW) #TODO:rename variable to West
        # save human-readable dimensions of the part section
        set_dimensions_mm_tuple = ( length_north_edge,length_west_face)

        # line segment3
        list_section_poly_outline.append( corner_top_SW)
        # line segment4
        # add verts to the list of sections to be cut
        section = PartSection(list_section_poly_outline, set_dimensions_mm_tuple)
        part_side.insertFrontSection( section)
        # build additional sections, until the list is thick enough
        grow_axis = ({0,1,2} - set(part_plane)).pop() # perpendicular axis
        while not self.isCompleteXyPlane( part_side.sections):
            # clone the xyz coords from the section we just created, into a new list
            set_dimensions_mm_new = deepcopy(part_side.sections[0].dimensions_mm)
            list_vertici_new = deepcopy(part_side.sections[0].vertici)
            section_new = PartSection(list_vertici_new, set_dimensions_mm_new)
            # now shift the set of lines material_thickness_mm to the Right
            for vert in section_new.vertici:
                if thickness_direction_negative:
                    vert[grow_axis] -= (material_thickness_mm/scale)
                else:
                    vert[grow_axis] += (material_thickness_mm/scale)
            part_side.insertFrontSection( section_new)
        return part_side

    def get_collada_unit_dist( self, list_coord_tuple1, list_coord_tuple2):
        """
        Computes distance between two 3d coords, measured in cartesian units

        e.g., distance between origin and the unit vector (1,0,0) is: 1 "unit"
        long
        >>> Calculator('test/cube.dae').get_collada_unit_dist( [1,0,0], [0,0,0])
        1.0
        """
        from scipy.spatial.distance import euclidean
        return euclidean( list_coord_tuple1, list_coord_tuple2)

    def get_unit_dist( self, mm_dist, list_coord_unit_vector):
        """
        Converts a distance in mm along a specific vector, into Collada units.

        >>> d = Calculator('test/cube_flipped.dae').get_unit_dist( 20, [1,0,0])
        >>> round( d, 4)
        22.8782
        """
        dist_vector = numpy.array(list_coord_unit_vector).dot( mm_dist)
        dist_vector_4x1 = dist_vector.tolist()[:]
        dist_vector_4x1.append( 1)#extend to 4x1, for scaling
        scale = self.getFirstTransformOfFirstScene().matrix
        dist_vector_scaled = scale.dot(dist_vector_4x1)[0:3]
        return self.get_collada_unit_dist( [0,0,0], dist_vector_scaled)

    def get_mm_dist( self, list_coord_tuple1, list_coord_tuple2):
        """
        Computes distance between two 3d coords, measured in millimeters.

        (coordinate units are converted to mm using our hardcoded scale factor.
        If we were really diligent, we could probably find the XML element from
        the loaded COLLADA file that defines the per-file scale.)
        >>> d = Calculator('test/cube.dae').get_mm_dist( [120/(0.0254*1000),0,0], [0,0,0])
        >>> round( d, 4)
        120.0
        """
        scale = self.ratio_mm_per_unit()
        # transform the 3d coords, as specified by the COLLADA file's scene.
        transform_matrix = self.getFirstTransformOfFirstScene().matrix

        list_coord_tuple1_4x1 = list_coord_tuple1[:]
        list_coord_tuple1_4x1.append(1)
        coord1 = transform_matrix.dot( list_coord_tuple1_4x1)
        list_coord_tuple2_4x1 = list_coord_tuple2[:]
        list_coord_tuple2_4x1.append(1)
        coord2 = transform_matrix.dot(list_coord_tuple2_4x1)
        length_collada_unit = self.get_collada_unit_dist( coord1[0:3], coord2[0:3])
        # now convert the COLLADA Unit length into mm
        return length_collada_unit * scale
