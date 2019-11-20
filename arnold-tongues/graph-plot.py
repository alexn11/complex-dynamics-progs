
import math
import cmath
import sys


import mathsvg

import tonglib

# const

two_pi = 2. * math . pi



# params

map_family = "doubling plus straight sine"
it = 2
image_name = "graph2"
a = 0.2
b = 0.995
padding = 0.2

# funs

def eval_the_map (x):
  y = x
  for i in range (it):
    y = tongue_family . compute_image_by_lifted_map (a, b, y)
  if (y < 0):
    y += height
  if (y >= height):
    y -= height
  return y




# derived params
height = 2 ** it


# main prog

tongue_family = tonglib . tongue_system (map_family)

im = mathsvg . SvgImage (pixel_density = 100, view_window = (( - padding, - padding ), (1 + padding, height + padding)))

old_stroke_width = im . stroke_width
im . stroke_width *= 0.5
im . set_dash_mode ("dash")
im . draw_arrow ((-0.5 * padding, 0.), (1. + 0.5 * padding, 0.))
im . draw_arrow ((0., -0.5 * padding), (0., height + 0.5 * padding))
im . draw_line_segment ((0., height), (1., height))
im . draw_line_segment ((1., height), (1., 0.))

im . point_size = 0.5 * old_stroke_width
nb_x = height * 57
x_step = 1 / (nb_x - 1)
for j in range (nb_x):
  x = j * x_step
  im . draw_point ((x, eval_the_map (x)))

for j in range (height):
 im . set_dash_mode ("dots")
 im . draw_function_graph (lambda x : x + j, 0., 1., 2)
 im . set_dash_mode ("dash")
 im . draw_line_segment ((0., j), (1., j))


im . save (image_name + ".svg")
