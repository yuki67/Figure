from math import cos, sin, pi
from Figure import *
from Figure2D import *
from Figure3D import *
from MyMatrix import Matrix
import random


class Blocks(Figure):
    """ ブロックたくさん """

    def get_iter(self):
        if self.n == 0:
            return iter((self.poly),)

        r = random.uniform(0.15, 0.5)
        s = random.uniform(r, 0.80)
        t = random.uniform(0.15, 0.5)
        u = random.uniform(t, 0.80)
        dx = (self.poly.points[1] - self.poly.points[0])[0]
        dy = (self.poly.points[3] - self.poly.points[0])[1]
        return iter((Blocks(self.poly.transformed(Matrix.affine2D(center=self.poly.points[0], trans=[0.0, 0.0], scale=[s, t])), self.n - 1),
                     Blocks(self.poly.transformed(Matrix.affine2D(center=self.poly.points[0], trans=[dx * s, 0.0], scale=[1 - s, u])), self.n - 1),
                     Blocks(self.poly.transformed(Matrix.affine2D(center=self.poly.points[0], trans=[0.0, dy * t], scale=[r, (1 - t)])), self.n - 1),
                     Blocks(self.poly.transformed(Matrix.affine2D(center=self.poly.points[0], trans=[dx * r, dy * u], scale=[1 - r, 1 - u])), self.n - 1),
                     Blocks(self.poly.transformed(Matrix.affine2D(center=self.poly.points[0], trans=[dx * r, dy * t], scale=[s - r, u - t])), self.n - 1),))

    def __init__(self, poly, n):
        super().__init__(3)
        self.n = n
        self.poly = poly

points = [point_2d(0.0, 0.0), point_2d(1.0, 0.0), point_2d(1.0, 1.0), point_2d(0.0, 1.0)]
figure = Blocks(Polygon(points), 4)
