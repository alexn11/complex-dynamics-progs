# Author:  alexn11 (alexn11.gh@gmail.com)
# Created: 2019-11-19
# Copyright (C) 2019, Alexandre De Zotti
# License: MIT License




"""
 Imports
"""

import math
import cmath
import sys

from PIL import Image
import numpy


import ezInputConf
import tonglib


"""
 Constants
"""

two_pi = 2. * math . pi

# the list of variables configurable by using a config file
config_variables = {
  "any_periodic_image_name" : "string",
  "b" : "float",
  "background_color" : "float rgba",
  "bifurcation_diagram_image_name" : "string",
  "default_starting_point" : "float",
  "do_draw_any_periodic" : "boolean",
  "do_draw_bifurcation_diagram" : "boolean",
  "do_draw_periods" : "boolean",
  "do_draw_tongues" : "boolean",
  "do_show_progress" : "boolean",
  "do_superlong_iterations" : "boolean",
  "do_test" : "boolean",
  "image_height" : "int",
  "image_width" : "int",
  "map_family" : "string",
  "max_a" : "float",
  "max_b" : "float",
  "max_period_to_test" : "int",
  "min_a" : "float",
  "min_b" : "float",
  "number_of_orbits_to_compute" : "int",
  "number_of_values_of_a" : "int",
  "orbit_final_segment_length" : "int",
  "orbit_initial_segment_length" : "int",
  "periods_image_name" : "string",
  "period_test_tol" : "float",
  "point_color" : "float rgba",
  "results_file_name_a_b_values" : "string",
  "results_file_name_last_iterates" : "string",
  "results_file_name_periods" : "string",
  "test_type" : "string",
  }


"""
 Parameters
"""


do_test = False

test_type = ""
#test_type = "running"
#test_type = "acceptable outputs"
#test_type = "almost full quality"
#test_type = "check with dsm"


do_draw_tongues = False
do_draw_bifurcation_diagram = False
do_superlong_iterations = False


orbit_initial_segment_length = 0


# Parameters specific to bifurcation diagram
b = 1.
orbit_final_segment_length = 0
bifurcation_diagram_image_name = ""
background_color = (1., 1., 1., 1.)
point_color = (.0, .0, .0, 1.)
if (do_superlong_iterations):
   orbit_initial_segment_length = 352
   orbit_final_segment_length = 3258
#

do_draw_periods = False
do_draw_any_periodic = False
do_save_numerical_results = False
do_save_last_iterates = False

map_family = ""

periods_image_name = ""
any_periodic_image_name = ""
results_file_name_a_b_values = ""
results_file_name_periods = ""
results_file_name_last_iterates = ""


default_starting_point = 0.2

max_period_to_test = 0
period_test_tol = 0.
# NOTE: could have interemediate precision with an intermediate region where the periodicity isnt sure

image_width = 0
image_height = 0

# the interesting part of the parameter space is:
min_b = 0.5
max_b = 1
min_a = 0
max_a = 1


do_show_progress = True
number_of_orbits_to_compute = 1



"""
old default
"""


"""
 Process input
"""



       

