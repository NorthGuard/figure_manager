import re
from functools import lru_cache

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
        self.__figure_manager = None
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
            self.__figure_manager = None
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
        self.__figure_manager, fig = self.create_test_figure()

        if self.__figure_manager is not None:
            # Make full screen and get geometry
            self.__figure_manager.full_screen_toggle()
            plt.pause(self._delay)
            full_screen = self.__figure_manager.window.geometry()

            # In newer versions this is passed as a string
            if isinstance(full_screen, str):
                dims = re.search(r"^(\d+)x(\d+)", full_screen)
                screen_size = (0, 0, int(dims.group(1)), int(dims.group(2)))
            else:
                screen_size = tuple(np.array(full_screen.getRect()) + _BAR_ADJUST)

            # Set measured dimensions
            self.screen_dimensions = QRect(*screen_size)
            self.__figure_manager.full_screen_toggle()
            self.__figure_manager.destroy()

        else:
            if self.verbose:
                print("_FigureMeasurer: On non-interactive and thus not initializing")
        plt.close(fig)

    def measure_test_figure(self):
        """
        Measure the current test figure (use after create_test_figure()).
        The FigureManager is initialized after measure_test_figure() has run.
        """
        if self.__figure_manager:
            self.__figure_manager.window.showMaximized()
            self.screen_dimensions = self.__figure_manager.window.geometry()
            self.__figure_manager.destroy()
            self.__figure_manager = None
        else:
            print("First run 'create_test_figure()'")

        return self.get_screen_dimensions()

    def get_dimensions(self):
        if not self.screen_dimensions:
            raise Exception("Something is wrong in _FigureMeasurer")
        full = self.screen_dimensions  # type: QRect
        x, y, _, _ = full.getCoords()
        height = full.height()
        width = full.width()

        return x, y, width, height

    def create_test_figure(self, text="Test Figure"):
        fig = plt.figure()
        try:
            plt.pause(self._delay)
        except TypeError:
            pass
        try:
            figure_manager = plt.get_current_fig_manager()
        except AttributeError:
            figure_manager = None
        plt.text(0.5, 0.5, text, ha="center", va="center", fontsize=40)
        ax = plt.gca()
        ax.spines['left'].set_color('none')
        ax.spines['right'].set_color('none')
        ax.spines['bottom'].set_color('none')
        ax.spines['top'].set_color('none')
        ax.xaxis.set_ticks([])
        ax.yaxis.set_ticks([])
        self.__figure_manager = figure_manager
        return figure_manager, fig

    def set_figure_position(self, position, figure=None):
        plt.pause(self._delay)

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

                if self.verbose:
                    print("_FigureMeasurer: On non-interactive and leaving figures as is")
                # Working on non-interactive machine
                pass

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
