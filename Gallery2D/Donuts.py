from math import pi
from Figure import Repeats
from Figure2D import point_2d, Ellipse
from MyMatrix import Matrix


class Donuts(Repeats):
    """ ドーナツ """

    def __init__(self, ellipse, n=50):
        super().__init__(ellipse, Matrix.affine2D(center=ellipse.center, rot=pi / n * 2), n)

figure = Donuts(Ellipse(point_2d(0.5, 0.5), 0.5, 0.25), 100)
