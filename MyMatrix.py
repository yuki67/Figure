from math import sin, cos


class Matrix(list):
    # よく使われそうな恒等行列を定値として持っておく

    def __init__(self, lst, is_identity=False):
        super().__init__(lst)
        self.is_identity = is_identity

    def __repr__(self):
        return "Matrix(%s)" % list.__str__(list(self))

    def __add__(self, other):
        return Matrix([[a + b for a, b in zip(a_list, b_list)] for a_list, b_list in zip(self, other)])

    def __sub__(self, other):
        return Matrix([[a - b for a, b in zip(a_list, b_list)] for a_list, b_list in zip(self, other)])

    def __mul__(self, other):
        if self.is_identity:
            return other
        elif other.is_identity:
            return self
        else:
            return Matrix([[sum([a * b for a, b in zip(self.row(i), other.column(j))]) for j in range(len(other))] for i in range(len(self))])

    def row(self, n):
        return self[n]

    def column(self, n):
        return [a[n] for a in self]

    @staticmethod
    def identity(n):
        # 定値として持っていればそれを返す
        if n == 3:
            return iden_three
        elif n == 4:
            return iden_four
        else:
            # 定値として持っていなければ作る
            ans = [[0 for j in range(n)] for i in range(n)]
            for i in range(n):
                ans[i][i] = 1
            return Matrix(ans, True)

    @staticmethod
    def rot2D(rot):
        if rot == 0.0:
            return Matrix.identity(3)
        else:
            return Matrix([[cos(rot), sin(rot), 0.0],
                           [-sin(rot), cos(rot), 0.0],
                           [0.0, 0.0, 1.0]])

    @staticmethod
    def trans2D(x, y):
        if x == y == 0.0:
            return Matrix.identity(3)
        else:
            return Matrix([[1.0, 0.0, 0.0],
                           [0.0, 1.0, 0.0],
                           [x, y, 1.0]])

    @staticmethod
    def scale2D(x, y):
        if x == y == 1.0:
            return Matrix.identity(3)
        else:
            return Matrix([[x, 0.0, 0.0],
                           [0.0, y, 0.0],
                           [0.0, 0.0, 1.0]])

    @staticmethod
    def swap2D(x, y):
        if x == y == False:
            return Matrix.identity(3)
        else:
            return Matrix([[2 * int(not x) - 1, 0.0, 0.0],
                           [0.0, 2 * int(not y) - 1, 0.0],
                           [0.0, 0.0, 1.0]])

    @staticmethod
    def affine2D(center=[0.0, 0.0], rot=0.0, scale=[1.0, 1.0], trans=[0.0, 0.0], swap=[False, False]):
        return Matrix.trans2D(-center[0], -center[1]) * \
            Matrix.swap2D(*swap) * \
            Matrix.rot2D(rot) * \
            Matrix.scale2D(scale[0], scale[1]) * \
            Matrix.trans2D(trans[0], trans[1]) * \
            Matrix.trans2D(center[0], center[1])

    @staticmethod
    def rot3D(x, y, z):
        if x == y == z == 0.0:
            return Matrix.identity(4)
        else:
            return Matrix([[1.0, 0.0, 0.0, 0.0],
                           [0.0, cos(x), -sin(x), 0.0],
                           [0.0, sin(x), cos(x), 0.0],
                           [0.0, 0.0, 0.0, 1.0]]) * \
                Matrix([[cos(y), 0.0, sin(y), 0.0],
                        [0.0, 1.0, 0.0, 0.0],
                        [-sin(y), 0.0, cos(y), 0.0],
                        [0.0, 0.0, 0.0, 1.0]]) * \
                Matrix([[cos(z), -sin(z), 0.0, 0.0],
                        [sin(z), cos(z), 0.0, 0.0],
                        [0.0, 0.0, 1.0, 0.0],
                        [0.0, 0.0, 0.0, 1.0]])

    @staticmethod
    def trans3D(x, y, z):
        if x == y == z == 0.0:
            return Matrix.identity(4)
        else:
            return Matrix([[1.0, 0.0, 0.0, 0.0],
                           [0.0, 1.0, 0.0, 0.0],
                           [0.0, 0.0, 1.0, 0.0],
                           [x, y, z, 1.0]])

    @staticmethod
    def scale3D(x, y, z):
        if x == y == z == 1.0:
            return Matrix.identity(4)
        else:
            return Matrix([[x, 0.0, 0.0, 0.0],
                           [0.0, y, 0.0, 0.0],
                           [0.0, 0.0, z, 0.0],
                           [0.0, 0.0, 0.0, 1.0]])

    @staticmethod
    def swap3D(x, y, z):
        if x == y == z == False:
            return Matrix.identity(4)
        else:
            return Matrix([[2 * int(not x) - 1, 0.0, 0.0, 0.0],
                           [0.0, 2 * int(not y) - 1, 0.0, 0.0],
                           [0.0, 0.0, 2 * int(not z) - 1, 0.0],
                           [0.0, 0.0, 0.0, 1.0]])

    @staticmethod
    def projection3D(n, f, l, b, r, t):
        return Matrix([[2 * n / (r - l), 0, 0, 0],
                       [0, 2 * n / (t - b), 0, 0],
                       [-(r + l) / (r - l), -(t + b) / (t - b), f / (f - n), 1],
                       [0, 0, -f * n / (f - n), 0]])

    @staticmethod
    def affine3D(center=(0.0, 0.0, 0.0), rot=(0.0, 0.0, 0.0), scale=(1.0, 1.0, 1.0), trans=(0.0, 0.0, 0.0), swap=(False, False, False)):
        # swapは変換の最初に行われるが、指定される頻度が低いと思われるので引数の最後においてある点に注意
        return Matrix.trans3D(-center[0], -center[1], -center[2]) * \
            Matrix.swap3D(*swap) * \
            Matrix.rot3D(*rot) * \
            Matrix.scale3D(*scale) * \
            Matrix.trans3D(*trans) * \
            Matrix.trans3D(*center)

iden_three = Matrix([[1.0, 0.0, 0.0],
                     [0.0, 1.0, 0.0],
                     [0.0, 0.0, 1.0]], True)
iden_four = Matrix([[1.0, 0.0, 0.0, 0.0],
                    [0.0, 1.0, 0.0, 0.0],
                    [0.0, 0.0, 1.0, 0.0],
                    [0.0, 0.0, 0.0, 1.0]], True)
