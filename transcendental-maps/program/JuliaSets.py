

import math


class NotFoundException (Exception):
    pass
class BadKDTRadiusException (Exception):
    pass

default_max_distance = 100000.
sqrt_2 = math . sqrt (2)


def compute_distance_to_discrete_set (list_of_points,
                                      z):
    distance = default_max_distance
    for point in list_of_points:
        try:
            current_distance = abs (point - z)
        except (OverflowError):
            continue
        distance = min (distance, current_distance)
    return distance

def check_if_pixel_lies_inside_disk (pixel_center,
                                     pixel_upper_disk_radius,
                                     disk_center,
                                     disk_radius):
    return (abs (pixel_center - disk_center)
            < disk_radius - pixel_upper_disk_radius)

def check_if_disk_lies_inside_disk (small_disk_center,
                                    small_disk_radius,
                                    big_disk_center,
                                    big_disk_radius):
    return (abs (small_disk_center - big_disk_center)
            < big_disk_radius - small_disk_radius)

def compute_koebe_lower_radius_factor (relative_radius):
    return 1. / (1. + relative_radius) ** 2

def compute_koebe_lower_relative_radius (relative_radius):
    return relative_radius / compute_koebe_lower_radius_factor (relative_radius)

def compute_koebe_upper_radius_factor (relative_radius):
    return 1. / (1. - relative_radius) ** 2

def compute_koebe_upper_relative_radius (relative_radius):
    return relative_radius / compute_koebe_upper_radius_factor (relative_radius)

def compute_data_for_image_estimate (function_singular_set,
                                     pixel_size,
                                     z):
    distance_to_singular_set = compute_distance_to_discrete_set (
        function_singular_set,
        z)
    pixel_radius = 0.5 * pixel_size
    if (distance_to_singular_set < pixel_radius):
        raise BadKDTRadiusException ("")
    relative_radius = pixel_radius / distance_to_singular_set
    return (distance_to_singular_set, relative_radius)


def compute_estimate_disk_from_koebe_data (f_z,
                                           f_prime_z,
                                           distance_to_singular_set,
                                           koebe_relative_radius):
    disk_center = f_z
    disk_radius = (
        distance_to_singular_set
        * koebe_relative_radius
        * abs (f_prime_z))
    return (disk_center, disk_radius)

def compute_lower_estimate_disk (f_z,
                                 f_prime_z,
                                 distance_to_singular_set,
                                 relative_radius):
    koebe_relative_radius = (
        compute_koebe_lower_relative_radius (relative_radius))
    return compute_estimate_disk_from_koebe_data (f_z,
                                                  f_prime_z,
                                                  distance_to_singular_set,
                                                  koebe_relative_radius)

def compute_upper_estimate_disk (f_z,
                                 f_prime_z,
                                 distance_to_singular_set,
                                 relative_radius):
    koebe_relative_radius = (
        compute_koebe_upper_relative_radius (relative_radius))
    return compute_estimate_disk_from_koebe_data (f_z,
                                                  f_prime_z,
                                                  distance_to_singular_set,
                                                  koebe_relative_radius)


def compute_pixel_image_lower_estimate (function_singular_set,
                                        z,
                                        image_of_z,
                                        derivative_at_z,
                                        pixel_size):
    (distance_to_singular_set, relative_radius) = (
        compute_data_for_image_estimate (
            function_singular_set,
            0.5 * pixel_size,
            z))
    
    return compute_lower_estimate_disk (image_of_z,
                                        derivative_at_z,
                                        distance_to_singular_set,
                                        relative_radius)

def compute_disk_image_lower_estimate (function_singular_set,
                                       z,
                                       image_of_z,
                                       derivative_at_z,
                                       disk_radius):
    (distance_to_singular_set, relative_radius) = (
        compute_data_for_image_estimate (
            function_singular_set,
            disk_radius,
            z))

    if (relative_radius >= 1.):
        raise BadKDTRadiusException ("As bad as it sounds.")
    
    return compute_lower_estimate_disk (image_of_z,
                                        derivative_at_z,
                                        distance_to_singular_set,
                                        relative_radius)



