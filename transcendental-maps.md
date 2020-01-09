# Documentation on tanscendental-maps

This script is used to draw some images related to the iteration of some specific transcendental maps. This includes "escape time" of iteration and "tracts" of class B functions.
The maps are linearizers of fixed point of quadratic polynomials and the inverse of the Fatou coordinates of the Cauliflower map.

## How to use

Create a configuration file and a corresponding command file. Run the main script `main.py` with the path to the configuration file as an argument.

The configuration file defined the general environment for the computations and the command file contains a sequence of instructions to run (including iterations and drawing).

### Configuration file

The configuration file contains the following sections:
	
1. `Paths`
1. `Variables`
1. `Grid`
1. `Program`

The `Paths` section contains the path to the directory where the resulting files (generally images) will be stored.
For example
```
[Paths]
results_dir = ../results/
```
The directory should already exist.

The `Variables` section is used to set up the values of the general parameters such as the window and number of iterations.
The set of variable that can be defined is not limited and many user defined variables can be created.
The type of the variables is determined by the way they are used the first time in the command file.

The only variables necessary for correct execution of the program are `top`, `left`, `bottom` and `right`.
They represent the limits of the region under consideration.

The `Grid` section is used to define the width of the width. It is done as follows:
```
[Grid]
grid_width = 400
```
The arrays have all the same sizes and contain all the computed values. They represent the images by some mappings of a discretized rectangular domain of the complex plane.
The height of the arrays is determined by the aspect ratio derived from the coordinates of the window (variables `top`, `left`, `bottom` and `right`).


The `Program` section contains the path to the command file, for example:
```
[Program]
program_file_name = ../examples/fatou-inverse/fatouinv-rescaled-commands.txt
```


### Command file

The command file is read by the main script and each (nonempty) line is executed, sequentially.
Everything after a `#` symbol is ignored.

The values of variables defined in the configuration file can be used by appending their name with a `$` sign.

General setup instructions (and a few examples):

