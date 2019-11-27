

import math
import cmath


# todo: put the rescaling constant inside the map class
# implement the class

class SimpleLinearizerMap:
    # TODO: work in progress
    def __init__ (self,
                  c,
                  fixed_point_index):
        self . polynomial_critical_value = c
        self . fixed_point_index = fixed_point_index
        self . eval_polynomial = (
            lambda z : z * z + self . polynomial_critical_value)
        self . compute_fixed_point_and_multiplier ()
        self . compute_polynomial_radii ()
        self . compute_power_series_parameters ()
        self . compute_other_stuff ()
        return

    def compute_other_stuff (self):
        # Arbitrary claim: exp (103) = infty
        # TODO: 103 should be user defined
        #self . exponent_after_which_power_will_explode = (
        #    math . log (103. / math . log (replace_map_by_monomial_radius))
        #    / math . log (2.))
        return

    
    def compute_power_series_radius (self, power_series_radius):
        if (power_series_radius <= 0):
            self . power_series_radius = (
                0.1
                * self . abs_multiplier_inverse
                * abs (self . fixed_point - self . polynomial_critical_value))
        else:
            self . power_series_radius = power_series_radius
        self . power_series_radius_inverse = 1. / self . power_series_radius
        return

    def compute_power_series_coefficients (self):
        if (self . power_series_order >= 2):
            self . order_two_term_factor = (
                1. / (self . multiplier * (multiplier - 1.)))
            self . inverse_order_two_term_factor = (
                - 1. / (self . multiplier * (multiplier - 1)))
        if (self . power_series_order >= 3):
            self . order_three_term_factor = (
                2.
                * self . order_two_term_factor
                * self . order_two_term_factor
                / (self . multiplier + 1.))
            self . inverse_order_three_term_factor = (
                - 2.
                * self . inverse_order_two_term_factor
                / (multiplier ** 2 - 1))
        if (self . power_series_order >= 4):
            # I haven't checked this one:
            self . order_four_term_factor = (
                (self . order_two_term_factor * self . order_two_term_factor
                 + 2. * self . order_three_term_factor)
                / (self . multiplier * (self . multiplier ** 3 - 1)))
            self . inverse_order_four_term_factor = (
                (- self . inverse_order_two_term_factor / self . multiplier
                 - 3. * self . inverse_order_three_term_factor)
                / (self . multiplier ** 3 - 1))
            
        return

    def compute_power_series_parameters (self, power_series_order):
        self . power_series_order = power_series_order
        self . compute_power_series_radius ()
        self . compute_power_series_coefficients ()
        return
    
    def compute_fixed_point_and_multiplier (self):
        (self . fixed_point,
         self . multiplier) = compute_the_fixed_point_and_the_multiplier (
             self . polynomial_critical_value,
             self . fixed_point_index == 1)
        self . abs_multiplier = abs (self . multiplier)
        self . multiplier_inverse = 1. / self . multiplier
        self . abs_multiplier_inverse = abs (self . multiplier_inverse)
        self . log_abs_multiplier_inverse = (
            1. / math . log (abs (self . multiplier)))
        return

    def compute_polynomial_radii (self):
        self . polynomial_escape_radius = 2. * abs (c) + 2.
        return



def eval_quadratic_polynomial (z):
    return z * z + polynomial_critical_value

def compute_preimages_by_quadratic_polynomial (z):
    first_preimage = cmath . sqrt (z - polynomial_critical_value)
    return (first_preimage, - first_preimage)

def compute_iterated_preimages_by_polynomial (z, nb_it):
    preimage_list = [z]
    previous_preimages = [z]
    for it in range (nb_it):
        new_preimages = []
        for w in previous_preimages:
            new_preimages += (
                list (compute_preimages_by_quadratic_polynomial (w)))
        preimage_list += new_preimages
    return preimage_list

