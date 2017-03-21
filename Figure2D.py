""" 2次元の図形 """
from math import sin, cos, pi
from Figure import Figure, Line, Point, Polygon
from MyMatrix import Matrix


def point_2d(x, y):
    """ 二次元の点を作る関数 """
    return Point([x, y, 1.0])


class Ellipse(Figure):
    """ 楕円 """

    def __init__(self, center, a, b, n=50):
        super().__init__(3)
        self.center = center
        self.a = a
        self.b = b
        self.n = n

    def copy(self):
        return Ellipse(self.center, self.a, self.b, self.n).transform(self.mat)

    def get_iter(self):
        def ans():
            p = point_2d(self.center[0] + self.a * cos(-2 / self.n * pi),
                         self.center[1] + self.b * sin(-2 / self.n * pi))
            for i in range(self.n):
                q = point_2d(self.center[0] + self.a * cos(i * 2 / self.n * pi),
                             self.center[1] + self.b * sin(i * 2 / self.n * pi))
                yield Line(p, q)
                p = q
        return ans()

    def transformed(self, mat):
        return Polygon([point_2d(self.center[0] + self.a * cos(i * 2 / self.n * pi),
                                 self.center[1] + self.b * sin(i * 2 / self.n * pi)).transform(mat) for i in range(self.n)])

    def __repr__(self):
        return "Ellipse(%s, %s, %s)" % (self.center, self.a, self.b)


class Circle(Ellipse):
    """ 円 """

    def __init__(self, center, r, n=50):
        super().__init__(center, r, r, n)

    def __repr__(self):
        return "Circle(%s, %s)" % (str(self.center), str(self.a))

    def copy(self):
        return Circle(self.center, self.a).transform(self.mat)

    def circle_points(self, n, stand=False):
        """
        演習をn分割するの点を返す
        stand=Trueの場合、n角形が立つように回転させてから返す
        """
        if stand:
            return [point_2d(self.a * cos(2 * pi * i / n) + self.center[0],
                             self.a * sin(2 * pi * i / n) + self.center[1]
                             ) * Matrix.affine2D(self.center, rot=-pi / 2 + pi * 3 / n) for i in range(n)]
        else:
            return [point_2d(self.a * cos(2 * pi * i / n) + self.center[0],
                             self.a * sin(2 * pi * i / n) + self.center[1]) for i in range(n)]


class Circloid(Figure):
    """ サークロイド(造語) """

    def __init__(self, circle, n, f):
        super().__init__(3)
        self.circle = circle
        self.n = n
        self.f = f

    def __iter__(self):
        points = self.circle.circle_points(self.n)
        for i in range(self.n):
            for j in range(self.n):
                if self.f(i, j):
                    yield Line(points[i], points[j])
