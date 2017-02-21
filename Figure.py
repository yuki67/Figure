from itertools import chain
from math import ceil, pi, sin, cos
from MyMatrix import Matrix

transform = Matrix.identity(3)


class Figure(object):

    def __init__(self, iterator):
        self.iter = iterator

    def __iter__(self):
        return self.iter

    def points(self):
        return list(self)

    def transformed(self, mat):
        return Figure((x.transformed(mat) for x in self))


class _Point(list, Figure):
    """
    transformを気にしない普通の点
    他のFigureが点を使うときはこちらを使う
    """

    def __repr__(self):
        return "_Point(%s)" % str(list(self))

    def interpolate(self, b, r):
        """
        selfとbをr:(1-r)に内分する点を返す(0<r<1)
        r = 0 で self
        r = 1 で b
        """
        return _Point((b - self).scale(r) + self)

    def __add__(self, other):
        return _Point([a + b for a, b in zip(self, other)])

    def __sub__(self, other):
        return _Point([a - b for a, b in zip(self, other)])

    def __mul__(self, other):
        return _Point([sum([self[j] * other[j][i] for j in range(len(other[i]))]) for i in range(len(other))])

    def scale(self, r):
        return _Point([r * x for x in self])

    def transformed(self, mat):
        return _Point(self * mat)


class Point(_Point):
    """
    Figure.scaleを気にする点
    ユーザーがプログラムで使うのはこっち
    ユーザーがFigure.scaleを適宜変更することで、扱いやすい座標系([0.0, 1.0]^2など)で図形を描くことが可能になる
    """

    def __init__(self, pos):
        """ 座標が(scale * x, scale * y)の点を返す """
        if len(pos) == 2:
            pos += [1.0]
        super().__init__(_Point(pos) * transform)


class Line(Figure):
    """ 線分 """

    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.max = max(abs(self.a[0] - self.b[0]), abs(self.a[1] - self.b[1]))

    def __repr__(self):
        return "Line(%s, %s)" % (self.a.__repr__(), self.b.__repr__())

    def __iter__(self):
        if self.max == 0:
            return (i for i in range(0))
        else:
            return (_Point.interpolate(self.a, self.b, i / self.max) for i in range(int(self.max) + 1))

    def mid(self):
        return [a / 2 for a in self.a + self.b]

    def transformed(self, mat):
        return Line(self.a.transformed(mat), self.b.transformed(mat))


class Polygon(Figure):
    """ 多角形 """

    def __init__(self, points):
        self.points = points

    def __iter__(self):
        return (Line(self.points[i - 1], self.points[i]) for i in range(len(self.points)))

    def transformed(self, mat):
        return Polygon([p.transformed(mat) for p in self.points])

    def __repr__(self):
        return "Polygon(%s)" % str(self.points)


class _Ellipse(Polygon):
    """ 楕円 """

    def __init__(self, center, a, b, n=100):
        self.center = center
        self.a = a
        self.b = b
        self.y = lambda x: b * (1 - (x / a) ** 2) ** 0.5
        self.x = lambda y: a * (1 - (y / b) ** 2) ** 0.5
        super().__init__([_Point([center[0] + a * cos(theta),
                                  center[1] + b * sin(theta),
                                  1.0])
                          for theta in [i / n * pi for i in range(-n, n)]])


class Ellipse(_Ellipse):

    def __init__(self, center, a, b):
        super().__init__(center,
                         a * transform[0][0],
                         b * transform[0][0])


class _Circle(_Ellipse):
    """ 円 """

    def __init__(self, center, r):
        super().__init__(center, r, r)


class Circle(_Circle):

    def __init__(self, center, r):
        super().__init__(center,
                         r * transform[0][0])

    def circle_points(self, n, stand=False):
        if stand:
            return [_Point([self.a * cos(2 * pi * i / n) + self.center[0],
                            self.a * sin(2 * pi * i / n) + self.center[1],
                            1.0]) * Matrix.affine2D(self.center, -pi + pi / 2 * 3 / n) for i in range(n)]
        else:
            return [_Point([self.a * cos(2 * pi * i / n) + self.center[0],
                            self.a * sin(2 * pi * i / n) + self.center[1],
                            1.0]) for i in range(n)]


class Fractal():
    """ フラクタル """

    def __init__(self, initiator, generator, n, each=False):
        self.initiator = initiator
        self.generator = generator
        self.n = n
        self.each = each

    def __iter__(self):
        if self.n == 0:
            yield self.initiator
            raise StopIteration
        elif self.each:
            yield self.initiator
        for mat in self.generator:
            yield Fractal(self.initiator.transformed(mat), self.generator, self.n - 1, self.each)

    def __repr__(self):
        return "Fractal(%s, %s, %d)" % (str(self.initiator), str(self.generator), self.n)
