import matplotlib.pyplot as plt
from figure_manager import get_figure_manager

# Get figure manager
figm = get_figure_manager()
print(f"FigureManager screen dimensions: {figm.figure_measurer.screen_dimensions}")

# Figure 1
fig1 = plt.figure()
plt.scatter([1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 9, 2, 8, 3, 7, 4, 6, 5])

# Snap this one to the top left
figm.split_2x2.ul()

# Figure 2
fig2 = plt.figure()
plt.plot([1, 2, 3, 4, 5, 6, 5, 4, 3, 2, 1], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])

# Snap this one to the full bottom
figm.b()

# Figure 3
fig3 = plt.figure()
plt.scatter([1, 1, 1, 2, 3, 3, 3, 4, 5], [1, 2, 3, 3, 3, 2, 1, 1, 1])

# Snap this one to a custom location of [1, 2] in a grid of [8, 3] positions
figm.position(n_rows=8, n_cols=3, row_nr=1, col_nr=2)
