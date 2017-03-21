from Figure2D import point_2d, Circle, Circloid


class Waves(Circloid):
    """ 波っぽいのが見える """

    def __init__(self, circle, n=256):
        super().__init__(circle, n, lambda i, j: i % (j + 1) == 0)

figure = Waves(Circle(point_2d(0.5, 0.5), 0.5), 256)
