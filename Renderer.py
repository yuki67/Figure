from Figure import Point
from MyMatrix import Matrix


class Renderer(object):

    def __init__(self, screen_mat):
        self.screen_mat = screen_mat

    def put_pixel(self, point):
        """ ドットを受け取る """
        pass

    def render(self, figure):
        """ figureの座標を変換して描画関数に渡す """
        pass
