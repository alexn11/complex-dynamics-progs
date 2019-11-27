        
import ezInputConf as inp

from Rectangle import *

import processor

# TODO be consistent with inp/ezInputConf
# TODO: rect coord is postpro or drawing?

# todo: in rect coord instruction, need to compute the rectangle as
#       part of the instruction

def insert_into_list_from_order (order_list,
                                 order,
                                 data):
    original_len = len (order_list)
    tuple_to_insert = (order, data)
    if (original_len == 0):
        order_list . append (tuple_to_insert)
        return
    # not optimal but it's going to be a very short list
    # so no point trying to be optimal
    for index in range (original_len):
        if (order < order_list [index] [0]):
            order_list . insert (index, (order, data))
            break
    if (index == original_len):
        order_list . append ((order, data))
    return


class ConfigDataProgram:
            
    def __init__ (self, main_config, config_parser):
        
        try:
            self . program_file_name = (
                inp . convert_string_to_string (
                    config_parser ["Program"] ["program_file_name"]))
        except (KeyError):
            raise Exception ("Obsolete, use legacy programs")
        
        with open (self . program_file_name, "r") as f:
            program_text = f . read  ()
            
        self . program = (processor . Processor (
            program_text,
            main_config . variables_config . variables))
        
        return


    def compute_dependent_variables (self, main_config):
        #raise Exception ("piece of code kept as reminder")
        # todo : implement rectangle things
        #if (self . do_compute_coordinates_in_rectangle):
        #    self . rectangle_data = Rectangle (self . rect_coord_tlbr [0],
        #                                       self . rect_coord_tlbr [2],
        #                                       self . rect_coord_tlbr [1],
        #                                       self . rect_coord_tlbr [3])
        return

