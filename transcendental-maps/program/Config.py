# TODO: edge_thickness
# TODO: type_colors
# TODO: replace image_width by nbr_x
#        and make a dependent variable image_width (height etc.)
# todo: clear all classes and subclasses
# todo: rect shading things

import ezInputConf
import LinearizerMaps
import Rectangle
from ConfigIterations import *
from ConfigProgram import *
from ConfigPreview import *
from ConfigDrawings import *
from ConfigVariables import *

import drawings


    

            
class ConfigData:
    
    def __init__ (self, config_file):
        
        self . read_config_file (config_file)

        self . check_config_consistency ()

        self . compute_dependent_variables ()


    def read_config_file (self, config_file):
        
        self . set_default_parameters ()
        
        config_parser = ezInputConf . get_config (config_file)

        self . results_dir = ezInputConf . convert_string_to_string (config_parser ["Paths"] ["results_dir"])
        
        self . variables_config = ConfigVariables (config_parser)
        try:
          self . region_top = float (self . variables_config . variables ["top"])
          self . region_left = float (self . variables_config . variables ["left"])
          self . region_bottom = float (self . variables_config . variables ["bottom"])
          self . region_right = float (self . variables_config . variables ["right"])
        except (KeyError):
          print ("ERROR : Missing some of the following needed variables: top, left, bottom, right\n")
          raise
        
        self . preview_config = ConfigDataPreview (config_parser)
        
        self . drawings_config = (
            ConfigDataDrawings (self . grid_width, config_parser))

        self . iterations_config = ConfigDataIterations (config_parser)
        
        self . grid_width = int (config_parser ["Grid"] ["grid_width"])

        self . program_config = ConfigDataProgram (self, config_parser)
        
        return

    def set_default_parameters (self):
        
        self . grid_width = 100
  
        
        # those variables are mostly obsolete
        
        self . name = ""


        self . results_path = "./"

        self . region_top = 1.
        self . region_left = -1.
        self . region_bottom = - self . region_top
        self . region_right = - self . region_left
        
        
        self . polynomial_critical_value = 0.+0.j
        self . main_map_type = "none"
        self . eval_main_map = None
        

        self . fixed_point = 0.+0.j
        self . fixed_point_multiplier = 1.+0.j

        self . fixed_point_choice = 0
        self . main_map_rescaling = 1.+0.j

        self . linearizer_power_series_radius = 0.02
        self . linearizer_power_series_order = 4

        self . main_map_extra_parameters = (self . main_map_rescaling, )
        self . main_map_object = None

        # todo: instruction to set this?
        self . polynomial_approx_by_hot_radius = 1000000.
        #TODO: will be redundant, really useful?
        self . polynomial_escape_radius = 6.

        self . number_of_iterations = 0

        self . do_display_the_number_of_nans = False

        self . number_of_indexes = 0

        return


        
    def check_config_consistency (self):

        if (self . grid_width <= 0):
            raise Exception ("grid_width must be > 0 (had "
                             + str (self . grid_width)
                             + ")")

        return

    def update_grid_parameters (self):
        
        self . region_top_left = (
            self . region_left + 1.j * self . region_top)
        self . region_bottom_right = (
            self . region_right + 1.j * self . region_bottom)
        

        self . drawings_config . compute_dependent_variables (
            self . grid_width,
            self . region_top,
            self . region_bottom,
            self . region_left,
            self . region_right)
        
        return

    def compute_index_colors (self):
        self . index_colors = (
            drawings . make_color_list (self . number_of_indexes))
        return

    def compute_dependent_variables (self):

        self . update_grid_parameters ()

       
        self . abs_multiplier = abs (self . fixed_point_multiplier)


        # todo: where needed? when to update?
        self . fundamental_annulus_outer_radius = (
            self . polynomial_approx_by_hot_radius)
        self . fundamental_annulus_inner_radius = (
            self . fundamental_annulus_outer_radius
            / self . abs_multiplier)

        
        self . program_config . compute_dependent_variables (self)
        

        if (self . preview_config . do_preview):
            self . preview_config . compute_dependent_variables ()


        self . compute_index_colors ()
        

        return
    
