from itertools import chain
from math import ceil, pi, sin, cos
from typing import List, Callable, Iterable


class Figure(object):
    """ 図形の基底クラス """

    def __iter__(self) -> Iterable:
        pass


class Point(Figure):
    """ 図形を扱うときの基本となる点 """

    def __init__(self, x: float, y: float, rgb: List[int]=None) -> None:
        """ 座標が(x,y)で色がrgbの点を返す """
        self.x = x
        self.y = y
        if rgb is not None:
            rgb[0] = int(rgb[0])
            rgb[1] = int(rgb[1])
            rgb[2] = int(rgb[2])
        self.rgb = rgb

    def __repr__(self):
        return "Point(%s, %s, %s)" % (self.x, self.y, self.rgb)

    def interpolate(self, b, r: float):
        """ selfとbをr:(1-r)に内分する点を返す(0<r<1) """
        # r = 0 で self
        # r = 1 で b
        x = (b.x - self.x) * r + self.x
        y = (b.y - self.y) * r + self.y
        rgb = [0, 0, 0]
        if self.rgb is not None:
            rgb[0] = (b.rgb[0] - self.rgb[0]) * r + self.rgb[0]
            rgb[1] = (b.rgb[1] - self.rgb[1]) * r + self.rgb[1]
            rgb[2] = (b.rgb[2] - self.rgb[2]) * r + self.rgb[2]
        return Point(x, y, rgb)


class Line(Figure):
    """ 線分 """

    def __init__(self, a: Point, b: Point) -> None:
        self.a = a
        self.b = b
        self.stopper = max(abs(self.a.x - self.b.x), abs(self.a.y - self.b.y))

    def __repr__(self):
        return "Line(%s, %s)" % (self.a.__repr__(), self.b.__repr__())

    def __iter__(self) -> Iterable[Point]:
        if self.stopper == 0:
            return (i for i in range(0))
        else:
            return (Point.interpolate(self.a, self.b, i / self.stopper) for i in range(int(self.stopper) + 1))


class Polygon(Figure):
    """ 多角形 """

    def __init__(self, points: List[Point]) -> None:
        self.points = points
        self.stopper = len(points)

    def __iter__(self) -> Iterable[Line]:
        return (Line(self.points[i - 1], self.points[i]) for i in range(self.stopper))


class Ellipse(Figure):
    """ 楕円 """

    def __init__(self, center: Point, a: float, b: float) -> None:
        # 全体の色はcenter.rgbで指定される
        self.center = center
        self.a = a
        self.b = b
        self.x_range = ceil((a ** 2 + b ** 2) ** -0.5 * a ** 2)
        self.y_range = ceil((a ** 2 + b ** 2) ** -0.5 * b ** 2)
        self.y = lambda x: b * (1 - (x / a) ** 2) ** 0.5
        self.x = lambda y: a * (1 - (y / b) ** 2) ** 0.5

    def __iter__(self) -> Iterable[Point]:
        return chain((Point(self.center.x + x,
                            self.center.y + self.y(x),
                            self.center.rgb)
                      for x in range(-self.x_range, self.x_range)),
                     (Point(self.center.x + x,
                            self.center.y - self.y(x),
                            self.center.rgb)
                      for x in range(-self.x_range, self.x_range)),
                     (Point(self.center.x + self.x(y),
                            self.center.y + y,
                            self.center.rgb)
                      for y in range(-self.y_range, self.y_range)),
                     (Point(self.center.x - self.x(y),
                            self.center.y + y,
                            self.center.rgb)
                      for y in range(-self.y_range, self.y_range)))


class Circle(Ellipse):
    """ 円 """

    def __init__(self, center: Point, r: float) -> None:
        super().__init__(center, r, r)


class Diamond(Figure):
    """ ダイヤモンドパターン """

    def __init__(self,
                 center: Point,
                 r: float,
                 n: int,
                 color: Callable[[float], List[int]]=lambda t: [0, 0, 0]
                 ) -> None:
        self.circle = lambda: circular_points(center, r, n, color)

    def __iter__(self) -> Iterable(Line):
        return (Line(p, q) for p in self.circle() for q in self.circle())


class ColorArray(Figure, list):
    """ 色配列 """

    def __init__(self, width: int, height: int) -> None:
        """ [255, 255, 255](白)に初期化された横width, 縦heightの色配列を返す """
        array = []
        for y in range(height):
            array.append(ColorArray(0, 0))
            for x in range(width):
                array[-1].append(Point(x, y, [255, 255, 255]))
        super().__init__(array)

    def __iter__(self) -> Iterable[Iterable[Point]]:
        return list.__iter__(self)

    def resize(self, width: int):
        """ 幅をwidthに縮小して返す """
        return self.from_source(width,
                                len(self[0]), len(self),
                                lambda x, y: self[int(y)][int(x)].rgb)

    @staticmethod
    def from_image(filename: str, width: int):
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
                    source_width: int,
                    source_height: int,
                    sampler: Callable[[int, int], List[int]]):
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
                array[-1].append(Point(m, n, list(sampler(x, y))))
                x += diff_x
                m += 1
            y += diff_y
            n += 1
        return array


def circular_points(center: Point,
                    r: float,
                    n: int,
                    color: Callable[[float], List[int]]=lambda t: [0, 0, 0]
                    ) -> Iterable[Point]:
    """ 円周上の点へのイテレータを返す """
    return (Point(r * cos(2 * pi * i / n) + center.x,
                  r * sin(2 * pi * i / n) + center.y,
                  color(i / n)) for i in range(n))
