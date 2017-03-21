from Figure2D import point_2d, Circle, Circloid


class Diamond(Circloid):
    """ ダイヤモンドパターン """

    def __init__(self, circle, n=16):
        super().__init__(circle, n, lambda i, j: True)

figure = Diamond(Circle(point_2d(0.5, 0.5), 0.5), 32)
