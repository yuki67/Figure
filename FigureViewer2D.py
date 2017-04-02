""" tkinterのクラスを自分が使いやすい様に改造したもの """
import time
import os
from FigureViewer import FigureViewer, RendererTk
from MyMatrix import Matrix


class FigureViewer2D(FigureViewer):

    def __init__(self, width, height):
        mat = Matrix.affine2D(scale=[width, height], trans=[self.SPACE, self.SPACE]) * \
            Matrix.affine2D(center=[0.0, height / 2 + self.SPACE], swap=[0, 1])
        super().__init__(width, height, mat, "Gallery2D", "FigureViewer2D")


r = FigureViewer2D(512, 512)
r.mainloop()
