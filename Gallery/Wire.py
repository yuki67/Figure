""" 図形描画のテスト """
from Figure import Fractal, Polygon
from Figure2D import point_2d, Circle
from MyMatrix import Matrix


class Wire(Fractal):
    """ ワイヤーが絡まったのに似てる """

    def __init__(self, points, n):
        center = sum(points, point_2d(0.0, 0.0)).scaled(1 / len(points))
        r = 0.5
        args = [
            [(0.5, 0.5), 0.0, [r, r], (points[i * 2] - center).scaled(0.5)] for i in range(len(points) // 2)
        ]
        generator = [Matrix.affine2D(c, r, s, t) for c, r, s, t in args]
        super().__init__(Polygon(points), generator, n, True)

figure = Wire(Circle(point_2d(0.5, 0.5), 0.5).circle_points(42, True), 2)
