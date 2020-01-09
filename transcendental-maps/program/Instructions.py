
# todo: setup will create & update map objects
# todo: put all the todo together

# todo: update map just before eval/iterate (maybe not necess, tx to update*)
# todo: update drawings parameterts just before drawing

# todo: implement set_color_* instructions
# todo: protocol for adding new map_type
# todo: clean config*

# todo: add error such as "used before defined"

# todo: add tests for upper and lower half planes
# todo: add half plane tests in is_ functions

# FUTURE:
# todo: implement grid_size change (requires reallocating everything)


import math
import cmath
import sys

import numpy

import Rectangle
import GeometricTests
import drawings
import GridsAndArrays
import JuliaSets

import LinearizerMaps
import FatouInverseMaps

import cauliflower

# -----------------------------------------------------------------------------





def compute_max_value (config_data,
                       variable_to_use_as_max,
                       data_to_max):
    if (variable_to_use_as_max == None):
        max_value = 0
    elif ((variable_to_use_as_max == "explicit real")
          or (variable_to_use_as_max == "explicit integer")):
        max_value = config_data . drawings_config . max_value
    elif (variable_to_use_as_max == "nb_iterations"):
        max_value = config_data . iterations_config . nb_iterations
    elif (variable_to_use_as_max == "compute max"):
        max_value = numpy . nanmax (data_to_max)
    return max_value

def compute_max_value_from_array (config_data,
                                  variable_to_use_as_max,
                                  data_to_max):
    if (variable_to_use_as_max == None):
        max_value = 0
    elif ((variable_to_use_as_max == "explicit real")
          or (variable_to_use_as_max == "explicit integer")):
        max_value = config_data . drawings_config . max_value
    elif (variable_to_use_as_max == "nb_iterations"):
        max_value = config_data . iterations_config . nb_iterations
    elif (variable_to_use_as_max == "compute max"):
        max_value = numpy . amax (data_to_max)
    return max_value



def draw_real_data (config_data, data):
    return draw_data (config_data, data)
    
def draw_integer_data (config_data, data):
    return draw_data (config_data, data)

def draw_data (config_data, data):
    
    max_value = compute_max_value (
        config_data,
        config_data . drawings_config . variable_to_use_as_max,
        data)
    #print ("max = " + str (max_value))
    #raise Exception ("stop")
    #print (config_data . drawings_config . drawing_options)
    pixel_values = drawings . compute_pixel_values (
        config_data . drawings_config . image_width,
        config_data . drawings_config . image_height,
        config_data . drawings_config . drawing_options,
        config_data . preview_config . preview_parameters,
        data,
        max_value)
    
    return pixel_values

def convert_drawing_type_from_string (drawing_type):
    if (drawing_type == "threshold"):
        drawing_type = ("threshold")
    elif (drawing_type == "shade"):
        drawing_type = ("shade")
    else:
        raise Exception ("Unknown drawing type:" + str (drawing_type))
    return drawing_type

def convert_shade_type_from_program (prog_shade_type):
    if (prog_shade_type in ["enhanced",
                            "smallest values more visible"]):
        shade_type = ("smallest values more visible")
    elif (prog_shade_type in ["normal",
                              "default"]):
        shade_type = ("default")
    else:
        raise Exception ("Unknown shade type:" + str (prog_shade_type))
    return shade_type

def make_image_name (main_name, local_image_name):
    if (main_name == ""):
        image_name = local_image_name
    else:
        image_name = main_name + "-" + local_image_name
    return image_name


# -------- INSTRUCTIONS -------------------------------------------------------

def apply_instruction_nop (config, data, arguments):
    pass
    return


def apply_instruction_abs (config, data, arguments):
    source_name = arguments [0] [0]
    destination_name = arguments [1] [0]
    array_source = data . variables [source_name]
    array_destination = (data . variables [destination_name])
    map_parameters = ()
    apply_map  = lambda p, z : abs (z)
    GridsAndArrays . apply_map_on_array (
        config . drawings_config . image_width,
        config . drawings_config . image_height,
        apply_map,
        map_parameters,
        array_source,
        array_destination)
    return

