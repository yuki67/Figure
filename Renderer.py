from Figure import Point
from MyMatrix import Matrix


class Renderer(object):

    def __init__(self, screen_mat):
        self.screen_mat = screen_mat
        self.render_functions = {}

    def render(self, figure):
        """ figureの座標を変換して描画関数に渡す """
        if self.render_functions.get(type(figure)):
            self.render_functions[type(figure)](figure.transformed(self.screen_mat))
        else:
            for sub_figure in figure:
                self.render(sub_figure)
