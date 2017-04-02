from math import pi
from Figure import Fractal
from Figure2D import point_2d, Ellipse
from MyMatrix import Matrix


class Tornade(Fractal):
    """ うずまき """

    def __init__(self, n):
        ellipse = Ellipse(point_2d(0.5, 0.5), 0.25, 0.5)
        r = 0.995
        args = [
            [(0.5, 0.5), pi / 125, (r, r), (0.0, 0.0)]
        ]
        generator = [Matrix.affine2D(c, r, s, t) for c, r, s, t in args]
        super().__init__(ellipse, generator, n, True)

figure = Tornade(300)
