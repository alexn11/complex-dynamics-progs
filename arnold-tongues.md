# Documentation on arnold-tongues

## What it is

The folder `arnold-tongues` contains programs that can be used to draw parameter spaces of several families of circles maps.
The families are:
- "double standard map" / "dsm" : *f<sub>a,b</sub>(x) = 2x + a - (b/&pi;) sin(2&pi;x)* (<https://www.cmup.pt/sites/default/files/publications/double.pdf>).
- "double dsm" : *f<sub>a,b</sub>(x) = 2x + a - (b/2&pi;) sin(2&pi;x)*
- "doubling plus tent": *f<sub>a,b</sub>(x) = 2x + a + bT(x)*, with *T(x) = 2x* if *x &le; 1/2* else *T(x) = 2(1 - x)*.
- "doubling plus straight sine" : *f<sub>a,b</sub>(x) = 2x + a + (b/2) S(x)*, with *S(x) = 4x - 1* if *x &le; 1/2* else *S(x) = -4x + 3*.

The list of programs inside the folders is as follows.
1. `tongues-usingc.py` :
It is the main program for this folder, it is used to draw parameter spaces of several families of circle maps.
1. `graph-plot.py` :
This program uses the `tonglib` module to draw a graph of some example of map from the "doubling plus straight sine" family, uses the Python module `mathsvg`.
1. `bifurcation-diagram-generator.py` :
This program creates many configuration files and runs the program on them to generate a sequence of bifurcation diagrams in the "doubling plus tent" family with different values of b (for the specific parameters: see source).

## What it can do

The main program can do one of the following two processes.

1. The use can select one of the families above and a range of parameter values in the form &#91; a<sub>min</sub>, a<sub>max</sub> &#93; &times; &#91; b<sub>min</sub>, b<sub>max</sub> &#93;. 
For each parameter in a discretized version of this range the program will compute a collection of orbits and try to determine whether these orbits are periodic or not.
It will pick a color according to the detected period or a specific color if no periodicty has been found.
The result will be an image where the coloration of the pixel correspond to the computed color at the corresponding parameter.
The relation between parameter and pixel on the image is a straightforward affine mapping (the height and width of the picture are modifiable parameters).
1. The user can select a family, a fixed value of *b* and an interval of values of *a*.
For each value of *a* in a discretized version of the interval, the program computes a collection orbits and plot the final points of the orbit.
The result is a bifurcation diagram in the same fashion as the familiar ones.

For more details on how to run theses processes see below.

## How to use

### Compilation

Before running the program the Cython source needs to be compiled. This is done only once. Compile the Cython source by typing the following command (in the terminal) in the `arnold-tongues` directory:
```
python setup.py build_ext --inplace
```
Ignore the warnings.


### Use, generalities

The typical use is in two steps:
1. Create a configuration file to set up the parameters, such as family, parameters windows etc.
2. run the program with the path to the configuration file as a parameter:
```
python3 tongues-usingc.py path/to/conf-file
```

### Generating a picture of the tongues

General structure of the configuration file, this should be pretty straightforward to understand:
```
[Program inputs]

map_family = <name of the family>

do_draw_tongues = True
do_draw_periods = True

min_a = <min value for a>
max_a = <max value for a>
min_b = <min value for b>
max_b = <max value for b>

max_period_to_test = <max period to test(!)>
period_test_tol = <a small number telling how error is allowed when checking periodicity>

number_of_orbits_to_compute = <number of orbits to compute and check for periodicity>

orbit_initial_segment_length = <number of iterations to compute before checking the orbit is periodic>

default_starting_point = <one of the orbit starting point, the other starting points will be derived from this parameters>

image_height = <image height in pixels>
image_width = <image width in pixels>

periods_image_name = <a name for the image, without the extension>

do_show_progress = True # this will show some dots
```

The program will compute `number_of_orbits_to_compute` orbits with starting point equally spaced on the 1D torus.
The value of `default_starting_point` is assigned to one of the starting point and the other are computed accordingly.

For each orbit, the program will first compute `orbit_initial_segment_length` iterates.
After that more iterates are computed and it periodicity of the resulting point is checked on these later iterates in the most naive way.
The value of `period_test_tol` is used to modulate how strict one wants the periodicity to be.

The parameter `do_draw_periods` is set to `True` to show a shade relating to the computed period.
If one only wants to draw the binary value of whether the orbit is detected periodic or not, one should instead set the following parameter:
```
do_draw_any_periodic = True
```

The image is saved into a `png` file.
Note that by specifying the image size in pixels the resulting image might be distorded if the aspect ratio of the image differs from the aspect ratio of the parameter range.

It is also possible to save the computation data as text files by specifying the corresponding file names:
```
results_file_name_a_b_values = <file name for storing the values of a and b>
results_file_name_periods = < file name for the computed periods>
```
Aslo if `do_save_last_iterates` is set to `True` (default is `False`), it will save the tails of computed orbits, the file name should be specified with `results_file_name_last_iterates`.



### Generating a bifurcation diagram

To compute a bifurcation driagram one uses a configuration file in the following format:
```
[Program inputs]
map_family = <name of the family>
do_draw_bifurcation_diagram = True
b = <value of b>
bifurcation_diagram_image_name = <image name without the extension>
min_a = <min a>
max_a = <max a>
image_width = <image width in pixels>
image_height = <image height in pixels>
orbit_initial_segment_length = <first iterates>
orbit_final_segment_length = <last iterates, will be drawn>
```


HERE3 specific


if do_draw_bifurcation_diagram:
compute many orbits equaly spaced (number is the number of pixel on the height of the image)
draw the last elements of the orbit
does this for equaly spaced values of a and some fixed value of b
the values of a are on the x axis
the values of the orbit final points are on the y axis (in black)

HERE
note on `bifurcation-diagram-generator.py`

### More options

The colors for the bifurcation diagram can be modified with the following parameters:
1. `background_color`
1. `point_color`



## Examples

### Tongues

The `conf` directory contains examples of configuration files.
1. `blowup-blowup.conf`: to draw part of the parameter plane of the "doubling plus tent" family.
** Selected region: 0.005505 &le; a < 0.007245, 0.99439 &le; b < 0.99613
** Period max: 20 (periodicity test with precision 1/1000)
** Test on 4 different orbits
** orbit_initial_segment_length: 300
** Creates an 800x800 image file named "project-blowup-strange-region.png"
1. Similar to the previous one: `project-blowup.conf` (0. &le; a < 0.012, 0.988 &le; b < 1), `project-picture.conf`, `straight-sine-blowup.conf` (for the family "doubling plus straight sine"), etc.

ddsm.conf
Draw the parameter plane of the "double dsm" family.
Features: tongues: periods
Selected region: 0.5 <= a < 1, 0.0625 <= b < 1
up to period 10 (1/1000)
check each parameters on 5 different orbits
orbit_initial_segment_length = 30
result is a 800x800 image called "ddsm.png"
SIMILAR (with different parameters):
- straight-sine-full.conf: for the family "doubling plus straight sine", 0 <= a < 1, 0.5 <= b < 2
- tent.conf: "doubling plus tent" family
- tent-all.conf
- tongues-straight-sine.conf

- tongues-straight-sine-data.conf:
saves all the results:
the values of a & b in dss-ab.txt,
the detected periods in dss-periods.txt,
the tail of the computed orbits in dss-x.txt

### Bifurcation diagrams

HERE/
bifd-doub-tent-dense-a.conf:
Will draw bifurcation diagram for b = 1
save a 1250x1250 image named "tent-bifdia-dense-bw.png"
Family: "doubling plus tent"
for 0.375 <= a < 0.5 (on the width)


## Other source files

1. `ezInputConf.py`: a home made library used to process configuration files using the module `configparser`
1. `setup.py` : setup file for compiling the Cython sources
1. `tonglib.pyx`: Cython library doing all the intensive computations

The `tonglib.pyx` contains the declaration of a `tongue_system` class that can be used to compute dynamical features of the families of mappings mentioned above.
It uses mainly iteration and check if orbits can be periodic.
The member function `create_tongue_picture` does the following.
It computes some orbits of points corresponding to the parameters in the selected window
then check if they could be periodic and create an array containing the corresponding periods.
The starting points of the orbits are equaly spaced.
It can returns the computed orbit if required.
The test on periodicity wokrs as follows. First it computes the orbit up some iterate, then iterates a few more times and check wether the last iterates are close to a periodic orbit.

To use this module instantiate a `tongue_system`, then call `set_dynamics_params` to set the parameters of the family and finally call `create_tongue_picture`.
It uses NumPy arrays: `parameters_grid`, `parameters_fates`, `parameters_periods`.










