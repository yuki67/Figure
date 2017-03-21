from math import pi
from Figure import Fractal, Polygon
from Figure2D import point_2d, Circle
from MyMatrix import Matrix


class Honeycomb(Fractal):
    """ ハニカム構造 """

    def __init__(self, points, n):
        center = sum(points, point_2d(0.0, 0.0)).scaled(1 / len(points))
        r = 1 / 3**0.5
        args = [
            [(0.5, 0.5), pi / 6, (r, r), p - center] for p in points
        ]
        generator = [Matrix.affine2D(c, r, s, t) for c, r, s, t in args]
        super().__init__(Polygon(points), generator, n, True)

figure = Honeycomb(Circle(point_2d(0.5, 0.5), 2 / 9).circle_points(6, True), 4)
