from Figure import Figure, Polygon
from Figure2D import point_2d
from MyMatrix import Matrix


class Battleground(Figure):
    """ 軍人将棋の駒が向き合っているようにみえる """

    def get_iter(self):
        if self.n == 0:
            return iter((self.poly),)

        dx = (self.poly.points[1] - self.poly.points[0])[0]
        dy = (self.poly.points[3] - self.poly.points[0])[1]
        center = sum([p for p in self.poly.points], point_2d(0, 0)).scaled(1 / 4)
        mid_points = [(self.poly.points[i - 1] + self.poly.points[i]).scaled(1 / 2) for i in range(4)]
        # ズレを(r, t)だけ追加する
        d = 0.1
        r = (-1)**self.n * d * dx
        t = (-1)**self.n * d * dy
        center = center + point_2d(r, t)
        return iter((Battleground(Polygon([self.poly.points[0], mid_points[1], center, mid_points[0]]), self.n - 1),
                     Battleground(Polygon([mid_points[1], self.poly.points[1], mid_points[2], center]), self.n - 1),
                     Battleground(Polygon([center, mid_points[2], self.poly.points[2], mid_points[3]]), self.n - 1),
                     Battleground(Polygon([mid_points[0], center, mid_points[3], self.poly.points[3]]), self.n - 1)))

    def __init__(self, poly, n):
        super().__init__(3)
        self.n = n
        self.poly = poly

points = [point_2d(0.0, 0.0), point_2d(1.0, 0.0), point_2d(1.0, 1.0), point_2d(0.0, 1.0)]
figure = Battleground(Polygon(points), 6)
