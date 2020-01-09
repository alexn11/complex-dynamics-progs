import ezInputConf as inp

from DrawingOptions import *

class ConfigDataDrawings:
    # note: drawing options make many members redundant, but i don't care :)
    
    def __init__ (self, image_width, config_parser):

        self . image_width = image_width

        self . set_default_drawing_options ()
        
        # below is probably obsolete code
        self . do_process_rectangle_coordinates_for_shading = (
            inp . try_read_a_boolean (
                config_parser,
                "Drawings",
                "do_process_rectangle_coordinates_for_shading",
                False))
        self . do_rectangle_edge = (
            inp . try_read_a_boolean (
                config_parser,
                "Drawings",
                "do_rectangle_edge",
                False))
        if (self . do_rectangle_edge):
            self . rectangle_edge_thickness = (
                float (config_parser ["Drawings"] ["rectangle_edge_thickness"]))
        else:
            #NOTE: needed because of the way of passing args in some function
            #TODO: could do an object/structure to avoid that (not soon)
            self . rectangle_edge_thickness = 0.
            
            
        self . do_rectangle_cross = (
            inp . try_read_a_boolean (
                config_parser,
                "Drawings",
                "do_rectangle_cross",
                False))
        if (self . do_rectangle_edge and self . do_rectangle_cross):
                raise Exception ("Rectangle do_edge and do_cross"
                                 + " are mutually exclusive.")


        # TODO: where is do_sharper_colors used?
        self . do_sharper_colors = (
            inp . try_read_a_boolean (config_parser,
                                "Drawings",
                                "do_sharper_colors",
                                False))


        # TODO: implement signal_sign_of_imaginary_part
        self . do_signal_sign_of_imaginary_part = (
            inp . try_read_a_boolean (config_parser,
                                "Drawings",
                                "do_signal_sign_of_imaginary_part",
                                False))


        
        try:
            self . drawing_type = config_parser ["Drawings"] ["drawing_type"]
        except (KeyError):
            pass

            

        
        if (self . drawing_type == "shade"):
            
            try:
                self . shade_type = config_parser ["Drawings"] ["shade_type"]
            except (KeyError):
                pass
                
            if (not (self . shade_type in ["smallest values more visible",
                                           "default"])):
                raise Exception ("shade_type ?")
            
            try:
                self . shade_enhancement_power = (
                    float (
                        config_parser ["Drawings"] ["shade_enhancement_power"]))
            except (KeyError):
                pass

            self . read_shade_colors (config_parser)
            
        elif (self . drawing_type == "threshold"):
            # todo: read thres optns, read drawing optns, shade options
            #       thres color, shade colrs
            self . threshold_value = (
                float (config_parser ["Drawings"] ["threshold_value"]))
            self . read_threshold_colors (config_parser)
        else:
            raise Exception ("drawing_type ?")
        

        return

    def set_default_drawing_options (self):
              
        self . do_smooth_argument = False
        self . variable_to_use_as_max = "compute max"
        self . max_value = 0
        
        self . drawing_type = "shade"
        self . threshold_value = 0.
        self . below_color = [0., 0., 0., 1.]
        self . above_color = [1., 1., 1., 1.]
        self . error_color = [1., 0., 0., 1.]
        self . shade_type = "default"
        self . shade_enhancement_power = 8
        self . negative_base_color = [0., 0., 0.18, 1.]
        self . negative_shade_color = [1., 0.3, 0., 1.]
        self . nonnegative_base_color = [0.13, 0.465, 0.37, 1.]
        self . nonnegative_shade_color = [0., 0.5, 0.2, 1.]
      
        return

    def read_shade_colors (self, config_parser):
        try:
            self . nonnegative_base_color = inp . string_to_rgba (
                config_parser ["Drawings"] ["nonnegative_base_color"])
        except (KeyError):
            pass
        try:
            self . nonnegative_shade_color = inp . string_to_rgba (
                config_parser ["Drawings"] ["nonnegative_shade_color"])
        except (KeyError):
            pass
        try:
            self . negative_base_color = inp . string_to_rgba (
                config_parser ["Drawings"] ["negative_base_color"])
        except (KeyError):
            pass
        try:
            self . negative_shade_color = inp . string_to_rgba (
                config_parser ["Drawings"] ["negative_shade_color"])
        except (KeyError):
            pass


    def read_threshold_colors (self, config_parser):
        
        try:
            self . above_color = (
                inp . string_to_rgba (
                    config_parser ["Drawings"] ["above_color"]))
        except (KeyError):
            pass
        
        try:
            self . below_color = (
                inp . string_to_rgba (
                    config_parser ["Drawings"] ["below_color"]))
        except (KeyError):
            pass
        
        try:
            self . error_color = (
                inp . string_to_rgba (
                    config_parser ["Drawings"] ["error_color"]))
        except (KeyError):
            pass
        
        return

    def update_drawing_options (self):
        self . drawing_options = DrawingOptions (self)

        
    def compute_dependent_variables (self,
                                     image_width,
                                     top,
                                     bottom,
                                     left,
                                     right):
        self . image_width = image_width
        self . image_height = (
            int (abs (image_width * (top - bottom) / (right - left))))
        self . tlbr = [top, left, bottom, right]
        self . image_sizes = [self . image_width, self . image_height]
        self . pixel_size = abs (right - left) / self . image_width

        self . update_drawing_options ()
        return
    
    

