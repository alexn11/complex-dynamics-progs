
import math


def check_if_is_in_disk (disk_data, z):
    (center, radius) = disk_data
    z_radius = abs (z - center)
    return (z_radius <= radius)

def check_if_is_not_in_disk (disk_data, z):
    (center, radius) = disk_data
    z_radius = abs (z - center)
    return (z_radius > radius)

def check_if_is_not_in_annulus (annulus_data, z):
    (center, inner_radius, outer_radius) = annulus_data
    z_radius = abs (z - center)
    return ((z_radius < inner_radius)
            or (z_radius > outer_radius))

def check_if_is_in_annulus (annulus_data, z):
    (center, inner_radius, outer_radius) = annulus_data
    z_radius = abs (z - center)
    return ((z_radius > inner_radius)
            and (z_radius < outer_radius))


def check_if_is_in_right_half_plane (right_half_plane_data, z):
    return (z . real > right_half_plane_data [0])

def check_if_is_in_left_half_plane (left_half_plane_data, z):
    return (z . real < left_half_plane_data [0])


def compute_position_wrt_annulus (annulus_data, z):
    (center, inner_radius, outer_radius) = annulus_data
    z_radius = abs (z - center)
    if (z_radius < inner_radius):
        position = 0
    elif (z_radius <= outer_radius):
        position = 1
    else:
        position = 2
    return position



# --- extra -------------------------------------------------------------------

def compute_disk_index (smallest_disk_radius,
                        radius_multiplicator_log_inverse,
                        abs_z):
    if (abs_z < smallest_disk_radius):
        disk_index = 0
    elif (math . isnan (abs_z)):
        disk_index = 255
    else:
        try:
            disk_index = (
                round (radius_multiplicator_log_inverse
                       * math . log (abs_z / smallest_disk_radius))
                + 1)
        except (RuntimeWarning):
            print (smallest_disk_radius)
            print (abs_z)
            #print (abs_z / smallest_disk_radius)
            #print (math . log (abs_z / smallest_disk_radius))
            raise
        #if (disk_index > 2):
        #    print (disk_index)
        if (disk_index > 255):
            disk_index = 255
    return disk_index

def compute_annulus_index (parameters, z):
    # it's bad to have similar names but different functioning!
    # it is also bad to use disk whils it should be annulus
    return compute_disk_index (parameters [0],
                               parameters [1],
                               abs (z))



def check_if_in_rectangle (rectangle, z):
    return ((rectangle . left <= z . real <= rectangle . right)
            and (rectangle . bottom <= z . imag <= rectangle . top))
        
def compute_coordinate_wrt_rectangle (rectangle, z):
    return (
        (rectangle . horizontal_coefficient
         * (z . real - rectangle . left))
        + 1.j * (rectangle . vertical_coefficient
                 * (z . imag - rectangle . bottom)))

def compute_rectangle_coordinates (rectangle_data, z):
    rectangle_object = rectangle_data
    rectangle_coordinates = - 1. - 1.j
    if (check_if_in_rectangle (rectangle_object, z)):
        rectangle_coordinates = (
            compute_coordinate_wrt_rectangle (rectangle_object, z))
    return rectangle_coordinates


def check_if_in_disk (center, radius, z):
    return abs (z - center) <= radius

def eval_where_is_wrt_disk (center, radius, z):
    return 0 if (abs (z - center) <= radius) else 1

def check_if_is_in_annulus_basic (center, r_ext, r_int, z):
    abs_z_minus_center = abs (z - center)
    return r_int < abs_z_minus_center <= r_ext

def eval_where_is_wrt_annulus_at_0 (r_int, r_ext, z):
    abs_z = abs (z)
    if (abs_z < r_int):
        where_is = -1
    elif (abs_z > r_ext):
        where_is = 1
    else:
        where_is = 0
    return where_is


def check_point_band_position (band_parameters, z):
    b = FatouInverseMaps . compute_band_distance_to_0 (band_parameters [0],
                                                       band_parameters [1],
                                                       z)
    #if (b == -1):
    #    b = 0
    return b

