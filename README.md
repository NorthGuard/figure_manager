# figure_manager

The FigureManager can be used to quickly snap a matplotlib-figure to various positions on the screen, 
for example consistently showing two figures, one above the other, on the left side of the screen. 


### Usage

The figure manager is created by:

```python
from figure_manager import FigureManager
import matplotlib.pyplot as plt
import numpy as np

# Create figure-manager
figm = FigureManager()

# Make a figure and put it in the top-left corner
plt.figure()
xs = np.linspace(0, 6, 200)
ys = np.sin(xs)
plt.plot(xs, ys)
plt.show()
figm.split_2x2.ul()
```

When the figure-manager is initialized it creates a *test-figure*. This test-figure is then maximized, 
has its size measured and then closed (takes a fraction of a second). This is the way the figure-manager knows the 
size of the given monitor. 

#### Available commands

Full-screen figure:
```
figm.full()
```

Left or right side of screen:
```
figm.l()
figm.r()
```

2-by-2 split of screen. Upper-left, upper-right, bottom-left and bottom-right:
```
figm.split_2x2.ul()
figm.split_2x2.ur()
figm.split_2x2.bl()
figm.split_2x2.br()
```

3-by-2 split of screen. Upper-left, middle-left,  bottom-left, upper-right, middle-right and bottom-right:
```
figm.split_3x2.ul()
figm.split_3x2.ml()
figm.split_3x2.bl()
figm.split_3x2.ur()
figm.split_3x2.mr()
figm.split_3x2.br()
```

3-by-1 split of screen. Upper, middle and bottom:
```
figm.split_3x1.u()
figm.split_3x1.m()
figm.split_3x1.b()
```


#### Test Script

Run `python -m figure_manager` for a test-script illustrating how everything works. It first asks if the user wants to 
see all available figure-positions. Answering "Y" to this creates 16 figures in the specified locations.
The script also creates a single remaining figure, that can then be moved around using the figure manager.


### Screenshots from Test Script

##### Full screen
![Full-screen figure.][full]
  
##### Left and right
![Left and right figure.][lr]
  
##### 2-by-2 figures
![2-by-2 figure grid.][2x2]
  
##### 3-by-2 figures
![3-by-2 figure grid.][3x2]
  
##### 3-by-1 figures
![3-by-1 figure grid.][3x1]  

[full]: https://github.com/North-Guard/figure_manager/blob/master/screenshots/full.png "Full-screen figure."
[lr]: https://github.com/North-Guard/figure_manager/blob/master/screenshots/lr.png "Left and right figure."
[2x2]: https://github.com/North-Guard/figure_manager/blob/master/screenshots/2x2.png "2-by-2 figure grid."
[3x2]: https://github.com/North-Guard/figure_manager/blob/master/screenshots/3x2.png "3-by-2 figure grid."
[3x1]: https://github.com/North-Guard/figure_manager/blob/master/screenshots/3x1.png "3-by-1 figure grid."
