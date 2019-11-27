


class ConfigVariables:

    def __init__ (self, config_parser):
        
        self . variables = {}
        
        try:
            config_variables = config_parser ["Variables"]
        except (KeyError):
            return

        for variable_name in config_variables:
            self . variables [variable_name] = config_variables [variable_name]

        self . show_variables ()

        return

    def show_variables (self):
        print (" ")
        print ("The following variables have been defined:")
        print ("------------------------------------------")
        for variable_name in self . variables:
            print (variable_name + " = " + self . variables [variable_name])
        print (" ")
        return
