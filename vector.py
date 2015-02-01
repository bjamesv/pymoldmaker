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
from OutputVector import Canvas
from ImportMesh import VectorMesh


if __name__ == '__main__':
    ## import a simple Sketchup COLLADA file
    mesh = VectorMesh('positive_for_mold.dae')
    ## test a modification to the file & resave
    file_new = 'cubeMOD.dae'
    # start a line from an arbitrary point - TODO: deprecated
    # poly_line_xyz = mesh.sections() # TODO: deprecated
    poly_line_xyz = list()
    s = mesh.bottomSections()
    for section in s:
        for triplet in section:
            poly_line_xyz.extend( triplet)
    mesh.save_lines( file_new, poly_line_xyz)
    ## test exporting to EPS
    img = Canvas()
    poly_line_mm = (  (80,80),(320,80)
                             ,(320,90)
                     ,(80,120)
                     ,(80,80)
                             )
    img.draw_line( poly_line_mm)
    img.save('vector_mm_box.eps')