def apply_instruction_add_test_enter_disk (config, data, arguments):
    test = ("enter_disk", (arguments [0], arguments [1]))
    config . iterations_config . test_list . append (test)
    return

def apply_instruction_add_test_leave_annulus (config, data, arguments):
    test = ("leave_annulus", (arguments [0], arguments [1], arguments [2]))
    config . iterations_config . test_list . append (test)
    return

def apply_instruction_add_test_leave_disk (config, data, arguments):
    test = ("leave_disk", (arguments [0], arguments [1]))
    config . iterations_config . test_list . append (test)
    return

def apply_instruction_add_test_leave_left_half_plane (config, data, arguments):
    test = ("leave_left_half_plane", (arguments [0], ))
    config . iterations_config . test_list . append (test)
    return

def apply_instruction_add_test_leave_right_half_plane (config, data, arguments):
    test = ("leave_right_half_plane", (arguments [0], ))
    config . iterations_config . test_list . append (test)
    return

def apply_instruction_annulus_index (config, data, arguments):
    source_name = arguments [3] [0]
    destination_name = arguments [4] [0]
    array_source = data . variables [source_name]
    array_destination = (data . variables [destination_name])
    map_parameters = (arguments [1], 1. / math . log (arguments [2]))
    # todo: center is ignored
    #map_parameters = (arguments [0], arguments [1], arguments [2])
    apply_map = GeometricTests . compute_annulus_index
    GridsAndArrays . apply_map_on_array (
        config . drawings_config . image_width,
        config . drawings_config . image_height,
        apply_map,
        map_parameters,
        array_source,
        array_destination)
    return

def apply_instruction_arg (config, data, arguments):
    source_name = arguments [1] [0]
    destination_name = arguments [2] [0]
    array_source = data . variables [source_name]
    array_destination = (data . variables [destination_name])
    map_parameters = (arguments [0], )
    apply_map = (
        ( lambda p, z : ((cmath . phase (z - p [0]))) . real + math . pi ))
    GridsAndArrays . apply_map_on_array (
        config . drawings_config . image_width,
        config . drawings_config . image_height,
        apply_map,
        map_parameters,
        array_source,
        array_destination)
    return


def apply_instruction_arg_density (config, data, arguments):
    density = drawings . process_arguments_for_shading (
        config . drawings_config . image_width,
        config . drawings_config . image_height,
        data . variables [arguments [0] [0]],
        config . drawings_config . do_smooth_argument)
    # todo: redundant copy
    data . variables [arguments [1] [0]] [:] = density [:]
    return

def apply_instruction_boundaries (config, data, arguments):
    source = data . variables [arguments [0] [0]]
    #print ("bound of=" + str (source))
    dest = data . variables [arguments [1] [0]]
    drawings . compute_boundary_density (
        config . drawings_config . image_width,
        config . drawings_config . image_height,
        config . preview_config . preview_parameters,
        source,
        dest)
    return

def apply_instruction_cauliflower_julia (config, data, arguments):
    nb_max_it = arguments [0]
    points = data . variables [arguments [1] [0]]
    stop_values = data . variables [arguments [2] [0]]
    GridsAndArrays . apply_map_on_array (
        config . drawings_config . image_width,
        config . drawings_config . image_height,
        cauliflower . check_point_position_wrt_dynamics,
        nb_max_it,
        points,
        stop_values)    
    return

def apply_instruction_coord_rect (config, data, arguments):
    # todo: implment rect things
    source_name = arguments [2] [0]
    destination_name = arguments [3] [0]
    array_source = data . variables [source_name]
    array_destination = (data . variables [destination_name])
    map_parameters = Rectangle . Rectangle (arguments [0] . imag,
                                            arguments [1] . imag,
                                            arguments [0] . real,
                                            arguments [1] . real)
    apply_map = GeometricTests . compute_rectangle_coordinates
    GridsAndArrays . apply_map_on_array (
        config . drawings_config . image_width,
        config . drawings_config . image_height,
        apply_map,
        map_parameters,
        array_source,
        array_destination)
    return

