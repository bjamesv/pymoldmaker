"""
Module, defining functions for adjusting part sizes to allow for some
loss of material due to cutting (the kerf of the tool)

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

def adjustment_axis_directions(edge, opposite, translation_axis, part_plane, corner, adjust_in=False):
    """
    Return 3tuple of 1, 0, -1 representing axis direction to move corner
      further or closer to center of rectangle defined by start & end edges 

    >>> edge = [(-1, 1, 1), (-1, 1, -1)]
    >>> opposite = [(1, 1, 1), (1, 1, -1)]
    >>> translation_axis = 0 #X
    >>> part_plane = (0, 2) #X/Z plane (Y-normal)
    >>> corner = (-1, 1, 1)
    >>> adjustment_axis_directions(edge, opposite, translation_axis, part_plane, corner)
    (-1, 0, 1)
    >>> edge, opposite =([1,-1,-1],[-1,-1,-1]), ([1,1,-1],[-1,1,-1])
    >>> translation_axis = 1 #Y
    >>> part_plane = (0, 1) #X/Y plane (Z-normal)
    >>> corner = (1, 1, -1)
    >>> adjustment_axis_directions(edge, opposite, translation_axis, part_plane, corner)
    (1, 1, 0)
    >>> edge, opposite =([1,-1,-1],[-1,-1,-1]), ([1,1,-1],[-1,1,-1])
    >>> translation_axis = 1 #Y
    >>> part_plane = (0, 1) #X/Y plane (Z-normal)
    >>> corner = (-1, 1, -1)
    >>> adjustment_axis_directions(edge, opposite, translation_axis, part_plane, corner)
    (-1, 1, 0)
    """
    scale = [0, 0, 0]

    #case1, X shrink dimension (use start/end edges as-is)
    if translation_axis == 0:
        start_edge, end_edge = edge, opposite

    #case1, Y shrink dimension (rotate orientation 90deg)
    if translation_axis == 1:
        # determine where on edge or opposite, the corner is
        edge_is_start = corner in edge
        if edge_is_start:
            start_vertex_index = [tuple(v) for v in edge].index(tuple(corner))
        else:
            start_vertex_index = [tuple(v) for v in opposite].index(tuple(corner))

        # rotate
        initial, second = opposite, edge
        if edge_is_start:
            initial, second = edge, opposite
        start_edge = (initial[start_vertex_index], second[start_vertex_index])
        second_vertex_index = ({0,1} - {start_vertex_index}).pop()
        end_edge = (initial[second_vertex_index], second[second_vertex_index])

    if 0 in part_plane:
        scale[0] = adjustment_direction(start_edge, end_edge, 0)
    if 1 in part_plane:
        scale[1] = adjustment_direction(start_edge, end_edge, 1) #TODO: is this right?
    if 2 in part_plane:
        scale[2] = adjustment_direction(start_edge, end_edge, 2) #TODO: is this right?
    return tuple(scale)

def adjustment_direction(edge, opposite_edge, adjust_axis):
    """
    Return 1 or -1 for adjust_axis value opposite_edge greater/less than edge

    TODO: this function is used for BOTH kerf adjustment & part shrink
    (butt joint) adjustment... consider renaming this Python module to reflect

    >>> edge = [(-1, 1, 1), (-1, 1, -1)]
    >>> opposite = [(1, 1, 1), (1, 1, -1)]
    >>> axis = 0 # X-axis
    >>> adjustment_direction(edge, opposite, axis)
    -1
    >>> # test, other-way-around
    >>> adjustment_direction(opposite, edge, axis)
    1
    >>> # Test a part along Y axis
    >>> edge = [(-1, 1, 1), (-1, 1, -1)]
    >>> opposite = [(-1, -1, 1), (-1, -1, -1)]
    >>> axis = 1 # Y-axis
    >>> adjustment_direction(edge, opposite, axis)
    1
    >>> # ... and other-way-around
    >>> #TODO!
    """
    adjust_direction = 1
    which_vertex = 0 #arbitrarily select first one
    edge_vertex = edge[which_vertex]
    opposite_edge_vertex = opposite_edge[which_vertex]
    edge_minus_opposite = edge_vertex[adjust_axis] - opposite_edge_vertex[adjust_axis]
    if (edge_minus_opposite) < 0:
        adjust_direction = -1
    return adjust_direction
