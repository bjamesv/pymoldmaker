#
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

from ImportMesh import Mesh
from ImportMesh.Part import Part
from ImportMesh.PartSection import PartSection
from copy import deepcopy
import math

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
    
    scale_collada = 25.38 # TODO: is this correct? ..how is 4.23 * 6 units per derived?

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

    
    def bottomSections(self):
        """
        Returns a list of vertex coodinates of the form [ x1, y1,z1, x2, y2, z2
        , ...] representing a set of line segments, defining the geometry of a 
        slice of final plaster mould blank.
        ##TODO: provide prototype implementation for the model slicing function
        """
        bottom_part = Part()
        section = PartSection()
        material_thickness_mm = self.material['thickness_mm']
        material_half_kerf_mm = 0.5 * self.material['kerf_mm']
        sections_needed = self.sectionsNeededToCompleteXyPlaneCut()
        part_thickness_mm = sections_needed*material_thickness_mm
        # define a rectangle for the left side
        corner_top_NW = self.get_corner( [-1,1,1])
        corner_bot_NW = self.get_corner( [-1,1,-1])
        # (shrink from the west side, to make room for the part on that side.)
        scale = self.scale_collada
        corner_top_NW[1] -= part_thickness_mm/scale
        corner_bot_NW[1] -= part_thickness_mm/scale
        ''' adjust for half of the cutting tool's kerf (other half of kerf lies
            outside our cut line & for the part dimensions can be ignored)'''
        corner_top_NW[1] += material_half_kerf_mm/scale
        corner_bot_NW[1] += material_half_kerf_mm/scale
        # (and make part taller, also to account for 1/2 kerf width)
        corner_top_NW[2] += material_half_kerf_mm/scale
        corner_bot_NW[2] -= material_half_kerf_mm/scale
        section.append( corner_top_NW)
        section.append( corner_bot_NW)
        # compute final height of west edge
        length_west_edge = self.get_mm_dist( corner_bot_NW, corner_top_NW)

        # line segment2
        section.append( corner_bot_NW[:]) #make copies of vertici already used
        # (also, translate the east side in, to make room for that side's part)
        corner_bot_NE = self.get_corner( [-1,-1,-1])
        corner_top_NE = self.get_corner( [-1,-1,1])
        corner_bot_NE[1] += part_thickness_mm/scale
        corner_top_NE[1] += part_thickness_mm/scale
        # adjust for 1/2 of the cutting tool's kerf width
        corner_bot_NE[1] -= material_half_kerf_mm/scale
        corner_top_NE[1] -= material_half_kerf_mm/scale
        # (again, make part taller to account for the cut's 1/2 kerf width)
        corner_top_NE[2] += material_half_kerf_mm/scale
        corner_bot_NE[2] -= material_half_kerf_mm/scale
        section.append( corner_bot_NE )
        # compute final length of north edge
        length_north_edge = self.get_mm_dist( corner_bot_NW, corner_bot_NE) 
        # save human-readable dimensions of the part section
        section.dimensions_mm = ( length_west_edge,length_north_edge)

        # line segment3
        section.append( corner_bot_NE[:])
        section.append( corner_top_NE)
        # line segment4
        section.append( corner_top_NE[:])
        section.append( corner_top_NW[:])
        # add verts to the list of sections to be cut
        bottom_part.insertFrontSection( section)
        # build additional sections, until the list is thick enough
        while not self.isCompleteXyPlane( bottom_part.sections):
            # clone the xyz coords from the section we just created, into a new list
            section_new = PartSection()
            section_new.dimensions_mm = bottom_part.sections[0].dimensions_mm
            section_new.vertici = deepcopy(bottom_part.sections[0].vertici)
            # now shift the set of lines material_thickness_mm to the Right
            for vert in section_new.vertici:
                vert[0] += (material_thickness_mm/scale)
            bottom_part.insertFrontSection( section_new)
        return bottom_part.sections

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

    def get_mm_dist( self, list_coord_tuple1, list_coord_tuple2):
        """
        Computes distance between two 3d coords, measured in millimeters.

        (coordinate units are converted to mm using our hardcoded scale factor.
        If we were really diligent, we could probably find the XML element from
        the loaded COLLADA file that defines the per-file scale.)
        >>> d = VectorMesh('test/cube.dae').get_mm_dist( [120/(4.23*6),0,0], [0,0,0])
        >>> round( d, 4)
        120.0
        """
        scale = self.scale_collada
        length_collada_unit = self.get_collada_unit_dist( list_coord_tuple1, list_coord_tuple2)
        return length_collada_unit*scale
