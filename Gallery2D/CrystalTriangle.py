from math import pi
from Figure import Fractal, Polygon
from Figure2D import point_2d, Circle
from MyMatrix import Matrix


class CrystalTriangle(Fractal):
    """ 雪の結晶っぽい """

    def __init__(self, points, n):
        center = sum(points, point_2d(0.0, 0.0)).scaled(1 / len(points))
        r = 1 / 4
        args = [
            [(0.5, 0.5), 0.0, (r, r), (p - center).scaled(1 - r)] for p in points
        ] + [
            [(0.5, 0.5), pi, (r, r), (p - center).scaled(1 - 2 * r)] for p in points
        ] + [
            [(0.5, 0.5), pi / 3, (1 / 2, 1 / 2), (0.0, 0.0)]
        ]
        generator = [Matrix.affine2D(c, r, s, t) for c, r, s, t in args]
        super().__init__(Polygon(points), generator, n, False)

figure = CrystalTriangle(Circle(point_2d(0.5, 0.5), 0.5).circle_points(3, True), 4)