def process_config_input (config_file_name):
    # probably better do an object, but i won't
    global any_periodic_image_name
    global b
    global background_color
    global bifurcation_diagram_image_name
    global default_starting_point
    global do_draw_any_periodic
    global do_draw_bifurcation_diagram
    global do_draw_periods
    global do_draw_tongues
    global do_show_progress
    global do_superlong_iterations
    global do_test
    global image_height
    global image_width
    global map_family
    global max_a
    global max_b
    global max_period_to_test
    global min_a
    global min_b
    global number_of_orbits_to_compute
    global orbit_final_segment_length
    global orbit_initial_segment_length
    global periods_image_name
    global results_file_name_a_b_values
    global results_file_name_last_iterates
    global results_file_name_periods
    global period_test_tol
    global point_color
    global test_type

    global do_save_last_iterates

    do_save_last_iterates = False

    config_parser = ezInputConf . get_config (config_file_name)
    config_section = config_parser ["Program inputs"]
    for variable_name in config_section . keys ():
       try:
          # given that i need the variable anyway, variable type here is here merely to check that the config file has no typo
          variable_type = config_variables [variable_name]
       except KeyError:
          raise Exception ("Unknown variable in config file: '" + variable_name + "'")
       variable_value = ezInputConf . convert_one_value (variable_type, config_section [variable_name])
       if (variable_name == "any_periodic_image_name"):
          any_periodic_image_name = variable_value
       elif (variable_name == "b"):
          b = variable_value
       elif (variable_name == "background_color"):
          background_color = variable_value
       elif (variable_name == "bifurcation_diagram_image_name"):
          bifurcation_diagram_image_name = variable_value
       elif (variable_name == "default_starting_point"):
          default_starting_point = variable_value
       elif (variable_name == "do_draw_any_periodic"):
          do_draw_any_periodic = variable_value
       elif (variable_name == "do_draw_bifurcation_diagram"):
          do_draw_bifurcation_diagram = variable_value
       elif (variable_name == "do_draw_periods"):
          do_draw_periods = variable_value
       elif (variable_name == "do_draw_tongues"):
          do_draw_tongues = variable_value
       elif (variable_name == "do_show_progress"):
          do_show_progress = variable_value
       elif (variable_name == "do_superlong_iterations"):
          do_superlong_iterations = variable_value
       elif (variable_name == "do_test"):
          do_test = variable_value
       elif (variable_name == "image_height"):
          image_height = variable_value
       elif (variable_name == "image_width"):
          image_width = variable_value
       elif (variable_name == "map_family"):
          map_family = variable_value
       elif (variable_name == "max_a"):
          max_a = variable_value
       elif (variable_name == "max_b"):
          max_b = variable_value
       elif (variable_name == "max_period_to_test"):
          max_period_to_test = variable_value
       elif (variable_name == "min_a"):
          min_a = variable_value
       elif (variable_name == "min_b"):
          min_b = variable_value
       elif (variable_name == "number_of_orbits_to_compute"):
          number_of_orbits_to_compute = variable_value
       elif (variable_name == "orbit_final_segment_length"):
          orbit_final_segment_length = variable_value
       elif (variable_name == "orbit_initial_segment_length"):
          orbit_initial_segment_length = variable_value
       elif (variable_name == "periods_image_name"):
          periods_image_name = variable_value
       elif (variable_name == "period_test_tol"):
          period_test_tol = variable_value
       elif (variable_name == "point_color"):
          point_color = variable_value
       elif (variable_name == "results_file_name_a_b_values"):
          results_file_name_a_b_values = variable_value
       elif (variable_name == "results_file_name_last_iterates"):
          results_file_name_last_iterates = variable_value
          do_save_last_iterates = True
       elif (variable_name == "results_file_name_periods"):
         results_file_name_periods  = variable_value
       elif (variable_name == "test_type"):
          test_type = variable_value
       else:
          raise Exception ("TODO: config: " + variable_name)
       
    try:
       extra_section = config_parser ["Extra"]
       do_extra_section = True
    except KeyError:
       do_extra_section = False

    if (do_extra_section):
       print (config_variables)
       #TODO: if (do_show_variables):




do_use_config_file = False
if (len (sys . argv) > 1):
   if (sys . argv [1] != "-h"):
      do_use_config_file = True
      config_file_name = sys . argv [1]
      process_config_input (config_file_name)
else:
   print ("(using default configuration)") 


"""
 Derived global variables (first part)
"""




if (do_test):
    orbit_initial_segment_length = 5
    max_period_to_test = 1
    image_width = 50
    image_height = 50
    number_of_orbits_to_compute = 1
    orbit_final_segment_length = 10
    if (test_type == "running"):
        orbit_initial_segment_length = 5
        max_period_to_test = 1
        image_width = 50
        image_height = 50
        number_of_orbits_to_compute = 1
    elif (test_type == "acceptable outputs"):
        orbit_initial_segment_length = 80
        max_period_to_test = 6
        image_width = 200
        image_height = 200
        number_of_orbits_to_compute = 1
    elif (test_type == "almost full quality"):
        orbit_initial_segment_length = 80
        max_period_to_test = 6
        image_width = 400
        image_height = 400
        number_of_orbits_to_compute = 1
    elif (test_type == "check with dsm"):
        orbit_initial_segment_length = 80
        max_period_to_test = 6
        image_width = 200
        image_height = 200
        number_of_orbits_to_compute = 1
        map_family = "dsm"
        periods_image_name = "dsm-tongues-periods"
        any_periodic_image_name = "dsm-tongues-any"
    else:
        raise Exception ("Unknown test type")