def compute_the_fixed_point_and_the_multiplier (
        critical_value,
        do_use_the_other_fixed_point):

    discriminant = cmath . sqrt (1.0 - 4.0 * critical_value)
    multiplier = 1.0 - discriminant
    if (abs (multiplier) < 1.0):
        multiplier = 1.0 + discriminant
    elif (do_use_the_other_fixed_point):
        the_other_multiplier = 1.0 + discriminant
        if (abs (the_other_multiplier) > 1.):
            multiplier = the_other_multiplier
        else:
            print ("Warning:"
                   + "tried to force the choice of a nonrepelling fixed point")
            raise Exception ("Wrong instructions")

    fixed_point = 0.5 * multiplier

    return fixed_point, multiplier


def setup_linearizer_computations_parameters (
        input_polynomial_critical_value,
        do_use_the_other_fixed_point,
        input_power_series_approximation_radius,
        input_power_series_order,
        input_polynomial_escape_radius,
        input_replace_map_by_monomial_radius,
        input_function_wild_zone_radius = 100.,
        input_function_too_large_value = 10000.):

    global fixed_point
    global multiplier
    global polynomial_critical_value
    global power_series_approximation_radius
    global power_series_order
    global polynomial_escape_radius
    global polynomial_critical_value
    global exponent_after_which_power_will_explode
    global eval_map
    global inverse_r0
    global inverse_log_abs_multiplier
    global multiplier_inverse
    global order_two_term_factor
    global order_three_term_factor
    global order_four_term_factor
    global function_wild_zone_radius
    global function_too_large_value
    global replace_map_by_monomial_radius
    global inverse_order_two_term_factor
    global inverse_order_three_term_factor
    global inverse_order_four_term_factor

    polynomial_critical_value = input_polynomial_critical_value
    power_series_approximation_radius = input_power_series_approximation_radius
    power_series_order = input_power_series_order
    polynomial_escape_radius = input_polynomial_escape_radius
    function_wild_zone_radius = input_function_wild_zone_radius
    function_too_large_value = input_function_too_large_value
    replace_map_by_monomial_radius = input_replace_map_by_monomial_radius
    
    fixed_point, multiplier = compute_the_fixed_point_and_the_multiplier (
        polynomial_critical_value,
        do_use_the_other_fixed_point)

    # ditch the lambdas?
    #eval_map = eval_quadratic_polynomial
    eval_map = lambda z : z * z + polynomial_critical_value

    inverse_r0 = 1. / power_series_approximation_radius

    multiplier_inverse = 1. / multiplier
    
    inverse_log_abs_multiplier = 1. / math . log (abs (multiplier))

    # Arbitrary claim: exp (103) = infty
    # TODO: 103 should be user defined
    exponent_after_which_power_will_explode = (
        math . log (103. / math . log (replace_map_by_monomial_radius))
        / math . log (2.))

    if (power_series_order >= 2):
        order_two_term_factor = 1. / (multiplier * (multiplier - 1.))
        inverse_order_two_term_factor = - 1. / (multiplier * (multiplier - 1))
    if (power_series_order >= 3):
        order_three_term_factor = (
            2. * order_two_term_factor * order_two_term_factor
            / (multiplier + 1.))
        inverse_order_three_term_factor = (
            - 2.
            * inverse_order_two_term_factor
            / (multiplier ** 2 - 1))
    if (power_series_order >= 4):
        # I haven't checked this one:
        order_four_term_factor = (
            (order_two_term_factor * order_two_term_factor
             + 2. * order_three_term_factor)
            / (multiplier * (multiplier ** 3 - 1)))
        inverse_order_four_term_factor = (
            (- inverse_order_two_term_factor / multiplier
             - 3. * inverse_order_three_term_factor)
            / (multiplier ** 3 - 1))
            

    return fixed_point, multiplier



def compute_map_iterate (nb_it, z):
    # TODO: update this code
    iterated_image = z
    it = 0
    while (it < nb_it):
        if (abs (iterated_image) > replace_map_by_monomial_radius):
            if ((nb_it - it) > exponent_after_which_power_will_explode):
                iterated_image = float ("NaN")
            else:
                try:
                    iterated_image = pow (iterated_image, pow (2, nb_it - it))
                except (OverflowError):
                    iterated_image = float ("NaN")
            it = nb_it
        else:
            iterated_image = eval_map (iterated_image)
            it += 1
    return iterated_image


