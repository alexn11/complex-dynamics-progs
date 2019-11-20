# Author:  alexn11 (alexn11.gh@gmail.com)
# Created: 2019-11-19
# Copyright (C) 2019, Alexandre De Zotti
# License: MIT License

# distutils: language=c++

"""
 compile with

python setup.py build_ext --inplace


 run example:
python tongues-usingc.py tongues-straight-sine.conf 

"""



import cython

from libc . math cimport sin
from libc . math cimport pi
from libcpp . vector cimport vector

import numpy
cimport numpy

"""
Constants
"""

cdef double two_pi
two_pi = 2. * pi



"""
Functions
"""

cdef double compute_mod_1 (double x):
    return x % 1.




# tent

cdef double eval_tent (double x):
    return 2. * x if (x <= 0.5) else 2. * (1. - x)

# this is important to evaluate the tent map mod 1
# otherwise the map doesn't go to the quotient mod 1
cdef double eval_tent_mod_1 (double x):
    return eval_tent (compute_mod_1 (x))

"""
cdef double eval_diff_tent (double x):
    return 2. if (x <= 0.5) else -2.
"""

cdef double eval_lifted_doubling_plus_tent (double a, double b, double x):
    return 2. * x + a + b * eval_tent_mod_1 (x)

cdef double eval_doubling_plus_tent (double a, double b, double x):
    y = eval_lifted_doubling_plus_tent (a, b, x)
    return compute_mod_1 (y)

"""
cdef double eval_diff_doubling_plus_tent (double a, double b, double x):
    return 2. + b * eval_diff_tent (x)
"""

# dsm

cdef double eval_lifted_dsm (double a, double b, double x):
    return 2. * x + a - (b / pi) * sin (two_pi * x)

cdef double eval_dsm (double a, double b, double x):
    return compute_mod_1 (eval_lifted_dsm (a, b, x)) 

# double dsm

cdef double eval_lifted_double_dsm (double a, double b, double x):
    return 2. * x + a - (b / (2. * pi)) * sin (2. * two_pi * x)

cdef double eval_double_dsm (double a, double b, double x):
    return compute_mod_1 (eval_lifted_double_dsm (a, b, x)) 


# straight sine

cdef double eval_straight_sine (double x):
  cdef double y
  x = x % 1.
  if (x <= 0.5):
    y = 4. * x - 1.
  else:
    y = -4. * x + 3.
  #if (x <= 0.25):
  #  y = 4. * x
  #elif (x <= 0.75):
  #  y = 2. - 4. * x
  #else:
  #  y = 4. * x - 4.
  return y

cdef double eval_lifted_doubling_plus_straight_sine (double a, double b, double x):
  return 2. * x + a + 0.5 * b * eval_straight_sine (x)

cdef double eval_doubling_plus_straight_sine (double a, double b, double x):
  return eval_lifted_doubling_plus_straight_sine (a, b, x) % 1.







# simpler than trying to understand how to use any_of with a vector in cython
cdef any_bool_vector (vector [int] & v):
  cdef int size, i, is_any
  size = v . size ()
  is_any = 0
  for i in range (size):
    if (v [i] == 0):
      continue
    is_any = 1
    break
  return is_any

# same
cdef naive_int_sum (vector [int] & v):
  cdef int size, i, s
  size = v . size ()
  s = 0
  for i in range (size):
    s += v [i]
  return s
  


"""
USAGE

instantiate
set_dynamics_params
create_tongue_picture
use numpy arrays: parameters_grid, parameters_fates, parameters_periods

"""

