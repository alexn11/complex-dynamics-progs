
import math
import os
import sys

import PIL
from PIL import Image

import numpy

two_pi_inverse = 1. / (2. * math . pi)


def save_image (image_name,
                image_width,
                image_height,
                pixels,
                do_flip = False,
                directory = "."):

    print ("Saving image: " + image_name)
    
    image_size = (image_width, image_height)
    image = Image . new ("RGBA", image_size, None)

    image_pixels = image . load ()
    for x in range (image_width):
        for y in range (image_height):
            try:
                pixel = (int (256. * pixels [x] [y] [0]),
                         int (256. * pixels [x] [y] [1]),
                         int (256. * pixels [x] [y] [2]),
                         int (256. * pixels [x] [y] [3]))
            except (ValueError):
                # why? some times pixels contains nans
                #print ("ValueError exception caught")
                #print ("pixels:"
                #       + str (pixels [x] [y] [0])
                #       + "... "
                #       + str (pixels [x] [y] [3]))
                pixel = (255, 0, 0, 255)
                #raise
            
            image_pixels [x, y] = pixel

    if (do_flip):
        image = image . transpose (Image . FLIP_TOP_BOTTOM)

            
    image_file_name = os . path . join (directory, image_name + ".png")
    image . save (image_file_name, "PNG")



    

def compute_shade_value (drawing_options,
                         original_value,
                         max_original_value):

    
    if (max_original_value < original_value):
        original_value = max_original_value
    try:
        shade_value = original_value / max_original_value
    except (RuntimeWarning): # why that?
        shade_value = 1.
        #raise in case of max=0

        
    if (drawing_options . shade_type == ord ("e")):
        try:
            enh_value = (
                pow (1. + shade_value,
                     drawing_options . shade_enhancement_power))
            shade_value = (
                drawing_options . shade_enhancement_factor
                * (1. - 1. / enh_value))
        except (RuntimeWarning):
            print (drawing_options . shade_enhancement_factor)
            print (shade_value)
            print (drawing_options . shade_enhancement_power)
            raise
        #shade_value = 64 * (1 - 1 / pow (1 + shade_value, 6)) / 63.
        #shade_value = 16 * (1 - 1 / pow (1 + shade_value, 4)) / 15.
        #shade_value = 2. * shade_value /  (1. + shade_value)
        
    return shade_value
                        

def alpha_combine (color1, color2):
    #print ("combine: "
    #       + str (color1)
    #       + " over "
    #       + str (color2))
    combination_rgb = [
        color1 [i] * color1 [3]
        + (1. - color1 [3]) * color2 [3] * color2 [i]
        for i in range (3)]
    combination_alpha = [color1 [3]
                         + (1. - color1 [3]) * color2 [3]]
    combination_rgba = combination_rgb + combination_alpha
    return combination_rgba

# -----------------------------------------------------------------------------

def prepare_preview (preview_parameters, image_width, image_height):
    [prev_cx,
     prev_cy,
     prev_threshold,
     preview_white,
     preview_black] = preview_parameters
    prev_pulse_x = int (image_width / prev_cx)
    if (prev_pulse_x == 0):
        prev_pulse_x = 1
    prev_pulse_y = int (image_height / prev_cy)
    if (prev_pulse_y == 0):
        prev_pulse_y = 1
    return preview_parameters + [prev_pulse_x, prev_pulse_y]

def preview_x_step (preview_parameters, x, y, max_image, value):
    [prev_cx,
     prev_cy,
     prev_threshold,
     preview_white,
     preview_black,
     prev_pulse_x,
     prev_pulse_y] = preview_parameters
    if ((not (x % prev_pulse_x)) and (not (y % prev_pulse_y))):
        if (value > max_image * prev_threshold):
            sys . stdout . write (preview_black)
        else:
            sys . stdout . write (preview_white)
        sys . stdout . flush ()


def preview_y_step (preview_parameters, y):
    prev_pulse_y = preview_parameters [6]
    if (not (y % prev_pulse_y)):
        print ("")

def preview_end (preview_parameters):
    print ("")
    return
# -----------------------------------------------------------------------------
        