"""
Internal parameters
"""

type_colors = [(.1, 1., 0.2, 1.),
               (.1, 0.2, 1., 1.),
               (0.66, 0.2, 0.66, 1.),
               (0.66, 0.66, 0.2, 1.),
               (0.77, 0.77, 0., 1.),
               (1., 1., 1., 1.),
               (1., 0, 0, 1.),
               (0.66, 0.2, 0.66, 1.),
               (0.66, 0.66, 0.2, 1.),
               (0.33, 0.12, 0.19, 1.),
               (0.67, 0.247, 0.89, 1.),
               (0.12, 0.87, 0.56, 1), ]



type_colors = [ (1, 0, 0, 1),
                (0, 1, 1, 1), ]



fate_nonperiodic = 0
fate_periodic = 1

"""
 Functions
"""

"""
Graphics
"""

def save_image (image_name,
                image_width,
                image_height,
                pixels,
                do_flip = False):
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

            
    image_file_name = image_name + ".png"
    image . save (image_file_name, "PNG")




def density_to_shade (image_width,
                      image_height,
                      densities):
    pixels = numpy . zeros ([image_width, image_height, 4], dtype = "double")
    for x in range (image_width):
        for y in range (image_height):
            density_color_value = densities [x, y]
            for c in range (3):
                try:
                    pixels [x, y, c] = density_color_value
                except (ValueError):
                    raise
                    pixels [x, y, c] = float ('NaN')
            pixels [x, y, 3] = 1.
    return pixels


def convert_point_coordinates_to_image_coordinates (
                 image_width,
                 image_height,
                 min_x,
                 max_x,
                 min_y,
                 max_y,
                 point_list):

    x_convert_factor = image_width / (max_x - min_x)
    y_convert_factor = image_height / (max_y - min_y)

    image_point_list = []

    for point in point_list:
  
       [x, y] = point

       if (x < min_x): continue
       if (x >= max_x): continue
       ix = int (round (x_convert_factor * (x - min_x)))
       if (ix >= image_width):  continue

       if (y < min_y): continue
       if (y >= max_y): continue
       iy = int (round (image_height - 1 - y_convert_factor * (y - min_y)))
       if (iy >= image_height): continue


       image_point_list . append ([ix, iy])


    return image_point_list

def draw_points (image_width,
                 image_height,
                 background_color,
                 point_color,
                 min_x,
                 max_x,
                 min_y,
                 max_y,
                 point_list):

    pixels = numpy . zeros ([image_width, image_height, 4], dtype = "double")

    for x in range (image_width):
        for y in range (image_height):
           for c in range (4):
               pixels [x, y, c] = background_color [c]

    points_to_draw = convert_point_coordinates_to_image_coordinates (image_width, image_height, min_x, max_x, min_y, max_y, point_list)

    for point in points_to_draw:
       for c in range (4):
           pixels [point [0], point [1], c] = point_color [c]

    return pixels
        
"""
"""




        
"""
Output to pixels
"""

def compute_pixel_values_simple (image_width,
                                 image_height,
                                 type_colors,
                                 point_types):
    
    values = numpy . zeros ([image_width, image_height, 4], dtype = "double")
    for y in range (image_height):
        for x in range (image_width):
            c = point_types [x, y]
            try:
                values [x] [y] = type_colors [point_types [x, y]]
            except IndexError:
                print (x)
                print (point_types [x, y])
                print (type_colors)
                raise
    return values

