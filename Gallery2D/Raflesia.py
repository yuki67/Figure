from math import sin, pi
from Figure import Figure, Polygon
from Figure2D import point_2d
from MyMatrix import Matrix


class Raflesia(Figure):
    """ ラフレシアの花に似てる """

    def get_iter(self):
        if self.n == 0:
            return iter((self.poly),)

        center = sum([p for p in self.poly.points], point_2d(0, 0)).scaled(1 / 4)
        mid_points = [(self.poly.points[i - 1] + self.poly.points[i]).scaled(1 / 2) for i in range(4)]
        points = [self.poly.points[3], mid_points[3], self.poly.points[2],
                  mid_points[0], center, mid_points[2],
                  self.poly.points[0], mid_points[1], self.poly.points[1]]

        f = lambda x, y: (x * 0.9 + 0.1 * x * sin(4 * pi * y),
                          y * 0.9 + 0.1 * y * sin(4 * pi * x))
        for i, p in enumerate(points):
            points[i] = point_2d(*f(p[0], p[1]))
        return iter((Raflesia(Polygon([points[6], points[7], points[4], points[3]]), self.n - 1),
                     Raflesia(Polygon([points[7], points[8], points[5], points[4]]), self.n - 1),
                     Raflesia(Polygon([points[4], points[5], points[2], points[1]]), self.n - 1),
                     Raflesia(Polygon([points[3], points[4], points[1], points[0]]), self.n - 1)))

    def __init__(self, poly, n):
        super().__init__(3)
        self.n = n
        self.poly = poly

s = 1.0
points = [point_2d(0.0, 0.0), point_2d(s, 0.0), point_2d(s, s), point_2d(0.0, s)]
figure = Raflesia(Polygon(points), 6).transform(Matrix.affine2D(trans=[0.025, 0.025], scale=[1.2, 1.2]))
