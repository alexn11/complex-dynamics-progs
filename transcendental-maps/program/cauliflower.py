

# TODO: change names

state_unknown = 2
state_filled_julia_set = 0
state_basin_of_infinity = 1

def eval_f (z):
    return z * z + z

def eval_F (z):
    return z + 1 + 1 / z


def check_if_in_safe_rectangle (z):
    x = z . real
    if ((x < -1) or (x > 0)):
        return False
    abs_y = abs (z . imag)
    return (abs_y <= 0.866)

def check_if_outside_safe_disk (z):
    return (abs (z + 0.5) >= 1.5)

def check_if_under_safe_parabolas (z):
    x = z . real
    if (x <= 0):
        return False
    abs_y = abs (z . imag)
    return (abs_y <= (0.07142857 * x * x))

def check_if_surely_in_filled_julia_set (z):
    return check_if_in_safe_rectangle (z)

def check_if_surely_in_basin_of_infinity (z):
    if (check_if_outside_safe_disk (z)):
        return True
    return check_if_under_safe_parabolas (z)

def check_if_already_in_surely_known_state (z):
    if (check_if_surely_in_filled_julia_set (z)):
        return state_filled_julia_set
    if (check_if_surely_in_basin_of_infinity (z)):
        return state_basin_of_infinity
    return state_unknown

def check_point_position_wrt_dynamics (nb_max_it, z):
    it = 0
    position = check_if_already_in_surely_known_state (z)
    while ((it < nb_max_it) and (position == state_unknown)):
        it += 1
        z = eval_f (z)
        position = check_if_already_in_surely_known_state (z)
    #print (" after " + str (it) + " found : " + str (position))
    return position