def compute_boundary (
        image_width,
        image_height,
        preview_parameters,
        eventual_landing_region,
        density_shift = 0.):

    if (preview_parameters != None):
        preview_data = prepare_preview (preview_parameters,
                                        image_width,
                                        image_height)

    boundary_density = numpy . zeros ([image_width, image_height],
                                      dtype = "double")
    
    for y in range (image_height):
        
        for x in range (image_width):
            
            centre_region = eventual_landing_region [x, y]
            non_similar_neighbor_count = 0
            
            if (x > 0):
                if (y > 0):
                    if (centre_region
                        != eventual_landing_region [x - 1, y - 1]):
                        
                        non_similar_neighbor_count += 1
                        
                if (centre_region != eventual_landing_region [x - 1, y]):
                    non_similar_neighbor_count += 1
                    
                if (y < image_height - 1):
                    if (centre_region
                        != eventual_landing_region [x - 1, y + 1]):
                        
                        non_similar_neighbor_count += 1
                        
            if (y > 0):
                if (centre_region != eventual_landing_region [x, y - 1]):
                    non_similar_neighbor_count += 1
                    
            if (y < image_height - 1):
                if (centre_region != eventual_landing_region [x, y + 1]):
                    non_similar_neighbor_count += 1

            if (x < image_width - 1):
                if (y > 0):
                    if (centre_region
                        != eventual_landing_region [x + 1, y - 1]):
                        
                        non_similar_neighbor_count += 1
                        
                if (centre_region != eventual_landing_region [x + 1, y]):
                    non_similar_neighbor_count += 1
                    
                if (y < image_height - 1):
                    if (centre_region
                        != eventual_landing_region [x + 1, y + 1]):
                        non_similar_neighbor_count += 1
                        
            if (non_similar_neighbor_count > 4):
                non_similar_neighbor_count = 4
                
            boundary_density [x, y] = ((non_similar_neighbor_count
                                        + density_shift)
                                       / (4. + density_shift))

            if (preview_parameters != None):
                preview_x_step (preview_data, x, y, 4, boundary_density [x, y])

        if (preview_parameters != None):
            preview_y_step (preview_data, y)
        
    if (preview_parameters != None):
        preview_end (preview_data)
    
    return boundary_density


def compute_boundary_density (image_width,
                              image_height,
                              preview_parameters,
                              eventual_landing_region,
                              boundary_density,
                              density_shift = 0):

    if (preview_parameters != None):
        preview_data = prepare_preview (preview_parameters,
                                        image_width,
                                        image_height)
    
    for y in range (image_height):
        
        for x in range (image_width):
            
            centre_region = eventual_landing_region [x, y]
            non_similar_neighbor_count = 0
            
            if (x > 0):
                if (y > 0):
                    if (centre_region
                        != eventual_landing_region [x - 1, y - 1]):
                        
                        non_similar_neighbor_count += 1
                        
                if (centre_region != eventual_landing_region [x - 1, y]):
                    non_similar_neighbor_count += 1
                    
                if (y < image_height - 1):
                    if (centre_region
                        != eventual_landing_region [x - 1, y + 1]):
                        
                        non_similar_neighbor_count += 1
                        
            if (y > 0):
                if (centre_region != eventual_landing_region [x, y - 1]):
                    non_similar_neighbor_count += 1
                    
            if (y < image_height - 1):
                if (centre_region != eventual_landing_region [x, y + 1]):
                    non_similar_neighbor_count += 1

            if (x < image_width - 1):
                if (y > 0):
                    if (centre_region
                        != eventual_landing_region [x + 1, y - 1]):
                        
                        non_similar_neighbor_count += 1
                        
                if (centre_region != eventual_landing_region [x + 1, y]):
                    non_similar_neighbor_count += 1
                    
                if (y < image_height - 1):
                    if (centre_region
                        != eventual_landing_region [x + 1, y + 1]):
                        non_similar_neighbor_count += 1
                        
            if (non_similar_neighbor_count > 4):
                non_similar_neighbor_count = 4
                
            boundary_density [x, y] = ((non_similar_neighbor_count
                                        + density_shift)
                                       / (4. + density_shift))

            if (preview_parameters != None):
                preview_x_step (preview_data, x, y, 4, boundary_density [x, y])

        if (preview_parameters != None):
            preview_y_step (preview_data, y)
        
    if (preview_parameters != None):
        preview_end (preview_data)
    
    return



def density_to_shade (image_width,
                      image_height,
                      densities):
    pixels = numpy . zeros ([image_width, image_height, 4], dtype = "double")
    for x in range (image_width):
        for y in range (image_height):
            density_color_value = 1. - densities [x, y]
            for c in range (3):
                try:
                    pixels [x, y, c] = density_color_value
                except (ValueError):
                    raise
                    pixels [x, y, c] = float ('NaN')
            pixels [x, y, 3] = 1.
    return pixels