cdef class tongue_system:

  cdef public mapping_family
  cdef public double a, b
  cdef double (* eval_map) (double, double, double)
  cdef double (* eval_lifted_map) (double, double, double)

  cdef public double default_starting_point
  cdef public int orbit_initial_segment_length
  cdef public int orbit_final_segment_length
  cdef public int max_period_to_test
  cdef public double period_test_tol
  cdef public int number_of_orbits_to_compute
  cdef public int do_save_last_iterates

  cdef vector [double] starting_points
  cdef vector [double] ending_points
  cdef vector [int] periodicity_test_results
  cdef vector [int] periods
  cdef int number_of_starting_points
  cdef double starting_points_sep

  cdef public numpy . ndarray parameters_grid
  cdef public numpy . ndarray parameters_fates
  cdef public numpy . ndarray parameters_periods
  cdef public numpy . ndarray last_iterates
  cdef public double min_a, max_a, min_b, max_b
  cdef public double step_a, step_b
  cdef public int nb_a, nb_b

  def __init__ (self, mapping_family):

     self . mapping_family = mapping_family

     if ((mapping_family == "dsm") or (mapping_family == "double standard map")):
        self . eval_map = eval_dsm
        self . eval_lifted_map = eval_lifted_dsm
     elif (mapping_family == "double dsm"):
        self . eval_map = eval_double_dsm
        self . eval_lifted_map = eval_lifted_double_dsm
     elif (mapping_family == "doubling plus tent"):
        self . eval_map = eval_doubling_plus_tent
        self . eval_lifted_map = eval_lifted_doubling_plus_tent
     elif (mapping_family == "doubling plus straight sine"):
        self . eval_map = eval_doubling_plus_straight_sine
        self . eval_lifted_map = eval_lifted_doubling_plus_straight_sine
     else:
        raise Exception ("Unknown map family: " + mapping_family)

     self . set_dynamics_params ()


  def compute_image_by_map (self, a, b, x):
    return self . eval_map (a, b, x)

  def compute_image_by_lifted_map (self, a, b, x):
    return self . eval_lifted_map (a, b, x)


  def set_dynamics_params (self,
                           default_starting_point = 0.,
                           number_of_orbits_to_compute = 1,
                           orbit_initial_segment_length = 0,
                           orbit_final_segment_length = 10,
                           max_period_to_test = 10,
                           period_test_tol = 1.E-4,
                           do_save_last_iterates = False):




     self . default_starting_point = default_starting_point
     self . number_of_orbits_to_compute = number_of_orbits_to_compute
     self . number_of_starting_points = self . number_of_orbits_to_compute
     self . starting_points_sep = 1. / self . number_of_starting_points
     self . orbit_initial_segment_length = orbit_initial_segment_length
     self . orbit_final_segment_length = orbit_final_segment_length
     self . max_period_to_test = max_period_to_test
     self . period_test_tol = period_test_tol
     self . do_save_last_iterates = do_save_last_iterates




  cpdef double compute_iterate (self, int number_of_iterations, double starting_point):
    cdef double end_point
    cdef int it
    end_point = starting_point
    for it in range (number_of_iterations):
        end_point = self . eval_map (self . a, self . b, end_point)
    return end_point


  cdef vector [int] check_if_approximately_periodic (self, vector [double] & orbit):
    cdef int period
    cdef int is_periodic
    cdef vector [int] res
    is_periodic = 0
    for period in range (1, self . max_period_to_test + 1):
       if (abs (orbit [0] - orbit [period]) <= self . period_test_tol):
         is_periodic = 1
         break
    if (is_periodic == 0):
      period = 0
    res . push_back (is_periodic)
    res . push_back (period)
    return res


  cdef compute_iteration_starting_points (self):
    cdef int starting_point_index
    self . starting_points . clear ()
    for starting_point_index in range (self . number_of_starting_points):
      self . starting_points . push_back ((self . default_starting_point + starting_point_index * self . starting_points_sep) % 1.)



  cpdef determine_parameter_global_dynamics (self, vector [int] & periodicity_test_results, vector [int] & periods, vector [double] & end_points):

    cdef int starting_point_index

    end_points . clear ()

    self . compute_iteration_starting_points ()

    for starting_point_index in range (self . number_of_starting_points):
      end_points . push_back (self . compute_iterate (self . orbit_initial_segment_length, self . starting_points [starting_point_index]))    

    self . starting_points . clear ()
    self . starting_points = end_points
    self . compute_periodicities (periodicity_test_results, periods)
    




  cdef compute_periodicities (self, vector [int] & is_periodic, vector [int] & periods):

    cdef vector [double] orbit
    cdef int it, starting_point_index

    is_periodic . clear ()
    periods . clear ()

    for starting_point_index in range (self . number_of_starting_points):
        starting_point = self . starting_points [starting_point_index]
        orbit . push_back (starting_point)
        for it in range (1, self . max_period_to_test + 1):
           orbit . push_back (self . eval_map (self . a, self . b, orbit [it - 1]))
        check_results = self . check_if_approximately_periodic (orbit)
        is_periodic . push_back (check_results [0])
        periods . push_back (check_results [1])

  cdef void set_grid_parameters (self, int image_width, int image_height, double min_a, double max_a, double min_b, double max_b):
    self . min_a = min_a
    self . max_a = max_a
    self . min_b = min_b
    self . max_b = max_b
    self . nb_a = image_width
    self . nb_b = image_height
    self . step_a = (max_a - min_a) / self . nb_a
    self . step_b = (max_b - min_b) / self . nb_b


  cpdef void compute_parameters_grid (self):

    cdef int a_index, b_index
    cdef double a, b

    self . parameters_grid = numpy . zeros ([ self . nb_a, self . nb_b ], dtype = "complex")

    for a_index in range (self . nb_a):
      a = self . min_a + a_index * self . step_a
      for b_index in range (self . nb_b):
        b = self . max_b - b_index * self . step_b
        self . parameters_grid [ a_index, b_index ] = a + 1.j * b


  def compute_starting_points (self):
    self . compute_iteration_starting_points ()
    starting_points = [ self . starting_points [i] for i in range (self . number_of_starting_points) ]
    return starting_points

  def apply_map (self, x):
    return self . eval_map (self . a, self . b, x)

  def set_parameters_values (self, a, b):
    self . a = a
    self . b = b

  def compute_grid_parameters (self, image_width, image_height, min_a, max_a, min_b, max_b):
    self . set_grid_parameters (image_width, image_height, min_a, max_a, min_b, max_b)


  def create_tongue_picture (self, image_width, image_height, min_a, max_a, min_b, max_b):

    cdef int a_index, b_index
    cdef double complex parameters
    cdef vector [double] current_last_iterates
    cdef int p

    self . set_grid_parameters (image_width, image_height, min_a, max_a, min_b, max_b)

    self . compute_parameters_grid ()

    self . parameters_fates = numpy . zeros ([ self . nb_a, self . nb_b ], dtype = "int")
    self . parameters_periods = numpy . zeros ([ self . nb_a, self . nb_b ], dtype = "int")
    if (self . do_save_last_iterates):
      self . last_iterates = numpy . zeros ([ self . nb_a, self . nb_b, self . number_of_starting_points ], dtype = "double")

    for a_index in range (self . nb_a):
       for b_index in range (self . nb_b):
           parameters = self . parameters_grid [ a_index, b_index ]
           self . a = parameters . real
           self . b = parameters . imag
           self . periodicity_test_results . clear ()
           self . periods . clear ()
           self . determine_parameter_global_dynamics (self . periodicity_test_results, self . periods, current_last_iterates)
           if (self . do_save_last_iterates):
             for p in range (self . number_of_starting_points):
               self . last_iterates [ a_index, b_index, p ] = current_last_iterates [ p ]
           self . parameters_fates [ a_index, b_index ] = 1 if any_bool_vector (self . periodicity_test_results) else 0
           self . parameters_periods [ a_index, b_index ] = naive_int_sum (self . periods)









