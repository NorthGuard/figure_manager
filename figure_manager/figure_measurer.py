import re
import warnings
from functools import lru_cache

from inspect import cleandoc
import numpy as np
from PyQt5.QtCore import QRect
from matplotlib import pyplot as plt

_BAR_ADJUST = np.array([0, 23, 0, -63])  # TODO: This is not very dynamic :/


class _NoOpFigureMeasurer:
    def __init__(self, *args, **kwargs):
        pass

    def set_screen_dimensions(self, *args, **kwargs):
        pass

    def get_screen_dimensions(self, *args, **kwargs):
        pass

    def auto_initialize(self, *args, **kwargs):
        pass

    def measure_test_figure(self, *args, **kwargs):
        pass

    def get_dimensions(self, *args, **kwargs):
        pass

    def create_test_figure(self, *args, **kwargs):
        pass

    def set_figure_position(self, *args, **kwargs):
        pass

    def get_qrect(self, *args, **kwargs):
        pass


class _FigureMeasurer:
    def __init__(self, screen_dimensions=None, verbose=False, delay=0.1):
        self._delay = delay
        self._figure_manager = None
        self.screen_dimensions = None
        self.verbose = verbose

        if screen_dimensions is not None:
            if isinstance(screen_dimensions, QRect):
                self.set_screen_dimensions(screen_dimensions)
            else:
                self.set_screen_dimensions(QRect(*screen_dimensions))

    def set_screen_dimensions(self, screen_dimensions):
        """
        Set screen dimensions to specific QRect.
        :param QRect screen_dimensions:
        """
        if isinstance(screen_dimensions, QRect):
            self.screen_dimensions = screen_dimensions
            self._figure_manager = None
        else:
            raise TypeError("FigureManager passed incorrect type. " +
                            "screen_dimensions variable should be type QRect, but was{0}".format(
                                str(type(screen_dimensions))))

    def get_screen_dimensions(self):
        return self.screen_dimensions

    def auto_initialize(self):
        """
        Automatically initialize FigureManager to current screen.
        """
        self._figure_manager, fig = self.make_test_figure(return_objects=True)

        if self._figure_manager is not None:
            # Make full screen and get geometry
            self._figure_manager.full_screen_toggle()
            plt.pause(self._delay)
            full_screen = self._figure_manager.window.geometry()

            # In newer versions this is passed as a string
            if isinstance(full_screen, str):
                dims = re.search(r"^(\d+)x(\d+)", full_screen)
                screen_size = (0, 0, int(dims.group(1)), int(dims.group(2)))
            else:
                screen_size = tuple(np.array(full_screen.getRect()) + _BAR_ADJUST)

            # Set measured dimensions
            self.screen_dimensions = QRect(*screen_size)

            # Destroy
            self._figure_manager.full_screen_toggle()
            plt.close(self._figure_manager.canvas.figure)
            # self._figure_manager.destroy()

        else:
            if self.verbose:
                print("_FigureMeasurer: On non-interactive and thus not initializing")
        plt.close(fig)

    def measure_test_figure(self, verbose=True, close=True, return_dimensions=False):
        """
        Measure the current test figure (use after create_test_figure()).
        The FigureManager is initialized after measure_test_figure() has run.
        """
        if self._figure_manager:
            # self._figure_manager.window.showMaximized()
            self.screen_dimensions = self._figure_manager.window.geometry()
            # self._figure_manager.destroy()

            if close:
                plt.close(self._figure_manager.canvas.figure)
                self._figure_manager = None
        else:
            print("First run 'create_test_figure()'")

        # Get dimensions
        dimensions = self.get_screen_dimensions()

        if verbose:
            temp = list(dimensions.getRect())
            print("\n" + cleandoc(f"""
            Measurement: 
                X-coordinate (from left)  : {temp[0]}
                Y-coordinate (from top)   : {temp[1]}
                Width                     : {temp[2]}
                Height                    : {temp[3]}

            Create figure manager with:
                get_figure_manager(screen_dimensions={temp})
            """) + "\n")

        if return_dimensions:
            return dimensions

    def get_dimensions(self):
        if not self.screen_dimensions:
            raise Exception("Something is wrong in _FigureMeasurer")
        full = self.screen_dimensions  # type: QRect
        x, y, _, _ = full.getCoords()
        height = full.height()
        width = full.width()

        return x, y, width, height

    def make_test_figure(self, text="Test Figure", return_objects=False):
        try:
            plt.pause(self._delay)
        except TypeError:
            pass

        # Make figure and get figure manager
        fig = plt.figure()
        plt.pause(self._delay)
        figure_manager = plt.get_current_fig_manager()

        # Mark as test-figure
        plt.text(0.5, 0.5, text, ha="center", va="center", fontsize=40)
        description = "Move to location and adjust size for measurement. \n" \
                      "Then use measure_test_figure() to make measurement."
        plt.text(0.5, 0.25, description, ha="center", va="center", fontsize=12)
        ax = plt.gca()
        ax.spines['left'].set_color('none')
        ax.spines['right'].set_color('none')
        ax.spines['bottom'].set_color('none')
        ax.spines['top'].set_color('none')
        ax.xaxis.set_ticks([])
        ax.yaxis.set_ticks([])

        # Set and print
        self._figure_manager = figure_manager

        if return_objects:
            return figure_manager, fig

    def _set_noninteractive_size(self, position, figure=None):
        # Get figure
        if figure is None:
            figure = plt.gcf()  # type: plt.Figure
        if isinstance(figure, int):
            figure = plt.figure(figure)  # type: plt.Figure

        # Get size
        width = position.width()
        height = position.height()

        # Get dpi
        dpi = float(figure.get_dpi())

        # Set size
        figure.set_size_inches(w=width / dpi, h=height / dpi)

    def set_figure_position(self, position, figure=None):
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("error")
                plt.pause(self._delay)

        except UserWarning:
            self._set_noninteractive_size(position=position, figure=figure)

        # For systems using QRect
        try:
            if not figure:
                figure_manager = plt.get_current_fig_manager()
                figure_manager.window.setGeometry(position)
            else:
                if isinstance(figure, int):
                    figure = plt.figure(figure)
                figure.canvas.manager.window.setGeometry(position)

        except AttributeError:

            # For systems using string
            try:
                figure_manager = plt.get_current_fig_manager()
                temp = position.getCoords()
                figure_manager.window.geometry("{}x{}+{}+{}".format(temp[2], temp[3], temp[0], temp[1]))
            except AttributeError:
                self._set_noninteractive_size(position=position, figure=figure)

    def get_qrect(self, n_rows, n_cols, row, col):
        x, y, width, height = self.get_dimensions()
        height = int(height / n_rows)
        width = int(width / n_cols)
        return QRect(int(x) + col * width,
                     int(y) + row * height,
                     int(width),
                     int(height))


def _get_figure_measurer(screen_dimensions=None, auto_initialize=True, delay=0.1):
    if screen_dimensions is not None and not isinstance(screen_dimensions, QRect):
        screen_dimensions = tuple(screen_dimensions)

    return _get_figure_measurer_src(screen_dimensions=screen_dimensions, auto_initialize=auto_initialize, delay=delay)


@lru_cache(maxsize=10)
def _get_figure_measurer_src(screen_dimensions=None, auto_initialize=True, delay=0.1):
    figure_measurer = _FigureMeasurer(screen_dimensions=screen_dimensions, delay=delay)

    if auto_initialize:
        figure_measurer.auto_initialize()

    return figure_measurer
