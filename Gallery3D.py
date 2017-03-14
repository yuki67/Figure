""" 図形描画のテスト """
import os
from PIL import Image
from Figure import Polygon
from Figure3D import Point3D, Grid, Box
from RendererJPG import RendererJPG3D
from MyMatrix import Matrix


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
