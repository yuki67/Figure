from itertools import chain
from math import ceil, pi, sin, cos

scale = 1.0


class Figure(object):
    """ 図形の基底クラス """

    def __iter__(self):
        pass

    def scaled(self):
        pass


class _Point(Figure):
    """
    scaleを気にしない普通の点
    他のFigureが点を使うときはこちらを使う
    """

    def __init__(self, x, y, rgb=(0, 0, 0)):
        """ 座標が(x,y)で色がrgbの点を返す """
        self.x = x
        self.y = y
        self.rgb = [int(x) for x in rgb]

    def __repr__(self):
        return "_Point(%s, %s, %s)" % (self.x, self.y, self.rgb)

    def interpolate(self, b, r):
        """ selfとbをr:(1-r)に内分する点を返す(0<r<1) """
        # r = 0 で self
        # r = 1 で b
        return _Point((b.x - self.x) * r + self.x,
                      (b.y - self.y) * r + self.y,
                      [(x - y) * r + y for x, y in zip(b.rgb, self.rgb)])

    def scaled(self, factor):
        return _Point(self.x * factor, self.y * factor, self.rgb)


class Point(_Point):
    """
    Figure.scaleを気にする点
    ユーザーがプログラムで使うのはこっち
    ユーザーがFigure.scaleを適宜変更することで、扱いやすい座標系([0.0, 1.0]^2など)で図形を描くことが可能になる
    """

    def __init__(self, x, y, rgb=(0, 0, 0)):
        """ 座標が(scale * x, scale * y)で色がrgbの点を返す """
        super().__init__(scale * x, scale * y, rgb)


class Line(Figure):
    """ 線分 """

    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.stopper = max(abs(self.a.x - self.b.x), abs(self.a.y - self.b.y))

    def __repr__(self):
        return "Line(%s, %s)" % (self.a.__repr__(), self.b.__repr__())

    def __iter__(self):
        if self.stopper == 0:
            return (i for i in range(0))
        else:
            return (_Point.interpolate(self.a, self.b, i / self.stopper) for i in range(int(self.stopper) + 1))

    def scaled(self, factor):
        return Line(self.a.scaled(factor), self.b.scaled(factor))


class Polygon(Figure):
    """ 多角形 """

    def __init__(self, points):
        self.points = points
        self.stopper = len(points)

    def __iter__(self):
        return (Line(self.points[i - 1], self.points[i]) for i in range(self.stopper))

    def scaled(self, factor):
        return Polygon([p.scaled(factor) for p in self.points])

    def __repr__(self):
        return "Polygon(%s)" % str(self.points)


class Ellipse(Figure):
    """ 楕円 """

    def __init__(self, center, a, b):
        # 全体の色はcenter.rgbで指定される
        self.center = center
        self.a = a
        self.b = b
        self.x_range = ceil((a ** 2 + b ** 2) ** -0.5 * a ** 2)
        self.y_range = ceil((a ** 2 + b ** 2) ** -0.5 * b ** 2)
        self.y = lambda x: b * (1 - (x / a) ** 2) ** 0.5
        self.x = lambda y: a * (1 - (y / b) ** 2) ** 0.5

    def __iter__(self):
        return chain((_Point(self.center.x + x,
                             self.center.y + self.y(x),
                             self.center.rgb)
                      for x in range(-self.x_range, self.x_range)),
                     (_Point(self.center.x + x,
                             self.center.y - self.y(x),
                             self.center.rgb)
                      for x in range(-self.x_range, self.x_range)),
                     (_Point(self.center.x + self.x(y),
                             self.center.y + y,
                             self.center.rgb)
                      for y in range(-self.y_range, self.y_range)),
                     (_Point(self.center.x - self.x(y),
                             self.center.y + y,
                             self.center.rgb)
                      for y in range(-self.y_range, self.y_range)))


class Circle(Ellipse):
    """ 円 """

    def __init__(self, center, r):
        super().__init__(center, r, r)


class Diamond(Figure):
    """ ダイヤモンドパターン """

    def __init__(self, center, r, n, color=lambda t: [0, 0, 0]):
        self.circle = lambda: circular_points(center, r, n, color)

    def __iter__(self):
        return (Line(p, q) for p in self.circle() for q in self.circle())


class ColorArray(Figure, list):
    """ 色配列 """

    def __init__(self, width, height):
        """ [255, 255, 255](白)に初期化された横width, 縦heightの色配列を返す """
        array = []
        for y in range(height):
            array.append(ColorArray(0, 0))
            for x in range(width):
                array[-1].append(_Point(x, y, [255, 255, 255]))
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
                array[-1].append(_Point(m, n, list(sampler(x, y))))
                x += diff_x
                m += 1
            y += diff_y
            n += 1
        return array


class Fractal(Figure):
    """ フラクタル """

    def __init__(self, initiator, generator, n):
        self.initiator = initiator
        self.generator = generator
        self.n = n

    def __iter__(self):
        if self.n == 0:
            return (self.initiator for i in range(1))
        else:
            return (Fractal(self.initiator.scaled(factor), self.generator, self.n - 1) for factor in self.generator)

    def __repr__(self):
        return "Fractal(%s, %s, %d)" % (str(self.initiator), str(self.generator), self.n)


def circular_points(center, r, n, color=lambda t: [0, 0, 0]):
    """ 円周上の点へのイテレータを返す """
    return (_Point(r * cos(2 * pi * i / n) + center.x,
                   r * sin(2 * pi * i / n) + center.y,
                   color(i / n)) for i in range(n))
