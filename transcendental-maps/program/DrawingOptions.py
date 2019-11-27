
class DrawingOptions:

    def __init__ (self, drawings_config):
        self . do_sharper_colors = drawings_config . do_sharper_colors
        self . drawing_type = drawings_config . drawing_type
        if (self . drawing_type == ("shade")):
            self . drawing_type = ord ('s')
            self . initialize_shade_options (drawings_config)
        elif (self . drawing_type == ("threshold")):
            self . drawing_type = ord ('t')
            self . initialize_threshold_options (drawings_config)
        else:
            raise Exception ("dawing_type ? " + str (self . drawing_type))
        return

    def initialize_shade_options (self, drawings_config):

        self . nonnegative_base_color = drawings_config . nonnegative_base_color
        self . nonnegative_shade_color = drawings_config . nonnegative_shade_color
        self . negative_base_color = drawings_config . negative_base_color
        self . negative_shade_color = drawings_config . negative_shade_color
        
        self . shade_type = drawings_config . shade_type
        
        if (self . shade_type == "smallest values more visible"):
            self . shade_type = ord ("e")
            self . shade_enhancement_power = (
                drawings_config . shade_enhancement_power)
            self . compute_shade_enhancement_parameters ()
        elif (self . shade_type == "default"):
            pass
        else:
            raise Exception ("shade_type ? "+ str (self . shade_type))
        return

    def compute_shade_enhancement_parameters (self):
        self . two_to_shade_enhancement_power = (
            pow (2, self . shade_enhancement_power))
        self . shade_enhancement_factor = (
            self . two_to_shade_enhancement_power
            / (self . two_to_shade_enhancement_power - 1.))
        return    

    
    def initialize_threshold_options (self, drawings_config):
        self . threshold_value = drawings_config . threshold_value
        self . below_color = drawings_config . below_color
        self . above_color = drawings_config . above_color
        self . error_color = drawings_config . error_color
        return

