from math import sin, cos


class Matrix(list):

    def __repr__(self):
        return "Matrix(%s)" % list.__str__(list(self))

    def __add__(self, other):
        return Matrix([[a + b for a, b in zip(a_list, b_list)] for a_list, b_list in zip(self, other)])

    def __sub__(self, other):
        return Matrix([[a - b for a, b in zip(a_list, b_list)] for a_list, b_list in zip(self, other)])

    def __mul__(self, other):
        return Matrix([[sum([a * b for a, b in zip(self.row(i), other.column(j))]) for j in range(len(other))] for i in range(len(self))])

    def row(self, n):
        return self[n]

    def column(self, n):
        return [a[n] for a in self]

    @staticmethod
    def identity(n):
        ans = [[0 for j in range(n)] for i in range(n)]
        for i in range(n):
            ans[i][i] = 1
        return Matrix(ans)

    @staticmethod
    def rot2D(rot):
        return Matrix([[cos(rot), sin(rot), 0.0],
                       [-sin(rot), cos(rot), 0.0],
                       [0.0, 0.0, 1.0]])

    @staticmethod
    def trans2D(x, y):
        return Matrix([[1.0, 0.0, 0.0],
                       [0.0, 1.0, 0.0],
                       [x, y, 1.0]])

    @staticmethod
    def scale2D(x, y):
        return Matrix([[x, 0.0, 0.0],
                       [0.0, y, 0.0],
                       [0.0, 0.0, 1.0]])

    @staticmethod
    def affine2D(center=[0.0, 0.0], rot=0.0, scale=[1.0, 1.0], trans=[0.0, 0.0]):
        return Matrix.trans2D(-center[0], -center[1]) * \
            Matrix.rot2D(rot) * \
            Matrix.scale2D(scale[0], scale[1]) * \
            Matrix.trans2D(trans[0], trans[1]) * \
            Matrix.trans2D(center[0], center[1])
