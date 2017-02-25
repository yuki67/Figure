from PIL import ImageDraw, Image
from Figure import Point, Line


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
        if isinstance(figure, Point):
            self.put_pixel(figure)
        elif isinstance(figure, Line):
            self.draw_line(figure)
        else:
            self.split_and_draw(figure)


def save_gif(figure, filename, width, height, duration=100, loop=True):
    """ figureを書くGIF画像を作る """
    # 注意: 一つの図形を書くたびにフレームが追加されるため場合によってはとても重くなる
    img = Image.new("RGB", (width + 1, height + 1), "white")
    gif_images = []

    class AnxiousPainter(JPGPainter):
        """ drawするたびにgif_imagesに画像のコピーを追加するようにしたJPGPainter """

        def draw(self, figure):
            """ canvasにfigureを描く """
            super().draw(figure)
            gif_images.append(self.canvas.copy())

    AnxiousPainter(img).draw(figure)
    # サイズを小さくしたいのは山々だが、optimizeをFalse以外にすると画像が壊れる(Pillowのバグ)
    Image.new("RGB", (width + 1, height + 1), "white").save(filename, save_all=True, append_images=gif_images, loop=loop, duration=duration, optimize=False)
