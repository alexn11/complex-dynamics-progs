
import ezInputConf as inp

class ConfigDataPreview:
    def __init__ (self, config_parser):

        self . preview_parameters = None
        
        self . do_preview = False
        self . width = 0
        self . height = 0
        self . threshold = 0
        self . white_text = "W"
        self . black_text = "B"
        
        return
    
    def compute_dependent_variables (self):
        self . preview_parameters = [self . width,
                                     self . height,
                                     self . threshold,
                                     self . white_text,
                                     self . black_text]
        return