def apply_instruction_draw_complex_density (config, data, arguments):
    double_density = data . variables [arguments [0] [0]]
    pixel_values = drawings . double_density_to_shade (
        config . drawings_config . image_width,
        config . drawings_config . image_height,
        double_density)
    drawings . save_image (make_image_name (config . name, arguments [1]),
                           config . drawings_config . image_width,
                           config . drawings_config . image_height,
                           pixel_values,
                           True,
                           directory = config . results_dir)
    return

def apply_instruction_draw_density (config, data, arguments):
    density = data . variables [arguments [0] [0]]
    pixel_values = drawings . density_to_shade (
        config . drawings_config . image_width,
        config . drawings_config . image_height,
        density)
    drawings . save_image (make_image_name (config . name, arguments [1]),
                           config . drawings_config . image_width,
                           config . drawings_config . image_height,
                           pixel_values,
                           True,
                           directory = config . results_dir)
    return

def apply_instruction_draw_indexes (config, data, arguments):
    indexes = data . variables [arguments [0] [0]]
    config . drawings_config . update_drawing_options ()
    image_width = config . drawings_config . image_width
    image_height = config . drawings_config . image_height
    pixel_values = drawings . compute_pixel_values_simple (
        image_width,
        image_height,
        config . index_colors,
        indexes)
    drawings . save_image (make_image_name (config . name, arguments [1]),
                           image_width,
                           image_height,
                           pixel_values,
                           True,
                           directory = config . results_dir)
    return


def apply_instruction_draw_integers (config, data, arguments):
    drawing_data = data . variables [arguments [0] [0]]
    config . drawings_config . update_drawing_options ()
    pixel_values = draw_integer_data (config, drawing_data)
    drawings . save_image (make_image_name (config . name, arguments [1]),
                           config . drawings_config . image_width,
                           config . drawings_config . image_height,
                           pixel_values,
                           True,
                           directory = config . results_dir)
    return

def apply_instruction_draw_reals (config, data, arguments):
    drawing_data = data . variables [arguments [0] [0]]
    config . drawings_config . update_drawing_options ()
    pixel_values = draw_real_data (config, drawing_data)
    drawings . save_image (make_image_name (config . name, arguments [1]),
                           config . drawings_config . image_width,
                           config . drawings_config . image_height,
                           pixel_values,
                           True,
                           directory = config . results_dir)
    return

def apply_instruction_eval_main_map (config, data, arguments):
    
    array_source = data . variables [arguments [0] [0]]
    array_destination = data . variables [arguments [1] [0]]

    #print (config . eval_main_map)
    #print (config . main_map_extra_parameters)
    
    nan_count = GridsAndArrays . evaluate_map_on_grid (
        config . drawings_config . image_width,
        config . drawings_config . image_height,
        config . eval_main_map,
        config . main_map_extra_parameters,
        array_source,
        array_destination)
    
    data . nan_count = nan_count
    if (config . do_display_the_number_of_nans):
        print ("Nans: " + str (data . nan_count))
    return
    


def apply_instruction_exit (config, data, arguments):
    print (arguments [0])
    sys . exit (0)
    #raise Exception (arguments [0])
    return

def apply_instruction_is_in_annulus (config, data, arguments):
    source_name = arguments [3] [0]
    destination_name = arguments [4] [0]
    array_source = data . variables [source_name]
    array_destination = (data . variables [destination_name])
    map_parameters = (arguments [0], arguments [1], arguments [2])
    apply_map = (
        lambda p, z :
        1 if GeometricTests . check_if_is_in_annulus (p, z) else 0)
    GridsAndArrays . apply_map_on_array (
        config . drawings_config . image_width,
        config . drawings_config . image_height,
        apply_map,
        map_parameters,
        array_source,
        array_destination)
    return

def apply_instruction_is_in_disk (config, data, arguments):
    source_name = arguments [2] [0]
    destination_name = arguments [3] [0]
    array_source = data . variables [source_name]
    array_destination = (data . variables [destination_name])
    map_parameters = (arguments [0], arguments [1])
    apply_map = (
        lambda p, z :
        1 if GeometricTests . check_if_is_in_disk (p, z) else 0)
    GridsAndArrays . apply_map_on_array (
        config . drawings_config . image_width,
        config . drawings_config . image_height,
        apply_map,
        map_parameters,
        array_source,
        array_destination)
    return


