""" 図形描画のテスト """
import os
from PIL import Image
import Figure
from Figure import Line, Point, Fractal, Polygon, Circle
from JPGPainter import JPGPainter
from MyMatrix import Matrix


class Diamond(object):
    """ ダイヤモンドパターン """

    def __init__(self, circle, n=16):
        self.circle = circle
        self.n = n

    def __iter__(self):
        points = self.circle.points(self.n)
        return (Line(p, q) for p in points for q in points)


class Cardioid(object):
    """ カージオイド """

    def __init__(self, circle, n=128):
        self.circle = circle
        self.n = n

    def __iter__(self):
        points = list(self.circle.points(self.n))
        n = len(points)
        return (Line(points[i], points[(2 * i) % n]) for i in range(n))


def demo():
    width, height = 1024, 1024
    Figure.transform = Matrix.scale2D(width, height)

    circle = Circle(Point(0.5, 0.5), 0.5)
    exhibits = [
        [Diamond, [circle, 64]],
        [Cardioid, [circle, 512]]
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
