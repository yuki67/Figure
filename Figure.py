from itertools import chain
from math import ceil, pi, sin, cos
from MyMatrix import Matrix

transform = Matrix.identity(3)


class Figure(object):
    """
    任意の図形を表すクラス
    核となるのはget_iter()関数である
    """

    def __init__(self, made_from=()):
        """ made_from: 変形される前の図形がなんであったかを記憶する """
        self.made_from = made_from

    def get_iter(self):
        """ selfを構成する部分図形が詰まったイテレータを"新しく作って"返す """
        pass

    def __iter__(self):
        return self.get_iter()

    def __list__(self):
        """ selfを構成する部分図形が詰まったリストを返す """
        return list(self.get_iter())

    def transformed(self, mat):
        """ selfを行列matで変形してものを返す """
        class Temp(Figure):

            def get_iter(_self):
                return (x.transformed(mat) for x in self)
        return Temp((self.__class__,))


def figure_union(figures):
    """
    figuresに含まれる図形をひとまとめにした図形を返す

    >>> a = Line(Point([0,0, 0.0]), Point([10, 10]))
    >>> b = Line(Point([10,0, 0.0]), Point([0, 10]))
    >>> c = Circle(Point([0.5, 0.5]), 4)
    >>> for f in figure_union((a, b, c)):
    ...     print(f)
    Line(Point([0, 0]), Point([10, 10]))
    Line(Point([10, 0]), Point([0, 10]))
    Circle(Point([0.5, 0.5]), 4)
    """
    class Temp(Figure):

        def get_iter(self):
            return (f for f in figures)
    return Temp()


class Point(list, Figure):
    """
    二次元平面上の点
    行列との乗算をサポートするが、保持する値は2つだけ

    >>> a = Point([1.0, 2.0])
    >>> a[0]
    1.0
    >>> a[1]
    2.0
    >>> a[2]
    Traceback (most recent call last):
    ...
    IndexError: list index out of range
    """

    def __init__(self, lst):
        super().__init__(lst[:2])
        Figure.__init__(self, (Point,))

    def __repr__(self):
        return "Point(%s)" % str(list(self))

    def __add__(self, other):
        """
        >>> Point([1.0, 2.0]) + Point([3.0, 5.0])
        Point([4.0, 7.0])
        """
        return Point([a + b for a, b in zip(self, other)])

    def __sub__(self, other):
        """
        >>> Point([1.0, 2.0]) - Point([3.0, 5.0])
        Point([-2.0, -3.0])
        """
        return Point([a - b for a, b in zip(self, other)])

    def __mul__(self, other):
        """
        行列との積
        >>> Point([1.0, 2.0]) * Matrix.affine2D(swap=[True, True], trans=[2.0, 3.0])
        Point([-3.0, -5.0])
        """
        temp = list.__add__(self, [1.0])
        return Point([sum([temp[j] * other[j][i] for j in range(len(other[i]))]) for i in range(len(other))])

    def scaled(self, r):
        """
        座標をr倍した点を返す
        >>> Point([3.0, 4.0]).scaled(0.5)
        Point([1.5, 2.0])
        """
        return Point([r * x for x in self])

    def transformed(self, mat):
        return Point(self * mat)


class Line(Figure):
    """ 線分 """

    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.max = max(abs(self.a[0] - self.b[0]), abs(self.a[1] - self.b[1]))
        super().__init__((Line,))

    def get_iter(self):
        """
        >>> list(Line(Point([0.0, 0.0]), Point([0.0, 0.0])))
        []
        >>> list(Line(Point([0.0, 4.0]), Point([2.0, 0.0])))
        [Point([0.0, 4.0]), Point([0.5, 3.0]), Point([1.0, 2.0]), Point([1.5, 1.0]), Point([2.0, 0.0])]
        """
        if self.max == 0:
            # 何もしないイテレータ
            return (i for i in range(0))
        else:
            return (self.a + (self.b - self.a).scaled(i / self.max) for i in range(int(self.max) + 1))

    def __repr__(self):
        return "Line(%s, %s)" % (self.a.__repr__(), self.b.__repr__())

    def mid(self):
        """
        線分の中点を返す

        >>> Line(Point([0.0, 3.0]), Point([6.0, 0.0])).mid()
        Point([3.0, 1.5])
        """
        return Point([a / 2 for a in self.a + self.b])

    def transformed(self, mat):
        """
        線分を変換するには、端点を変換する

        >>> mat = Matrix.affine2D(center=[4.0, 2.0], scale=[0.25, 0.25])
        >>> Line(Point([0.0, 4.0]), Point([8.0, 0.0])).transformed(mat)
        Line(Point([3.0, 2.5]), Point([5.0, 1.5]))
        """
        return Line(self.a.transformed(mat), self.b.transformed(mat))


