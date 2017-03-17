""" 2次元の図形 """
from math import sin, cos, pi
from Figure import Point, Polygon
from MyMatrix import Matrix


def point_2d(x, y):
    """ 二次元の点を作る関数 """
    return Point([x, y, 1.0])



class Ellipse(Polygon):
    """ 楕円 """

    def __init__(self, center, a=None, b=None, n=50):
        # a, bがNoneの場合に限ってPolygonを第一引数から直接作る
        if not a and not b:
            self.n = n
            super().__init__(center)
        else:
            self.center = center
            self.a = a
            self.b = b
            self.n = n
            points = [Point2D([self.center[0] + self.a * cos(theta * 2 / n * pi),
                               self.center[1] + self.b * sin(theta * 2 / n * pi)]) for theta in range(self.n)]
            super().__init__(points)

    def copy(self):
        return Ellipse(self.center, self.a, self.b, self.n).transform(self.mat)

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
                             ) * Matrix.affine2D(self.center, rot=-pi + pi / 2 * 3 / n) for i in range(n)]
        else:
            return [point_2d(self.a * cos(2 * pi * i / n) + self.center[0],
                             self.a * sin(2 * pi * i / n) + self.center[1]) for i in range(n)]
