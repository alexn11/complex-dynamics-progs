#!/bin/python


#TODO: convert to c++ for better performances

# todo: test back all

# TODO: cobble together the other todos
# TODO: output/input results to/from text file
# TODO: nan color
# TODO: compute multipliers
# TODO: compute lyapunov
# todo: pb with threshold drawing

# NEVER:

#TODO: error message for missing configuration keys
#TODO: help message
#TODO: the number of iterate of pow map considered as resulting in a NaN
#TODO:                                            should be user defined
#TODO: more general compute_pixel_values function


# ----- Imports ---------------------------------------------------------------

import sys
import math
import cmath
import warnings


import numpy

import ezInputConf

import drawings

import LinearizerMaps
import FatouInverseMaps
import JuliaSets
import GeometricTests

import Config
import Data
import Instructions


# ------ Constants ------------------------------------------------------------


pi = 3.141592653589793
two_pi = 2. * pi
two_pi_inverse = 1. / two_pi
sqrt2 = math . sqrt (2.)



# ------ Functions -----------------------------------------------------------



# todo: code kept for what?
            
def eval_map (c, z):
    return z * z + c

def compute_map_inverse_images (c, w, nb_iterates):
    nb_iterations = 2 ** nb_iterates
    step_size = nb_iterations
    print ("nb_iterations = " + str (nb_iterations))
    next_step_size = step_size // 2
    preimages = nb_iterations * [w]
    current_size = 1
    for i in range (nb_iterates - 1):
        for j in range (current_size):
            z = cmath . sqrt (preimages [step_size * j] - c)
            preimages [step_size * j] = z
            preimages [step_size * j + next_step_size] = - z
        step_size = next_step_size
        next_step_size //= 2
        current_size *= 2
    return preimages

# ----------------------------------------------------------------------------


def find_first_iterate_in_fundamental_annulus (A_center,
                                               A_r_ext,
                                               A_r_int,
                                               orbit):
    first_found = -1
    for iterate in range (len (orbit)):
        if (check_if_in_annulus (A_center,
                                 A_r_ext,
                                 A_r_int,
                                 orbit [iterate] [0])):
            first_found = iterate
            break
    return first_found

# -----------------------------------------------------------------------------

# ----- replacing the lambdas -----

def eval_if_in_disk (disk_parameters, z):
    return 1 if GeometricTest . check_if_in_disk (disk_parameters) else 0

def eval_if_in_annulus (annulus_parameters, z):
    return 1 if GeometricTest . check_if_in_annulus (annulus_parameters) else 0

def compute_argument (params, z):
    center = params [0]
    return ((cmath . phase (z - center))) . real + pi

# ----------------------------------


# ------------------------------------------------------------------------------
def exec_instruction (config_data,
                       computations_data,
                       instruction):
    
    # TODO use int instead of string
    #      meanwhile, it's only going to be a very short list,
    #      so it doesn't matter
    
    operator = instruction [0]
    arguments = instruction [1]

    #print ("instruction=")
    #print (instruction)
    #print ("operator=")
    #print (operator)
    #print ("args=")
    #print (arguments)

    print ("Applying instruction: " + str (operator))

    Instructions . instruction_dictionary [operator] (config_data,
                                                      computations_data,
                                                      arguments)
    return


def exec_program (config_data, computations_data):
    
    prog = config_data . program_config . program . instructions
    if (prog == []):
        return
    
    for instruction in prog:
        exec_instruction (config_data,
                          computations_data,
                          instruction)
    return

# -----------------------------------------------------------------------------

# todo: legacy

def compute_images (config_data):
    for z in config_data . points_list_for_compute_image:
        image = (
            config_data . linearizer_rescaling_factor
            * LinearizerMaps . compute_image_by_linearizer (z))
        print (" "
               + str (z)
               + " -> "
               + str (image))

    return

# -----------------------------------------------------------------------------




# ------ main loops ----------------------------------------------------------

# todo: what is that? still useful?

def compute_preimages_main_loop (
        nb_iterations,
        eval_landing_value,
        landing_value_eval_parameters,
        check_if_loop_must_end,
        loop_end_check_parameters,
        compute_next_point,
        next_point_computation_parameters,
        starting_point):
    
    z = starting_point
    landing_value = eval_landing_value (landing_value_eval_parameters,
                                        z)
    is_nan = math . isnan (abs (z))
    
    for it in range (nb_iterations):

        if (is_nan):
            break
        
        do_must_end = check_if_loop_must_end (loop_end_check_parameters,
                                              landing_value,
                                              z)
        if (do_must_end):
            break
        
        z = compute_next_point (next_point_computation_parameters, z)
        
        landing_value = eval_landing_value (landing_value_eval_parameters,
                                            z)
        is_nan = math . isnan (abs (z))
        
    return (it, is_nan, do_must_end, landing_value, z)


def eval_if_in_annulus_at_0_for_loop (annulus_parameters, z):
    return (
        1 if check_if_in_annulus (0.0,
                                  annulus_parameters [0],
                                  annulus_parameters [1],
                                  z)
        else 0 )

def eval_where_is_wrt_annulus_at_0_for_loop (annulus_data, z):
    return eval_where_is_wrt_annulus_at_0 (annulus_inner_radius,
                                           annulus_outer_radius,
                                           z)

def eval_where_is_wrt_disk_for_loop (landing_parameters, z):
    return eval_where_is_wrt_disk (landing_parameters [0],
                                   landing_parameters [1],
                                   z)

def eval_if_in_disk_for_loop (disk_data, z):
    return 1 if check_if_in_disk (disk_data [0], disk_data [1], z) else 0


def eval_if_abs_greater_than_for_loop (param, z):
    return abs (z) > param

def check_if_landing_value_is_0 (landing_value,
                                 ignored_argument,
                                 z_also_ignored):
    return (landing_value == 0)

def check_if_landing_value_is_not_0 (ignored,
                                     landing_value,
                                     also_ignored):
    return not (landing_value == 0)


def eval_abs (ignored, z):
    return abs (z)


# ----------------------------------------------------------------------------

def process_command_line_and_read_config ():
    if (len (sys . argv) > 1):
        if (sys . argv [1] != "-h"):
            config_data = Config . ConfigData (sys . argv [1])
        else:
            print ("Sorry no help.")
            exit (0)
    else:
        print ("Needs a config file as parameter.")
        exit (0)
    return config_data


# ----- Inits ----------------------------------------------------------------


# stop at first issue

warnings . filterwarnings ("error")


# read inputs

config_data = process_command_line_and_read_config ()

# prepare computations

computations_data = Data . Data (config_data)


print (" Fixed point: " + str (config_data . fixed_point))
print (" Multiplier: " + str (config_data . fixed_point_multiplier))
print (" ")

    
# --- main



exec_program (config_data, computations_data)


        



