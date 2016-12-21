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

class Part:
    """
    object representing one sub-assembly of the final mold.

    If uniform raw material used for mold construction is sufficiently thick, 
    Part will consist of a single cut PartSection. For thin construction 
    materials, multiple PartSections will compose the Part - so they may be cut
     and stacked/assembled to form a final mold part.

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
        """list of vertex coodinates of the form [ x1, y1,z1, x2, y2, z2
        , ...] representing a set of line segments, defining the geometry of
        the plaster molding blank's bottom section.
        """
        self.material = material_dict 

    
    def __getitem__(self, key):
        return self.sections[key]

    def insertFrontSection( self, part_section):
        """
        insert new PartSection into 0th index of the Part section list.        
        
        >>> p = Part()
        >>> p.insertFrontSection([0,0,1])
        >>> p.insertFrontSection([0,1,1])
        >>> p.sections
        [[0, 1, 1], [0, 0, 1]]
        """
        self.sections.insert(0, part_section)

    def getAsLineSegments( self):
        """
        returns a list of XYZ coord pairs, representing the part.

        >>> p = Part()
        >>> from calculator.PartSection import PartSection
        >>> l1 = [[0,0,0],[0,0,1]]
        >>> l2 = [[0,4,0],[0,4,1]]
        >>> p.insertFrontSection(PartSection(l1,(1,0)))
        >>> p.insertFrontSection(PartSection(l2,(1,0)))
        >>> p.getAsLineSegments()
        [[0, 4, 0], [0, 4, 1], [0, 4, 1], [0, 4, 0], [0, 0, 0], [0, 0, 1], [0, 0, 1], [0, 0, 0]]
        """
        listReturn = list()
        for section in self.sections:
            listReturn.extend( section.vertici[:])
        return listReturn

if __name__ == "__main__":
    import doctest
    doctest.testmod()