def apply_instruction_is_in_filled_julia_set (config, data, arguments):
    source_name = arguments [2] [0]
    destination_name = arguments [3] [0]
    array_source = data . variables [source_name]
    array_destination = (data . variables [destination_name])
    map_parameters = (config . polynomial_critical_value,
                      arguments [0],
                      arguments [1])
    apply_map = JuliaSets . simple_julia_loop
    GridsAndArrays . apply_map_on_array (
        config . drawings_config . image_width,
        config . drawings_config . image_height,
        apply_map,
        map_parameters,
        array_source,
        array_destination)
    return

def apply_instruction_is_in_left_half_plane (config, data, arguments):
    # todo: left/right up/down
    raise Exception ("todo")
    GridsAndArrays . apply_map_on_array (
        config . drawings_config . image_width,
        config . drawings_config . image_height,
        apply_map,
        map_parameters,
        array_source,
        array_destination)
    return


def apply_instruction_is_nan (config, data, arguments):
    source_name = arguments [0] [0]
    destination_name = arguments [1] [0]
    array_source = data . variables [source_name]
    array_destination = (data . variables [destination_name])
    map_parameters = ()
    apply_map = lambda p, z : 1 if (math . isnan (z . real)) else 0
    GridsAndArrays . apply_map_on_array (
        config . drawings_config . image_width,
        config . drawings_config . image_height,
        apply_map,
        map_parameters,
        array_source,
        array_destination)
    return

def apply_instruction_iterate_main_map (config, data, arguments):
    config . number_of_iterations = arguments [0]
    grid = data . variables [arguments [1] [0]]
    last_points = data . variables [arguments [2] [0]]
    iterations_before_end = data . variables [arguments [3] [0]]
    stop_values = data . variables [arguments [4] [0]]
    data . compile_test_chain (config . iterations_config)
    nan_count = GridsAndArrays . iterate_map_on_grid (
        # todo: width and height should not belong to drawings
        config . drawings_config . image_width,
        config . drawings_config . image_height,
        config . eval_main_map,
        # todo: what to do with this?
        config . main_map_extra_parameters,
        config . number_of_iterations,
        data . stop_test_chain,
        grid,
        iterations_before_end,
        stop_values,
        last_points)

    data . nan_count = nan_count
    if (config . do_display_the_number_of_nans):
        print ("Nans: " + str (data . nan_count))
        
    return

def apply_instruction_is_where_wrt_annulus (config, data, arguments):
    source_name = arguments [3] [0]
    destination_name = arguments [4] [0]
    array_source = data . variables [source_name]
    array_destination = (data . variables [destination_name])
    map_parameters = (arguments [0], arguments [1], arguments [2])
    apply_map = GeometricTests . compute_position_wrt_annulus
    GridsAndArrays . apply_map_on_array (
        config . drawings_config . image_width,
        config . drawings_config . image_height,
        apply_map,
        map_parameters,
        array_source,
        array_destination)
    return

def apply_instruction_make_grid (config, data, arguments):

    config . update_grid_parameters ()
  
    # reallocate the arrays (all data will be lost)
    data . allocate_arrays (config)

    grid_array = data . variables [arguments [0] [0]]
    # todo: end this mixed up with image_wisht and grid_width etc.
    width = config . drawings_config . image_width
    height = config . drawings_config . image_height
    top = config . region_top
    left = config . region_left
    bottom = config . region_bottom
    right = config . region_right
    sizes = [width, height]
    
    for x in range (width):
        for y in range (height):
            grid_array [x, y]= GridsAndArrays . compute_point (
                sizes,
                top, left, bottom, right,
                [x, y])

    return

def apply_instruction_name (config, data, arguments):
    name = arguments [0]
    config . name = name
    return

def apply_instruction_print_complexes (config, data, arguments):
    text = str (data . variables [arguments [0] [0]])
    print (text)
    return

def apply_instruction_replace_nans (config, data, arguments):
    source_name = arguments [1] [0]
    destination_name = arguments [2] [0]
    array_source = data . variables [source_name]
    array_destination = (data . variables [destination_name])
    map_parameters = (arguments [0], )
    apply_map = (
        lambda p, z :
        p [0]
        if (math . isnan (z . real))
        else z)
    GridsAndArrays . apply_map_on_array (
        config . drawings_config . image_width,
        config . drawings_config . image_height,
        apply_map,
        map_parameters,
        array_source,
        array_destination)    
    return