class Polygon(Figure):
    """ 多角形 """

    def __init__(self, points):
        self.points = points
        super().__init__((Polygon,))

    def get_iter(self):
        """
        >>> points = [Point([i, i**2]) for i in range(3)]
        >>> points
        [Point([0, 0]), Point([1, 1]), Point([2, 4])]
        >>> list(Polygon(points))
        [Line(Point([2, 4]), Point([0, 0])), Line(Point([0, 0]), Point([1, 1])), Line(Point([1, 1]), Point([2, 4]))]
        """
        return (Line(self.points[i - 1], self.points[i]) for i in range(len(self.points)))

    def get_points(self):
        """
        Polygonの制御点を返す

        >>> a = Polygon([Point([0, 0]), Point([0, 10]), Point([10, 0])])
        >>> a.get_points()
        [Point([0, 0]), Point([0, 10]), Point([10, 0])]
        """
        return self.points

    def transformed(self, mat):
        """
        >>> points = [Point([0, 0]), Point([0, 10]), Point([10, 0])]
        >>> poly = Polygon(points)
        >>> poly.transformed(Matrix.affine2D(rot=pi/2, scale=[0.25, 0.25], trans=[15.0, -15.0]))
        Polygon([Point([15.0, -15.0]), Point([12.5, -15.0]), Point([15.0, -12.5])])
        """
        return Polygon([p.transformed(mat) for p in self.points])

    def __repr__(self):
        return "Polygon(%s)" % str(self.points)


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
            points = [Point([self.center[0] + self.a * cos(theta * 2 / n * pi),
                             self.center[1] + self.b * sin(theta * 2 / n * pi)]) for theta in range(self.n)]
            super().__init__(points)

    def __repr__(self):
        return "Ellipse(%s, %s, %s)" % (self.center, self.a, self.b)

    def transformed(self, mat):
        """
        >>> ellipse = Ellipse(Point([0.0, 0.0]), 3.0, 4.0, 4).transformed(Matrix.affine2D(trans=[2.0, 2.0]))
        >>> type(ellipse)
        <class '__main__.Ellipse'>
        >>> ellipse.get_points()
        [Point([5.0, 2.0]), Point([2.0, 6.0]), Point([-1.0, 2.0000000000000004]), Point([1.9999999999999996, -2.0])]
        """
        return Ellipse([p.transformed(mat) for p in self.points], n=self.n)


class Circle(Ellipse):
    """ 円 """

    def __init__(self, center, r):
        super().__init__(center, r, r)

    def __repr__(self):
        return "Circle(%s, %s)" % (str(self.center), str(self.a))

    def transformed(self, mat):
        return Circle(self.center * mat, self.a * mat[0][0])

    def circle_points(self, n, stand=False):
        """
        演習をn分割するの点を返す
        stand=Trueの場合、n角形が立つように回転させてから返す

        >>> for p in Circle(Point([0.0, 0.0]), 10.0).circle_points(4): print(p)
        Point([10.0, 0.0])
        Point([6.123233995736766e-16, 10.0])
        Point([-10.0, 1.2246467991473533e-15])
        Point([-1.8369701987210296e-15, -10.0])
        >>> for p in Circle(Point([0.0, 0.0]), 10.0).circle_points(4, True): print(p)
        Point([-3.826834323650897, -9.238795325112868])
        Point([9.238795325112868, -3.8268343236508975])
        Point([3.8268343236508984, 9.238795325112868])
        Point([-9.238795325112868, 3.826834323650899])
        """
        if stand:
            return [Point([self.a * cos(2 * pi * i / n) + self.center[0],
                           self.a * sin(2 * pi * i / n) + self.center[1],
                           1.0]) * Matrix.affine2D(self.center, rot=-pi + pi / 2 * 3 / n) for i in range(n)]
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
        super().__init__((Fractal,))

    def get_iter(self):
        """
        >>> mats = [Matrix.affine2D(trans=[0.0, i]) for i in range(2)]
        >>> list(Fractal(Line(Point([0.0, 0.0]), Point([10.0, 10.0])), mats, 1, False))
        [Line(Point([0.0, 0.0]), Point([10.0, 10.0])), Line(Point([0.0, 1.0]), Point([10.0, 11.0]))]
        """
        if self.n == 0:
            return (self.initiator for i in range(0))
        if self.n == 1:
            return (self.initiator.transformed(gen) for gen in self.generator)
        if self.each:
            return chain((self.initiator.transformed(gen) for gen in self.generator),
                         (Fractal(self.initiator, [gen * mat for gen in self.init_generator], self.n - 1, self.each, self.init_generator) for mat in self.generator))
        return (Fractal(self.initiator, [gen * mat for gen in self.init_generator], self.n - 1, self.each, self.init_generator) for mat in self.generator)

    def __repr__(self):
        return "Fractal(%s, %s, %d)" % (str(self.initiator), str(self.generator), self.n)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
