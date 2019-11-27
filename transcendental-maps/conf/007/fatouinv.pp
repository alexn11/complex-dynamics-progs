
name "fatou-inverse"




set_main_map_type fatou-inverse
setup_fatou_inverse_data 1.0, 100

set_preview_parameters True, 50, 20, 0.2, ".", "X"


set_grid_tlbr $top, $left, $bottom, $right
make_grid grid


eval_main_map grid, images
is_in_disk 0.+0.j, 2., images, tracts
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


cauliflower_julia $cauliflower_nit, images, cauliflower_stop

set_number_of_indexes 3
draw_indexes cauliflower_stop, "cauliflower"

boundaries cauliflower_stop, cauliflower_stop_boundaries
draw_density cauliflower_stop_boundaries, "cauliflower-bnds"


set_grid_tlbr 2., -2., -2., 2.
make_grid grid 
cauliflower_julia  $cauliflower_nit, grid, cauliflower_stop
set_number_of_indexes 3
draw_indexes cauliflower_stop, "actual-cauliflower"

#exit "cut"



set_grid_tlbr $top, $left, $bottom, $right
make_grid grid

reset_tests
add_test_leave_disk 0+0j, $escape_radius
iterate_main_map $nit, grid, last_point, nb_iterations, stop_value

boundaries nb_iterations, nit_bounds

abs last_point, abs_end



set_number_of_indexes 4
draw_indexes stop_value, "stop"

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




