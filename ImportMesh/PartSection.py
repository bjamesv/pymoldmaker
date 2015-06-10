#!/usr/bin/python3
from ImportMesh.Part import Part
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

class PartSection:
    """
    object representing an individual cut piece for use in mold construction.

    """

    def __init__( self, list_vertex, set_dimension_mm_tuple, material_dict=None):
        """
        create a new PartSection

        Keyword arguments:
        list_vertex -- collection of [x,y,z] coordinates representing a
            polygonal line.
        material_dict -- collection of material properties

        >>> l = [[0,0,0],[0,1,0,],[1,1,0],[1,0,0]]
        >>> p = PartSection(l,())
        >>> p.material == None
        True
        >>> len(p.vertici)
        8
        >>> l = [[0,0,1]]
        >>> p = PartSection( l, ())
        >>> p.vertici
        [[0, 0, 1], [0, 0, 1]]
        """
        self.vertici = []
        self.material = material_dict
        self.dimensions_mm = set_dimension_mm_tuple
        # convert the list of poly vertici, into pairs of vertici representing
        # line segments
        for i, coord in enumerate(list_vertex):
            list_next_coord = None
            #line segment termintates at the next coord (unless end
            # has been reached, then next coord is the first one provided )
            if i >= len(list_vertex)-2:
                list_next_coord = list_vertex[0]
            else:
                list_next_coord = list_vertex[i+1]
            self.vertici.append(coord[:])
            self.vertici.append(list_next_coord[:])

    def __str__( self):
        """ returns a simple human-readable representation of this PartSection.

        >>> l = [[0,0,1],[0,0,1]]
        >>> p = PartSection( l, (0,0))
        >>> str(p)
        '(0.00 mm, 0.00 mm)'
        """
        return '({0:.2f} mm, {0:.2f} mm)'.format(self.dimensions_mm[0], self.dimensions_mm[1])

if __name__ == "__main__":
    import doctest
    doctest.testmod()
