from itertools import chain
from math import pi, sin, cos
from MyMatrix import Matrix


class Figure(object):
    """
    任意の図形を表すクラス
    核となるのはget_iter()関数である
    """

    def __iter__(self):
        return self.get_iter()

    def __list__(self):
        """ selfを構成する部分図形が詰まったリストを返す """
        return list(self.get_iter())

    def get_iter(self):
        """ selfを構成する部分図形が詰まったイテレータを"新しく作って"返す """
        pass

    def transformed(self, mat):
        """ selfを行列matで変形してものを返す """
        pass

    def projected(self):
        """ ひとつ下の次元に平行投影された図形を返す """
        pass


def figure_union(figures):
    """ figuresに含まれる図形をひとまとめにした図形を返す """

    class Temp(Figure):

        def get_iter(self):
            return (f for f in figures)
    return Temp()


class Point(list, Figure):
    """ n次元平面上の点 """
    # 最も基本的な図形なので、get_iter()は存在しない(点は分解のしようがない)

    def __init__(self, lst):
        super().__init__(lst)
        Figure.__init__(self)

    def __repr__(self):
        return "Point(%s)" % str(list(self))

    def __add__(self, other):
        return Point([a + b for a, b in zip(self, other)])

    def __sub__(self, other):
        return Point([a - b for a, b in zip(self, other)])

    def __mul__(self, mat):
        """ 行列との積 """
        temp = list.__add__(self, [1.0])
        return Point([mat[i][-1] + sum([temp[j] * mat[j][i] for j in range(len(mat[i]))]) for i in range(len(mat) - 1)])

    def transformed(self, mat):
        return Point(self * mat)

    def projected(self):
        return Point(self[:-1])

    def scaled(self, r):
        """
        座標をr倍した点を返す
        >>> Point([3.0, 4.0]).scaled(0.5)
        Point([1.5, 2.0])
        """
        return Point([r * x for x in self])


class Line(Figure):
    """ 線分 """

    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.max = max([abs(i - j) for i, j in zip(self.a, self.b)])
        super().__init__()

    def __repr__(self):
        return "Line(%s, %s)" % (self.a.__repr__(), self.b.__repr__())

    def get_iter(self):
        if self.max == 0:
            # 何もしないイテレータ
            return iter(())
        else:
            return (self.a + (self.b - self.a).scaled(i / self.max) for i in range(int(self.max) + 1))

    def transformed(self, mat):
        return Line(self.a.transformed(mat), self.b.transformed(mat))

    def projected(self):
        return Line(self.a.projected(), self.b.projected())

    def mid(self):
        """ 線分の中点を返す

        >>> Line(Point([0.0, 3.0]), Point([6.0, 0.0])).mid()
        Point([3.0, 1.5])
        """
        return Point([a / 2 for a in self.a + self.b])


class Polygon(Figure):
    """ 多角形 """

    def __init__(self, points):
        self.points = points
        super().__init__()

    def __repr__(self):
        return "Polygon(%s)" % str(self.points)

    def get_iter(self):
        return (Line(self.points[i - 1], self.points[i]) for i in range(len(self.points)))

    def transformed(self, mat):
        return Polygon([p.transformed(mat) for p in self.points])

    def projected(self):
        return Polygon([p.transformed() for p in self.points])

    def get_points(self):
        """ Polygonの制御点を返す """
        return self.points


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
        """
        if stand:
            return [Point([self.a * cos(2 * pi * i / n) + self.center[0],
                           self.a * sin(2 * pi * i / n) + self.center[1]
                           ]) * Matrix.affine2D(self.center, rot=-pi + pi / 2 * 3 / n) for i in range(n)]
        else:
            return [Point([self.a * cos(2 * pi * i / n) + self.center[0],
                           self.a * sin(2 * pi * i / n) + self.center[1]
                           ]) for i in range(n)]


class Fractal(Figure):
    """ フラクタル """

    def __init__(self, initiator, generator, n, each=False, init_generator=False):
        # init_generatorはget_iter()からの再帰呼び出しでのみ使われる
        self.initiator = initiator
        self.generator = generator
        self.n = n
        self.each = each
        self.init_generator = init_generator if init_generator else generator
        super().__init__()

    def get_iter(self):
        if self.each:
            return (Fractal(self.initiator, self.init_generator, n, False, self.init_generator) for n in range(self.n + 1))
        if self.n == 0:
            return iter((self.initiator,))
        if self.n == 1:
            return (self.initiator.transformed(gen) for gen in self.generator)
        else:
            return (Fractal(self.initiator, [gen * mat for gen in self.init_generator], self.n - 1, self.each, self.init_generator) for mat in self.generator)

    def transformed(self, mat):
        return Fractal(self.initiator.transformed(mat), self.generator, self.n, self.each)

    def projected(self):
        return Fractal(self.initiator.projected(), self.generator, self.n, self.each)

    def __repr__(self):
        return "Fractal(%s, %s, %d)" % (str(self.initiator), str(self.generator), self.n)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    doctest.testfile("FigureTest.txt")
