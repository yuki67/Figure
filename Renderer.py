from Figure import Point
from MyMatrix import Matrix


class Renderer(object):

    def __init__(self, screen_mat):
        self.screen_mat = screen_mat
        self.render_functions = {}
        self.transform_mat = Matrix.identity(len(screen_mat))

    def render(self, figure):
        """ figureの座標を変換して描画関数に渡す """
        if figure.mat is not None:
            self.transform_mat = figure.mat
        if self.render_functions.get(type(figure)):
            print(figure.mat)
            self.render_functions[type(figure)](figure.transformed(self.transform_mat * self.screen_mat))
        else:
            for sub_figure in figure:
                self.render(sub_figure)
