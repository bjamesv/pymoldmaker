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
from calculator.calculator import Calculator

def test_top_part_i_of_iii():
    """
    Check dimensions of Part representing leftmost portion of mold top

    >>> test_args = { "start_edge": ([1,1,1],[1,1,-1])
    ...              ,"end_edge": ([1,-1,1],[1,-1,-1])
    ...              ,"part_plane": (1,2) #oriented along Y Z plane
    ...              ,"shrink_edges": {"left": 'joint-default', "right": 104+115.4+18.7}#room for other Top parts
    ...              ,"shrink_axis": 1 # shrink along Y axis
    ...              }
    >>> vect = Calculator('test/cube_flipped.dae') #112.1 x 271.6mm face
    >>> part = vect.make_part(**test_args)
    >>> len(part.sections)
    2
    >>> #(112.1+.4/2+.4/2, 271.6+.4/2+.4/2-2*6-104-115.4-18.7)
    >>> [ round(x, 1) for x in part[0].dimensions_mm ] #FIXME: precision finer than 0.1mm should be possible
    [112.5, 21.9]
    """
    pass

def test_bottom_part():
    """
    Check dimensions of Part representing bottom edge of mold making positive

    >>> test_args = { "start_edge": ([-1,1,1],[-1,1,-1])
    ...            ,"end_edge": ([-1,-1,1],[-1,-1,-1])
    ...            ,"part_plane": (1,2) # oriented along Y Z plane
    ...            ,"shrink_edges": {"left", "right"}
    ...            ,"shrink_axis": 1 # shrink along Y axis
    ...            ,"thickness_direction_negative": False #model_center_along_negative_x_axis_from_part
    ...            }
    >>> vect = Calculator('test/cube_flipped.dae') #112.1 x 271.6mm face
    >>> part = vect.make_part(**test_args)
    >>> len(part.sections)
    2
    >>> #(112.1+.4/2+.4/2, 271.6+.4/2+.4/2-2*6-2*6)
    >>> [ round(x, 1) for x in part[0].dimensions_mm ] #FIXME: precision finer than 0.1mm should be possible
    [112.5, 248.0]
    """
    pass
