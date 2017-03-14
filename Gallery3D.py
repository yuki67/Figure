""" 図形描画のテスト """
import os
from PIL import Image
from Figure import Polygon, Repeats
from Figure3D import Point3D, Grid, Box
from RendererJPG import RendererJPG3D
from MyMatrix import Matrix


class BoxLined(Repeats):

    def __init__(self, a, b, n):
        box = Box(a, b)
        super().__init__(box.transform(Matrix.affine3D(center=box.a[:3], scale=(1 / n, 1.0, 1.0))),
                         Matrix.affine3D(trans=((b[0] - a[0]) / n, 0.0, 0.0)),
                         n)


class BoxGrid(Repeats):

    def __init__(self, a, b, n):
        super().__init__(BoxLined(a, b, n).transform(Matrix.affine3D(a[:3], scale=(1.0, 1 / n, 1.0))),
                         Matrix.affine3D(trans=(0.0, (b[1] - a[1]) / n, 0.0)),
                         n)


def demo():
    width, height = 1024, 1024
    a = Point3D([-10.0, -10.0, 10.0])
    b = Point3D([10.0, 10.0, 15.0])
    poly = Polygon([Point3D([-5.0, 0.0, 6.0]),
                    Point3D([5.0, 0.0, 6.0]),
                    Point3D([5.0, 0.0, 15.0]),
                    Point3D([-5.0, 0.0, 15.0]), ])

    exhibits = [
        [Grid, (poly, 15, 15)],
        [Box, (a, b)],
        [BoxLined, (a, b, 5)],
        [BoxGrid, (a, b, 5)],
    ]

    for exhibit, args in exhibits:
        img = Image.new("RGB", (width + 1, height + 1), "white")
        renderer = RendererJPG3D(img, Matrix.affine3D())

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
