from PIL import Image, ImageDraw

from Figure import Point


class Painter(object):
    """ 絵を描くための基底クラス """

    def __init__(self):
        # draw_functionsで描画に使う関数を指定する
        # 何も指定しなければ、すべて点で描画される(遅い)
        self.draw_functions = {
            Point: self.put_pixel
        }

    def put_pixel(self, point):
        """ canvasにpointを描画する """
        pass

    def split_and_draw(self, figure):
        """ figureを分解して描く """
        for sub_figure in figure:
            self.draw(sub_figure)

    def draw(self, figure):
        """ canvasにfigureを描く """
        self.draw_functions.get(type(figure), self.split_and_draw)(figure)


class JPGPainter(Painter):
    """ PillowのImage用のPainter """

    def __init__(self, img):
        super().__init__()
        self.canvas = img
        self.drawer = ImageDraw.Draw(img)

    def put_pixel(self, point):
        """ canvasにpointを描画する """
        if 0 <= point.x < self.canvas.width and 0 <= point.y < self.canvas.height:
            self.canvas.putpixel((int(point.x), int(point.y)),
                                 tuple(point.rgb))