def apply_instruction_reset_tests (config, data, arguments):
    config . iterations_config . test_list = []
    return

def apply_instruction_set_critical_value (config, data, arguments):
    config . polynomial_critical_value = arguments [0]
    return

def apply_instruction_set_drawing_threshold (config, data, arguments):
    threshold_value = arguments [0]
    #config_data . drawings_config . drawing_type = "threshold"
    config . drawings_config . threshold_value = threshold_value
    return

def apply_instruction_set_drawing_type (config, data, arguments):
    #TODO: check type strings below are valid
    drawing_type = arguments [0]
    drawing_type = convert_drawing_type_from_string (drawing_type)
    config . drawings_config . drawing_type = drawing_type
    #print (config . drawings_config . drawing_type)
    return

def apply_instruction_set_grid_tlbr (config, data, arguments):
    config . region_top = arguments [0]
    config . region_left = arguments [1]
    config . region_bottom = arguments [2]
    config . region_right = arguments [3]
    # todo: check that everything is updated and setup correctly
    # todo: this is done when make_grid is invocked?
    # todo: (including drawings params)
    # config . update_grid_parameters ()
    return

def apply_instruction_set_grid_width (config, data, arguments):
    #raise Exception ("set_grid_width not implemented")
    print ("set_grid_width: don't forget to rebuild the grids with make_grid")
    # todo: need to reallocate the variable arrays
    config . grid_width = arguments [0]
    config . update_grid_parameters ()
    return

def apply_instruction_set_main_map_type (config, data, arguments):
    # NOTE: this is a useless instruction
    config . main_map_type = arguments [0]
    # todo: update map parameters
    # todo: update map pointer
    return

def apply_instruction_set_number_of_indexes (config, data, arguments):
    number_of_indexes = arguments [0]
    config . number_of_indexes = number_of_indexes
    config . compute_index_colors ()
    return
    
def apply_instruction_set_number_of_iterations (config, data, arguments):
    # todo: useless: set_number_of_iterations
    raise Exception ("useless")
    config . number_of_iterations = arguments [0]
    return


def apply_instruction_set_preview_parameters (config, data, arguments):
    preview_config  = config . preview_config
    # todo: need the boolean type:
    preview_config . do_preview = arguments [0]
    # todo: check short name is right (otherwise switch evrytg to short name)
    preview_config . width = arguments [1]
    preview_config . height = arguments [2]
    preview_config . threshold = arguments [3]
    preview_config . white_text = arguments [4]
    preview_config . black_text = arguments [5]
    preview_config . compute_dependent_variables ()
    return

def apply_instruction_set_shade_enhance_power (config, data, arguments):
    shade_enhancement_power = arguments [0]
    #config_data . drawings_config . drawing_type = "shade"
    #config_data . drawings_config . shade_type = (
    #    "smallest values more visible")
    # todo: drawings_config . set_*
    config . drawings_config . shade_enhancement_power = (
        shade_enhancement_power)
    return


def apply_instruction_set_shade_max (config, data, arguments):
    shade_max = arguments [0]
    if (shade_max == "compute"):
        config . drawings_config . variable_to_use_as_max = ("compute max")
    elif (shade_max == "nb_iterations"):
        config . drawings_config . variable_to_use_as_max = ("nb_iterations")
    else:
        config . drawings_config . variable_to_use_as_max = ("explicit real")
        config . drawings_config . max_value = float (shade_max)
    return

def apply_instruction_set_shade_type (config, data, arguments):
    shade_type = arguments [0]
    #config_data . drawings_config . drawing_type = "shade"
    # todo:convert_shade_type_from_program 
    config . drawings_config . shade_type = (
        convert_shade_type_from_program (shade_type))
    return

def apply_instruction_set_smooth_argument (config, data, arguments):
    config . drawings_config . do_smooth_argument = arguments [0]
    return

