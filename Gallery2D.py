""" 図形描画のテスト """
import os
from math import pi
from PIL import Image
from Figure import Line, Fractal, Polygon
from Figure2D import Point2D, Circle, Ellipse
from RendererJPG import RendererJPG2D
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
        r = 1 / 3
        args = [
            [line.a, 0.0, [r, r], Point2D([0.0, 0.0])],
            [line.a, -pi / 3, [r, r], (line.b - line.a).scaled(r)],
            [line.b, pi / 3, [r, r], (line.a - line.b).scaled(r)],
            [line.b, 0.0, [r, r], Point2D([0.0, 0.0])],
        ]
        generator = [Matrix.affine2D(c, r, s, t) for c, r, s, t in args]
        super().__init__(line, generator, n, each)


class DragonCurve(Fractal):
    """ ドラゴン曲線 """

    def __init__(self, line, n, each=True):
        r = 2 ** -0.5
        args = [
            [line.a, -pi / 4, [r, r], Point2D([0.0, 0.0])],
            [line.a, -pi / 4 * 3, [r, r], line.b - line.a],
        ]
        generator = [Matrix.affine2D(c, r, s, t) for c, r, s, t in args]
        super().__init__(line, generator, n, each)


class SierpinskiGasket(Fractal):
    """ シェルピンスキーのギャスケット """

    def __init__(self, points, n):
        center = sum(points, Point2D([0.0, 0.0])).scaled(1 / len(points))
        args = [
            [center, 0.0, [0.5, 0.5], (p - center).scaled(0.5)] for p in points
        ]
        generator = [Matrix.affine2D(c, r, s, t) for c, r, s, t in args]
        super().__init__(Polygon(points), generator, n)


class Donuts(Fractal):
    """ ドーナツ """

    def __init__(self, ellipse, n=50):
        mat = Matrix.affine2D(center=ellipse.center, rot=pi / n * 2)
        generator = [mat]
        super().__init__(ellipse, generator, n, each=True)


class OneLineSweeping(Fractal):
    """ 直線からの掃討 """

    def __init__(self, line, n, each=True):
        p = (line.b - line.a).scaled(0.5)
        args = [
            [line.a, -pi / 4, [2**-0.5, 2**-0.5], Point2D([0.0, 0.0]), [False, True]],
            [line.a, 0, [0.5, 0.5], Point2D([p[1], -p[0]]) + p, [False, False]],
            [line.b, pi / 2, [0.5, 0.5], Point2D([p[1], -p[0]]), [True, True]],
        ]
        generator = [Matrix.affine2D(c, r, s, t, m) for c, r, s, t, m in args]
        super().__init__(line, generator, n, each)


def demo():
    center = Point2D([0.5, 0.5])
    circle = Circle(center, 0.5)
    ellipse = Ellipse(center, 0.5, 0.25)
    line = Line(Point2D([0.05, 0.5]), Point2D([0.95, 0.5]))
    bottom_line = Line(Point2D([0.05, 0.95]), Point2D([0.95, 0.95]))
    exhibits = [
        [Diamond, [circle, 32]],
        [Cardioid, [circle, 256]],
        [Thirdioid, [circle, 256]],
        [Waves, [circle, 256]],
        [PineCone, [circle, 128]],
        [JumpRope, [circle, 256]],
        [Flower, [circle, 256, 8]],
        [KochCurve, [line, 6, False]],
        [SierpinskiGasket, [circle.circle_points(3, True), 7]],
        [Donuts, [ellipse, 100]],
        [DragonCurve, [line.transformed(Matrix.affine2D(center=line.mid(), scale=[0.6, 0.6])), 12, False]],
        [OneLineSweeping, [bottom_line, 8, False]],
    ]

    width, height = 1024, 1024
    for exhibit, args in exhibits:
        img = Image.new("RGB", (width, height), "white")
        renderer = RendererJPG2D(img, Matrix.scale2D(width - 1, height - 1))

        figure = exhibit(*args)
        print("%s begin." % figure.__class__.__name__)
        renderer.render(figure)

        filename = os.path.join("Gallery", figure.__class__.__name__) + ".jpg"
        img.save(filename)
        print("%s end." % figure.__class__.__name__)


if __name__ == "__main__":
    if not os.path.exists("Gallery"):
        os.mkdir("Gallery")
    demo()
    print("All end.")
