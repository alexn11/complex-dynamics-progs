# Documentation on tanscendental-maps

## What it is

## What it does

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
The grids have all the same sizes and contain all the computed values. They represent the images by some mappings of a discretized rectangular domain of the complex plane.
The height of the grids is determined by the aspect ratio derived from the coordinates of the window (variables `top`, `left`, `bottom` and `right`).


The `Program` section contains the path to the command file, for example:
```
[Program]
program_file_name = ../examples/fatou-inverse/fatouinv-rescaled-commands.txt
```


### Command file

The command file is read by the main script and each (nonempty) line is executed, sequentially.
Everything after a `#` symbol is ignored.

The values of variables defined in the configuration file can be used by appending their name with a `$` sign.

General setup instructions (with examples):
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
1. `set_grid_tlbr`: set the grid parameters (top, left, bottom and right extremities), this allows to change the window. 
The following instruction is redundant with the default initialization:
```
set_grid_tlbr $top, $left, $bottom, $right
```
When the grid parameters the arrays need to be reallocated. For that use the instruction `make_grid`.


Other instructions:
1. `exit`: leave the program before executing the following instruction (this instruction is for convenience).
```
exit "message"
```


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
1. `setup_linearizer_data`: set the parameters for the computation of the linearizer.
Parameters are:
 1. fixed point choice (integer) either `0` or `1`
 1. rescaling (complex) as for Fatou inverse maps
 1. power series radius (real): the radius of the disk around the fixed point where the linearizer is computed using a power series
 1. power series order (integer): the degree of the power series to use, max is `4`.
Set up the parameters for the linearizer for the first (`0`, whatever this means) fixed point, 
rescaled by `0.435`,
with a power series evaluation on the disk of radius `0.01` of degree `3`:
```
setup_linearizer_data 0, 0.435, 0.01, 3
```

Computations:
1. `make_grid`: allocate the variable grids and create an array of complex numbers corresponding to the discretization of the rectangular domain defined by the grid parameters.
The argument is the name for the computed array of complex numbers.
 All the previous computations will be lost.
```
make_grid grid
```
1. `eval_main_map` : eval the main map.
The first parameter is the domain grid and the second parameter the range grid.
Both parameters should have complex type.
 If the the second parameter does not exits yet, it will be automatically allocated.
```
eval_main_map grid, images
```
1. 
is_in_disk
abs
arg
cauliflower_julia

arg_density
boundaries

Iterations:
reset_tests
add_test_leave_disk
iterate_main_map

Drawings:
set_drawing_type
set_shade_type
set_shade_max
set_number_of_indexes

draw_integers
draw_density
draw_reals
draw_indexes











### Requirements

### Use, generalities

## Examples

## Source files
