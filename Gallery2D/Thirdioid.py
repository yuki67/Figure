from Figure2D import point_2d, Circle, Circloid


class Thirdioid(Circloid):
    """ サージオイド(造語) """

    def __init__(self, circle, n=256):
        super().__init__(circle, n, lambda i, j: (3 * i) % n == j)

figure = Thirdioid(Circle(point_2d(0.5, 0.5), 0.5), 256)
