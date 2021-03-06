# Documentation on arnold-tongues

## What it is

The folder [`arnold-tongues`](https://github.com/alexn11/complex-dynamics-progs/tree/master/arnold-tongues) contains programs that can be used to draw parameter spaces of several families of circles maps.
The families are:
- "double standard map" / "dsm" : *f<sub>a,b</sub>(x) = 2x + a - (b/&pi;) sin(2&pi;x)* (<https://www.cmup.pt/sites/default/files/publications/double.pdf>).
- "double dsm" : *f<sub>a,b</sub>(x) = 2x + a - (b/2&pi;) sin(2&pi;x)*
- "doubling plus tent": *f<sub>a,b</sub>(x) = 2x + a + bT(x)*, with *T(x) = 2x* if *x &le; 1/2* else *T(x) = 2(1 - x)*.
- "doubling plus straight sine" : *f<sub>a,b</sub>(x) = 2x + a + (b/2) S(x)*, with *S(x) = 4x - 1* if *x &le; 1/2* else *S(x) = -4x + 3*.

The list of programs inside the folders is as follows.
1. [`tongues.py`][main prog] :
It is the main program for this folder, it is used to draw parameter spaces of several families of circle maps.
1. [`bifurcation-diagram-generator.py`][bif dia script] :
This program creates many configuration files and runs the program on them to generate a sequence of bifurcation diagrams in the "doubling plus tent" family with different values of b (for the specific parameters: see source).
1. [`graph-plot.py`][graph plot script] :
This program uses the `tonglib` module to draw a graph of some example of map from the "doubling plus straight sine" family. This uses the Python module [`mathsvg`][mathsvg module].

## What it does

The main program can do one of the following two processes.
For more details on how to run these processes see below.

### Tongues

The user can select one of the families above and a range of parameter values in the form &#91; a<sub>min</sub>, a<sub>max</sub> &#93; &times; &#91; b<sub>min</sub>, b<sub>max</sub> &#93;. 

For each parameter in a discretized version of this range the program will compute a collection of orbits and try to determine whether these orbits are periodic or not.
It will pick a color according to the detected period or a specific color if no periodicty has been found.

The result will be an image where the coloration of the pixel correspond to the computed color at the corresponding parameter.
The relation between parameter and pixel on the image is a straightforward affine mapping (the height and width of the picture are modifiable parameters).


### Bifurcation diagrams

The user can select a family, a fixed value of *b* and an interval of values of *a*.
For each value of *a* in a discretized version of the interval, the program computes a collection orbits and plot the final points of the orbit.

The result is a bifurcation diagram in the same fashion as the familiar ones.

![A bifurcation diagram generated by the script][bifdia]


## How to use

### Requirements

This runs with Python 3. The following modules are needed:
1. [NumPy](https://pypi.org/project/numpy/)
2. [ConfigParser][configparser module]

Finally [Cython](https://cython.org/) is needed for the main module of the program.

The module [mathsvg][mathsvg module] is needed only for the script [`graph-plot.py`][graph plot script].

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
python3 tongues.py path/to/conf-file
```

### Generating a picture of the tongues

Here is the general structure of the configuration file, this should be pretty straightforward to understand:
```
[Program inputs]

map_family = <name of the family>

do_draw_tongues = True
do_draw_periods = True

min_a = <min value for a>
max_a = <max value for a>
min_b = <min value for b>
max_b = <max value for b>

max_period_to_test = <max period to test>
period_test_tol = <a small number telling how much error is allowed when checking periodicity>

number_of_orbits_to_compute = <number of orbits to compute and check for periodicity>

orbit_initial_segment_length = <number of iterations to compute before checking if the orbit is periodic>

default_starting_point = <one of the orbit starting point, the other starting points will be derived from this parameter>

image_height = <image height in pixels>
image_width = <image width in pixels>

periods_image_name = <a name for the image, without the extension>

do_show_progress = True # this will show some dots
```

The program will compute `number_of_orbits_to_compute` orbits with starting point equally spaced on the 1D torus.
The value of `default_starting_point` is assigned to one of the starting point and the other are computed accordingly.

For each orbit, the program will first compute `orbit_initial_segment_length` iterates.
After that more iterates are computed and the periodicity of the resulting point is checked on these later iterates in the most naive way.
The value of `period_test_tol` is used to modulate how strict this test is.
A small value of `period_test_tol` will make the test stricter but might miss slowly converging orbits.
Inversely a larger value will introduce false positives.

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
min_a = <min a>
max_a = <max a>

number_of_orbits_to_compute = <number of orbits to compute>
default_starting_point = <one of the orbit starting point, the other starting points will be derived from this parameter>
orbit_initial_segment_length = <first iterates>
orbit_final_segment_length = <last iterates, will be drawn>

bifurcation_diagram_image_name = <image name without the extension>
image_width = <image width in pixels>
image_height = <image height in pixels>
```

The interval *&#91; min_a, max_a &#91;* is discretized into `image_width` values of *a* equally spaced.
For each value of *a*, the program will compute `number_of_orbits_to_compute` orbits with equally spaced starting points.
The value of `default_starting_point` is assigned to one of the starting point and the other starting points are computed accordingly.

The first `orbit_initial_segment_length` iterates are discarded and the program draws only the last `orbit_final_segment_length` elements of the orbit on the *y*-axis.

The script [`bifurcation-diagram-generator.py`][bif dia script] uses this functionality to draw many bifurcations diagrams for different values of *b*.
For each value of *b*, this generates a configuration file then launch the main program with this file as parameter.
The parameters of `bifurcation-diagram-generator.py` are hard coded inside the script but this is easily modifiable.

### More options

The colors for the bifurcation diagram can be modified with the following parameters:
1. `background_color`
1. `point_color`



## Examples

The `conf` directory contains examples of configuration files.

### Tongues

1. [`tongues-blowup-blowup.conf`](https://github.com/alexn11/complex-dynamics-progs/blob/master/arnold-tongues/conf/tongues-blowup-blowup.conf): to draw part of the parameter plane of the "doubling plus tent" family.
  * Selected region: *0.005505 &le; a < 0.007245, 0.99439 &le; b < 0.99613*
  * Period max: 20 (periodicity test with precision 1/1000)
  * Test on 4 different orbits
  * `orbit_initial_segment_length`: 300
  * Creates an 800x800 image file named ["project-blowup-strange-region.png"](https://github.com/alexn11/complex-dynamics-progs/blob/master/arnold-tongues/selected-results/project-blowup-strange-region.png)
1. [`ddsm.conf`](https://github.com/alexn11/complex-dynamics-progs/blob/master/arnold-tongues/conf/ddsm.conf), for the "double dsm" family.
  * *0.5 &le; a < 1, 0.0625 &le; b < 1*
  * max period 10 (1/1000 tol.)
  * 5 orbits for each parameter
  * `orbit_initial_segment_length`: 30
  * Creates an 800x800 image file named "ddsm.png"
1. Similar to the previous ones:
  * [`project-picture.conf`](https://github.com/alexn11/complex-dynamics-progs/blob/master/arnold-tongues/conf/project-picture.conf)
  * [`straight-sine-blowup.conf`](https://github.com/alexn11/complex-dynamics-progs/blob/master/arnold-tongues/conf/straight-sine-blowup.conf), for the family "doubling plus straight sine"
  * [`straight-sine-full.conf`](https://github.com/alexn11/complex-dynamics-progs/blob/master/arnold-tongues/conf/straight-sine-full.conf), for the family "doubling plus straight sine", *0 &le; a < 1, 0.5 &le; b < 2*.
  * [`tent.conf`](https://github.com/alexn11/complex-dynamics-progs/blob/master/arnold-tongues/conf/tent.conf), "doubling plus tent" family
  * [`tent-all.conf`](https://github.com/alexn11/complex-dynamics-progs/blob/master/arnold-tongues/conf/tent-all.conf)
  * [`tongues-blowup.conf`](https://github.com/alexn11/complex-dynamics-progs/blob/master/arnold-tongues/conf/tongues-blowup.conf), *0. &le; a < 0.012, 0.988 &le; b < 1*
  * [`tongues-straight-sine.conf`](https://github.com/alexn11/complex-dynamics-progs/blob/master/arnold-tongues/conf/tongues-straight-sine.conf)
  * [`tongues-straight-sine-data.conf`](https://github.com/alexn11/complex-dynamics-progs/blob/master/arnold-tongues/conf/tongues-straight-sine-data.conf), saves all the results: the values of a & b in `dss-ab.txt`, the detected periods in `dss-periods.txt`, the tail of the computed orbits in `dss-x.txt`.
  * [`tongues-straight-sine-large-region.conf`](https://github.com/alexn11/complex-dynamics-progs/blob/master/arnold-tongues/conf/tongues-straight-sine-large-region.conf)

Here are some images generated by some of the scripts above:
![Example of tongue images generated by the script][tongue-blowup]

![Example of tongue images generated by the script][full-fam]

### Bifurcation diagrams

The configuration file [`bifd-doub-tent-dense-a.conf`](https://github.com/alexn11/complex-dynamics-progs/blob/master/arnold-tongues/conf/bifd-doub-tent-dense-a.conf) can be used to draw a bifurcation diagram for *b = 1* for the "doubling plus tent" map.
It will produce a 1250x1250 image named [`tent-bifdia-dense-bw.png`][bifdia].
The interval of *a* is *0.375 &le; a < 0.5*.


## Other source files

1. [`ezInputConf.py`](https://github.com/alexn11/complex-dynamics-progs/blob/master/arnold-tongues/ezInputConf.py): a home made library used to process configuration files using the module [`configparser`][configparser module].
1. [`setup.py`](https://github.com/alexn11/complex-dynamics-progs/blob/master/arnold-tongues/setup.py) : setup file for compiling the Cython sources.
1. [`tonglib.pyx`][tonglib file]: Cython library doing all the intensive computations.

The `tonglib.pyx` contains the declaration of the `tongue_system` class.
This class is used to compute dynamical features of the families of mappings mentioned above.
It uses mainly iteration and check if orbits are close to periodic.

The member function `create_tongue_picture` is the main tool from this class.
This computes some orbits of points corresponding to the parameters in the selected window
then check if they could be periodic and create an array containing the corresponding periods.
The starting points of the orbits are equaly spaced.
It can returns the computed orbit if required.
The test on periodicity works as follows. First it computes the orbit up to some iterate, then iterates a few more times and check wether the last iterates are close to a periodic orbit.

To use this module instantiate a `tongue_system`, then call `set_dynamics_params` to set the parameters of the family and finally call `create_tongue_picture`.
It uses NumPy arrays for the following data: `parameters_grid`, `parameters_fates`, `parameters_periods`.



[bifdia]: https://github.com/alexn11/complex-dynamics-progs/blob/master/arnold-tongues/selected-results/tent-bifdia-dense-bw.png
[tongue-blowup]: https://github.com/alexn11/complex-dynamics-progs/blob/master/arnold-tongues/selected-results/straight-sine-blowup.png
[full-fam]: https://github.com/alexn11/complex-dynamics-progs/blob/master/arnold-tongues/selected-results/straight-sine-full.png
[main prog]: https://github.com/alexn11/complex-dynamics-progs/blob/master/arnold-tongues/tongues.py
[bif dia script]: https://github.com/alexn11/complex-dynamics-progs/blob/master/arnold-tongues/bifurcation-diagrams-generator.py
[mathsvg module]: https://pypi.org/project/mathsvg/
[tonglib file]: https://github.com/alexn11/complex-dynamics-progs/blob/master/arnold-tongues/tonglib.pyx
[graph plot script]: https://github.com/alexn11/complex-dynamics-progs/blob/master/arnold-tongues/graph-plot.py
[configparser module]: https://pypi.org/project/configparser/


