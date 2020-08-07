from figure_manager.figure_measurer import _FigureMeasurer


class _Splitter:
    def __init__(self, figure_measurer: _FigureMeasurer):
        self._figure_measurer = figure_measurer  # type: _FigureMeasurer

    def position(self, n_rows, n_cols, row_nr, col_nr, figure=None):
        position = self._figure_measurer.get_qrect(n_rows=n_rows, n_cols=n_cols, row=row_nr, col=col_nr)
        self._figure_measurer.set_figure_position(position, figure)


class _Split2x2(_Splitter):
    def __init__(self, figure_measurer):
        """
        :param figure_manager.figure_measurer._FigureMeasurer figure_measurer:
        """
        super().__init__(figure_measurer=figure_measurer)

    def ul(self, figure=None):
        self.position(n_rows=2, n_cols=2, row_nr=0, col_nr=0, figure=figure)

    def ur(self, figure=None):
        self.position(n_rows=2, n_cols=2, row_nr=0, col_nr=1, figure=figure)

    def bl(self, figure=None):
        self.position(n_rows=2, n_cols=2, row_nr=1, col_nr=0, figure=figure)

    def br(self, figure=None):
        self.position(n_rows=2, n_cols=2, row_nr=1, col_nr=1, figure=figure)

    def moves(self):
        return [self.ul, self.ur, self.bl, self.br]


class _Split3x2(_Splitter):
    def __init__(self, figure_measurer):
        """
        :param figure_manager.figure_measurer._FigureMeasurer figure_measurer:
        """
        super().__init__(figure_measurer=figure_measurer)

    def ul(self, figure=None):
        self.position(n_rows=3, n_cols=2, row_nr=0, col_nr=0, figure=figure)

    def ml(self, figure=None):
        self.position(n_rows=3, n_cols=2, row_nr=1, col_nr=0, figure=figure)

    def bl(self, figure=None):
        self.position(n_rows=3, n_cols=2, row_nr=2, col_nr=0, figure=figure)

    def ur(self, figure=None):
        self.position(n_rows=3, n_cols=2, row_nr=0, col_nr=1, figure=figure)

    def mr(self, figure=None):
        self.position(n_rows=3, n_cols=2, row_nr=1, col_nr=1, figure=figure)

    def br(self, figure=None):
        self.position(n_rows=3, n_cols=2, row_nr=2, col_nr=1, figure=figure)

    def moves(self):
        return [self.ul, self.ml, self.bl, self.ur, self.mr, self.br]


class _Split3x1(_Splitter):
    def __init__(self, figure_measurer):
        """
        :param figure_manager.figure_measurer._FigureMeasurer figure_measurer:
        """
        super().__init__(figure_measurer=figure_measurer)

    def u(self, figure=None):
        self.position(n_rows=3, n_cols=1, row_nr=0, col_nr=0, figure=figure)

    def m(self, figure=None):
        self.position(n_rows=3, n_cols=1, row_nr=1, col_nr=0, figure=figure)

    def b(self, figure=None):
        self.position(n_rows=3, n_cols=1, row_nr=2, col_nr=0, figure=figure)

    def moves(self):
        return [self.u, self.m, self.b]


class _Split1x3(_Splitter):
    def __init__(self, figure_measurer):
        """
        :param figure_manager.figure_measurer._FigureMeasurer figure_measurer:
        """
        super().__init__(figure_measurer=figure_measurer)

    def l(self, figure=None):
        self.position(n_rows=1, n_cols=3, row_nr=0, col_nr=0, figure=figure)

    def m(self, figure=None):
        self.position(n_rows=1, n_cols=3, row_nr=0, col_nr=1, figure=figure)

    def r(self, figure=None):
        self.position(n_rows=1, n_cols=3, row_nr=0, col_nr=2, figure=figure)

    def moves(self):
        return [self.l, self.m, self.r]
