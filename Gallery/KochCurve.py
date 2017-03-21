from math import pi
from Figure import Fractal, Line
from Figure2D import point_2d
from MyMatrix import Matrix


class KochCurve(Fractal):
    """ コッホ曲線 """

    def __init__(self, line, n, each=False):
        r = 1 / 3
        args = [
            [line.a, 0.0, [r, r], point_2d(0.0, 0.0)],
            [line.a, pi / 3, [r, r], (line.b - line.a).scaled(r)],
            [line.b, -pi / 3, [r, r], (line.a - line.b).scaled(r)],
            [line.b, 0.0, [r, r], point_2d(0.0, 0.0)],
        ]
        generator = [Matrix.affine2D(c, r, s, t) for c, r, s, t in args]
        super().__init__(line, generator, n, each)

figure = KochCurve(Line(point_2d(0.05, 0.5), point_2d(0.95, 0.5)), 5, False)
