from Figure2D import point_2d, Circle, Circloid


class PineCone(Circloid):
    """ 松ぼっくりに見えなくもない """

    def __init__(self, circle, n=32):
        def f(i, j):
            k = self.n**0.5
            if -k < (j + i) % self.n < k or (j + i) % self.n > -k % self.n:
                return True
            return False
        super().__init__(circle, n, f)

figure = PineCone(Circle(point_2d(0.5, 0.5), 0.5), 128)
