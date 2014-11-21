#!/bin/python3
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
from PIL import Image
from PIL import ImageDraw

class Canvas:
    """ an object representing a drawable vector image that can be written out 
        to disk as an image file.
    """
    def __init__(self):
        """ initializes the internal self.image object and pairs it with a 
            self.draw object for composing new visual content.
        """
        # create a Python Image Library image object
        mode = 'RGB'
        self.dpi = 72 #25.4*15
        size = (400, 300)
        color_background = 'white'
        self.image = Image.new(mode, size, color_background)
        #prepare Image for drawing
        color_lines = 'black'
        self.draw = ImageDraw.Draw(self.image)
        self.draw.setink( color_lines)
    
    def draw_line(self, poly_line_mm):
        """
        draws a polygonal line onto the image.
        Arguments: poly_line_mm a list of x,y tuplets representing the vertices
        of a polygonal shape in milimeters.
        """
        # now draw something onto it
        self.draw.line( poly_line_mm)
        
    def save(self,  destination):
        """ saves the internal image representation to the specified path or
            file object. """
        # .. and save it out to disk
        self.image.save( destination)
        
    def mm_to_px(self, mm):
        mm_per_inch = 25.4
        pixels_per_mm = self.dpi/mm_per_inch
        pixels_to_draw = mm*pixels_per_mm
        if( (pixels_to_draw % 1) != 0):
            pass #TODO: fix above to support mapping 1/3 mm to PS strokes/dots 
            #raise ValueError("specified dpi has resulted in lost precision")
        return int(pixels_to_draw)
