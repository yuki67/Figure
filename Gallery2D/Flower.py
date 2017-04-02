from Figure2D import point_2d, Circle, Circloid


class Flower(Circloid):
    """ 花を真上から見たのに似てる """

    def __init__(self, circle, n=128, k=8):
        def f(i, j):
            return i < j and (i + j) % (self.n // k) == 0
        super().__init__(circle, n, f)

figure = Flower(Circle(point_2d(0.5, 0.5), 0.5), 256, 8)
