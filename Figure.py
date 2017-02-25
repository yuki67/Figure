from itertools import chain
from math import ceil, pi, sin, cos
from MyMatrix import Matrix

transform = Matrix.identity(3)


class Figure(object):

    def get_iter(self):
        """ イテレータを"新しく作って"返す """
        pass

    def __iter__(self):
        return self.get_iter()

    def get_points(self):
        """ selfのなかの部分図形が詰まったリストを返す """
        return list(self.get_iter())

    def transformed(self, mat):
        """ selfを行列matで変形してものを返す """
        class Temp(Figure):

            def get_iter(_self):
                return (x.transformed(mat) for x in self)
        return Temp()


def FigureUnion(a, b):
    """ aとbを一緒にした図形を返す """
    class Temp(Figure):

        def get_iter(self):
            return chain(a.get_iter(), b.get_iter())
    return Temp()


class Point(list, Figure):
    """ 点 """

    def __init__(self, lst):
        super().__init__(lst[:2])

    def __repr__(self):
        return "Point(%s)" % str(list(self))

    def interpolate(self, b, r):
        """
        selfとbをr:(1-r)に内分する点を返す(0<r<1)
        r = 0 で self
        r = 1 で b
        """
        return Point((b - self).scale(r) + self)

    def __add__(self, other):
        return Point([a + b for a, b in zip(self, other)])

    def __sub__(self, other):
        return Point([a - b for a, b in zip(self, other)])

    def __mul__(self, other):
        temp = list.__add__(self, [1.0])
        return Point([sum([temp[j] * other[j][i] for j in range(len(other[i]))]) for i in range(len(other))])

    def scale(self, r):
        """ 座標をr倍した点を返す """
        return Point([r * x for x in self])

    def transformed(self, mat):
        return Point(self * mat)


class Line(Figure):
    """ 線分 """

    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.max = max(abs(self.a[0] - self.b[0]), abs(self.a[1] - self.b[1]))

    def get_iter(self):
        if self.max == 0:
            # 何もしないイテレータ
            return (i for i in range(0))
        else:
            return (Point.interpolate(self.a, self.b, i / self.max) for i in range(int(self.max) + 1))

    def __repr__(self):
        return "Line(%s, %s)" % (self.a.__repr__(), self.b.__repr__())

    def mid(self):
        """ 線分の中点を返す """
        return Point([a / 2 for a in self.a + self.b])

    def transformed(self, mat):
        return Line(self.a.transformed(mat), self.b.transformed(mat))


class Polygon(Figure):
    """ 多角形 """

    def __init__(self, points):
        self.points = points

    def get_iter(self):
        return (Line(self.points[i - 1], self.points[i]) for i in range(len(self.points)))

    def transformed(self, mat):
        return Polygon([p.transformed(mat) for p in self.points])

    def __repr__(self):
        return "Polygon(%s)" % str(self.points)


class Ellipse(Figure):
    """ 楕円 """

    def __init__(self, center, a, b, n=50):
        self.center = center
        self.a = a
        self.b = b
        self.n = n
        self.y = lambda x: b * (1 - (x / a) ** 2) ** 0.5
        self.x = lambda y: a * (1 - (y / b) ** 2) ** 0.5

    def get_iter(self):
        return (Line(Point([self.center[0] + self.a * cos(theta),
                            self.center[1] + self.b * sin(theta),
                            1.0]),
                     Point([self.center[0] + self.a * cos(theta + 1 / self.n * pi),
                            self.center[1] + self.b * sin(theta + 1 / self.n * pi),
                            1.0]))
                for theta in [i / self.n * pi for i in range(-self.n, self.n)])

    def transformed(self, mat):
        temp = super().transformed(mat)
        temp.center = self.center.transformed(mat)
        return temp


class Circle(Ellipse):
    """ 円 """

    def __init__(self, center, r):
        super().__init__(center, r, r)

    def transformed(self, mat):
        return Circle(self.center * mat, self.a * mat[0][0])

    def circle_points(self, n, stand=False):
        """
        演習をn分割するの点を返す
        stand=Trueの場合、n角形が立つように回転させてから返す
        """
        if stand:
            return [Point([self.a * cos(2 * pi * i / n) + self.center[0],
                           self.a * sin(2 * pi * i / n) + self.center[1],
                           1.0]) * Matrix.affine2D(self.center, -pi + pi / 2 * 3 / n) for i in range(n)]
        else:
            return [Point([self.a * cos(2 * pi * i / n) + self.center[0],
                           self.a * sin(2 * pi * i / n) + self.center[1],
                           1.0]) for i in range(n)]


class Fractal(Figure):
    """ フラクタル """

    def __init__(self, initiator, generator, n, each=False, init_generator=False):
        self.initiator = initiator
        self.generator = generator
        self.n = n
        self.each = each
        self.init_generator = init_generator if init_generator else generator

    def get_iter(self):
        if self.n == 0:
            return (self.initiator for i in range(0))
        if self.n == 1:
            return (self.initiator.transformed(gen) for gen in self.generator)
        if self.each:
            return chain((self.initiator.transformed(gen) for gen in self.generator),
                         (Fractal(self.initiator, [gen * mat for gen in self.init_generator], self.n - 1, self.each, self.init_generator) for mat in self.generator))
        return (Fractal(self.initiator, [gen * mat for gen in self.init_generator], self.n - 1, self.each, self.init_generator) for mat in self.generator)

    def __repr__(self):
        return "Fractal(%s, %d)" % (str(self.initiator), self.n)
