from functools import lru_cache

from figure_manager.figure_measurer import _NoOpFigureMeasurer, _get_figure_measurer, _FigureMeasurer
from figure_manager.splitters import _Split2x2, _Split3x2, _Split3x1, _Split1x3, _Splitter

try:
    from PyQt5.QtCore import QRect
except ImportError:
    # raise ImportError("Could not import PyQt4.QtCore.QRect or matplotlib.pyplot")
    QRect = None

# TODO: Make the test figure print out all relevant information when closed.


def get_figure_manager(screen_dimensions=None, auto_initialize=True, delay=0.1):
    if screen_dimensions is not None and not isinstance(screen_dimensions, QRect):
        screen_dimensions = tuple(screen_dimensions)
    return _get_figure_manager(screen_dimensions=screen_dimensions, auto_initialize=auto_initialize, delay=delay)


@lru_cache(maxsize=5)
def _get_figure_manager(screen_dimensions=None, auto_initialize=True, delay=0.1):
    return FigureManager(screen_dimensions=screen_dimensions, auto_initialize=auto_initialize, delay=delay)


class FigureManager(_Splitter):
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

    def __init__(self, screen_dimensions=None, auto_initialize=True, delay=0.1):
        auto_initialize = auto_initialize if screen_dimensions is None else False
        screen_dimensions = screen_dimensions if (screen_dimensions is None or isinstance(screen_dimensions, QRect)) \
            else tuple(screen_dimensions)

        # Get figure measurer or no-op version
        try:
            figure_measurer = _get_figure_measurer(
                screen_dimensions=screen_dimensions,
                auto_initialize=auto_initialize,
                delay=delay)  # type: _FigureMeasurer
        except AttributeError:  # Running on machine without graphical interface - use no-op system
            # noinspection PyTypeChecker
            figure_measurer = _NoOpFigureMeasurer()  # type: _FigureMeasurer

        # Initialize super (splitter)
        super().__init__(figure_measurer=figure_measurer)

        # Split-managers
        self.split_2x2 = _Split2x2(figure_measurer=self.figure_measurer)
        self.split_3x2 = _Split3x2(figure_measurer=self.figure_measurer)
        self.split_3x1 = _Split3x1(figure_measurer=self.figure_measurer)
        self.split_1x3 = _Split1x3(figure_measurer=self.figure_measurer)

    @property
    def figure_measurer(self):
        return self._figure_measurer

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

    def possible_positions(self):
        return ["{}.{}()".format(_field, _move.__name__) for _move, _field in self._moves_w_fields()]

    def _test_all_positions(self):
        for _move, _field in self._moves_w_fields():
            name = "{}.{}".format(_field, _move.__name__)
            _, fig = self.figure_measurer.make_test_figure(text=name)
            # noinspection PyArgumentList
            _move(figure=fig)

    ###
    # Full screen

    def full(self, figure=None):
        self.position(n_rows=1, n_cols=1, row_nr=0, col_nr=0, figure=figure)

    ###
    # Left and right

    def l(self, figure=None):
        self.position(n_rows=1, n_cols=2, row_nr=0, col_nr=0, figure=figure)

    def r(self, figure=None):
        self.position(n_rows=1, n_cols=2, row_nr=0, col_nr=1, figure=figure)

    ###
    # Top and bottom

    def t(self, figure=None):
        self.position(n_rows=2, n_cols=1, row_nr=0, col_nr=0, figure=figure)

    def b(self, figure=None):
        self.position(n_rows=2, n_cols=1, row_nr=1, col_nr=0, figure=figure)


if __name__ == "__main__":
    figman = FigureManager()
    print("Screen dimensions: {}".format(figman.figure_measurer.screen_dimensions))

    figman._test_all_positions()
