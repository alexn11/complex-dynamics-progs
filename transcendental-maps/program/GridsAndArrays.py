
import math
import sys

# note: modifications...


def compute_point_indexes (window_data, z):
    raise Exception ("brrr")
    # todo: no more dictionary below
    [image_width, image_height] = window_data ["image size"]
    [top, left, bottom, right] = window_data ["tlbr"]
    x = z . real
    if ((x < left) or (x >= right)): return [-1, -1]
    y = z . imag
    if ((y < bottom) or (y >= top)): return [-1, -1]
    return [int ((x - left) * image_width / (right - left)),
            int ((y - bottom) * image_height / (top - bottom))]



def compute_point (image_size, top, left, bottom, right, point_indexes):
    x = left + (right - left) * point_indexes [0] / image_size [0]
    y = bottom + (top - bottom) * point_indexes [1] / image_size [1]
    return x + y * 1.0j





def apply_map_on_array (nbr_x,
                        nbr_y,
                        apply_map,
                        map_parameters,
                        array_source,
                        array_destination):
    # note: then allocating array_destination was useless
    #array_destination = apply_map (map_parameters, array_source)
    for x in range (nbr_x):
        for y in range (nbr_y):
            array_destination [x, y] = apply_map (map_parameters,
                                                  array_source [x, y])
    return

def evaluate_map_on_grid (grid_width,
                          grid_height,
                          eval_map,
                          map_eval_parameters,
                          points,
                          results):

    # note: then allocating array_destination was useless
    #results = eval_map (map_eval_parameters, points)
    #nan_count = numpy . count_nonzero (numpy . isnan (results))

    #print (eval_map)
    #print (map_eval_parameters)
    
    nan_count = 0
    
    for x in range (grid_width):
        
        for y in range (grid_height):
            
            z = points [x, y]
            image = eval_map (map_eval_parameters, z)
            #print (image)
            results [x, y] = image

            if (math . isnan (image . real)):
                nan_count += 1
                
        sys . stdout . write ('.')
        sys . stdout . flush ()
            
    print (" ")

    

    return nan_count

def check_test (test, z):
    return test [0] (test [1], z)

def check_test_chain (test_chain, z):
    for test_index in range (len (test_chain)):
        test = test_chain [test_index]
        if (check_test (test, z)):
            return test_index + 1
    return 0

def iterate_with_test_chain (eval_map,
                             eval_map_parameters,
                             nb_iterations,
                             stop_test_chain,
                             z):
    stop_value = 0
    for it in range (nb_iterations):
        if (math . isnan (z . real)):
            break
        stop_value = check_test_chain (stop_test_chain, z)
        if (stop_value > 0):
            break
        z = eval_map (eval_map_parameters, z)
    return (it, stop_value, z)



def iterate_map_on_grid (grid_width,
                         grid_height,
                         eval_map,
                         eval_map_parameters,
                         nb_iterations,
                         stop_test_chain,
                         points,
                         iterations_before_end,
                         stop_values,
                         results):

    # todo: then no need to allocate iterations_before_end, stop_values, results
    #(iterations_before_end,
    # stop_vales,
    # results) = iterate_with_test_chain (
    #     eval_map,
    #     eval_map_parameters,
    #     nb_iterations,
    #     stop_test_chain,
    #     points)
    #
    #nan_count = numpy . count_nonzero (numpy . isnan (results))



    
    nan_count = 0
    for x in range (grid_width):
        for y in range (grid_height):
            z = points [x, y]

            (it, stop_value, z_final) = iterate_with_test_chain (
                eval_map,
                eval_map_parameters,
                nb_iterations,
                stop_test_chain,
                z)

            #print ("z="+str(z)+", z_final="+str(z_final))

            iterations_before_end [x, y] = it
            stop_values [x, y] = stop_value
            results [x, y] = z_final

            if (math . isnan (z_final . real)):
                nan_count += 1
                
        sys . stdout . write ('.')
        sys . stdout . flush ()
            
    print (" ")
    

    return nan_count

def iterate_with_test_function (eval_map,
                                eval_map_parameters,
                                nb_iterations,
                                stop_test_function,
                                stop_test_parameters,
                                z):
    stop_value = 0
    for it in range (nb_iterations):
        if (math . isnan (z . real)):
            break
        if (stop_test_function (stop_test_parameter, z)):
            stop_value = 1
            break
        z = eval_map (eval_map_parameters, z)
    return (it, stop_value, z)

def iterate_map_on_grid_simple (grid_width,
                                grid_height,
                                eval_map,
                                eval_map_parameters,
                                nb_iterations,
                                stop_test_function,
                                stop_test_parameters,
                                points,
                                iterations_before_end,
                                stop_values,
                                results):

    
    nan_count = 0
    for x in range (grid_width):
        for y in range (grid_height):
            z = points [x, y]

            (it, stop_value, z_final) = iterate_with_test_function (
                eval_map,
                eval_map_parameters,
                nb_iterations,
                stop_test_function,
                stop_test_parameters,
                z)

            iterations_before_end [x, y] = it
            stop_values [x, y] = stop_value
            results [x, y] = z_final

            if (math . isnan (z_final . real)):
                nan_count += 1
                
        sys . stdout . write ('.')
        sys . stdout . flush ()
            
    print (" ")
    

    return nan_count
