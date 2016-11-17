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

def adjustment_direction(edge, opposite_edge, adjust_axis):
    """

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
