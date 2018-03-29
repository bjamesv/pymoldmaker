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
    ...              ,"shrink_edges": {"left": 'joint-default', "right": 104+115.4+18.7#room for other Top parts
    ...                               ,"bottom": 'joint-default'}#room for Back part
    ...              ,"shrink_axis": 1 # shrink along Y axis
    ...              }
    >>> vect = Calculator('test/cube_flipped.dae') #112.1 x 271.6mm face
    >>> part = vect.make_part(**test_args)
    >>> len(part.sections)
    2
    >>> #(112.1+.4/2+.4/2-2*6, 271.6+.4/2+.4/2-2*6-104-115.4-18.7)
    >>> [ round(x, 1) for x in part[0].dimensions_mm ] #FIXME: precision finer than 0.1mm should be possible
    [100.5, 21.9]
    """
    pass

def test_top_part_ii_of_iii():
    """
    Check dimensions of Part representing center portion of mold top

    >>> test_args = { "start_edge": ([1,1,1],[1,1,-1])
    ...              ,"end_edge": ([1,-1,1],[1,-1,-1])
    ...              ,"part_plane": (1,2) #oriented along Y Z plane
    ...              ,"shrink_edges": {"left": 18.7+130.2, "right": 115.4+18.7}#room for other Top parts
    ...              ,"shrink_axis": 1 # shrink along Y axis
    ...              }
    >>> vect = Calculator('test/cube_flipped.dae') #112.1 x 271.6mm face
    >>> part = vect.make_part(**test_args)
    >>> len(part.sections)
    2
    >>> #[ 112.1+.4/2+.4/2, (271.6-115.4-18.7*2-130.2)+(+.4/2+.4/2)
    >>> #FIXME: yields a 11.4 wide part instead of 11.0 because test
    >>> # part is less wide than the total left+right shrink distance.
    >>> # After exploratory testing, confident 11.4 (not "-11") is Ok
    >>> [ round(x, 1) for x in part[0].dimensions_mm ] #FIXME: precision finer than 0.1mm should be possible
    [112.5, 11.4]
    """
    pass

def test_top_part_iii_of_iii():
    """
    Check dimensions of Part representing rightmost portion of mold top

    >>> test_args = { "start_edge": ([1,1,1],[1,1,-1])
    ...              ,"end_edge": ([1,-1,1],[1,-1,-1])
    ...              ,"part_plane": (1,2) #oriented along Y Z plane
    ...              ,"shrink_edges": {"left": 18.7+130.2+104, "right": 'joint-default' #room for other Top parts
    ...                               ,"bottom": 'joint-default'}#room for Back part
    ...              ,"shrink_axis": 1 # shrink along Y axis
    ...              }
    >>> vect = Calculator('test/cube_flipped.dae') #112.1 x 271.6mm face
    >>> part = vect.make_part(**test_args)
    >>> len(part.sections)
    2
    >>> #(112.1+.4/2+.4/2-2*6, 271.6+.4/2+.4/2-2*6-130.2-18.7-104)
    >>> [ round(x, 1) for x in part[0].dimensions_mm ] #FIXME: precision finer than 0.1mm should be possible
    [100.5, 7.1]
    """
    pass

def test_bottom_part():
    """
    Check dimensions of Part representing bottom edge of mold making positive

    >>> test_args = { "start_edge": ([-1,1,1],[-1,1,-1])
    ...            ,"end_edge": ([-1,-1,1],[-1,-1,-1])
    ...            ,"part_plane": (1,2) # oriented along Y Z plane
    ...            ,"shrink_edges": {"left": 'joint-default', "right": 'joint-default'
    ...                              ,"bottom": 'joint-default'} #room for Back part
    ...            ,"shrink_axis": 1 # shrink along Y axis
    ...            ,"thickness_direction_negative": False #model_center_along_negative_x_axis_from_part
    ...            }
    >>> vect = Calculator('test/cube_flipped.dae') #112.1 x 271.6mm face
    >>> part = vect.make_part(**test_args)
    >>> len(part.sections)
    2
    >>> #(112.1+.4/2+.4/2, 271.6+.4/2+.4/2-2*6-2*6)
    >>> [ round(x, 1) for x in part[0].dimensions_mm ] #FIXME: precision finer than 0.1mm should be possible
    [100.5, 248.0]
    """
    pass

def test_back_part_i_of_v():
    """
    Check dimensions of Part representing leftmost back of mold making positive

    >>> test_args = { "start_edge": ([1,-1,-1],[-1,-1,-1])
    ...              ,"end_edge": ([1,1,-1],[-1,1,-1])
    ...              ,"part_plane": (0,1) #oriented along X Y plane
    ...              ,"shrink_edges": {"right": 104+115.4+18.7}#room for other Back parts
    ...              ,"shrink_axis":1 #Y axis
    ...              ,"thickness_direction_negative": False
    ...              }
    >>> vect = Calculator('test/cube_flipped.dae') #577mm x 271.6mm face
    >>> part = vect.make_part(**test_args)
    >>> len(part.sections)
    2
    >>> [ round(x, 1) for x in part[0].dimensions_mm ] #FIXME: precision finer than 0.1mm should be possible
    [577.4, 33.9]
    """
    pass

def test_back_part_ii_of_v():
    """
    Check dimensions of Part representing center back of mold making positive

    >>> test_args = { "start_edge": ([1,-1,-1],[-1,-1,-1])
    ...              ,"end_edge": ([1,1,-1],[-1,1,-1])
    ...              ,"part_plane": (0,1) #oriented along X Y plane
    ...              ,"shrink_edges": {"left": 115.4+18.7, "right": 18.7+130.2#room for other Back parts
    ...                                ,"top": 'joint-default'}#room for Top part
    ...              ,"shrink_axis":1 #Y axis
    ...              ,"thickness_direction_negative": False
    ...              }
    >>> vect = Calculator('test/cube_flipped.dae') #112.1 x 271.6mm face
    >>> part = vect.make_part(**test_args)
    >>> len(part.sections)
    2
    >>> [ round(x, 1) for x in part[0].dimensions_mm ] #FIXME: precision finer than 0.1mm should be possible
    [565.4, 11.4]
    """
    pass

def test_back_part_iii_of_v():
    """
    Check dimensions of Part representing rightmost back of mold making positive

    >>> test_args = { "start_edge": ([1,-1,-1],[-1,-1,-1])
    ...              ,"end_edge": ([1,1,-1],[-1,1,-1])
    ...              ,"part_plane": (0,1) #oriented along X Y plane
    ...              ,"shrink_edges": {"right": 104+130.2+18.7} #room for other Back parts
    ...              ,"shrink_axis": 1 #Y axis
    ...              ,"thickness_direction_negative": False
    ...              ,"subtract_parts": [{ "start_edge": ([1,-1,-1],[-1,-1,-1])
    ...                                   ,"end_edge": ([1,1,-1],[-1,1,-1])
    ...                                   ,"part_plane": (0,1) #oriented along X Y plane
    ...                                   ,"shrink_edges": {"right": 380.8
    ...                                   ,"top": 50.6
    ...                               ,"bottom": 128.6}
    ...                               ,"shrink_axis": 1 #Y axis
    ...              ,"thickness_direction_negative": False
    ...              }
    ...                                 ]
    ...              }
    >>> vect = Calculator('test/cube_flipped.dae') #577.0 x 271.6mm face
    >>> part = vect.make_part(**test_args)
    >>> len(part.sections)
    2
    >>> #part width: 271.6-(104+130.2+18.7)+.4/2+.4/2
    >>> [ round(x, 1) for x in part[0].dimensions_mm ] #FIXME: precision finer than 0.1mm should be possible
    [577.4, 19.1]
    >>> #hole in part: 398.2mm x 109.2mm
    >>> [round(x, 1) for x in part.voids[0][0].dimensions_mm] #FIXME: precision finer than 0.1mm should be possible
    [398.2, 109.2]
    """
    pass

def test_back_part_iv_of_v():
    """
    Check dimensions of Part representing a void in right side of rightmost back part of mold making positive

    >>> test_args = { "start_edge": ([1,-1,-1],[-1,-1,-1])
    ...              ,"end_edge": ([1,1,-1],[-1,1,-1])
    ...              ,"part_plane": (0,1) #oriented along X Y plane
    ...              ,"shrink_edges": {"right": 380.8
    ...                               ,"top": 50.6
    ...                               ,"bottom": 128.6}
    ...              ,"shrink_axis": 1 #Y axis
    ...              ,"thickness_direction_negative": False
    ...              }
    >>> vect = Calculator('test/cube_flipped.dae') #577.0 x 271.6mm face
    >>> part = vect.make_part(**test_args)
    >>> len(part.sections)
    2
    >>> #part height: 577-(252-(201.4-128.6)-50.6)-50.6+.4
    >>> #part width: 271.6-(387-6.2)+.4
    >>> [ round(x, 1) for x in part[0].dimensions_mm ] #FIXME: precision finer than 0.1mm should be possible
    [398.2, 109.2]
    """
    pass

def test_back_part_v_of_v():
    """
    Check dimensions of Part representing a second void for ethernet port on right side of rightmost back part of mold making positive

    >>> test_args = {"start_edge": ([1,-1,-1],[-1,-1,-1])
    ...              ,"end_edge": ([1,1,-1],[-1,1,-1])
    ...              ,"part_plane": (0,1) #oriented along X Y plane
    ...              ,"shrink_edges": {"right": 378.7
    ...                               ,"top": 129.4
    ...                               ,"bottom": 106.3}
    ...              ,"shrink_axis": 1 #Y axis
    ...              ,"thickness_direction_negative": False
    ...              }
    >>> vect = Calculator('test/cube_flipped.dae') #577.0 x 271.6mm face
    >>> part = vect.make_part(**test_args)
    >>> len(part.sections)
    2
    >>> #part height: 577-(252-129.4-106.3)+.4
    >>> #part width: 271.6-(387-8.3)+.4
    >>> [ round(x, 1) for x in part[0].dimensions_mm ] #FIXME: precision finer than 0.1mm should be possible
    [341.7, 107.1]
    """
    pass

def test_left():
    """
    Check dimensions of Part representing lleft edge

    >>> test_args = { "start_edge": ([-1,1,1],[-1,1,-1])
    ...              ,"end_edge": ([1,1,1],[1,1,-1])
    ...              ,"part_plane": (0,2) #oriented along X Z plane
    ...              ,"shrink_edges": {"bottom": 'joint-default'}#room for Back part
    ...              ,"shrink_axis": 0 #X axis for left/right
    ...             }
    >>> vect = Calculator('test/cube_flipped.dae') #112.1 x 271.6mm face
    >>> right_side = vect.make_part(**test_args)
    >>> len(right_side.sections)
    2
    >>> #(112.1+.4/2+.4/2-2*6, 577.0+.4/2+.4/2)
    >>> [ round(x, 1) for x in right_side[0].dimensions_mm ] #FIXME: precision finer than 0.1mm should be possible
    [100.5, 577.4]
    """
    pass

def test_right_part_i_of_v():
    """
    Check dimensions of Part representing bottommost portion of right edge

    >>> test_args = { "start_edge": ([-1,-1,1],[-1,-1,-1])
    ...              ,"end_edge": ([1,-1,1],[1,-1,-1])
    ...              ,"part_plane": (0,2) #oriented along X Z plane
    ...              ,"shrink_edges": {'right': 145.8 #room for other Right parts
    ...                               ,'bottom': 'joint-default'}#room for Bottom part
    ...              ,"shrink_axis": 0 # shrink along X axis
    ...              ,"thickness_direction_negative": False
    ...              }
    >>> vect = Calculator('test/cube_flipped.dae') #112.1 x 271.6mm face
    >>> right_side = vect.make_part(**test_args)
    >>> len(right_side.sections)
    2
    >>> #(112.1+.4/2+.4/2-6*2, 577.0+.4/2+.4/2-145.8)
    >>> [ round(x, 1) for x in right_side[0].dimensions_mm ] #FIXME: precision finer than 0.1mm should be possible
    [100.5, 431.6]
    """
    pass

def test_right_part_ii_of_v():
    """
    Check dimensions of Part representing next-to-bottommost portion of right edge

    >>> test_args = { "start_edge": ([-1,-1,1],[-1,-1,-1])
    ...              ,"end_edge": ([1,-1,1],[1,-1,-1])
    ...              ,"part_plane": (0,2) #oriented along X Z plane
    ...              ,"shrink_edges": {'left': 106.3, 'right': 129.4}#room for other Right parts
    ...              ,"shrink_axis": 0 # shrink along X axis
    ...              ,"thickness_direction_negative": False
    ...              }
    >>> vect = Calculator( 'test/cube_flipped.dae') #112.1 x 271.6mm face
    >>> right_side = vect.make_part(**test_args)
    >>> len(right_side.sections)
    2
    >>> #(112.1+.4/2+.4/2, 577.0+.4/2+.4/2-106.3-129.4)
    >>> [ round(x, 1) for x in right_side[0].dimensions_mm ] #FIXME: precision finer than 0.1mm should be possible
    [112.5, 341.7]
    """
    pass

def test_right_part_iii_of_v():
    """
    Check dimensions of Part representing center portion of right edge

    >>> test_args = { "start_edge": ([-1,-1,1],[-1,-1,-1])
    ...              ,"end_edge": ([1,-1,1],[1,-1,-1])
    ...              ,"part_plane": (0,2) #oriented along X Z plane
    ...              ,"shrink_edges": {'left': 122.7, 'right': 123.5 #room for other Right parts
    ...                               ,'bottom': 'joint-default'}#room for Bottom part
    ...              ,"shrink_axis": 0 # shrink along X axis
    ...              ,"thickness_direction_negative": False
    ...              }
    >>> vect = Calculator('test/cube_flipped.dae') #112.1 x 271.6mm face
    >>> right_side = vect.make_part(**test_args)
    >>> len(right_side.sections)
    2
    >>> #(112.1+.4/2+.4/2-6*2, 577.0+.4/2+.4/2-122.7-123.5)
    >>> [ round(x, 1) for x in right_side[0].dimensions_mm ] #FIXME: precision finer than 0.1mm should be possible
    [100.5, 331.2]
    """
    pass

def test_right_part_iv_of_v():
    """
    Check dimensions of Part representing next-to-topmost portion of right edge

    >>> test_args = { "start_edge": ([-1,-1,1],[-1,-1,-1])
    ...              ,"end_edge": ([1,-1,1],[1,-1,-1])
    ...              ,"part_plane": (0,2) #oriented along X Z plane
    ...              ,"shrink_edges": {'left': 128.6, 'right': 50.7}#room for other Right parts
    ...              ,"shrink_axis": 0 # shrink along X axis
    ...              ,"thickness_direction_negative": False
    ...              }
    >>> vect = Calculator('test/cube_flipped.dae') #112.1 x 271.6mm face
    >>> right_side = vect.make_part(**test_args)
    >>> len(right_side.sections)
    2
    >>> #(112.1+.4/2+.4/2, 577.0+.4/2+.4/2-128.6-50.7)
    >>> [ round(x, 1) for x in right_side[0].dimensions_mm ] #FIXME: precision finer than 0.1mm should be possible
    [112.5, 398.1]
    """
    pass

def test_right_part_v_of_v():
    """
    Check dimensions of Part representing topmost portion of right edge

    >>> test_args = { "start_edge": ([-1,-1,1],[-1,-1,-1])
    ...              ,"end_edge": ([1,-1,1],[1,-1,-1])
    ...              ,"part_plane": (0,2) #oriented along X Z plane
    ...              ,"shrink_edges": {'left': 201.4 #room for other Right parts
    ...                               ,"bottom": 'joint-default'}#room for Back part
    ...              ,"shrink_axis": 0 # shrink along X axis
    ...              ,"thickness_direction_negative": False
    ...              }
    >>> vect = Calculator('test/cube_flipped.dae') #112.1 x 271.6mm face
    >>> right_side = vect.make_part(**test_args)
    >>> len(right_side.sections)
    2
    >>> #(112.1+.4/2+.4/2-6*2, 577.0+.4/2+.4/2-128.6-72.8)#todo: adjust +5.9 left -72.8 r
    >>> [ round(x, 1) for x in right_side[0].dimensions_mm ] #FIXME: precision finer than 0.1mm should be possible
    [100.5, 376.0]
    """
    pass
