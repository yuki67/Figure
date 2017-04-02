from math import pi
from Figure import Fractal, Polygon
from Figure2D import point_2d, Circle
from MyMatrix import Matrix


class ExpandingCarpet(Fractal):
    """ 目の錯覚で手書きみたいに見える """

    def __init__(self, points, n):
        center = sum(points, point_2d(0.0, 0.0)).scaled(1 / len(points))
        r = 1 / 2
        args = [
            [(0.5, 0.5), 0.0, (r, r), (p - center)] for p in points
        ] + [
            [(0.5, 0.5), pi / 4, (2**-0.5, 2**-0.5), (0.0, 0.0)]
        ]
        generator = [Matrix.affine2D(c, r, s, t) for c, r, s, t in args]
        super().__init__(Polygon(points), generator, n, False)

figure = ExpandingCarpet(Circle(point_2d(0.5, 0.5), 2**-0.55 / 2).circle_points(4, True), 5)
