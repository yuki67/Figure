from Figure import Fractal, Polygon
from Figure2D import point_2d, Circle
from MyMatrix import Matrix


class City(Fractal):
    """ 都市の発達理論の説明で出てくる図に似てる """

    def __init__(self, points, n):
        center = sum(points, point_2d(0.0, 0.0)).scaled(1 / len(points))
        r = 0.5
        args = [
            [(0.5, 0.5), 0.0, [r, r], (points[i - 1] + points[i]).scaled(0.5) - center] for i in range(len(points))
        ]
        generator = [Matrix.affine2D(c, r, s, t) for c, r, s, t in args]
        super().__init__(Polygon(points), generator, n, True)

figure = City(Circle(point_2d(0.5, 0.5), 0.25).circle_points(6, True), 5)
