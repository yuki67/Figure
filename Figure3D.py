""" 2次元の図形 """
from Figure import Point


class Point3D(Point):
    """ 3次元の点 """

    def __init__(self, lst):
        assert len(lst) == 3
        super().__init__(lst + [1.0])
