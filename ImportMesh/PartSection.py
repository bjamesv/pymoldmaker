#!/usr/bin/python3
from ImportMesh import Part
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

        >>> p = Part()
        >>> p.material == None
        True
        >>> len(p.sections)
        0
        """
        self.sections = []
        self.material = material_dict

    def addSections( self, part_sections):
        """
        
        >>> p = Part()
        >>> p.addSections([0,0,1])
        >>> p.addSections([0,0,1])
        >>> p.sections
        [[0, 0, 1], [0, 0, 1]]
        """
        self.sections.append( part_sections)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
