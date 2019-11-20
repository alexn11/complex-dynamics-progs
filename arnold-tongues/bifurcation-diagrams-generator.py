#!/usr/bin/python


import subprocess

config_file_name = "config.txt"
image_file_name_head = "tent-bifdia-"
config_fixed_parameters = "do_draw_bifurcation_diagram = True\nmap_family = doubling plus tent\nimage_width = 800\nimage_height = 800\n"
config_fixed_parameters += "min_a = 0\nmax_a = 1.\n"
config_fixed_parameters += "orbit_initial_segment_length = 20\norbit_final_segment_length = 40\n"

number_of_b = 4
b_list = [ 0.996 + 0.004 * i / number_of_b for i in range (number_of_b) ]

for b in b_list:
   config = "[Program inputs]\n\n"
   config += config_fixed_parameters
   str_b = str (b)
   config += "b = " + str_b + "\n"
   config += "bifurcation_diagram_image_name = " + image_file_name_head + str_b + "\n"
   config_file = open (config_file_name, "w")
   config_file . write (config)
   config_file . close ()
   subprocess . call (["python", "./tongues-usingc.py", config_file_name])





