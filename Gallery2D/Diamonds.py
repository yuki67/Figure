from math import sin, pi
from Figure import Figure, Polygon
from Figure2D import point_2d


class Diamonds(Figure):
    """ ひし形がたくさん並ぶ """

    def get_iter(self):
        if self.n == 0:
            return iter((self.poly),)

        dx = (self.poly.points[1] - self.poly.points[0])[0]
        dy = (self.poly.points[3] - self.poly.points[0])[1]
        center = sum([p for p in self.poly.points], point_2d(0, 0)).scaled(1 / 4)
        mid_points = [(self.poly.points[i - 1] + self.poly.points[i]).scaled(1 / 2) for i in range(4)]
        # ズレを(r, t)だけ追加する
        d = 0.1
        f = lambda x, y: d * dx * sin(x * 8 * pi)
        g = lambda x, y: d * dy * sin(y * 8 * pi)
        r = f((center[0] - 0.5) * 2, (center[1] - 0.5) * 2)
        t = g((center[0] - 0.5) * 2, (center[1] - 0.5) * 2)
        center = center + point_2d(r, t)
        return iter((Diamonds(Polygon([self.poly.points[0], mid_points[1], center, mid_points[0]]), self.n - 1),
                     Diamonds(Polygon([mid_points[1], self.poly.points[1], mid_points[2], center]), self.n - 1),
                     Diamonds(Polygon([center, mid_points[2], self.poly.points[2], mid_points[3]]), self.n - 1),
                     Diamonds(Polygon([mid_points[0], center, mid_points[3], self.poly.points[3]]), self.n - 1)))

    def __init__(self, poly, n):
        super().__init__(3)
        self.n = n
        self.poly = poly

s = 1.0
points = [point_2d(0.0, 0.0), point_2d(s, 0.0), point_2d(s, s), point_2d(0.0, s)]
figure = Diamonds(Polygon(points), 7)
