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
from image import Canvas
from calculator.calculator import Calculator
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", help="file path to COLLADA input model"
        , default='positive_for_mold.dae')
    parser.add_argument("--thickness_mm", help="(optional) thickness of the \
        material positive will be cut from.", type=int, default=6)
    parser.add_argument("--out", help="file path to output"
        , default='out.dae')
    args = parser.parse_args()
    input_file = args.input
    ## import a simple Sketchup COLLADA file
    mold_generator = Calculator(input_file)
    ## set the thickness
    mold_generator.material['thickness_mm'] = args.thickness_mm
    ## test a modification to the file & resave
    file_new = args.out
    mold_generator.save(file_new)
    ## test exporting to EPS
    img = Canvas()
    poly_line_mm = (  (80,80),(320,80)
                             ,(320,90)
                     ,(80,120)
                     ,(80,80)
                             )
    img.draw_line( poly_line_mm)
    img.save('vector_mm_box.eps')
