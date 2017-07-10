

import matplotlib.pyplot as plt
import numpy as np

from figure_manager import FigureManager

figm = FigureManager()
print(f"FigureManager screen dimensions: {figm.figure_measurer.screen_dimensions}")

plt.close("all")

# Showing all positions
query_text = "Do you want to look at all possible figure positions? (Y/N)" \
             "\nThis will create {} figures on the screen.".format(len(figm.possible_position()))
answer = input(query_text)
if "y" in answer.lower() and "n" not in answer.lower():
    figm.test_all_positions()

# Making a single figure for moving around
plt.figure()
xs = np.linspace(0, 6, 200)
ys = np.sin(xs)
plt.plot(xs, ys)
plt.show()
figm.split_2x2.bl()

print("\nMove figure around with one of the commands")
for move in figm.possible_position():
    print("figm" + move)

plt.show(block=True)
