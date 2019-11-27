
name "disjt"




set_main_map_type linearizer
set_critical_value -0.123+0.745j
setup_linearizer_data 0, 0.435, 0.01, 3

set_preview_parameters True, 50, 20, 0.2, ".", "X"

#set_grid_tlbr 10, -10, -10, 10
##set_grid_width $size
#make_grid grid

set_grid_tlbr $top, $left, $bottom, $right
#set_grid_width $size
make_grid grid


eval_main_map grid, images
is_in_disk 0.+0.j, 24., images, tracts
boundaries tracts, tracts_boundaries
abs images, abs_images
arg 0+0j, images, arg_images


set_drawing_type "shade"
set_shade_type "normal"


set_shade_max 1
draw_integers tracts, "tracts-shade"

draw_density tracts_boundaries, "tracts"

set_shade_max 10.
draw_reals abs_images, "abs-image"

arg_density arg_images, arg_density
draw_density arg_density, "arg-image"

#exit "cut"



set_grid_tlbr $top, $left, $bottom, $right
#set_grid_width $size
make_grid grid

reset_tests
add_test_leave_disk 0+0j, $escape_radius
iterate_main_map $nit, grid, last_point, nb_iterations, stop_value

boundaries nb_iterations, nit_bounds

abs last_point, abs_end





set_drawing_type "shade"
set_shade_type "normal"
set_shade_max "compute"
draw_density nit_bounds, "nit_bounds"

set_shade_type "enhanced"
set_shade_enhance_power 8
set_shade_max $nit
draw_integers nb_iterations, "iterations"


set_shade_type "enhanced"
set_shade_enhance_power 8
set_shade_max 2.3
draw_reals abs_end, "end_abs"

set_shade_type "enhanced"
set_shade_enhance_power 8
set_shade_max compute
draw_integers stop_value, "stopv"

boundaries stop_value, stop_bounds
draw_density stop_bounds, "stopvb"




