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

from ImportMesh import Mesh
from ImportMesh.Part import Part
from ImportMesh.PartSection import PartSection

from . import kerf

from copy import deepcopy
import math
import numpy

class VectorMesh ( Mesh ):
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

    def save(self, file_path):
        """ save mesh and supplemental PartSections out to a COLLADA file.
        """
        # get Parts (... and their component PartSections)
        dictParts = self.generateParts()

        # convert mold-making PartSections into list of 3d-coord pairs("lines")
        list_line_segment_endpoints_xyz = list()
        # ..and while we convert, also print human-readable cutlist
        print ("# Cutlist")
        for keyPartName in dictParts.keys():
            part = dictParts[keyPartName] #get part, print its name        
            print ("## {} Part".format(keyPartName))
            for partSection in part: #print its component PartSections
                print (" * {} section".format(partSection))
            #collect the line segment endpoints, for this Part's sections
            list_line_segment_endpoints_xyz.extend( part.getAsLineSegments())

        # overlay a visualization of this part, onto original COLLADA model,and
        # save original mesh+ these lines to the specified file
        self.save_lines( file_path, list_line_segment_endpoints_xyz)
        return

    def generateParts(self):
        """
        generates the inventory of Parts needed to assemble the mold positive.

        Returns: Dict of Parts needed,indexed by human-readable part name
        """
        ## generation strategy: start by determining size of bottom edge,then
        # side edges. Then, assuming the mold positive needs an exhaust on the
        # top edge, determine sizes for the three parts for the top edge.
        # Finally calculate dimensions of the mold positive's top face.
        dictParts = {'Bottom': self.bottomPart()
                    ,'Left'  : self.make_part( ([-1,1,1],[-1,1,-1]), ([1,1,1],[1,1,-1]), (0,2))
                    }

        #TODO: generate side edges,top edge, and top face.
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

    def bottomPart(self):
        """
        Returns a Part representing the bottom edge of the mold making positive

        >>> vect = VectorMesh( 'test/cube_flipped.dae') #112.1 x 271.6mm face
        >>> part = vect.bottomPart()
        >>> len(part.sections)
        2
        >>> #(112.1+.4/2+.4/2, 271.6+.4/2+.4/2-2*6-2*6)
        >>> [ round(x, 1) for x in part[0].dimensions_mm ] #FIXME: precision finer than 0.1mm should be possible
        [112.5, 248.0]
        """
        start_edge, end_edge = ([-1,1,1],[-1,1,-1]), ([-1,-1,1],[-1,-1,-1])
        plane = (1,2) # oriented along Y Z plane
        shrink_edges = ['left','right']
        shrink_axis = 1 # shrink along Y axis
        model_center_along_negative_x_axis_from_part = False #it's along positive X axis
        return self.make_part( start_edge, end_edge, plane, shrink_edges, shrink_axis
                              ,model_center_along_negative_x_axis_from_part)

    def getMaterialHalfKerf(self):
        """
        Returns 1/2 the # mm of material the configured tool destroys, per cut
        """
        return 0.5 * self.material['kerf_mm']

    def make_part(self, start_edge, end_edge, part_plane, shrink_sides=[], shrink_axis=0
            ,thickness_direction_negative=True):
        """
        Returns a Part representing a full edge of the molding positive

        Keyword Arguments:
        start_edge  -- list of two unit-square tuples
        end_edge  -- list of two unit-square tuples
        part_plane  -- integer 2tuple, values 0-2, representing the pair of axis
          parallel to the plane part is majorly oriented along (TODO: should be
          derived from start_edge + end_edge but parameterizing is simple)
        shrink_sides -- list of strings representing which sides (top,right,
            bottom,left) of the part must be translated in toward the center to
            accommodate a butt joint with another part, on that side.
        shrink_axis -- integer, values 0-2 representing axis part is to shrink
          along
        thickness_direction_negative  -- boolean, indicating if part should be
          grown more thick (to permit corner-cuts) negatively along axis or
          positively

        >>> vect = VectorMesh( 'test/cube_flipped.dae') #112.1 x 577.0mm face
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
        >>> shrink_sides = ['left','right']
        >>> shrink_axis = 1 # Y-axis
        >>> negative_x_is_toward_center = False
        >>> bottom = vect.make_part(start_edge, end_edge, part_plane, shrink_sides, shrink_axis, negative_x_is_toward_center)
        >>> len(bottom.sections)
        2
        >>> #(112.1+.4/2+.4/2, 271.6+.4/2+.4/2-2*6-2*6)
        >>> [ round(x, 1) for x in bottom[0].dimensions_mm ] #FIXME: precision finer than 0.1mm should be possible
        [112.5, 248.0]
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
        if 'left' in shrink_sides:
            plane = shrink_axis #FIXME: detect which plane the part is oriented on
            corner_top_NW[plane] -= part_thickness_mm/scale
            corner_bot_NW[plane] -= part_thickness_mm/scale
        ''' adjust for half of the cutting tool's kerf (other half of kerf lies
            outside our cut line & for the part dimensions can be ignored)'''
        adjust_direction = kerf.adjustment_direction(start_edge, end_edge, shrink_axis)
        corner_top_NW[part_plane[0]] += material_half_kerf_mm/scale * adjust_direction
        corner_bot_NW[part_plane[0]] += material_half_kerf_mm/scale * adjust_direction
        # (and make part taller, also to account for 1/2 kerf width)
        corner_top_NW[part_plane[1]] += material_half_kerf_mm/scale
        corner_bot_NW[part_plane[1]] -= material_half_kerf_mm/scale
        list_section_poly_outline.append( corner_top_NW)
        list_section_poly_outline.append( corner_bot_NW)
        # compute final height of north edge #TODO:refactor this into PartSection
        length_north_edge = self.get_mm_dist( corner_bot_NW, corner_top_NW)

        # line segment2
        #make copies of vertici already used
        #FIXME: does not need to translate (also, translate the south edge out, to make room for that side's part)
        top_vert, bottom_vert = end_edge
        corner_bot_SW = self.get_corner( bottom_vert)
        corner_top_SW = self.get_corner( top_vert)
        if 'right' in shrink_sides:
            plane = shrink_axis #FIXME: detect which plane the part is oriented on
            corner_bot_SW[plane] += part_thickness_mm/scale
            corner_top_SW[plane] += part_thickness_mm/scale
        # adjust for 1/2 of the cutting tool's kerf width
        adjust_direction = kerf.adjustment_direction(end_edge, start_edge, shrink_axis)
        corner_bot_SW[part_plane[0]] += material_half_kerf_mm/scale * adjust_direction
        corner_top_SW[part_plane[0]] += material_half_kerf_mm/scale * adjust_direction
        # (again, make part taller to account for the cut's 1/2 kerf width)
        corner_top_SW[part_plane[1]] += material_half_kerf_mm/scale
        corner_bot_SW[part_plane[1]] -= material_half_kerf_mm/scale
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
        >>> VectorMesh('test/cube.dae').get_collada_unit_dist( [1,0,0], [0,0,0])
        1.0
        """
        from scipy.spatial.distance import euclidean
        return euclidean( list_coord_tuple1, list_coord_tuple2)

    def get_unit_dist( self, mm_dist, list_coord_unit_vector):
        """
        Converts a distance in mm along a specific vector, into Collada units.

        >>> d = VectorMesh('test/cube_flipped.dae').get_unit_dist( 20, [1,0,0])
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
        >>> d = VectorMesh('test/cube.dae').get_mm_dist( [120/(0.0254*1000),0,0], [0,0,0])
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
