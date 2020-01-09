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
program_file_name = "../examples/fatou-inverse/fatouinv-rescaled-commands.txt"
```


### Command file

### Requirements

### Use, generalities

## Examples

## Source files
