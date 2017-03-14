""" 2次元の図形 """
from Figure import Figure, Point, Line


class Point3D(Point):
    """ 3次元の点 """

    def __init__(self, lst):
        assert len(lst) == 3
        super().__init__(lst + [1.0])


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


class Box(Figure):
    """ 直方体 """

    def __init__(self, a, b):
        super().__init__(4)
        self.a = a
        self.b = b

    def __iter__(self):
        x, y, z, _ = self.a
        s, t, u, _ = self.b
        return iter([Line(self.a, Point3D([x, y, u])),
                     Line(self.a, Point3D([x, t, z])),
                     Line(self.a, Point3D([s, y, z])),
                     Line(self.b, Point3D([s, t, z])),
                     Line(self.b, Point3D([s, y, u])),
                     Line(self.b, Point3D([x, t, u])),
                     Line(Point3D([x, t, z]), Point3D([s, t, z])),
                     Line(Point3D([s, y, z]), Point3D([s, t, z])),
                     Line(Point3D([s, y, z]), Point3D([s, y, u])),
                     Line(Point3D([x, t, z]), Point3D([x, t, u])),
                     Line(Point3D([x, t, u]), Point3D([x, y, u])),
                     Line(Point3D([x, y, u]), Point3D([s, y, u]))])
