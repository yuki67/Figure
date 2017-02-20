from itertools import chain
from math import ceil, pi, sin, cos
from MyMatrix import Matrix, Vector

transform = Matrix.identity(3)


class _Point(Vector):
    """
    transformを気にしない普通の点
    他のFigureが点を使うときはこちらを使う
    """

    def __init__(self, pos):
        """ 座標が(x,y)の点を返す """
        if len(pos) == 2:
            pos += [1.0]
        super().__init__(pos)

    def __repr__(self):
        return "_Point(%s, %s)" % str(list(self))

    def interpolate(self, b, r):
        """ selfとbをr:(1-r)に内分する点を返す(0<r<1) """
        # r = 0 で self
        # r = 1 で b
        return _Point((b - self).scale(r) + self)

    def transformed(self, mat):
        return _Point(self * mat)


class Point(_Point):
    """
    Figure.scaleを気にする点
    ユーザーがプログラムで使うのはこっち
    ユーザーがFigure.scaleを適宜変更することで、扱いやすい座標系([0.0, 1.0]^2など)で図形を描くことが可能になる
    """

    def __init__(self, x, y):
        """ 座標が(scale * x, scale * y)の点を返す """
        super().__init__(Vector([x, y, 1.0]) * transform)


class Line():
    """ 線分 """

    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.stopper = max(abs(self.a[0] - self.b[0]), abs(self.a[1] - self.b[1]))

    def __repr__(self):
        return "Line(%s, %s)" % (self.a.__repr__(), self.b.__repr__())

    def __iter__(self):
        if self.stopper == 0:
            return (i for i in range(0))
        else:
            return (_Point.interpolate(self.a, self.b, i / self.stopper) for i in range(int(self.stopper) + 1))

    def mid(self):
        return [a / 2 for a in self.a + self.b]

    def transformed(self, mat):
        return Line(self.a.transformed(mat), self.b.transformed(mat))


class Polygon():
    """ 多角形 """

    def __init__(self, points):
        self.points = points
        self.stopper = len(points)

    def __iter__(self):
        return (Line(self.points[i - 1], self.points[i]) for i in range(self.stopper))

    def transformed(self, mat):
        return Polygon([p.transformed(mat) for p in self.points])

    def __repr__(self):
        return "Polygon(%s)" % str(self.points)


class _Ellipse():
    """ 楕円 """

    def __init__(self, center, a, b):
        self.center = center
        self.a = a
        self.b = b
        self.x_range = ceil((a ** 2 + b ** 2) ** -0.5 * a ** 2)
        self.y_range = ceil((a ** 2 + b ** 2) ** -0.5 * b ** 2)
        self.x = lambda x: b * (1 - (x / a) ** 2) ** 0.5
        self.y = lambda y: a * (1 - (y / b) ** 2) ** 0.5

    def __iter__(self):
        return chain((_Point([self.center[0] + x,
                              self.center[1] + self.y(x)])
                      for x in range(-self.x_range, self.x_range)),
                     (_Point([self.center[0] + x,
                              self.center[1] - self.y(x)])
                      for x in range(-self.x_range, self.x_range)),
                     (_Point([self.center[0] + self.x(y),
                              self.center[1] + y])
                      for y in range(-self.y_range, self.y_range)),
                     (_Point([self.center[0] - self.x(y),
                              self.center[1] + y])
                      for y in range(-self.y_range, self.y_range)))

    def transformed(self, mat):
        return _Ellipse(self.center.transformed(mat), self.a, self.b)


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

    def points(self, n):
        return [_Point([self.a * cos(2 * pi * i / n) + self.center[0],
                        self.a * sin(2 * pi * i / n) + self.center[1]]) for i in range(n)]


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
