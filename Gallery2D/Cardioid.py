from Figure2D import point_2d, Circle, Circloid


class Cardioid(Circloid):
    """ カージオイド """

    def __init__(self, circle, n=256):
        super().__init__(circle, n, lambda i, j: (2 * i) % n == j)

figure = Cardioid(Circle(point_2d(0.5, 0.5), 0.5), 256)
