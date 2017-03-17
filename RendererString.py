from Renderer import Renderer
from Figure import Point, Line, Polygon
from Figure3D import Grid, Box
from Figure2D import Ellipse, Circle


class RendererString(Renderer):

    def __init__(self, screen_mat):
        super().__init__(screen_mat)
        f = lambda figure: print(figure)
        self.render_functions[Point] = f
        self.render_functions[Line] = f
        self.render_functions[Polygon] = f
        self.render_functions[Ellipse] = f
        self.render_functions[Circle] = f
        self.render_functions[Grid] = f
        self.render_functions[Box] = f
