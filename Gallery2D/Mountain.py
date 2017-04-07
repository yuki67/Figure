import random
from Figure import Figure, Polygon
from Figure2D import point_2d


class Mountain(Figure):
    """ 山 """

    def get_iter(self):
        if self.n == 0:
            return iter((self.poly),)

        dx = (self.poly.points[1] - self.poly.points[0])[0]
        dy = (self.poly.points[3] - self.poly.points[0])[1]
        # ズレを(r, t)だけ追加する
        d = 0.25
        r = (2 * d * random.random()**2 - d) * dx
        t = (2 * d * random.random()**2 - d) * dy
        center = sum([p for p in self.poly.points], point_2d(0, 0)).scaled(1 / 4) + point_2d(r, t)
        mid_points = [(self.poly.points[i - 1] + self.poly.points[i]).scaled(1 / 2) for i in range(4)]
        return iter((Mountain(Polygon([self.poly.points[0], mid_points[0], center, mid_points[1]]), self.n - 1),
                     Mountain(Polygon([self.poly.points[1], mid_points[1], center, mid_points[2]]), self.n - 1),
                     Mountain(Polygon([self.poly.points[2], mid_points[2], center, mid_points[3]]), self.n - 1),
                     Mountain(Polygon([self.poly.points[3], mid_points[3], center, mid_points[0]]), self.n - 1)))

    def __init__(self, poly, n):
        super().__init__(3)
        self.n = n
        self.poly = poly

points = [point_2d(0.0, 0.0), point_2d(1.0, 0.0), point_2d(1.0, 1.0), point_2d(0.0, 1.0)]
figure = Mountain(Polygon(points), 5)