def compute_map_iterate_and_its_derivative (nb_it, z):
    
    iterated_image = z
    iterated_derivative = 1.
    it = 0
    
    for it in range (nb_it):
        iterated_derivative *= 2. * iterated_image
        try:
            iterated_image = eval_map (iterated_image)
        except (OverflowError):
            iterated_image = float ("NaN")
            break
        
    return iterated_image, iterated_derivative


def eval_linearizer (z):
    return compute_image_by_linearizer (z)


def eval_linearizer_near_0 (u):
    L_u = 0.
    if (power_series_order >= 2):
        u_squared = u * u
        if (power_series_order >= 3):
            if (power_series_order >= 4):
                L_u += order_four_term_factor * u_squared * u_squared
            L_u += order_three_term_factor * u_squared * u
        L_u += order_two_term_factor * u_squared
    L_u +=  u + fixed_point
    return L_u

def eval_linearizer_derivative_near_0 (u):
    DL_u = 0.
    if (power_series_order >= 2):
        if (power_series_order >= 3):
            u_squared = u * u
            if (power_series_order >= 4):
                DL_u += 4. * order_four_term_factor * u_squared * u
            DL_u += 3. * order_three_term_factor * u_squared
        DL_u += 2. * order_two_term_factor * u
    DL_u +=  1.
    return DL_u
    

def eval_linearizer_inverse_near_fixed_point (v):
    u = v - fixed_point
    LI_u = 0.
    if (power_series_order >= 2):
        u_squared = u * u
        if (power_series_order >= 3):
            if (power_series_order >= 4):
                LI_u += inverse_order_four_term_factor * u_squared * u_squared
            LI_u += inverse_order_three_term_factor * u_squared * u
        LI_u += inverse_order_two_term_factor * u_squared
    LI_u +=  u
    return LI_u


def compute_rescaling_for_linearizer (z):
    try:
        rescaling_power = int (
            math . log (abs (z) * inverse_r0) * inverse_log_abs_multiplier)
    except (ValueError):
        return 100000, float ("NaN"), float ("NaN")
    rescaling_factor = pow (multiplier_inverse, rescaling_power)
    z_rescaled = z * rescaling_factor
    return rescaling_power, rescaling_factor, z_rescaled
    

def compute_image_by_linearizer (z):
    if (abs (z) == 0.0):
        image = fixed_point
    else:
        rescaling_power, rescaling_factor, rescaled_z = (
            compute_rescaling_for_linearizer (z))
        
        image_of_rescaled_z = eval_linearizer_near_0 (rescaled_z)

        image = compute_map_iterate (rescaling_power, image_of_rescaled_z)
        
    return image


def compute_linearizer_preimages (z, preimages_level):
    # note: will be completely wrong if preimages_level is too low
    preimages_list = compute_iterated_preimages_by_polynomial (z,
                                                               preimages_level)
    rescaling_factor = pow (multiplier, preimages_level)
    preimages_list = [ rescaling_factor
                       * eval_linearizer_inverse_near_fixed_point (w)
                       for w in preimages_list ]
    return preimages_list




def eval_linearizer_and_its_derivative (z):
    abs_z = abs (z)
    if (abs_z == 0.0):
        image = fixed_point
        derivative = 1.
    elif (math . isnan (abs_z)):
        image = float ("NaN")
        derivative = float ("NaN")
    else:
        rescaling_power, rescaling_factor, z_rescaled = (
            compute_rescaling_for_linearizer (z))

        image_of_rescaled_z = eval_linearizer_near_0 (z_rescaled)
        
        derivative_at_rescaled_z = (
            eval_linearizer_derivative_near_0 (z_rescaled))
        
        image, polynomial_derivative = compute_map_iterate_and_its_derivative (
            rescaling_power,
            image_of_rescaled_z)
        
        derivative = (polynomial_derivative
                      * derivative_at_rescaled_z
                      * rescaling_factor)
        
    return (image, derivative)
    



def eval_normalized_linearizer (z):
    return compute_image_by_linearizer (z)

def eval_rescaled_linearizer (rescaling_factor,
                              z):
    return rescaling_factor * eval_normalized_linearizer (z)
