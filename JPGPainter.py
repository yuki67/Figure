from PIL import ImageDraw
from Figure import _Point, Line


class JPGPainter(object):
    """ PillowのImage用のPainter """

    def __init__(self, img):
        self.canvas = img
        self.drawer = ImageDraw.Draw(img)

    def put_pixel(self, point):
        """ canvasにpointを描画する """
        if 0 <= point[0] < self.canvas.width and 0 <= point[1] < self.canvas.height:
            self.canvas.putpixel((int(point[0]), int(point[1])),
                                 (0, 0, 0))

    def draw_line(self, line):
        """ canvasにlineを描画する """
        self.drawer.line([*line.a[:2], *line.b[:2]], fill="black")

    def split_and_draw(self, figure):
        """ figureを分解して描く """
        for sub_figure in figure:
            self.draw(sub_figure)

    def draw(self, figure):
        """ canvasにfigureを描く """
        if isinstance(figure, _Point):
            self.put_pixel(figure)
        elif isinstance(figure, Line):
            self.draw_line(figure)
        else:
            self.split_and_draw(figure)
