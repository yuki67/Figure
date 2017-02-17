from PIL import ImageDraw
from Figure import _Point


class JPGPainter(object):
    """ PillowのImage用のPainter """

    def __init__(self, img):
        self.canvas = img
        self.drawer = ImageDraw.Draw(img)

    def put_pixel(self, point):
        """ canvasにpointを描画する """
        if 0 <= point.pos[0] < self.canvas.width and 0 <= point.pos[1] < self.canvas.height:
            self.canvas.putpixel((int(point.pos[0]), int(point.pos[1])),
                                 tuple(point.rgb))

    def split_and_draw(self, figure):
        """ figureを分解して描く """
        for sub_figure in figure:
            self.draw(sub_figure)

    def draw(self, figure):
        """ canvasにfigureを描く """
        if isinstance(figure, _Point):
            self.put_pixel(figure)
        else:
            self.split_and_draw(figure)
