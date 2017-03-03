from Figure import Point
from MyMatrix import Matrix


class Renderer(object):

    def __init__(self, proj, screen):
        self.bootstrap = Matrix.identity(len(proj))
        self.world_to_screen = proj * screen

    def put_pixel(self, point):
        """ ドットを受け取る """
        pass

    def render(self, figure):
        """ figureの座標を変換して描画関数に渡す """
        if isinstance(figure, Point):
            self.put_pixel(figure.transformed(self.bootstrap * self.world_to_screen))
        else:
            for sub_figure in figure:
                self.render(sub_figure)
