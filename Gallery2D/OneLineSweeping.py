from math import pi
from Figure import Fractal, Line
from Figure2D import point_2d
from MyMatrix import Matrix


class OneLineSweeping(Fractal):
    """ 直線からの掃討 """

    def __init__(self, line, n, each=True):
        p = (line.b - line.a).scaled(0.5)
        args = [
            [line.a, pi / 4, [2**-0.5, 2**-0.5], point_2d(0.0, 0.0), [False, True]],
            [line.a, 0, [0.5, 0.5], point_2d(p[1], p[0]) + p, [False, False]],
            [line.b, -pi / 2, [0.5, 0.5], point_2d(-p[1], p[0]), [True, True]],
        ]
        generator = [Matrix.affine2D(c, r, s, t, m) for c, r, s, t, m in args]
        super().__init__(line, generator, n, each)

figure = OneLineSweeping(Line(point_2d(0.05, 0.05), point_2d(0.95, 0.05)), 6, True)