def double_density_to_shade (image_width,
                             image_height,
                             densities):
    pixels = numpy . zeros ([image_width, image_height, 4], dtype = "double")
    for x in range (image_width):
        for y in range (image_height):
            if ((densities [x, y] . real < 0)
                or
                (densities [x, y] . imag < 0)):
                  pixels [x, y] = [ 1., 1., 1., 1. ]
            else:
                pixels [x, y, 0] = 1. - densities [x, y] . real
                pixels [x, y, 1] = 1. - densities [x, y] . imag
                pixels [x, y, 2] = 0.
                pixels [x, y, 3] = 1.
    return pixels


def compute_pixel_values (image_width,
                          image_height,
                          drawing_options,
                          preview_parameters,
                          point_values,
                          max_image):

    #print (any ([ (points_image_abs [x, y] > 0)
    #              for x in range (image_width)
    #              for y in range (image_height) ]))

    if (preview_parameters != None):
        preview_data = prepare_preview (preview_parameters,
                                        image_width,
                                        image_height)

    drawing_type = drawing_options . drawing_type
    #print (drawing_type)
    if (drawing_type == ord ("t")):
        threshold_value = drawing_options . threshold_value
        #print ("thrval="+str(threshold_value))
        below_color = drawing_options . below_color
        above_color = drawing_options . above_color
        error_color = drawing_options . error_color
    elif (drawing_type == ord ("s")):
        negative_base_color = drawing_options . negative_base_color
        negative_shade_color = drawing_options . negative_shade_color
        nonnegative_base_color = drawing_options . nonnegative_base_color
        nonnegative_shade_color = drawing_options . nonnegative_shade_color
    else:
        raise Exception ("Unknown drawing type: " + drawing_type)
        
    pixels = numpy . zeros ([image_width, image_height, 4], dtype = "double")
    for y in range (image_height):
        for x in range (image_width):
            value = point_values [x, y]
            if (drawing_type == ord ("s")):
                if (value < 0.):
                    base_color = negative_base_color
                    intensity = compute_shade_value (
                        drawing_options,
                        - value,
                        max_image)
                    shade_color = [
                        pixels [x] [y] [c]
                        + intensity * negative_shade_color [c]
                        for c in range (4)]
                else:
                    base_color = nonnegative_base_color
                    intensity = compute_shade_value (
                        drawing_options,
                        value,
                        max_image)
                    shade_color = [
                        pixels [x] [y] [c]
                        + intensity * nonnegative_shade_color [c]
                        for c in range (4)]
                    
                pixels [x] [y] = alpha_combine (shade_color,
                                                base_color)
                        
                #TODO: implement this back
                #if (not (points_image is None)):
                #    if (points_image [x, y] . imag < 0.0):
                #        (values [x] [y] [0], values [x] [y] [1]) = (
                #            values [x] [y] [1],
                #            values [x] [y] [0])

            elif (drawing_type == ord ("t")):
                pixels [x] [y] [:] = below_color [:]
                if (value == -1.):
                    pixels [x] [y] [:] = error_color [:]
                elif (value > threshold_value):
                    pixels [x] [y] [:] = above_color [:]


            if (preview_parameters != None):
                preview_x_step (preview_data,
                                x,
                                y,
                                max_image,
                                value)
                
        if (preview_parameters != None):
            preview_y_step (preview_data, y)


    if (preview_parameters != None):
        preview_end (preview_data)

        
    return pixels




def compute_pixel_values_simple (image_width,
                                 image_height,
                                 type_colors,
                                 point_types):
    
    values = numpy . zeros ([image_width, image_height, 4], dtype = "double")
    for y in range (image_height):
        for x in range (image_width):
            c = point_types [x, y]
            values [x] [y] = type_colors [point_types [x, y]]
    return values



def draw_crosses (image_width,
                  image_height,
                  image_pixels,
                  cross_size,
                  cross_color,
                  cross_centers):
    for (center_x, center_y) in cross_centers:
        # TODO: func: draw_cross
        
        x_min = max (center_x - cross_size, 0)
        x_max = min (center_x + cross_size + 1, image_width)
        y_min = max (center_y - cross_size, 0)
        y_max = min (center_y + cross_size + 1, image_height)
        
        y = center_y
        if (0 <= y < image_height):
            for x in range (x_min, x_max):
                image_pixels [x] [y] = cross_color
                
        x = center_x
        if (0 <= x < image_width):
            for y in range (y_min, y_max):
                image_pixels [x] [y] = cross_color
    return