def apply_instruction_setup_fatou_inverse_data (config, data, arguments):
    # todo: is that all?
    rescaling_factor = arguments [0]
    large_real_part = arguments [1]
    config . main_map_object = FatouInverseMaps . SimpleFatouInverseMap (
        {"large real part" : large_real_part})
    config . main_map_extra_parameters = rescaling_factor
    config . eval_main_map = (
        config . main_map_object . eval_rescaled_inverse_fatou_coordinates)
    return


def apply_instruction_setup_linearizer_data (config, data, arguments):
    # todo: escape radius and approx_etc not set by this command
    config . fixed_point_choice = arguments [0]
    config . main_map_rescaling = arguments [1]
    config . linearizer_power_series_radius = arguments [2]
    config . linearizer_power_series_order = arguments [3]
    # TODO: LinearizerMaps is not reentrant
    #     the command below will set up the power series coefficients
    #     as global variables inside that module
    (config . fixed_point, config . fixed_point_multiplier) = (
        LinearizerMaps . setup_linearizer_computations_parameters (
            config . polynomial_critical_value,
            (config . fixed_point_choice != 0),
            config . linearizer_power_series_radius,
            config . linearizer_power_series_order,
            config . polynomial_escape_radius,
            config . polynomial_approx_by_hot_radius))
    config . abs_multiplier = abs (config . fixed_point_multiplier)
    config . eval_main_map = LinearizerMaps . eval_rescaled_linearizer
    config . main_map_extra_parameters = config . main_map_rescaling
    # todo:
    config . main_map_object = None
    return

def apply_instruction_show_help (config, data, arguments):
    instruction_to_explain = arguments [0]
    (show_instruction_help [instruction_to_explain]) ()
    return
# -----------------------------------------------------------------------------

def show_all_help ():
    for show_help in show_instruction_help:
        if (show_help == "*"):
            continue
        show_instruction_help [show_help] ()
    return

def show_help_nop ():
    print ("nope")
    return

def show_help_abs ():
    print ("abs src, dest")
    print ("  src = complex table,")
    print ("  dest = real table")
    return

def show_help_exit ():
    print ("exit message")
    print ("  message = string")
    return

def show_help_show_help ():
    print ("\"haha\"")
    return

# -----------------------------------------------------------------------------



instruction_dictionary = {
    "nop" : apply_instruction_nop,
    "abs" : apply_instruction_abs,
    "add_test_enter_disk" : apply_instruction_add_test_enter_disk,
    "add_test_leave_annulus" : apply_instruction_add_test_leave_annulus,
    "add_test_leave_disk" : apply_instruction_add_test_leave_disk,
    "add_test_leave_left_half_plane" :
    apply_instruction_add_test_leave_left_half_plane,
    "add_test_leave_right_half_plane" :
    apply_instruction_add_test_leave_right_half_plane,
    "annulus_index" : apply_instruction_annulus_index,
    "arg" : apply_instruction_arg,
    "arg_density" : apply_instruction_arg_density,
    "boundaries" : apply_instruction_boundaries,
    "cauliflower_julia" : apply_instruction_cauliflower_julia,
    "coord_rect" : apply_instruction_coord_rect,
    "draw_complex_density" : apply_instruction_draw_complex_density,
    "draw_density" : apply_instruction_draw_density,
    "draw_indexes" : apply_instruction_draw_indexes,
    "draw_integers" : apply_instruction_draw_integers,
    "draw_reals" : apply_instruction_draw_reals,
    "eval_main_map" : apply_instruction_eval_main_map,
    "exit" : apply_instruction_exit,
    "iterate_main_map" : apply_instruction_iterate_main_map,
    "is_in_annulus" : apply_instruction_is_in_annulus,
    "is_in_disk" : apply_instruction_is_in_disk,
    "is_in_filled_julia_set" : apply_instruction_is_in_filled_julia_set,
    "is_nan" : apply_instruction_is_nan,
    "is_where_wrt_annulus" : apply_instruction_is_where_wrt_annulus,
    "make_grid" : apply_instruction_make_grid,
    "name" : apply_instruction_name,
    "print_complexes" : apply_instruction_print_complexes,
    "replace_nans" : apply_instruction_replace_nans,
    "reset_tests" : apply_instruction_reset_tests,
    "set_critical_value" : apply_instruction_set_critical_value,
    "set_drawing_threshold" : apply_instruction_set_drawing_threshold,
    "set_drawing_type" : apply_instruction_set_drawing_type,
    "set_grid_tlbr" : apply_instruction_set_grid_tlbr,
    "set_grid_width" : apply_instruction_set_grid_width,
    "set_main_map_type" : apply_instruction_set_main_map_type,
    "set_number_of_indexes" : apply_instruction_set_number_of_indexes,
    "set_preview_parameters" : apply_instruction_set_preview_parameters,
    "set_shade_type" : apply_instruction_set_shade_type,
    "set_shade_enhance_power" : apply_instruction_set_shade_enhance_power,
    "set_shade_max" : apply_instruction_set_shade_max,
    "set_smooth_argument" : apply_instruction_set_smooth_argument,
    "setup_fatou_inverse_data" : apply_instruction_setup_fatou_inverse_data,
    "setup_linearizer_data" : apply_instruction_setup_linearizer_data,
    "show_help" : apply_instruction_show_help,
}
# TODO
"""
    "load_complexes" : apply_instruction_load_complexes,
    "load_integers" : apply_instruction_load_integers,
    "load_reals" : apply_instruction_load_reals,
    "save_complexes" : apply_instruction_save_complexes,
    "save_integers" : apply_instruction_save_integers,
    "save_reals" : apply_instruction_save_reals,
(27)
"""

