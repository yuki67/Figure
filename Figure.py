from itertools import chain
from math import ceil, pi, sin, cos
from MyMatrix import Matrix, Vector

transform = Matrix.identity(3)


class _Point(object):
    """
    scaleを気にしない普通の点
    他のFigureが点を使うときはこちらを使う
    """

    def __init__(self, pos, rgb=(0, 0, 0)):
        """ 座標が(x,y)で色がrgbの点を返す """
        if len(pos) == 2:
            pos += [1.0]
        self.pos = Vector(pos)
        self.rgb = Vector([int(x) for x in rgb])

    def __repr__(self):
        return "_Point(%s, %s)" % (self.pos, self.rgb)

    def interpolate(self, b, r):
        """ selfとbをr:(1-r)に内分する点を返す(0<r<1) """
        # r = 0 で self
        # r = 1 で b
        return _Point((b.pos - self.pos).scale(r) + self.pos,
                      (b.rgb - self.rgb).scale(r) + self.rgb)

    def transformed(self, mat):
        return _Point(self.pos * mat, self.rgb)


class Point(_Point):
    """
    Figure.scaleを気にする点
    ユーザーがプログラムで使うのはこっち
    ユーザーがFigure.scaleを適宜変更することで、扱いやすい座標系([0.0, 1.0]^2など)で図形を描くことが可能になる
    """

    def __init__(self, x, y, rgb=(0, 0, 0)):
        """ 座標が(scale * x, scale * y)で色がrgbの点を返す """
        super().__init__(Vector([x, y, 1.0]) * transform, rgb)


class Line():
    """ 線分 """

    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.stopper = max(abs(self.a.pos[0] - self.b.pos[0]), abs(self.a.pos[1] - self.b.pos[1]))

    def __repr__(self):
        return "Line(%s, %s)" % (self.a.__repr__(), self.b.__repr__())

    def __iter__(self):
        if self.stopper == 0:
            return (i for i in range(0))
        else:
            return (_Point.interpolate(self.a, self.b, i / self.stopper) for i in range(int(self.stopper) + 1))

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
        # 全体の色はcenter.rgbで指定される
        self.center = center
        self.a = a
        self.b = b
        self.x_range = ceil((a ** 2 + b ** 2) ** -0.5 * a ** 2)
        self.y_range = ceil((a ** 2 + b ** 2) ** -0.5 * b ** 2)
        self.x = lambda x: b * (1 - (x / a) ** 2) ** 0.5
        self.y = lambda y: a * (1 - (y / b) ** 2) ** 0.5

    def __iter__(self):
        return chain((_Point([self.center.pos[0] + x,
                              self.center.pos[1] + self.y(x)],
                             self.center.rgb)
                      for x in range(-self.x_range, self.x_range)),
                     (_Point([self.center.pos[0] + x,
                              self.center.pos[1] - self.y(x)],
                             self.center.rgb)
                      for x in range(-self.x_range, self.x_range)),
                     (_Point([self.center.pos[0] + self.x(y),
                              self.center.pos[1] + y],
                             self.center.rgb)
                      for y in range(-self.y_range, self.y_range)),
                     (_Point([self.center.pos[0] - self.x(y),
                              self.center.pos[1] + y],
                             self.center.rgb)
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
        return [_Point([self.a * cos(2 * pi * i / n) + self.center.pos[0],
                        self.a * sin(2 * pi * i / n) + self.center.pos[1]],
                       self.center.rgb) for i in range(n)]


class ColorArray(list):
    """ 色配列 """

    def __init__(self, width, height):
        """ [255, 255, 255](白)に初期化された横width, 縦heightの色配列を返す """
        array = []
        for y in range(height):
            array.append(ColorArray(0, 0))
            for x in range(width):
                array[-1].append(_Point([x, y], [255, 255, 255]))
        super().__init__(array)

    def __iter__(self):
        return list.__iter__(self)

    def resize(self, width: int):
        """ 幅をwidthに縮小して返す """
        return self.from_source(width,
                                len(self[0]), len(self),
                                lambda x, y: self[int(y)][int(x)].rgb)

    @staticmethod
    def from_image(filename, width):
        """
        画像から色配列を作って返す
        widthは出来上がる色配列の幅
        """
        from PIL import Image

        image = Image.open(filename)
        w, h = image.size
        return ColorArray.from_source(width, w, h,
                                      lambda x, y: image.getpixel((int(x), int(y))))

    @staticmethod
    def from_source(width: int,
                    source_width,
                    source_height,
                    sampler):
        """ samplerを使って幅widthの色配列を作って返す """
        height = width / source_width * source_height
        diff_x = (source_width - 1) / (width - 1)
        diff_y = (source_height - 1) / (height - 1)

        y = n = 0
        array = ColorArray(0, 0)
        while y <= source_height:
            x = m = 0
            array.append(ColorArray(0, 0))
            while x <= source_width:
                array[-1].append(_Point([m, n], list(sampler(x, y))))
                x += diff_x
                m += 1
            y += diff_y
            n += 1
        return array


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
