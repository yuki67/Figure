""" 図形描画のテスト """
import os
from PIL import Image
import Figure
from Figure import Line, Point, Fractal, Polygon, Circle
from JPGPainter import JPGPainter
from MyMatrix import Matrix


class Circloid(object):
    """ サークロイド(造語) """

    def __init__(self, circle, n, f):
        self.circle = circle
        self.n = n
        self.f = f

    def __iter__(self):
        points = self.circle.points(self.n)
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


def demo():
    width, height = 1024, 1024
    Figure.transform = Matrix.scale2D(width, height)

    circle = Circle(Point(0.5, 0.5), 0.5)
    exhibits = [
        [Diamond, [circle, 32]],
        [Cardioid, [circle, 256]],
        [Thirdioid, [circle, 256]],
        [Waves, [circle, 256]],
        [PineCone, [circle, 128]],
        [JumpRope, [circle, 256]],
    ]

    for exhibit, args in exhibits:
        img = Image.new("RGB", (width + 1, height + 1), "white")
        painter = JPGPainter(img)

        figure = exhibit(*args)
        painter.draw(figure)

        filename = os.path.join("Gallary", figure.__class__.__name__) + ".jpg"
        img.save(filename)
        os.startfile(filename)


if __name__ == "__main__":
    if not os.path.exists("Gallary"):
        os.mkdir("Gallary")
    demo()
