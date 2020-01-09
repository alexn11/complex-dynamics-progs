#!/usr/bin/python

# todo: preview doesnt work
# TODO: new types: pixel (rgba)
# todo: legacy? e.g. compute image of points, computation illustration etc.
# todo: doesn't detect wrong number of args
# todo: set color
# todo: filled julia with the number of it
# todo: implement missing rect and arg and line complex
# todo: filled julia: nb it as output also
# todo: copy, useless?
# todo: lyapunov
# todo: implement arg_density + option set_smooth_argument
# todo: "rect_cdensity" : 7, # real src, double density, bool, bool, real, bool
# todo: "set_color" : 5,
# todo: "set_edge_thickness" : 1,
# todo: #"set_arg_shading" : 1,
# todo: "set_rect_shading" : 1,
# todo: "set_imaginary_part" : 1,
# todo: "draw_rect_edge" : 2,
# todo: "draw_rect_cross" : 2,
# todo: "draw_shade_arg" : 2,
# todo:  implement load/save


from ezInputConf import convert_string_to_boolean
from ezInputConf import convert_string_to_string

# todo: this should be external
instruction_descriptors = {
    # name : (arg types, var types)
    "abs" : (
        ("variable", "variable"),
        ("complex", "real")),
    "add_test_enter_disk" : (
        ("complex", "real"),
        ()),
    "add_test_leave_annulus" : (
        ("complex", "real", "real"),
        ()),
    "add_test_leave_disk" : (
        ("complex", "real"),
        ()),
    "add_test_leave_left_half_plane" : (
        ("real", ),
        ()),
    "add_test_leave_right_half_plane" : (
        ("real", ),
        ()),
    "annulus_index" : (
        ("complex", "real", "real", "variable", "variable"),
        ("complex", "integer")),
    "arg" : (
        ("complex", "variable", "variable"),
        ("complex", "real")),
    "arg_density" : (
        ("variable", "variable"),
        ("real", "real")),
    "boundaries" : (
        ("variable", "variable"),
        ("integer", "real")),
    "cauliflower_julia" : ( # nit, pts, stop
        ("integer", "variable", "variable"),
        ("complex", "integer")),
    "coord_rect" : (
        ("complex", "complex", "variable", "variable"),
        ("complex", "complex")),
    "draw_complex_density" : (
        ("variable", "string"),
        ("complex", )),
    "draw_density" : (
        ("variable", "string"),
        ("real", )),
    "draw_indexes" : (
        ("variable", "string"),
        ("integer", ),
        ),
    "draw_integers" : (
        ("variable", "string"),
        ("integer", )),
    "draw_reals" : (
        ("variable", "string"),
        ("real", )),
    "eval_main_map" : (
        ("variable", "variable"),
        ("complex", "complex")),
    "exit" : (
        ("string", ),
        ()),
    "is_in_annulus" : (
        ("complex", "real", "real", "variable", "variable"),
        ("complex", "integer")),
    "is_in_disk" : (
        ("complex", "real", "variable", "variable"),
        ("complex", "integer")),
    "is_in_filled_julia_set" : (
        ("integer", "real", "variable", "variable"),
        ("complex", "integer")),
    "is_nan" : (
        ("variable", "variable"),
        ("complex", "integer")),
    "is_where_wrt_annulus" : (
        ("complex", "real", "real", "variable", "variable"),
        ("complex", "integer")),
    "iterate_main_map" : ( # z, z_n, n=nb_it, stop_value
        ("integer", "variable", "variable", "variable", "variable"),
        ("complex", "complex", "integer", "integer")),
    "load_complexes" : (
        ("string", "variable"),
        ("complex", )),
    "load_integers" : (
        ("string", "variable"),
        ("integer", )),
    "load_reals" : (
        ("string", "variable"),
        ("real", )),
    "make_grid" : (
        ("variable", ),
        ("complex", )),
    "name" : (
        ("string", ),
        ()),
    "nop" : (
        (),
        ()),
    "print_complexes" : (
        ("variable", ),
        ("complex", )),
    "replace_nans" : (
        ("complex", "variable", "variable"),
        ("complex", "complex")),
    "save_complexes" : (
        ("variable", "string"),
        ("complex", )),
    "save_integers" : (
        ("variable", "string"),
        ("integer", )),
    "save_reals" : (
        ("variable", "string"),
        ("real", )),
    "reset_tests" : (
        (),
        ()),
    "set_critical_value" : (
        ("complex", ),
        ()),
    "set_drawing_threshold" : (
        ("real", ),
        ()),
    "set_drawing_type" : (
        ("string", ),
        ()),
    "set_grid_tlbr" : (
        ("real", "real", "real", "real"),
        ()),
    "set_grid_width" : (
        ("integer", ),
        ()),
    "set_main_map_type" : (
        ("string", ),
        ()),
    "set_number_of_indexes" : (
        ("integer", ),
        ()),
    "set_number_of_iterations" : (
        ("integer", ),
        ()),
    "set_preview_parameters" : (
        ("boolean", "integer", "integer", "real", "string", "string"),
        ()),
    "set_shade_enhance_power" : (
        ("real", ),
        ()),
    "set_shade_max" : (
        ("string", ),
        ()),
    "set_shade_type" : (
        ("string", ),
        ()),
    "set_smooth_argument" : (
        ("boolean",),
        ()),
    "setup_fatou_inverse_data" : (
        ("complex", "real"),
        ()),
    "setup_linearizer_data" : (
        ("integer", "complex", "real", "integer"),
        ()),
    "show_help" : (
        ("string", ),
        ()),
    }

