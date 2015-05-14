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

    def __init__( self, material_dict=None):
        """

        >>> p = PartSection()
        >>> p.material == None
        True
        >>> len(p.vertici)
        0
        """
        self.vertici = []
        self.material = material_dict
        self.single_plane = None
        self.dimensions_mm = None
        #False if not all vertex lie on a common plane

    def append( self, *part_sections):
        """
        append 'part_sections' list of COLLADA coord [x,y,z], to vertex list
        
        >>> p = PartSection()
        >>> p.append([0,0,1])
        >>> p.append([0,0,1])
        >>> p.vertici
        [[0, 0, 1], [0, 0, 1]]
        """
        for coord in part_sections:
            self.vertici.append( coord)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
