from Figure import Fractal, Polygon
from Figure2D import point_2d, Circle
from MyMatrix import Matrix


class SierpinskiGasket(Fractal):
    """ シェルピンスキーのギャスケット """

    def __init__(self, points, n):
        center = sum(points, point_2d(0.0, 0.0)).scaled(1 / len(points))
        args = [
            [center, 0.0, [0.5, 0.5], (p - center).scaled(0.5)] for p in points
        ]
        generator = [Matrix.affine2D(c, r, s, t) for c, r, s, t in args]
        super().__init__(Polygon(points), generator, n)

figure = SierpinskiGasket(Circle(point_2d(0.5, 0.5), 0.5).circle_points(3, True), 7)
