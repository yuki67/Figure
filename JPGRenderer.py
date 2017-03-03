from PIL import ImageDraw, Image
from Figure import Point, Line, Fractal
from MyMatrix import Matrix
from Renderer import Renderer


class JPGRenderer(Renderer):
    """ PillowのImage用のRenderer """

    def __init__(self, img):
        self.canvas = img
        self.drawer = ImageDraw.Draw(img)
        width, height = img.size
        proj = Matrix.projection3D(9.9, 50, -10, -10, 10, 10)
        screen = Matrix.affine3D(center=(0.0, 0.0, 0.0), scale=(width / 2, height / 2, 1.0), trans=(width / 2, height / 2, 0.0))
        super().__init__(proj, screen)

    def put_pixel(self, point):
        """ canvasにpointを描画する """
        if 0 <= point[0] < self.canvas.width and 0 <= point[1] < self.canvas.height:
            self.canvas.putpixel((int(point[0]), int(point[1])),
                                 (0, 0, 0))

    def render_line(self, line):
        """ canvasにlineを描画する """
        self.drawer.line([*line.a[:2], *line.b[:2]], fill="black")

    def render(self, figure):
        """ canvasにfigureを描く """
        if isinstance(figure, Point):
            self.put_pixel(figure.transformed(self.bootstrap * self.world_to_screen))
        elif isinstance(figure, Line):
            self.render_line(figure.transformed(self.bootstrap * self.world_to_screen))
        else:
            for sub_figure in figure:
                self.render(sub_figure)


def save_gif(figure, filename, width, height, duration=100, loop=True):
    """ figureを書くGIF画像を作る """
    # 注意: 一つの図形を書くたびにフレームが追加されるため場合によってはとても重くなる
    img = Image.new("RGB", (width + 1, height + 1), "white")
    gif_images = []

    class AnxiousRenderer(JPGRenderer):
        """ renderするたびにgif_imagesに画像のコピーを追加するようにしたJPGRenderer """

        def render(self, figure):
            """ canvasにfigureを描く """
            super().render(figure)
            gif_images.append(self.canvas.copy())

    AnxiousRenderer(img).render(figure)
    # サイズを小さくしたいのは山々だが、optimizeをFalse以外にすると画像が壊れる(Pillowのバグ)
    Image.new("RGB", (width + 1, height + 1), "white").save(filename, save_all=True, append_images=gif_images, loop=loop, duration=duration, optimize=False)


def save_fractal_gif(fractal, filename, width, height, duration=100, loop=0xffff):
    """ フラクタルを書くGIF画像を作る """
    img = Image.new("RGB", (width + 1, height + 1), "white")
    initiator_class = fractal.initiator.__class__
    gif_images = []

    class AnxiousRenderer(JPGRenderer):
        """ fractal.initiatorを書くたびにgif_imagesに画像のコピーを追加するJPGRenderer """
        n = 0

        def render(self, figure):
            """ canvasにfigureを描く """
            super().render(figure)
            # イニシエータを書いたらgif_imagesに保存する
            if figure.__class__ == initiator_class:
                gif_images.append(self.canvas.copy())

    AnxiousRenderer(img).render(fractal)
    # サイズを小さくしたいのは山々だが、optimizeをFalse以外にすると画像が壊れる(Pillowのバグ)
    Image.new("RGB", (width + 1, height + 1), "white").save(filename, save_all=True, append_images=gif_images, loop=loop, duration=duration, optimize=False)
