""" 図形描画のテスト """
from math import pi
from Figure import Fractal, Polygon
from Figure2D import point_2d, Circle
from MyMatrix import Matrix


class Test(Fractal):

    def __init__(self, points, n):
        center = sum(points, point_2d(0.0, 0.0)).scaled(1 / len(points))
        r = 1 / 4
        args = [
            [(0.5, 0.5), 0.0, (r, r), (points[0] - center).scaled(1 - r)],
            [(0.5, 0.5), 0.0, (r, r), (points[1] - center).scaled(1 - r)],
            [(0.5, 0.5), 0.0, (r, r), (points[2] - center).scaled(1 - r)],

            [(0.5, 0.5), pi / 3, (r, r), (points[0] - center).scaled(1 - 2 * r)],
            [(0.5, 0.5), pi / 3, (r, r), (points[1] - center).scaled(1 - 2 * r)],
            [(0.5, 0.5), pi / 3, (r, r), (points[2] - center).scaled(1 - 2 * r)],

            [(0.5, 0.5), 0.0, (2 * r, 2 * r), ((points[0] + points[1]).scaled(0.5) - center).scaled(2 * r)],
            [(0.5, 0.5), 0.0, (2 * r, 2 * r), ((points[1] + points[2]).scaled(0.5) - center).scaled(2 * r)],
            [(0.5, 0.5), 0.0, (2 * r, 2 * r), ((points[2] + points[0]).scaled(0.5) - center).scaled(2 * r)],
        ]
        generator = [Matrix.affine2D(c, r, s, t) for c, r, s, t in args]
        super().__init__(Polygon(points), generator, n, False)

figure = Test(Circle(point_2d(0.5, 0.5), 0.5).circle_points(3, True), 4)
