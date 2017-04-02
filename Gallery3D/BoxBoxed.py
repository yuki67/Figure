from Figure import Repeats
from Figure3D import point_3d, Box
from MyMatrix import Matrix


class BoxLined(Repeats):

    def __init__(self, a, b, n):
        box = Box(a, b)
        super().__init__(box.transform(Matrix.affine3D(center=box.a[:3], trans=((b - a).scaled(1 / n / 4)[0], 0.0, 0.0), scale=(1 / n / 2, 1.0, 1.0))),
                         Matrix.affine3D(trans=((b[0] - a[0]) / n, 0.0, 0.0)),
                         n)


class BoxGrid(Repeats):

    def __init__(self, a, b, n):
        super().__init__(BoxLined(a, b, n).transform(Matrix.affine3D(a[:3], trans=(0.0, (b - a).scaled(1 / n / 4)[1], 0.0), scale=(1.0, 1 / n / 2, 1.0))),
                         Matrix.affine3D(trans=(0.0, (b[1] - a[1]) / n, 0.0)),
                         n)


class BoxBoxed(Repeats):

    def __init__(self, a, b, n):
        super().__init__(BoxGrid(a, b, n).transform(Matrix.affine3D(a[:3], trans=(0.0, 0.0, (b - a).scaled(1 / n / 4)[2]), scale=(1.0, 1.0, 1 / n / 2))),
                         Matrix.affine3D(trans=(0.0, 0.0, (b[2] - a[2]) / n)),
                         n)

a = point_3d(-10.0, -10.0, 10.0)
b = point_3d(10.0, 10.0, 15.0)
figure = BoxBoxed(a, b, 5)
