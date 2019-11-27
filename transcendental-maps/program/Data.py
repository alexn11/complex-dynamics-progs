


import numpy

#import Config
import GeometricTests



class Data:

    def __init__ (self, config):
        
        self . nan_count = 0

        self . allocate_arrays (config)

        # todo, check max is well implemented
        if (config . drawings_config . variable_to_use_as_max == "compute max"):
            # TODO: add parameter to set starting max_value / or not
            self . max_value = 0.

        self . compile_test_chain (config . iterations_config)
            
        return

    def compile_test_chain (self, itconfig):
        
        stop_test_chain = []

        for test in itconfig . test_list:

            test_name = test [0]
            test_parameters = test [1]
            
            if (test_name == "enter_disk"):
                stop_test_chain . append (
                    (GeometricTests . check_if_is_in_disk,
                     test_parameters))
                # params=
                # (itconf . disk_enters_center,
                #  itconf . disk_enters_radius)

            elif (test_name == "leave_annulus"):
                stop_test_chain . append (
                    (GeometricTests . check_if_is_not_in_annulus,
                     test_parameters))
                # params =
                # (itconf . annulus_leaves_center,
                # itconf . annulus_leaves_inner_radius,
                #  itconf . annulus_leaves_outer_radius)

            elif (test_name == "leave_disk"):
                stop_test_chain . append (
                    (GeometricTests . check_if_is_not_in_disk,
                     test_parameters))
                # params=
                # (itconf . disk_leaves_center,
                # itconf . disk_leaves_radius)

            elif (test_name == "leave_left_half_plane"):
                stop_test_chain . append (
                    (GeometricTests . check_if_is_in_right_half_plane,
                     test_parameters))

            elif (test_name == "leave_right_half_plane"):
                stop_test_chain . append (
                    (GeometricTests . check_if_is_in_left_half_plane,
                     test_parameters))


        self . stop_test_chain = stop_test_chain
        return

    def allocate_program_variables (self, config, postprocessing_config):

        image_sizes = config . drawings_config . image_sizes
            
        self . variables = {}
        #print (postprocessing_config . program . requested_variables)
        variables_to_allocate = (
            postprocessing_config . program . requested_variables)
        for var_name in variables_to_allocate:
            var_type = variables_to_allocate [var_name] 
            if (var_type == "integer"):
                allocated_variable = (
                    numpy . zeros (image_sizes, dtype = "int"))
            elif (var_type == "real"):
                allocated_variable = (
                    numpy . zeros (image_sizes, dtype = "double"))
            elif (var_type == "complex"):
                allocated_variable = (
                    numpy . zeros (image_sizes, dtype = "complex"))
            else:
                raise Exception ("Unknown variable type:" + var_type)
            self . variables [var_name] = allocated_variable

        return

    def allocate_arrays (self, config):

        self . allocate_program_variables (config,
                                           config . program_config)
        
        return
        
