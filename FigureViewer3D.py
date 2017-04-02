""" tkinterのクラスを自分が使いやすい様に改造したもの """
import tkinter
import os
import sys
import time
from MyMatrix import Matrix
from FigureViewer import FigureViewer, RendererTk


class FigureViewer3D(FigureViewer):
    """
    三次元のFigureのビューア
    """
    DIFF = 0.3
    Z_ADD = Matrix.affine3D(trans=(0.0, 0.0, DIFF))
    Z_SUB = Matrix.affine3D(trans=(0.0, 0.0, -DIFF))
    Y_ADD = Matrix.affine3D(trans=(0.0, DIFF, 0.0))
    Y_SUB = Matrix.affine3D(trans=(0.0, -DIFF, 0.0))
    X_ADD = Matrix.affine3D(trans=(DIFF, 0.0, 0.0))
    X_SUB = Matrix.affine3D(trans=(-DIFF, 0.0, 0.0))

    def __init__(self, width, height):
        self.proj = Matrix.projection3D(9.9, 50, -10, -10, 10, 10)
        self.screen = Matrix.affine3D(center=(0.0, 0.0, 0.0), scale=(width / 2, height / 2, 1.0), trans=(width / 2, height / 2, 0.0))
        super().__init__(width, height, self.proj * self.screen, "Gallery3D", "FigureViewer3D")
        self.bind("<Key>", self.key_event)
        self.bind("<space>", self.up)
        self.bind("<Control_L>", self.down)

    def update_camera(self, mat):
        """ カメラの座標にmatを掛けて更新する """
        self.proj = mat * self.proj
        self.renderer.screen_mat = self.proj * self.screen
        self.load_figure()

    def up(self, _):
        self.update_camera(self.Y_ADD)

    def down(self, _):
        self.update_camera(self.Y_SUB)

    def key_event(self, event):
        if event.char == "w":
            self.update_camera(self.Z_SUB)
        if event.char == "s":
            self.update_camera(self.Z_ADD)
        if event.char == "a":
            self.update_camera(self.X_ADD)
        if event.char == "d":
            self.update_camera(self.X_SUB)


r = FigureViewer3D(512, 512)
r.mainloop()