# -----------------------------------------------------------------------------

instruction_number_args = {
    name : len (instruction_descriptors [name] [0])
    for name in instruction_descriptors }


variable_types_in_arguments = {
    name : instruction_descriptors [name] [1]
    for name in instruction_descriptors }

instruction_argument_types = {
    name : instruction_descriptors [name] [0]
    for name in instruction_descriptors }
    

def make_variable_positions_in_arguments (instruction_descriptors):
    positions = {}
    for instr_name in instruction_descriptors:
        pos = []
        args = instruction_descriptors [instr_name] [0]
        for pos_id in range (len (args)):
            if (args [pos_id] == "variable"):
                pos . append (pos_id)
        positions [instr_name] = tuple (pos)
    return positions

variable_positions_in_arguments = (
    make_variable_positions_in_arguments (instruction_descriptors))


def cat_dict (dict0, dict1):
    return { ** dict0, ** dict1 }


class Processor:

    def __init__ (self, program, external_variables):
        self . program = program
        self . split_program ()
        self . cursor = 0
        self . external_variables = external_variables
        self . original_variables = {
            "Results" : "complex",
            "Iterations" : "integer", }
        self . original_variable_names = (
            list (self . original_variables . keys ()))
        self . requested_variables = {}
        #self . requested_variables_names = []
        self . instructions = []
        self . assemble ()
        self . variables = cat_dict (self . original_variables,
                                     self . requested_variables)
        return

    def assemble (self):
        current_line = self . get_next_line ()
        while (current_line != ""):
            self . interpret_line (current_line)
            current_line = self . get_next_line ()
        return

    def split_program (self):
        prog_lines = self . program . splitlines ()
        self . prog_lines = []
        self . line_numbers = []
        line_number = 0
        for line in prog_lines:
            line_number += 1
            line = line . strip ()
            if (line == ""):
                continue
            if (line [0] == "#"):
                continue
            comment_start = line . find ("#")
            # NOTE: this forbid "#" in arguments
            if (comment_start > 0):
                line = line [:comment_start]
            self . prog_lines . append (line)
            self . line_numbers . append (line_number)
        self . prog_len = len (self . prog_lines)

        

    def get_next_line (self):
        if (self . cursor == self . prog_len):
            return ""
        line = self . prog_lines [self . cursor]
        self . cursor += 1
        return line


    def describe_position (self):
      if (self . cursor == 0):
        return "(nowhere)"
      return "(@ " + str (self . line_numbers [self . cursor - 1]) + ")"
        

    def add_requested_variables (self, arg_variables):
        #print ("arg_variables="+str(arg_variables))
        previous_variable_names = list (self . requested_variables . keys ())
        for variable in arg_variables:
            var_name = variable [0]
            var_type = variable [1]
            try:
                expected_var_type = self . original_variables [var_name]
            except (KeyError):
                pass
            else:
                if (var_type == expected_var_type):
                    continue
                else:
                    raise Exception (self . describe_position () + " Wrong var type")
            try:
                expected_var_type = self . requested_variables [var_name]
            except (KeyError):
                self . requested_variables [var_name] = var_type
            else:
                if (expected_var_type == "any"):
                    continue
                elif (var_type != expected_var_type):
                    raise Exception (self . describe_position () + " Wrong var type")

        return


    def skip_spaces_in_line (self, cursor):
        while ((self . instruction_text [cursor] == " ")
               and (cursor < len (self . instruction_text))):
            cursor += 1
        return cursor

    def find_end_of_argument_string (self, cursor):
        line_len = len (self . instruction_text)
        while (self . instruction_text [cursor] not in ['"']):
            if (cursor == line_len - 1):
                raise Exception ("Unended string "
                                 + self . describe_position ()
                                 + " in \""
                                 + self . instruction_text
                                 + "\"")
            else:
                if (self . instruction_text [cursor] == '\\'):
                    cursor += 2
                    if (cursor == line_len):
                        raise Exception ("Unended string "
                                         + self . describe_position ()
                                         + " in \""
                                         + self . instruction_text
                                         + "\"")
                else:
                    cursor += 1
        return cursor + 1
                    
    def find_argument_end (self, argument_start):
        if (self . instruction_text [argument_start] == '"'):
            argument_end = (
                self . find_end_of_argument_string (argument_start + 1))
        else:
            c = argument_start
            while ((c < len (self . instruction_text))
                   and (self . instruction_text [c] != ",")
                   and (self . instruction_text [c] != " ")):
                c += 1
            argument_end = c
        return argument_end

    def split_instuction_line (self):
        raise Exception ("not here yet")
        line = self . instruction_text
        len_line = len (line)
        next_space = line . find (" ")
        if (next_space < 0):
            first_word = line
            arguments = []
        else:
            first_word = line [: next_space]
            next_nonspace = self . skip_spaces_in_line (next_space)
            if (next_nonspace == len_line):
                arguments = []
            else:
                while (False):
                    #todo
                    pass
                
        self . structured_line = [first_word] + arguments
            
            
    def get_next_word (self):
        cursor = self . instruction_cursor
        line = self . instruction_text
        len_line = len (line)

        #print (cursor)
        
        if (cursor == len_line):
            return ""
        
        word_start = cursor
        #print ("line="+line)
        #print ("start="+line [word_start:])
        
        if (cursor == 0):
            word_end = line . find (" ")
            if (word_end < 0):
                word_end = len_line
                next_cursor = len_line
            else:
                next_cursor = self . skip_spaces_in_line (word_end)
        else:
            # NOTE: this restrict the use of coma only between arguments
            # NOTE: that is forbid it in strings (=only file names)
            # it's changing
            #NOTE: no empty string allowed?

            #if (line [word_start] != ","):
            #    raise Exception ("Missing coma in \""
            #                     + line
            #                     + "\" -> "
            #                     + line [word_start :])
            if (line [word_start] == ","):
                word_start += 1
            word_start = self . skip_spaces_in_line (word_start)
            word_end = self . find_argument_end (word_start)
            #print ("word_end="+str(word_end))
            if (word_end == len_line):
                next_cursor = len_line
            else:
                next_cursor = self . skip_spaces_in_line (word_end)
            if ((next_cursor < len_line) and (line [next_cursor] != ",")):
                raise Exception (self . describe_position ()
                                 + " Expected coma, had:"
                                 + line [word_end :]
                                 + " <- "
                                 + line)


        if (next_cursor != len_line):
            # note: line has been stripped of trailing spaces
            # NOTE: no "," at the end of the line (will provocke an error)
            while (line [next_cursor] == " "):
                next_cursor += 1

                
        word = line [word_start : word_end]
        #print ("*** word="+word)

        if (word == ""):
            raise Exception (self . describe_position () + " Empty word: " + line)
        
        self . instruction_cursor = next_cursor
        
        return word

    def get_instruction_and_arguments (self, line):
        self . instruction_cursor = 0
        self . instruction_text = line
        instruction = self . get_next_word ()
        nb_args = instruction_number_args [instruction]
        arguments = nb_args * [""]
        for arg_index in range (nb_args):
            arguments [arg_index] = self . get_next_word ()
        if (self . instruction_cursor != len (self . instruction_text)):
            raise Exception (self . describe_position () + " Extra arguments: " + self . instruction_text)
        return (instruction, arguments)

    def determine_variable_type (self,
                                 instruction,
                                 variable_index):
        var_type = variable_types_in_arguments [instruction] [variable_index]
        if (var_type == "any"):
            var_type = "any"
            #raise Exception ("Could not determine type of variable")
        return var_type

    def convert_variable_id_to_full_variable_object (self,
                                                     argument,
                                                     instruction,
                                                     variable_index):
        if (argument [0] == "$"):
            argument = argument [1:]
        type_char = argument [0]
        var_type = self . determine_variable_type (instruction,
                                                   variable_index)
        var_name = argument
        return (var_name, var_type)

    def get_instruction_variables (self, instruction_and_arguments):
        (instruction, arguments) = instruction_and_arguments
        variable_positions = variable_positions_in_arguments [instruction]
        variables = []
        for variable_index in range (len (variable_positions)):
            position = variable_positions [variable_index]
            variables . append (
                self . convert_variable_id_to_full_variable_object (
                    arguments [position],
                    instruction,
                    variable_index))
        return variables

    def interpret_arguments (self,
                             instruction_and_arguments,
                             variables,
                             external_variables_dict):
        instruction = instruction_and_arguments [0]
        arguments = instruction_and_arguments [1]
        argument_types = instruction_argument_types [instruction]
        variable_index = 0
        interpreted_arguments = []
        for arg_type, arg in zip (argument_types, arguments):
            if (arg [0] == "$"):
                arg = external_variables_dict [arg [1:]]
            if (arg_type == "boolean"):
                interpreted_argument = (convert_string_to_boolean (arg))
            elif (arg_type == "integer"):
                interpreted_argument = (int (arg))
            elif (arg_type == "real"):
                interpreted_argument = (float (arg))
            elif (arg_type == "complex"):
                interpreted_argument = (complex (arg))
            elif (arg_type == "string"):
                interpreted_argument = (convert_string_to_string (arg))
            elif (arg_type == "variable"):
                interpreted_argument = (variables [variable_index])
                variable_index += 1
            else:
                raise Exception (self . describe_position () + " Unknown argument type: " + str (arg_type))
            interpreted_arguments . append (interpreted_argument)
        return interpreted_arguments

    def interpret_line (self, line):
        instruction_and_arguments = self . get_instruction_and_arguments (line)
        arg_variables = (
            self . get_instruction_variables (instruction_and_arguments))
        self . add_requested_variables (arg_variables)
        instruction = instruction_and_arguments [0]
        arguments = self . interpret_arguments (instruction_and_arguments,
                                                arg_variables,
                                                self . external_variables)
        self . instructions . append ((instruction, arguments))
        return

    