#todo: in a distant future

show_instruction_help = {
    "*" : show_all_help,
    "nop" : show_help_nop,
    "abs" : show_help_abs,
    "exit" : show_help_exit,
    "show_help" : show_help_show_help,
}
"""
    "add_test_enter_disk" : show_help_add_test_enter_disk,
    "add_test_leave_annulus" : show_help_add_test_leave_annulus,
    "add_test_leave_disk" : show_help_add_test_leave_disk,
    "add_test_leave_left_half_plane" : show_help_add_test_leave_left_half_plane,
    "annulus_index" : show_help_annulus_index,
    "arg" : show_help_arg,
    "arg_density" : show_help_arg_density,
    "boundaries" : show_help_boundaries,
    "cauliflower_julia" : show_help_cauliflower_julia,
    "coord_rect" : show_help_coord_rect,
    "draw_complex_density" : show_help_draw_complex_density,
    "draw_density" : show_help_draw_density,
    "draw_integers" : show_help_draw_integers,
    "draw_reals" : show_help_draw_reals,
    "eval_main_map" : show_help_eval_main_map,
"""
"""
    "is_in_annulus" : show_help_is_in_annulus,
    "is_in_disk" : show_help_is_in_disk,
    "is_in_filled_julia_set" : show_help_is_in_filled_julia_set,
    "is_nan" : show_help_is_nan,
    "is_where_wrt_annulus" : show_help_is_where_wrt_annulus,
    "iterate_main_map" : show_help_iterate_main_map,
    "load_complexes" : show_help_load_complexes,
    "load_integers" : show_help_load_integers,
    "load_reals" : show_help_load_reals,
    "make_grid" : show_help_make_grid,
    "name" : show_help_name,
    "replace_nans" : show_help_replace_nans,
    "reset_tests" : show_help_reset_tests,
    "save_complexes" : show_help_save_complexes,
    "save_integers" : show_help_save_integers,
    "save_reals" : show_help_save_reals,
    "set_critical_value" : show_help_set_critical_value,
    "set_drawing_threshold" : show_help_set_drawing_threshold,
    "set_drawing_type" : show_help_set_drawing_type,
    "set_grid_tlbr" : show_help_set_grid_tlbr,
    "set_grid_width" : show_help_set_grid_width,
    "set_main_map_type" : show_help_set_main_map_type,
    "set_preview_parameters" : show_help_set_preview_parameters,
    "set_shade_type" : show_help_set_shade_type,
    "set_shade_enhance_power" : show_help_set_shade_enhance_power,
    "set_shade_max" : show_help_set_shade_max,
    "set_smooth_argument" : show_help_set_smooth_argument,
    "setup_fatou_inverse_data" : show_help_set_fatou_inverse_data,
    "setup_linearizer_data" : show_help_set_linearizer_data,
"""

