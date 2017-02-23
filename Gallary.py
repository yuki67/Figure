""" 図形描画のテスト """
import os
from math import pi
from PIL import Image
import Figure
from Figure import Line, Point, _Point, Fractal, Polygon, Circle, Ellipse
from JPGPainter import JPGPainter
from MyMatrix import Matrix


class Circloid(object):
    """ サークロイド(造語) """

    def __init__(self, circle, n, f):
        self.circle = circle
        self.n = n
        self.f = f

    def __iter__(self):
        points = self.circle.circle_points(self.n)
        for i in range(self.n):
            for j in range(self.n):
                if self.f(i, j):
                    yield Line(points[i], points[j])


class Diamond(Circloid):
    """ ダイヤモンドパターン """

    def __init__(self, circle, n=16):
        super().__init__(circle, n, lambda i, j: True)


class Cardioid(Circloid):
    """ カージオイド """

    def __init__(self, circle, n=256):
        super().__init__(circle, n, lambda i, j: (2 * i) % n == j)


class Thirdioid(Circloid):
    """ サージオイド(造語) """

    def __init__(self, circle, n=256):
        super().__init__(circle, n, lambda i, j: (3 * i) % n == j)


class Waves(Circloid):
    """ 波っぽいのが見える """

    def __init__(self, circle, n=256):
        super().__init__(circle, n, lambda i, j: i % (j + 1) == 0)


class PineCone(Circloid):
    """ 松ぼっくりに見えなくもない """

    def __init__(self, circle, n=32):
        def f(i, j):
            k = self.n**0.5
            if -k < (j + i) % self.n < k or (j + i) % self.n > -k % self.n:
                return True
            return False
        super().__init__(circle, n, f)


class JumpRope(Circloid):
    """ 縄跳びをスローシャッターで撮ったときの模様に似てる """

    def __init__(self, circle, n=256):
        def f(i, j):
            k = self.n**0.25
            if -k < (j + i) % self.n < k or (j + i) % self.n > -k % self.n:
                return True
            return False
        super().__init__(circle, n, f)


class Flower(Circloid):
    """ 花を真上から見たのに似てる """

    def __init__(self, circle, n=128, k=8):
        def f(i, j):
            return i < j and (i + j) % (self.n // k) == 0
        super().__init__(circle, n, f)


class KochCurve(Fractal):
    """ コッホ曲線 """

    def __init__(self, line, n, each=False):
        args = [
            [line.a, 0.0, [1 / 3, 1 / 3], Point([0.0, 0.0])],
            [line.a, -pi / 3, [1 / 3, 1 / 3], Point.interpolate(Point([0.0, 0.0]), line.b - line.a, 1 / 3)],
            [line.b, pi / 3, [1 / 3, 1 / 3], Point.interpolate(Point([0.0, 0.0]), line.a - line.b, 1 / 3)],
            [line.b, 0.0, [1 / 3, 1 / 3], Point([0.0, 0.0])],
        ]
        generator = [Matrix.affine2D(c, r, s, t) for c, r, s, t in args]
        super().__init__(line, generator, n, each)


class DragonCurve(Fractal):
    """ ドラゴン曲線 """

    def __init__(self, line, n, each=True):
        r = 2 ** -0.5
        args = [
            [line.a, -pi / 4, [r, r], Point([0.0, 0.0])],
            [line.a, -pi / 4 * 3, [r, r], line.b - line.a],
        ]
        generator = [Matrix.affine2D(c, r, s, t) for c, r, s, t in args]
        super().__init__(line, generator, n, each)


class SierpiskiGasket(Fractal):
    """ シェルピンスキーのギャスケット """

    def __init__(self, points, n, each):
        center = sum(points, Point([0.0, 0.0])).scale(1 / len(points))
        args = [
            [center, 0.0, [0.5, 0.5], Point.interpolate(Point([0.0, 0.0]), p - center, 0.5)] for p in points
        ]
        generator = [Matrix.affine2D(c, r, s, t) for c, r, s, t in args]
        super().__init__(Polygon(points), generator, n, each)


class Donuts(Fractal):
    """ ドーナツ """

    def __init__(self, ellipse, n=50):
        mat = Matrix.affine2D(center=ellipse.center, rot=pi / n * 2)
        generator = [mat]
        super().__init__(ellipse, generator, n, each=True)


def demo():
    width, height = 1024, 1024
    Figure.transform = Matrix.scale2D(width, height)

    circle = Circle(Point([0.5, 0.5]), 0.5)
    ellipse = Ellipse(Point([0.5, 0.5]), 0.5, 0.2)
    line = Line(Point([0.05, 0.5]), Point([0.95, 0.5]))
    exhibits = [
        [Diamond, [circle, 32]],
        [Cardioid, [circle, 256]],
        [Thirdioid, [circle, 256]],
        [Waves, [circle, 256]],
        [PineCone, [circle, 128]],
        [JumpRope, [circle, 256]],
        [Flower, [circle, 256, 8]],
        [KochCurve, [line, 6, False]],
        [SierpiskiGasket, [circle.circle_points(3, True), 7, False]],
        [Donuts, [ellipse, 100]],
        [DragonCurve, [line.transformed(Matrix.affine2D(center=line.mid(), scale=[0.6, 0.6])), 15, False]]
    ]

    for exhibit, args in exhibits:
        img = Image.new("RGB", (width + 1, height + 1), "white")
        painter = JPGPainter(img)

        figure = exhibit(*args)
        painter.draw(figure)

        filename = os.path.join("Gallary", figure.__class__.__name__) + ".jpg"
        img.save(filename)
        print("%s end." % figure.__class__.__name__)


if __name__ == "__main__":
    if not os.path.exists("Gallary"):
        os.mkdir("Gallary")
    demo()
    print("All end.")
