""" 図形描画のテスト """
import os
from PIL import Image
from Figure import Figure, Line, Polygon
from Figure3D import Point3D
from RendererJPG import RendererJPG3D
from MyMatrix import Matrix


class Grid(Figure):
    """ 四角形内部のグリッド """

    def __init__(self, poly, n1, n2):
        assert len(poly.get_points()) == 4
        self.poly = poly
        # グリッドの分割数
        self.n1 = n1
        self.n2 = n2

    def get_iter(self):
        points = self.poly.get_points()

        def gen():
            for p, q in zip(Line(points[0], points[1], self.n1), Line(points[3], points[2], self.n1)):
                yield Line(p, q)
            for p, q in zip(Line(points[1], points[2], self.n2), Line(points[0], points[3], self.n2)):
                yield Line(p, q)
        return gen()


class Box(Figure):
    """ 直方体 """

    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __iter__(self):
        x, y, z, _ = self.a
        s, t, u, _ = self.b
        return iter([Line(self.a, Point3D([x, y, u])),
                     Line(self.a, Point3D([x, t, z])),
                     Line(self.a, Point3D([s, y, z])),
                     Line(self.b, Point3D([s, t, z])),
                     Line(self.b, Point3D([s, y, u])),
                     Line(self.b, Point3D([x, t, u])),
                     Line(Point3D([x, t, z]), Point3D([s, t, z])),
                     Line(Point3D([s, y, z]), Point3D([s, t, z])),
                     Line(Point3D([s, y, z]), Point3D([s, y, u])),
                     Line(Point3D([x, t, z]), Point3D([x, t, u])),
                     Line(Point3D([x, t, u]), Point3D([x, y, u])),
                     Line(Point3D([x, y, u]), Point3D([s, y, u]))])


def demo():
    width, height = 1024, 1024

    poly = Polygon([Point3D([-5.0, 0.0, 6.0]),
                    Point3D([5.0, 0.0, 6.0]),
                    Point3D([5.0, 0.0, 15.0]),
                    Point3D([-5.0, 0.0, 15.0]), ])

    exhibits = [
        [Grid, (poly, 15, 15)],
        [Box, (Point3D([-5.0, -5.0, 10.0]), Point3D([5.0, 5.0, 15.0]))]
    ]

    for exhibit, args in exhibits:
        img = Image.new("RGB", (width + 1, height + 1), "white")
        renderer = RendererJPG3D(img, Matrix.affine3D(trans=(0.1, 3.0, 0.1)))

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