def compute_pixel_values_with_shade (image_width,
                                     image_height,
                                     type_colors,
                                     point_types,
                                     point_values,
                                     max_value,
                                     do_reverse = False):
    
    values = numpy . zeros ([image_width, image_height, 4], dtype = "double")
    for y in range (image_height):
        for x in range (image_width):
            c = point_types [x, y]
            shade_value = point_values [x, y] / max_value
            if (do_reverse):
              shade_value = 1 - shade_value
            try:
                color = type_colors [point_types [x, y]]
                values [x] [y] [0:3] = [ shade_value * c for c in color [0:3] ]
                values [x] [y] [3] = color [3]
            except IndexError:
                print (x)
                print (point_types [x, y])
                print (type_colors)
                raise
    return values


"""
Derived parameters
"""

top = max_b
left = min_a
bottom = min_b
right = max_a


pixel_dx = (right - left) / image_width
pixel_dy = (top - bottom) / image_height


tongue_space = tonglib . tongue_system (map_family)

tongue_space . set_dynamics_params (default_starting_point,
                                    number_of_orbits_to_compute,
                                    orbit_initial_segment_length,
                                    orbit_final_segment_length,
                                    max_period_to_test,
                                    period_test_tol,
                                    do_save_last_iterates = do_save_last_iterates)



def draw_the_tongues ():

   global tongue_space


   tongue_space . create_tongue_picture (image_width, image_height, left, right, bottom, top)

   parameters_grid = tongue_space . parameters_grid
   parameters_fates = tongue_space . parameters_fates
   parameters_periods = tongue_space . parameters_periods

   numpy . place (parameters_periods, parameters_periods == 0, [ max_period_to_test * number_of_orbits_to_compute, ])


   """
    Draw and save images
   """

   if (do_draw_any_periodic):
     
     print ("Saving image " + any_periodic_image_name)

     pixels = compute_pixel_values_simple (image_width,
                                           image_height,
                                           type_colors,
                                           parameters_fates)

     save_image (any_periodic_image_name,
                 image_width,
                 image_height,
                 pixels)



   if (do_draw_periods):
     print ("Saving image " + periods_image_name)
     pixels = compute_pixel_values_with_shade (image_width,
                                               image_height,
                                               type_colors,
                                               parameters_fates,
                                               parameters_periods,
                                               max_period_to_test * number_of_orbits_to_compute)
     save_image (periods_image_name,
                 image_width,
                 image_height,
                 pixels)





if (do_draw_tongues):
    draw_the_tongues ()
    if (results_file_name_a_b_values != ""):
      numpy . savetxt (results_file_name_a_b_values, tongue_space . parameters_grid)
    if (results_file_name_periods != ""):
      numpy . savetxt (results_file_name_periods, tongue_space . parameters_periods)
    if (results_file_name_last_iterates != ""):
      numpy . savetxt (results_file_name_last_iterates, tongue_space . last_iterates [ :, :, 0 ])

if (do_draw_bifurcation_diagram):

  bottom = b
  top = b + 1.

  tongue_space . compute_grid_parameters (image_width, 1, left, right, bottom, top)
  tongue_space . compute_parameters_grid ()

  step_a = tongue_space . step_a
  number_of_values_of_a = tongue_space . nb_a
  a_list = numpy . real (tongue_space . parameters_grid [ :, 0 ])

  final_points = [ tongue_space . orbit_final_segment_length * [ 0. ] for i in range (number_of_values_of_a) ]

  for ai in range (number_of_values_of_a):

        a = a_list [ai]
        tongue_space . set_parameters_values (a, b)

        starting_point = tongue_space . compute_starting_points () [0]
        final_points_start = tongue_space . compute_iterate (orbit_initial_segment_length, starting_point)

        final_points [ai] [0] = final_points_start

        for it in range (1, orbit_final_segment_length):
            final_points [ai] [it] = tongue_space . apply_map (final_points [ai] [it - 1])

        if (do_show_progress):
           print (".", end = "")
           sys . stdout . flush ()

  if (do_show_progress):
    print ("")

  all_points = [ [a_list [ai], x]
                 for ai in range (number_of_values_of_a)
                 for x in final_points [ai] ]
  pixels = draw_points (image_width, image_height, background_color, point_color, min_a, max_a, 0, 1, all_points)
  save_image (bifurcation_diagram_image_name,
              image_width,
              image_height,
              pixels)






































