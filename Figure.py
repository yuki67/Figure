""" 次元が関係ない図形 """
from MyMatrix import Matrix


class Figure(object):
    """
    任意の図形を表すクラス
    核となるのはget_iter()関数である
    """

    def __init__(self, dimension):
        self.mat = Matrix.identity(dimension)

    def __iter__(self):
        return (p.transform(self.mat) for p in self.get_iter())

    def __list__(self):
        """ selfを構成する部分図形が詰まったリストを返す """
        return list(self.get_iter())

    def copy(self):
        """ 自分のコピーを返す """
        assert False, "%s.copy() not defined" % self.__class__.__name__

    def get_iter(self):
        """ selfを構成する部分図形が詰まったイテレータを"新しく作って"返す """
        assert False, "%s.get_iter() not defined" % self.__class__.__name__

    def transform(self, mat):
        """
        図形をmatで変形するという情報を追加する
        ただし図形はまだ変形されない (figure.transform(mat) === figure)
        便利のためにselfが返されるが、受け取らなくても情報は追加される
        """
        self.mat = self.mat * mat
        return self

    def transformed(self, mat):
        """
        selfを行列matで変形したものを返す
        本当に図形を変化させる (figure.transformed(mat) != figure)
        Rendererで描画関数に渡される直前にのみ実行されるべき関数である。
        それ以外のときははtransformed()ではなくcopy().transform()を使うこと
        """
        assert False, "%s.transformed() not defined" % self.__class__.__name__


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
        Figure.__init__(self, len(lst))

    def __repr__(self):
        return "Point(%s)" % str(list(self))

    def __add__(self, other):
        return Point([a + b for a, b in zip(self[:-1], other[:-1])] + [1.0])

    def __sub__(self, other):
        return Point([a - b for a, b in zip(self[:-1], other[:-1])] + [1.0])

    def __mul__(self, mat):
        """ 行列との積 """
        return Point([sum([self[j] * mat[j][i] for j in range(len(mat[i]))]) for i in range(len(mat))]).regularize()

    def regularize(self):
        """ selfを最後の要素を1.0にした斉次座標として等しい点にしてそれを返す """
        for i in range(len(self)):
            self[i] /= self[-1]
        return self

    def copy(self):
        return Point(self).transform(self.mat)

    def transformed(self, mat):
        return Point(self * mat)

    def scaled(self, r):
        """ 座標をr倍した点を返す """
        return Point([r * x for x in self[:-1]] + [1.0])


class Line(Figure):
    """ 線分 """

    def __init__(self, a, b, n=None):
        super().__init__(len(a))
        self.a = a
        self.b = b
        self.n = n - 1 if n is not None else max([abs(i - j) for i, j in zip(self.a, self.b)])

    def __repr__(self):
        return "Line(%s, %s)" % (self.a.__repr__(), self.b.__repr__())

    def get_iter(self):
        if self.n == 0:
            # 何もしないイテレータ
            return iter(())
        else:
            return (self.a + (self.b - self.a).scaled(i / self.n) for i in range(int(self.n) + 1))

    def copy(self):
        return Line(self.a, self.b).transform(self.mat)

    def transformed(self, mat):
        return Line(self.a.transformed(mat), self.b.transformed(mat))

    def mid(self):
        """ 線分の中点を返す """
        return (self.a + self.b).scaled(0.5)


class Polygon(Figure):
    """ 多角形 """

    def __init__(self, points):
        super().__init__(len(points[0]))
        self.points = points

    def __repr__(self):
        return "Polygon(%s)" % str(self.points)

    def get_iter(self):
        return (Line(self.points[i - 1], self.points[i]) for i in range(len(self.points)))

    def copy(self):
        return Polygon(self.points).transform(self.mat)

    def transformed(self, mat):
        return Polygon([p.transformed(mat) for p in self.points])


class Fractal(Figure):
    """ フラクタル """

    def __init__(self, initiator, generator, n, each=False, init_generator=None):
        # init_generatorはget_iter()からの再帰呼び出しでのみ使われる
        super().__init__(len(generator[0]))
        self.initiator = initiator
        self.generator = generator
        self.n = n
        self.each = each
        self.init_generator = init_generator if init_generator else generator

    def copy(self):
        return Fractal(self.initiator, self.generator, self.n, self.each, self.init_generator).transform(self.mat)

    def get_iter(self):
        if self.each:
            return (Fractal(self.initiator, self.init_generator, n, False, self.init_generator) for n in range(self.n + 1))
        if self.n == 0:
            return iter((self.initiator.copy(),))
        if self.n == 1:
            return (self.initiator.copy().transform(gen) for gen in self.generator)
        else:
            return (Fractal(self.initiator, [gen * mat for gen in self.init_generator], self.n - 1, self.each, self.init_generator) for mat in self.generator)

    def __repr__(self):
        return "Fractal(%s, %s, %d)" % (str(self.initiator), str(self.generator), self.n)


class Repeats(Fractal):
    """ figureにmatを繰り返し適用した図形 """

    def __init__(self, figure, mat, n):
        assert n != 0
        super().__init__(figure, [mat], n - 1, True)
