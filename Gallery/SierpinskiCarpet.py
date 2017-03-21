""" 図形描画のテスト """
from Figure import Fractal, Polygon
from Figure2D import point_2d, Circle
from MyMatrix import Matrix


class HandWriteSquare(Fractal):
    """ 目の錯覚で手書きみたいに見える """

    def __init__(self, points, n):
        center = sum(points, point_2d(0.0, 0.0)).scaled(1 / len(points))
        r = 1 / 3
        args = [
            [(0.5, 0.5), 0.0, (r, r), (p - center).scaled(1 - r)] for p in points
        ] + [
            [(0.5, 0.5), 0.0, (r, r), ((points[i - 1] + points[i]).scaled(0.5) - center).scaled(1 - r)] for i in range(len(points))
        ]
        generator = [Matrix.affine2D(c, r, s, t) for c, r, s, t in args]
        super().__init__(Polygon(points), generator, n, True)

figure = HandWriteSquare(Circle(point_2d(0.5, 0.5), 2**-0.55).circle_points(4, True), 4)
