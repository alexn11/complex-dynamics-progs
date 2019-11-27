import configparser

"""

 - "manual":

def get_config (config_file_name)

section = config_parser [""]

def read_variable (section,
                   variable_name,
                   variable_type_descriptor)

       ***    OR     ***

 - All at once, but complicated init:

def read_config (config_file_name,
                 variable_dictionary)

"""

"""
Variable dictionary is of the form:

variable name in the file : [[variable type], [default value (can be empty)]]

Variable name is:
section:variable_name

Types of variables:
string
boolean
int
float
complex
real rgba
list

for list: (simple list)
 (no default value)
 ["list", variable type, separator (optional)]


It reads all the variables in all the sections of the file,
 check if it appears in the dictionary
 convert
 appends the value of the variable
 and appends true to mark the assignment of the variable
"""

# -----------------------------------------------------------------------------


def string_to_rgba (s):
    return convert_one_value ("float rgba", s)


def try_read_a_boolean (config_parser, section, variable, default):
    try:
        value = (
            convert_one_value ("boolean",
                               config_parser [section] [variable]))
    except (KeyError):
        value = default
    return value

# -----------------------------------------------------------------------------

def convert_string_to_string (string):
    if (string [0] == '"'):
        converted_string = string [1 :]
        string_end = converted_string . find ('"')
        if (string_end < 0):
            # note: only one line string allowed
            raise Exception ("Missing end of string")
        if (string_end != len (converted_string) - 1):
            raise Exception ("Extra characters after the end of string:"
                             + string
                             + " -> "
                             + converted_string [string_end:])
        converted_string = converted_string [: string_end]
    else:
        converted_string = string
    return converted_string

def convert_string_to_rgba (text, separator = ','):
    # todo: "splited" correct english word?
    splited_string = text . split (separator)
    
    if (len (splited_string) == 3):
        splited_string . append ("1.")
        
    if (len (splited_string) != 4):
        raise Exception ("Not a valid RGBA value (expected: 4 values)")
    try:
        rgba_values = [float (splited_string [i]) for i in range (4)]
    except (ValueError):
        raise Exception ("Not a valid RGBA value (expected: float)")
    if (any (v < 0. for v in rgba_values)
        or any (v > 1. for v in rgba_values)):
        raise Exception ("Not a valid RGBA value (should be between 0 and 1)")
    return rgba_values
    

def convert_string_to_boolean (text):
    if (text in ["true",
                 "True",
                 "TRUE",
                 "1",
                 "t",
                 "T",
                 "#t",
                 "yes",
                 "YES",
                 "y",
                 "Y"]):
        return True
    elif (text in ["false",
                   "False",
                   "FALSE",
                   "0",
                   "f",
                   "F",
                   "#f",
                   "no",
                   "NO",
                   "n",
                   "N"]):
        return False
    else:
        raise Exception ("String does not represent a boolean")

# -----------------------------------------------------------------------------

def convert_one_value (variable_type,
                       variable_string_value):
    if (variable_type == "string"):
        variable_value = variable_string_value
    elif (variable_type == "boolean"):
        variable_value = convert_string_to_boolean (variable_string_value)
    elif (variable_type == "int"):
        variable_value = int (variable_string_value)
    elif (variable_type == "float"):
        variable_value = float (variable_string_value)
    elif (variable_type == "complex"):
        variable_value = complex (variable_string_value)
    elif (variable_type in ["float rgba",
                            "float rgb"]):
        variable_value = convert_string_to_rgba (variable_string_value)
    else:
        raise Exception ("Unknown variable type: " + str(variable_type))
    return variable_value

def read_variable_list (variable_type,
                        variable_string_value,
                        separator = ','):

    string_value_list = variable_string_value . split (separator)

    value_list = [convert_one_value (variable_type, string_value)
                  for string_value in string_value_list]
    
    return value_list

def read_variable (section,
                   variable_name,
                   variable_type_descriptor):
    variable_string_value = section [variable_name]
    variable_type = variable_type_descriptor [0]
    variable_value = None

    if (variable_type == "list"):
        try:
            separator = variable_type_descriptor [2]
        except (IndexError):
            separator = ','
        variable_value = read_variable_list (variable_type_descriptor [1],
                                             variable_string_value,
                                             separator)
    else:
        variable_value = convert_one_value (variable_type,
                                            variable_string_value)
    return variable_value

def read_variable_according_to_descriptor (section,
                                           variable_name,
                                           variable_descriptor):
    variable_string_value = section [variable_name]
    variable_type_descriptor = variable_descriptor [0]

    variable_value = read_variable (section,
                                    variable_name,
                                    variable_type_descriptor)

    variable_descriptor . append (variable_value)
    return


def fill_missing_values_with_default_values (variable_dictionary):
    # note: looping on ". values ()" doesn't seem right?
    for variable_name in variable_dictionary . keys ():
        variable_descriptor = variable_dictionary [variable_name]
        if (len (variable_descriptor) == 3):
            # already filled: not missing
            continue
        if (len (variable_descriptor) != 2):
            # totally unexpected
            raise Exception ("PFRT")
        default_value_list = variable_descriptor [1]
        if (default_value_list == []):
            # no default
            continue
        variable_descriptor . append (default_value_list [0])
    return
        

def get_config (config_file_name):
    config_parser = (
        configparser . ConfigParser (
            interpolation = configparser . ExtendedInterpolation ()))
    read_result = config_parser . read (config_file_name)
    if (len (read_result) == 0):
        raise Exception ("Configuration file not found.")
    return config_parser

def read_config (config_file_name,
                 variable_dictionary):
    
    config_parser = get_config (config_file_name)
    
    for section_name in config_parser . sections ():
        config_section = config_parser [section_name]
        for variable_name in config_section . keys ():
            full_variable_name = section_name + ":" + variable_name
            try:
                variable_descriptor = variable_dictionary [full_variable_name]
                read_variable_according_to_descriptor (config_section,
                                                       variable_name,
                                                       variable_descriptor)
            except (KeyError):
                pass

    fill_missing_values_with_default_values (variable_dictionary)
            

    return


    