def compute_pixel_image_estimate (function_singular_set,
                                  z,
                                  image_of_z,
                                  derivative_at_z,
                                  pixel_size):
    # H.. don't forget to multiply by sqrt_2
    
    return

def find_a_point_in_the_julia_set (eval_function_and_derivative,
                                   function_singular_set,
                                   temptative_points,
                                   closeness_radius,
                                   #min_derivative,
                                   abs_too_large):

    # NOTE: could even estimate the derivative on the whole pixel with koebe
    # NOTE:   for the min_derivative criterion
    # NOTE:   derivative is at least f'(center)*(1-a)/(1+a)^3
    # NOTE:   this would require to externalize the computation of a
    # NOTE: ACTUALLY this is redudant


    #pixel_upper_disk_radius = 0.5 * sqrt_2 * pixel_size

    
    points_found = []
    has_found_points_in_julia_set = False

    nbr_points = len (temptative_points)
    
    pixels_have_a_julia_point = [ False ] * nbr_points
    
    for point_index in range (nbr_points):

        candidate_point = temptative_points [point_index]

        #print ("checking:" + str (candidate_point))
        
        try:
            point_image, derivative = eval_function_and_derivative (
                candidate_point)
        except (OverflowError):
            continue
        if (math . isnan (point_image . real)):
            continue
        
        if (abs (point_image) > abs_too_large):
            continue

        #print ("has: " + str (point_image) + " and " + str (derivative))

        try:
            (image_disk_center, image_disk_radius) = (
                compute_disk_image_lower_estimate (function_singular_set,
                                                   candidate_point,
                                                   point_image,
                                                   derivative,
                                                   closeness_radius))
        except (BadKDTRadiusException):
            continue

        #print ("KDT: D(" + str (image_disk_center)
        #       + ", " + str (image_disk_radius)+")")
            
        is_disk_inside_image = check_if_disk_lies_inside_disk (
            candidate_point,
            closeness_radius,
            image_disk_center,
            image_disk_radius)

        #print ("D ("+str(candidate_point)+", "+str(closeness_radius)+")")
        #print ("*** is or not (" + str (is_disk_inside_image) + ") inside")
        #print ("D ("+str(image_disk_center)+", " + str (image_disk_radius)+")")
        
        if (is_disk_inside_image):
            #if (abs (derivative) > min_derivative):
            print ("x", end = "")
            has_found_points_in_julia_set = True
            points_found . append (candidate_point)
            pixels_have_a_julia_point [point_index] = True
        else:
            print (".", end = "")

    print (" ")
        
    if (not has_found_points_in_julia_set):
        raise NotFoundException (":(")

        
    return points_found, pixels_have_a_julia_point


def compute_image_and_derivative_by_iterate (eval_map_and_derivative,
                                             nb_iterations,
                                             z):
    image_of_z = z
    derivative = 1
    for it in range (nb_iterations):
        image_of_z, next_derivative = eval_map_and_derivative (
            image_of_z)
        derivative *= next_derivative
        
    return (image_of_z, derivative)


def compute_image_of_discrete_set (eval_map,
                                   list_of_points):
    list_of_images = []
    for point in list_of_points:
        try:
            image = eval_map (point)
        except (OverflowError):
            continue
        list_of_images . append (image)
    return list_of_images

def compute_iterates_singular_sets (
        eval_function,
        function_singular_set,
        nbr_iterate):

    # NOTE: does not (and will not) check for (pre)periodicity
    
    function_iterates_singular_sets = [[]]
    
    for it in range (nbr_iterate + 1):
        function_iterates_singular_sets . append (
                function_singular_set
                + compute_image_of_discrete_set (
                    eval_function,
                    function_iterates_singular_sets [-1]))
        
    return function_iterates_singular_sets