def draw_disk (image_width,
               image_height,
               image_pixels,
               center,
               radius,
               color):
    x_min = max (round (center [0] - radius), 0)
    x_max = min (round (center [0] + radius) + 1, image_width)
    y_min = max (round (center [1] - radius), 0)
    y_max = min (round (center [1] + radius) + 1, image_height)
    radius_squared = radius * radius
    for x in range (x_min, x_max):
        dx = x - center [0]
        for y in range (y_min, y_max):
             dy = y - center [1]
             if ((dx * dx + dy * dy) <= radius_squared):
                 image_pixels [x, y] = color
    return

def process_arguments_for_shading (image_width,
                                   image_height,
                                   arguments,
                                   do_smoothing):
    
    processed_arguments = numpy . zeros ([image_width, image_height],
                                         dtype = "double")
    for x in range (image_width):
        for y in range (image_height):
            
            if (math . isnan (arguments [x, y])):
                processed_argument = float ('NaN')
            else:
                processed_argument = two_pi_inverse * arguments [x, y]
                if (do_smoothing):
                    processed_argument = (
                        4. * processed_argument * (1. - processed_argument))
                

            processed_arguments [x, y] = processed_argument
            
    return processed_arguments

def process_rectangle_positions_for_shading (image_width,
                                             image_height,
                                             positions,
                                             do_sharper_colors,
                                             do_edges,
                                             edge_thickness,
                                             do_cross):
    double_densities = numpy . zeros ([image_width, image_height],
                                      dtype = "complex")
    upper_edge_value = 1. - edge_thickness
    lower_edge_value = edge_thickness
    for x in range (image_width):
        for y in range (image_height):
            if (positions [x, y] . real >= 0):
                # double_density = (1. + 1.j) - positions [x, y]
                double_density = positions [x, y]
                if (do_sharper_colors):
                    double_density *= 0.5
                elif (do_edges):
                    if ((double_density . real < lower_edge_value)
                        or
                        (double_density . real > upper_edge_value)
                        or
                        (double_density . imag < lower_edge_value)
                        or
                        (double_density . imag > upper_edge_value)):
                          double_density = 1. + 0.j
                    else:
                          double_density = 0. + 1.j
                elif (do_cross):
                    if (double_density . real < double_density . imag):
                        if (1. < double_density . real + double_density . imag):
                            double_density = 1. + 1.j
                        else:
                            double_density = 0. + 1.j
                    else:
                        if (1. < double_density . real + double_density . imag):
                            double_density = 1. + 0.j
                        else:
                            double_density = 0.5 + 0.5j

                        
                double_densities [x, y] = double_density
            else:
                double_densities [x, y] = - 1. - 1.j
    return double_densities



def convert_grid_to_pixels (state_colors,
                            image_width,
                            image_height,
                            grid_values):
    pixels = numpy . zeros ([image_width, image_height, 4], dtype = "double")
    for y in range (image_height):
        for x in range (image_width):
            color = state_colors [grid_values [y] [x]]
            for c in range (4):
                pixels [x, y, c] = color [c]
    return pixels

def rescale_color_preserve_alpha (color,
                                  rescaling_factor):
    rescaled_color = [rescaling_factor * c for c in color [:3]]
    rescaled_color . append (color [3])
    return rescaled_color

def convert_bool_int_grid_to_pixel (rescaling_constant,
                                    true_color,
                                    false_color,
                                    image_width,
                                    image_height,
                                    grid_values):
    pixels = numpy . zeros ([image_width, image_height, 4], dtype = "double")
    for y in range (image_height):
        for x in range (image_width):
            flag, value = grid_values [y] [x]
            if (rescaling_constant > 0):
                color_intensity = value * rescaling_constant
            else:
                color_intensity = 1
            if (flag):
                color = rescale_color_preserve_alpha (true_color,
                                                      color_intensity)
            else:
                color = rescale_color_preserve_alpha (false_color,
                                                      color_intensity)
            for c in range (4):
                pixels [x, y, c] = color [c]
    return pixels



def make_color_list (number_of_colors):
    if (number_of_colors < 0):
        raise Exception ("number of colors is negative")
    if (number_of_colors == 0):
        return []
    colors = []
    if (number_of_colors == 1):
        colors = [(0.5, 0.5, 0.5)]
    else:
        n = round (pow (number_of_colors, 1/3) + 0.5)
        step = 1. / (n + 1)
        start = 1 - step
        n_squared = n * n
        index_step = (n * n_squared) / number_of_colors
        colors = [ (start - step * ((index_step * c) % n),
                    start - step * (((index_step * c) // n) % n),
                    start - step * ((index_step * c) // n_squared),
                    1.)
                   for c in range (number_of_colors) ]
    return colors
