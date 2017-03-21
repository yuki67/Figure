""" tkinterのクラスを自分が使いやすい様に改造したもの """
import tkinter
import importlib
import os
import sys
from Renderer import Renderer
from MyMatrix import Matrix
from Figure import Point, Line


class RendererTk2D(tkinter.Canvas, Renderer):
    """ tkinter用レンダラー """
    # 単体でも使えないことはないが使いみちがないと思う

    def __init__(self, master, screen_mat):
        tkinter.Canvas.__init__(self, master, width=master.winfo_width(), height=master.winfo_height())
        Renderer.__init__(self, screen_mat)
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
        self.master.master.load_figure()


class SaveButton(tkinter.Button):
    """ 画像の保存用ボタン """

    def __init__(self, master):
        super().__init__(master)
        self["text"] = "save"
        self.bind("<Button-1>", self.on_button_click)

    def on_button_click(self, _):
        self.master.master.save_figure()


class FilenameList(tkinter.Listbox):
    """ Galleryフォルダ内のpythonファイルの一覧を表示するリスト """

    def __init__(self, master):
        super().__init__(master)
        self["height"] = 3
        self["selectmode"] = tkinter.SINGLE
        for file in os.listdir("./Gallery"):
            if file[-3:] == ".py":
                self.insert(tkinter.END, file)

    def load(self):
        """ 選択されているファイルを読み込んでモジュールオブジェクトを返す """
        filename = self.get(tkinter.ACTIVE)
        module = __import__(filename[:-3])
        importlib.reload(module)
        return module


class FrameTop(tkinter.Frame):
    """ 各種ボタンを収めるフレーム """

    def __init__(self, master):
        super().__init__(master)
        self.reload_button = ReloadButton(self)
        self.save_button = SaveButton(self)
        self.filename_list = FilenameList(self)
        self.reload_button.pack(side=tkinter.LEFT)
        self.save_button.pack(side=tkinter.LEFT)
        self.filename_list.pack(side=tkinter.LEFT)
        self.pack()


class FigureViewer(tkinter.Tk):
    """
    Figureのビューア
    FigureViewer.figureの[0, 1]*[0, 1]の範囲がレンダリングされる
    """
    # 上下左右の余白
    SPACE = 50
    # 保存される画像のサイズ
    IMG_SIZE = 1024

    def __init__(self, width, height, filename, window_name="My window"):
        """ self.filenameの中で定義されたfigureが描画される """
        super().__init__()
        self.initialize(width, height, window_name)

        # ファイルをロード
        sys.path.append(os.path.abspath("./Gallery"))
        # レンダリングされるのは[0, 1]*[0, 1]の部分
        self.renderer = RendererTk2D(self,
                                     Matrix.affine2D(scale=[width, height], trans=[self.SPACE, self.SPACE]) *
                                     Matrix.affine2D(center=[0.0, height / 2 + self.SPACE], swap=[0, 1]))
        self.renderer.pack()
        # figureをロードする
        self.load_figure()

    def initialize(self, width, height, window_name):
        """ ウィンドウの初期化とフレームの配置 """
        self.wm_title(window_name)
        self.geometry("%dx%d" % (width + self.SPACE * 2, height + self.SPACE * 2))
        self.attributes("-topmost", True)
        self.frame = FrameTop(self)
        # このupdate()を抜かすとCanvasとButtonが配置されない
        self.update()

    def load_figure(self):
        """ self.module.figureをself.rendererに書く """
        self.renderer.delete("all")
        module = self.frame.filename_list.load()
        # self.moduleは関数が呼ばれるたびにリロードする
        self.renderer.render(module.figure)
        self.update()

    def save_figure(self):
        """ self.module.figureをjpg画像で保存する """
        from PIL import Image
        from RendererJPG import RendererJPG2D
        img = Image.new("RGB", (self.IMG_SIZE + 1, self.IMG_SIZE + 1), "white")
        renderer = RendererJPG2D(img,
                                 Matrix.affine2D(scale=[self.IMG_SIZE, self.IMG_SIZE]) *
                                 Matrix.affine2D(center=[0.0, self.IMG_SIZE / 2], swap=[0, 1]))
        renderer.render(self.frame.filename_list.load().figure)
        img.save("Gallery//" + self.frame.filename_list.get(tkinter.ACTIVE)[:-3] + ".jpg")

r = FigureViewer(512, 512, "playground.py")
r.mainloop()
