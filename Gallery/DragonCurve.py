from math import pi
from Figure import Fractal, Line
from Figure2D import point_2d
from MyMatrix import Matrix


class DragonCurve(Fractal):
    """ ドラゴン曲線 """

    def __init__(self, line, n, each=True):
        r = 2 ** -0.5
        args = [
            [line.a, -pi / 4, [r, r], point_2d(0.0, 0.0)],
            [line.a, -pi / 4 * 3, [r, r], line.b - line.a],
        ]
        generator = [Matrix.affine2D(c, r, s, t) for c, r, s, t in args]
        super().__init__(line, generator, n, each)

figure = DragonCurve(Line(point_2d(0.2, 0.5), point_2d(0.8, 0.5)), 12, False)
