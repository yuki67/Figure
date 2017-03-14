from Figure import Point


class Renderer(object):

    def __init__(self, screen_mat):
        """
        注意: transformed()が定義されていないFigureに対してrender_functionを設定することはできない
        """
        self.screen_mat = screen_mat
        self.render_functions = {Point: lambda self, p: print("rendered: " + str(p))}

    def render(self, figure):
        """ figureの座標を変換して描画関数に渡す """
        if self.render_functions.get(type(figure)):
            # Figure.transformedはここでのみ使われる
            self.render_functions[type(figure)](figure.transformed(figure.mat * self.screen_mat))
        else:
            for sub_figure in figure:
                self.render(sub_figure)
