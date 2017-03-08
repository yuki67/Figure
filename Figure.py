""" 次元が関係ない図形 """


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


class UnionFigure(Figure):
    """ 複数の図形をひとまとめにした図形 """

    def __init__(self, figures):
        self.figures = figures
        super().__init__()

    def get_iter(self):
        return (f for f in self.figures)

    def transformed(self, mat):
        return UnionFigure((f.transformed(mat) for f in self.figures))


class Point(list, Figure):
    """ n次元平面上の点 """
    # 最も基本的な図形なので、get_iter()は存在しない(点は分解のしようがない)

    def __init__(self, lst):
        super().__init__(lst)
        Figure.__init__(self)

    def __repr__(self):
        return "Point(%s)" % str(list(self))

    def __add__(self, other):
        return Point([a + b for a, b in zip(self[:-1], other[:-1])] + [1.0])

    def __sub__(self, other):
        return Point([a - b for a, b in zip(self[:-1], other[:-1])] + [1.0])

    def __mul__(self, mat):
        """ 行列との積 """
        return Point([sum([self[j] * mat[j][i] for j in range(len(mat[i]))]) for i in range(len(mat))]).regularized()

    def regularized(self):
        """
        最後の要素を1.0にした、斉次座標として等しい点を返す
        """
        return Point([x / self[-1] for x in self])

    def transformed(self, mat):
        return Point(self * mat)

    def scaled(self, r):
        """
        座標をr倍した点を返す
        >>> Point([3.0, 4.0]).scaled(0.5)
        Point([1.5, 2.0])
        """
        return Point([r * x for x in self[:-1]] + [1.0])


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

    def mid(self):
        """ 線分の中点を返す

        >>> Line(Point([0.0, 3.0]), Point([6.0, 0.0])).mid()
        Point([3.0, 1.5])
        """
        return (self.a + self.b).scaled(0.5)


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
        return self.__class__([p.transformed(mat) for p in self.points])

    def get_points(self):
        """ Polygonの制御点を返す """
        return self.points


class Fractal(Figure):
    """ フラクタル """

    def __init__(self, initiator, generator, n, each=False, init_generator=None, last_transform=None):
        # init_generatorはget_iter()からの再帰呼び出しでのみ使われる
        # last_transformはFractal.transformed()でのみ指定される
        self.initiator = initiator
        self.generator = generator
        self.n = n
        self.each = each
        self.init_generator = init_generator if init_generator else generator
        self.last_transform = last_transform
        super().__init__()

    def get_iter(self):
        if self.each:
            return (Fractal(self.initiator, self.init_generator, n, False, self.init_generator, self.last_transform) for n in range(self.n + 1))
        if self.n == 0:
            if self.last_transform:
                return iter((self.initiator.transformed(self.last_transform),))
            else:
                return iter((self.initiator,))
        if self.n == 1:
            if self.last_transform:
                return (self.initiator.transformed(gen * self.last_transform) for gen in self.generator)
            else:
                return (self.initiator.transformed(gen) for gen in self.generator)
        else:
            return (Fractal(self.initiator, [gen * mat for gen in self.init_generator], self.n - 1, self.each, self.init_generator, self.last_transform) for mat in self.generator)

    def transformed(self, mat):
        return Fractal(self.initiator, self.generator, self.n, self.each, self.generator, mat)

    def __repr__(self):
        return "Fractal(%s, %s, %d)" % (str(self.initiator), str(self.generator), self.n)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    doctest.testfile("FigureTest.txt")
