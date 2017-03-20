""" tkinterのクラスを自分が使いやすい様に改造したもの """
import tkinter
import importlib
from Renderer import Renderer
from MyMatrix import Matrix
from Figure import Point, Line


class RendererTk2D(tkinter.Canvas, Renderer):
    """ tkinter用レンダラー """
    # 単体でも使えないことはないが使いみちがないと思う

    def __init__(self, master, screen_mat):
        tkinter.Canvas.__init__(self, master, width=master.winfo_width(), height=master.winfo_height())
        Renderer.__init__(self, screen_mat)
        self.pack()
        self.render_functions[Point] = self.render_point
        self.render_functions[Line] = self.render_line

    def render_point(self, p):
        self.create_rectangle(p[0], p[1], p[0] + 1, p[1] + 1, width=0)

    def render_line(self, line):
        self.create_line(line.a[0], line.a[1], line.b[0], line.b[1])


class ReloadButton(tkinter.Button):
    """ ファイルのリロード用ボタン """

    def __init__(self, master):
        super().__init__(master)
        self["text"] = "reload"
        self.bind("<Button-1>", self.on_button_click)

    def on_button_click(self, _):
        self.master.reload_figure()


class FigureViewer(tkinter.Tk):
    """
    Figureのビューア
    FigureViewer.figureの[0, 1]*[0, 1]の範囲がレンダリングされる
    """

    def __init__(self, width, height, filename, window_name="My window"):
        """ self.filenameの中で定義されたfigureが描画される """
        super().__init__()
        self.initialize(width, height, window_name)

        # ファイルをロード
        self.module = __import__(filename[:-3])
        # レンダリングされるのは[0, 1]*[0, 1]の部分
        self.renderer = RendererTk2D(self, Matrix.affine2D(scale=[width, height]))
        # figureをロードする
        self.reload_figure()

    def initialize(self, width, height, window_name):
        """ ウィンドウの初期化とウィジェットの配置 """
        ReloadButton(self).pack()
        self.wm_title(window_name)
        self.geometry("%dx%d" % (width, height))
        self.attributes("-topmost", True)
        # このupdate()を抜かすとCanvasとButtonが配置されない
        self.update()

    def reload_figure(self):
        """ self.module.figureをself.rendererに書く """
        self.renderer.delete("all")
        # self.moduleは関数が呼ばれるたびにリロードする
        importlib.reload(self.module)
        self.renderer.render(self.module.figure)
        self.update()

r = FigureViewer(512, 512, "test.py")
r.mainloop()
