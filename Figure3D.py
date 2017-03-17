""" 2次元の図形 """
from Figure import Figure, Point, Line


def point_3d(x, y, z):
    """ 3次元の点を作る """
    return Point([x, y, z, 1.0])


class Grid(Figure):
    """ 四角形内部のグリッド """

    def __init__(self, poly, n1, n2):
        super().__init__(4)
        assert len(poly.points) == 4
        self.poly = poly
        # グリッドの分割数
        self.n1 = n1
        self.n2 = n2

    def get_iter(self):
        points = self.poly.points

        def gen():
            for p, q in zip(Line(points[0], points[1], self.n1), Line(points[3], points[2], self.n1)):
                yield Line(p, q)
            for p, q in zip(Line(points[1], points[2], self.n2), Line(points[0], points[3], self.n2)):
                yield Line(p, q)
        return gen()

    def __repr__(self):
        return "Grid(%s, %s, %s)" % (str(self.poly), str(self.n1), str(self.n2))


class Box(Figure):
    """ 直方体 """

    def __init__(self, a, b):
        super().__init__(4)
        self.a = a
        self.b = b

    def copy(self):
        return Box(self.a, self.b).transform(self.mat)

    def center(self):
        """ 中点 """
        return (self.a + self.b).scaled(0.5).transformed(self.mat)

    def get_iter(self):
        _a = self.a.transformed(self.a.mat)
        _b = self.b.transformed(self.b.mat)
        x, y, z, _ = _a
        s, t, u, _ = _b
        return iter([Line(_a, point_3d(x, y, u)),
                     Line(_a, point_3d(x, t, z)),
                     Line(_a, point_3d(s, y, z)),
                     Line(_b, point_3d(s, t, z)),
                     Line(_b, point_3d(s, y, u)),
                     Line(_b, point_3d(x, t, u)),
                     Line(point_3d(x, t, z), point_3d(s, t, z)),
                     Line(point_3d(s, y, z), point_3d(s, t, z)),
                     Line(point_3d(s, y, z), point_3d(s, y, u)),
                     Line(point_3d(x, t, z), point_3d(x, t, u)),
                     Line(point_3d(x, t, u), point_3d(x, y, u)),
                     Line(point_3d(x, y, u), point_3d(s, y, u))])

    def __repr__(self):
        return "Box(%s, %s)" % (str(self.a), str(self.b))