1. `name`: Sets a name that will be prefixed to each file name produced during the execution of the script:
```
name "my-script"
```
1. `set_preview_parameters`: set up the parameters for the live character preview.
```
set_preview_parameters True, 50, 20, 0.2, ".", "X"
```
sets text preview (`True`) of 20 lines of 50 characters. Values below the threshold of 0.2 are marked with a ``.`` and the values above with a ``X``.
To set no preview use
```
set_preview_parameters False, 0, 0, 0, "", ""
```
1. `set_main_map_type`: choose a map type among `fatou-inverse` (inverse of the Fatou coordinates of the Cauliflower map), `linearizer` (linearizer of a quadratic polynomial).
```
set_main_map_type linearizer
```
(Note: this instruction doesn't really do anything and the main map type is not set until the corresponding `set_<map type name>_data` instruction is called).
1. `set_grid_tlbr`: set the grid parameters (top, left, bottom and right extremities), this allows to change the window. 
The following instruction is redundant with the default initialization:
```
set_grid_tlbr $top, $left, $bottom, $right
```
When the grid parameters the arrays need to be reallocated. For that use the instruction `make_grid`.



Instructions specific to `fatou-inverse` type of maps:

1. `setup_fatou_inverse_data`: set the parameters for the computations of the Fatou inverse map.
First argument is a rescaling factor (complex number) and a large value used for numerical estimates of the Fatou coordinates (real).
The rescaling factor is just a multiplicative factor in front of the function.
```
setup_fatou_inverse_data .10, 100
```

Instructions specific to `linearizer` type of maps:

1. `set_critical_value`: choose the value of `c`, critical value of the quadratic polynomial. For the (an approximate of) rabbit:
```
set_critical_value -0.123+0.745j
```
1. `setup_linearizer_data`: set the parameters for the computation of the linearizer. Parameters:
 fixed point choice (integer) either `0` or `1`,
 rescaling (complex) as for Fatou inverse maps,
 power series radius (real): the radius of the disk around the fixed point where the linearizer is computed using a power series,
 power series order (integer): the degree of the power series to use, max is `4`.
Set up the parameters for the linearizer for the first (`0`, whatever this means) fixed point, 
rescaled by `0.435`,
with a power series evaluation on the disk of radius `0.01` of degree `3`:
```
setup_linearizer_data 0, 0.435, 0.01, 3
```

Computations:

1. `make_grid`: allocate the variable arrays and create an array of complex numbers corresponding to the discretization of the rectangular domain defined by the grid parameters.
The argument is the name for the computed array of complex numbers.
 All the previous computations will be lost.
```
make_grid grid
```
1. `eval_main_map` : eval the main map.
The first parameter is the domain array and the second parameter the range array.
Both parameters should have complex type.
 If the the second parameter does not exits yet, it will be automatically allocated.
```
eval_main_map grid, images
```
1. `abs`: compute the aboluste value, parameters: domain array (complex), range array (real).
1. `arg`: compute the argument with respect to some center, parameters: center (complex), domain array (complex), range array (real).
1. `cauliflower_julia`: compute the Cauliflower Julia set. Parameters: number of iterations (integer), domain array (complex), fate array (integer)


Tests: tests create a array of integer values. The values are `0` for false and `1` for true.

 1. `is_in_annulus`: check if the points in the domain array belong to a round annulus.
 Parameters: center of the annulus (complex), inner radius (real), outer radius (real), domain array (complex), range array (integer)
 1. `is_in_disk`: parameters are center of the disk (complex), radius of the disk (real), domain array (complex), range array (integer).
 1. `is_in_filled_julia_set`: check if the points in the domain array are in the filled Julia set of the quadratic polynomial.
 Parameters: number of iterations (integer), escape radius (real), domain array (complex), range array (integer)
 1. `is_nan`: check if the value is (complex) NaN. Parameters: domain array (complex), range array (integer).



Iterations: append tests then launch the computations with `iterate_main_map`:

1. `reset_tests`: Reset all the tests. (no argument)
1. `add_test_enter_disk`: Append the test that will stop the iteration when the orbit enters a disk.
Parameters: center (complex), radius (real).
1. `test_leave_annulus`: Append the test that will stop the iteration when the orbit leaves an annulus.
Parameters: center (complex), inner radius (real), outer radius (real).
1. `add_test_leave_disk`: Append the test that will stop the iteration when the orbit leaves a disk.
Parameters: center (complex), radius (real).
1. `leave_left_half_plane`: Append the test that will stop the iteration when the orbit leaves a left half plane.
Parameters: boundary real part (real).
1. `leave_right_half_plane`: Append the test that will stop the iteration when the orbit leaves a right half plane.
Parameters: boundary real part (real).
1. `iterate_main_map`: 
The iteration stops when one of the added tests returns true. The stop value is the index of the corresponding test.
Parameters: number of iterations (integer), starting points array (complex), last iterates array (complex), number of iterations done array (integer), stop value array (integer).



Computations for drawing:

1. `arg_density`: derive a better looking value for drawing the argument (computed with) using `draw_density`. First thing it does is a rescaling (from 2 pi to 1).
Then if requested it maps the rescaled values by `4*x*(1-x)` for a smoother look.
Parameters: arguments array (real), processed arguments array (real)
1. `boundaries`: compute the boundaries of plane domains marked by different integer values. The result is some density charaterizing the distance to the boundary.
Parameters: marking array (integer), boundary marker (real).


Note on drawings: there are a few types of drawings:

1. `draw_reals` and `draw_integers`: plot colors depending on the values of the arrays. The way this color is computed is determined by the drawing parameters.
1. `draw_indexes`: draw colors reprensenting a small collection of consecutive integers ("indexes") starting from 0.
1. `draw_density`: draw a grey shade (with darker values for lower densities), for arrays of values between 0 and 1.
1. `draw_complex_density`: the red component of the color correspond to the real part and the green component to the imaginary part (no blue component).

Drawing instructions:

1. `set_drawing_type`: set the drawing type, among: `"shade"` (draw colors depending continuously on the data) and `"threshold"` (two different colors only, one when the value is below the thresold, the other for above).
Parameters: drawing type (string, either `"shade"` or `"threshold"`)
(Note: there is also a specific color for NaN values, colors cannot be modified directly).
1. `set_shade_type`: set the shade type, choices are: `"normal"` and `"enhanced"`.
The "normal" mode will basically be an affine interpolation between two colors, proportionated to the values in the array.
The "enhanced" mode is an attempt to make the shade more progressive near smaller values.
Parameters: shade type (string, either `"normal"` or `"enhanced"`).
1. `set_shade_enhance_power`: parameter for the "enhanced" version of shade drawing, larger value means more distortion.
Parameters: parameter (real).
1. `set_shade_max`: set the variable to use for rescaling data before transforming into shades.
It can be a real value, in which case this sets the max explicitely.
If this is set to 
 `"compute"`
then the max is set to the max of the values of the array being drawn.
Finally the parameter `"nb_iterations"` means the number of iterations that has been used in the previous call to `iterate_main_map`.
Parameters: max value for shade (string, either `"compute"` or `"nb_iterations"`, or a real number)
example:
```
set_shade_max $nit
```
1. `set_drawing_threshold`: set the threshold for the "threshold" type of drawing.
Parameters: threshold (real).
1. `set_number_of_indexes`: set the number of different indexes and compute a corresponding palette of colors. Use with the instruction `draw_indexes`.
Parameters: number of different indexes (integer).
1. `draw_integers`: Draw the content of an array of integer values.
Parameters: values array (integer), image name (string).
1. `draw_reals`:  Draw the content of an array of real values.
Parameters: values array (real), image name (string).
1. `draw_indexes`: Draw the content of an array of indexes using the palette created by the instruction `set_number_of_indexes`.
Parameters: values array (integer), image name (string).
1. `draw_density`: Draw a density.
Parameters: values array (real), image name (string).
1. `draw_complex_density`: Draw a complex density.
Parameters: values array (complex), image name (string).


Other instructions:

1. `exit`: leave the program before executing the following instruction (this instruction is for convenience).
```
exit "message"
```









