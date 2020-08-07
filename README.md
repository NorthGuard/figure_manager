# figure_manager

`figure_manager` can snap matplotlib-figures to various positions on the screen.  
For example, more one figure to upper-left corner of the screen or make a figure full-screen. 

### Example

The figure manager is used as follows:

```python
import matplotlib.pyplot as plt
import numpy as np
from figure_manager import get_figure_manager

# Get figure-manager
figm = get_figure_manager()  # Here the figure manager measures the screen

# Make a figure
plt.figure()
xs = np.linspace(0, 6, 200)
ys = np.sin(xs)
plt.plot(xs, ys)
plt.show()

# Split screen into a 2-by-2 grid and move figure to upper-left corner
figm.split_2x2.ul()
```

When the figure-manager is initialized it creates a *test-figure*, which is then maximized, used to 
measure the size of the screen and closed (takes a fraction of a second). 

### Installation
Install by `pip install figure-manager`



## More Usage

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

Custom grid and position
```
figm.position(n_rows=8, n_cols=3, row_nr=1, col_nr=2)
```


#### Test Script

The `example.py` further exemplifies the use.


### Screenshots of grid

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

[full]: https://github.com/NorthGuard/figure_manager/blob/master/figure_manager/screenshots/full.png "Full-screen figure."
[lr]: https://github.com/NorthGuard/figure_manager/blob/master/figure_manager/screenshots/lr.png "Left and right figure."
[2x2]: https://github.com/North-Guard/figure_manager/blob/master/figure_manager/screenshots/2x2.png "2-by-2 figure grid."
[3x2]: https://github.com/North-Guard/figure_manager/blob/master/figure_manager/screenshots/3x2.png "3-by-2 figure grid."
[3x1]: https://github.com/North-Guard/figure_manager/blob/master/figure_manager/screenshots/3x1.png "3-by-1 figure grid."
