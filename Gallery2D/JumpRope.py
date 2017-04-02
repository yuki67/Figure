from Figure2D import point_2d, Circle, Circloid


class JumpRope(Circloid):
    """ 縄跳びをスローシャッターで撮ったときの模様に似てる """

    def __init__(self, circle, n=256):
        def f(i, j):
            k = self.n**0.25
            if -k < (j + i) % self.n < k or (j + i) % self.n > -k % self.n:
                return True
            return False
        super().__init__(circle, n, f)

figure = JumpRope(Circle(point_2d(0.5, 0.5), 0.5), 256)
