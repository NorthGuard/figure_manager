import matplotlib.pyplot as plt
import numpy as np

try:
    from PyQt5.QtCore import QRect
except ImportError:
    # raise ImportError("Could not import PyQt4.QtCore.QRect or matplotlib.pyplot")
    pass


_BAR_ADJUST = np.array([0, 23, 0, -63])


class _FigureMeasurer:
    def __init__(self, screen_dimensions=None, verbose=False):
        self.__figure_manager = None
        self.screen_dimensions = None
        self.verbose = verbose

        if isinstance(screen_dimensions, QRect):
            self.set_screen_dimensions(screen_dimensions)

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
            self.__figure_manager.full_screen_toggle()
            full_screen = self.__figure_manager.window.geometry()
            screen_size = tuple(np.array(full_screen.getRect()) + _BAR_ADJUST)
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

    def get_dimensions(self):
        if not self.screen_dimensions:
            raise Exception("Something is wrong in FigureManager")
        full = self.screen_dimensions  # type: QRect
        x, y, _, _ = full.getCoords()
        height = full.height()
        width = full.width()

        return x, y, width, height

    @staticmethod
    def create_test_figure(title="Test Figure", text="Test Figure"):
        fig = plt.figure()
        try:
            figure_manager = plt.get_current_fig_manager()
            figure_manager.window.setWindowTitle(title)
        except AttributeError:
            figure_manager = None
        plt.text(0.5, 0.5, text, ha="center", va="center", fontsize=40)
        ax = plt.axes()
        ax.spines['left'].set_color('none')
        ax.spines['right'].set_color('none')
        ax.spines['bottom'].set_color('none')
        ax.spines['top'].set_color('none')
        ax.xaxis.set_ticks([])
        ax.yaxis.set_ticks([])
        return figure_manager, fig

    def set_figure_position(self, position, figure=None):
        try:
            if not figure:
                figure_manager = plt.get_current_fig_manager()
                figure_manager.window.setGeometry(position)
            else:
                figure.canvas.manager.window.setGeometry(position)
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


class _Split2x2:
    def __init__(self, figure_measurer):
        """
        :param _FigureMeasurer figure_measurer:
        """
        self._figure_measurer = figure_measurer

    def ul(self, figure=None):
        position = self._figure_measurer.get_qrect(2, 2, 0, 0)
        self._figure_measurer.set_figure_position(position, figure)

    def ur(self, figure=None):
        position = self._figure_measurer.get_qrect(2, 2, 0, 1)
        self._figure_measurer.set_figure_position(position, figure)

    def bl(self, figure=None):
        position = self._figure_measurer.get_qrect(2, 2, 1, 0)
        self._figure_measurer.set_figure_position(position, figure)

    def br(self, figure=None):
        position = self._figure_measurer.get_qrect(2, 2, 1, 1)
        self._figure_measurer.set_figure_position(position, figure)

    def moves(self):
        return [self.ul, self.ur, self.bl, self.br]


class _Split3x2:
    def __init__(self, figure_measurer):
        """
        :param _FigureMeasurer figure_measurer:
        """
        self._figure_measurer = figure_measurer

    def ul(self, figure=None):
        position = self._figure_measurer.get_qrect(3, 2, 0, 0)
        self._figure_measurer.set_figure_position(position, figure)

    def ml(self, figure=None):
        position = self._figure_measurer.get_qrect(3, 2, 1, 0)
        self._figure_measurer.set_figure_position(position, figure)

    def bl(self, figure=None):
        position = self._figure_measurer.get_qrect(3, 2, 2, 0)
        self._figure_measurer.set_figure_position(position, figure)

    def ur(self, figure=None):
        position = self._figure_measurer.get_qrect(3, 2, 0, 1)
        self._figure_measurer.set_figure_position(position, figure)

    def mr(self, figure=None):
        position = self._figure_measurer.get_qrect(3, 2, 1, 1)
        self._figure_measurer.set_figure_position(position, figure)

    def br(self, figure=None):
        position = self._figure_measurer.get_qrect(3, 2, 2, 1)
        self._figure_measurer.set_figure_position(position, figure)

    def moves(self):
        return [self.ul, self.ml, self.bl, self.ur, self.mr, self.br]


class _Split3x1:
    def __init__(self, figure_measurer):
        """
        :param _FigureMeasurer figure_measurer:
        """
        self._figure_measurer = figure_measurer

    def u(self, figure=None):
        position = self._figure_measurer.get_qrect(3, 1, 0, 0)
        self._figure_measurer.set_figure_position(position, figure)

    def m(self, figure=None):
        position = self._figure_measurer.get_qrect(3, 1, 1, 0)
        self._figure_measurer.set_figure_position(position, figure)

    def b(self, figure=None):
        position = self._figure_measurer.get_qrect(3, 1, 2, 0)
        self._figure_measurer.set_figure_position(position, figure)

    def moves(self):
        return [self.u, self.m, self.b]


class FigureManager:
    """
    Handles the positioning of figures and can be initialized in three different ways:
        1.  FigureManager(QRect)
            - Initializes the object with a screen-size specified in the QRect.
        2.  FigureManager()
            auto_initialize()
            - Automatically fits FigureManager to the current screen.
        3.  FigureManager()
            create_test_figure()
            Move test figure to wanted monitor
            measure_test_figure()
            - Can be used to make the FigureManager automatically measure a secondary monitor and fit to this screen.
    After initialization, FigureManager.set_figure_position(position, figure) can be used to move a figure to a
    wanted position. I no figure is given it will move the current figure.
    get_possible_positions() can be used to find possible position identifiers.
    """

    def __init__(self, screen_dimensions=None, auto_initialize=True):
        self.figure_measurer = _FigureMeasurer(screen_dimensions=screen_dimensions)

        if auto_initialize:
            self.figure_measurer.auto_initialize()

        # Split-managers
        self.split_2x2 = _Split2x2(figure_measurer=self.figure_measurer)
        self.split_3x2 = _Split3x2(figure_measurer=self.figure_measurer)
        self.split_3x1 = _Split3x1(figure_measurer=self.figure_measurer)

    def _moves(self):
        return [item[0] for item in self._moves_w_fields()]

    def _moves_w_fields(self):
        moves = [self.full, self.l, self.r,
                 *self.split_2x2.moves(),
                 *self.split_3x2.moves(),
                 *self.split_3x1.moves()]
        fields = [""] * 3 + \
                 [".split_2x2"] * len(self.split_2x2.moves()) + \
                 [".split_3x2"] * len(self.split_3x2.moves()) + \
                 [".split_3x1"] * len(self.split_3x1.moves())
        return list(zip(moves, fields))

    def possible_position(self):
        return ["{}.{}()".format(_field, _move.__name__) for _move, _field in self._moves_w_fields()]

    def test_all_positions(self):
        for _move, _field in self._moves_w_fields():
            name = "{}.{}".format(_field, _move.__name__)
            _, fig = self.figure_measurer.create_test_figure(name, name)
            _move(fig)

    ###
    # Full screen

    def full(self, figure=None):
        self.figure_measurer.set_figure_position(self.figure_measurer.screen_dimensions, figure)

    ###
    # Left and right

    def l(self, figure=None):
        position = self.figure_measurer.get_qrect(1, 2, 0, 0)
        self.figure_measurer.set_figure_position(position, figure)

    def r(self, figure=None):
        position = self.figure_measurer.get_qrect(1, 2, 0, 1)
        self.figure_measurer.set_figure_position(position, figure)
