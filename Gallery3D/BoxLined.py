""" 図形描画のテスト """
from Figure import Repeats
from Figure3D import point_3d, Box
from MyMatrix import Matrix


class BoxLined(Repeats):

    def __init__(self, a, b, n):
        box = Box(a, b)
        super().__init__(box.transform(Matrix.affine3D(center=box.a[:3], trans=((b - a).scaled(1 / n / 4)[0], 0.0, 0.0), scale=(1 / n / 2, 1.0, 1.0))),
                         Matrix.affine3D(trans=((b[0] - a[0]) / n, 0.0, 0.0)),
                         n)

a = point_3d(-10.0, -10.0, 10.0)
b = point_3d(10.0, 10.0, 15.0)
figure = BoxLined(a, b, 5)