def find_some_points_in_the_julia_set (
        eval_function_and_derivative,
        eval_function,
        function_iterates_singular_sets,
        temptative_points,
        closeness_radius,
        #min_derivative,
        max_period,
        abs_too_large):

    nbr_temptative_points = len (temptative_points)
    points_in_the_julia_set = []
    pixels_have_a_julia_point = [ False ] * nbr_temptative_points

    for period_index in range (max_period):
        period = period_index + 1
        if (period == 1):
            eval_iterated_function_and_derivative = eval_function_and_derivative
            #iterated_singular_set = function_singular_set
        else:
            eval_iterated_function_and_derivative = (
                lambda z : compute_image_and_derivative_by_iterate (
                    eval_function_and_derivative,
                    period,
                    z))
            #iterated_singular_set = (
            #    function_singular_set
            #    + compute_image_of_discrete_set (eval_function,
            #                                     iterated_singular_set))
        try:
            points_found, point_flags = find_a_point_in_the_julia_set (
                eval_iterated_function_and_derivative,
                function_iterates_singular_sets [period],
                temptative_points,
                closeness_radius,
                #min_derivative,
                abs_too_large)

        except (NotFoundException):
            pass

        #except (OverflowError):
        #    pass

        #except (BadKDTRadiusException):
        #    pass
    
        else:
            points_in_the_julia_set += points_found
            pixels_have_a_julia_point = [
                p or n
                for (p, n) in zip (pixels_have_a_julia_point, point_flags) ]


    return points_in_the_julia_set, pixels_have_a_julia_point

# NOTE: koebe relative radius computation unnecessary
# TODO: simplify these unnecessary multiplications

def compute_orbit_and_multipliers (eval_map_and_derivative,
                                   max_iteration,
                                   escape_radius,
                                   starting_point):

    orbit = [starting_point] + max_iteration * [0]
    multipliers = [1] + max_iteration * [1]

    for it in range (1, max_iteration + 1):
        try:
            (next_point, derivative) = eval_map_and_derivative (orbit [it - 1])
        except (OverflowError):
            break
        orbit [it] = next_point
        multipliers [it] = derivative * multipliers [it - 1]
        if (abs (next_point) > escape_radius):
            break
    
    return (orbit, multipliers)

def compute_distance_to_julia_set (
        eval_map_and_derivative,
        max_iteration,
        singular_sets,
        base_points,
        distance_from_base_points_to_julia_set,
        escape_radius,
        z):

    #print ("checking dist for " + str (z))
    
    
    orbit, multipliers = compute_orbit_and_multipliers (
        eval_map_and_derivative,
        max_iteration,
        escape_radius,
        z)

    inverse_abs_multipliers = [ 1. / abs (m)
                                for m in multipliers ]

    # Note: if the computation overflowed,
    #       then the length of the orbit is smaller than expected
    orbit_len = len (orbit)
    
    smallest_distance_so_far = compute_distance_to_discrete_set (
        base_points,
        orbit [0])

    #print ("starting with " + str (distance_to_julia_set))
    
    for iterate_index in range (1, orbit_len):

        z = orbit [iterate_index]
        
        distance_to_base_points = (
            compute_distance_to_discrete_set (
                base_points,
                z)
            + distance_from_base_points_to_julia_set)

        distance_to_singular_set = (
            compute_distance_to_discrete_set (
                singular_sets [iterate_index],
                z))

        if (distance_to_singular_set < distance_to_base_points):
            continue

        relative_radius = distance_to_base_points / distance_to_singular_set
        koebe_factor = compute_koebe_upper_radius_factor (relative_radius)
        new_distance_estimate = (koebe_factor
                                 * distance_to_base_points
                                 * inverse_abs_multipliers [iterate_index])
        
        if (new_distance_estimate < smallest_distance_so_far):
            smallest_distance_so_far = new_distance_estimate

    #print ("found dist " + str (distance_to_julia_set))
            
    return smallest_distance_so_far


def compute_orbit_until_escape (eval_map,
                                max_iterate,
                                escape_radius,
                                z):
    orbit = [z]
    has_escaped = False
    for it in range (max_iterate):
        abs_z = abs (z)
        if (abs_z > escape_radius):
            has_escaped = True
            break
        z = eval_map (z)
        orbit . append (z)
    return (has_escaped, it, orbit)


# extra -----------------------------------------------------------------------

def simple_julia_loop (parameters, z):
    has_escaped = 0
    c = parameters [0]
    nb_max_iterations = parameters [1]
    escape_radius = parameters [2]
    for iteration in range (nb_max_iterations):
        if (abs (z) > escape_radius):
            has_escaped = 1
            break
        z = z * z + c
    return has_escaped

