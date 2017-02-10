# -*- coding: utf-8 -*-
""" 図形描画のテスト """
import os

from PIL import Image

from Figure import Line, Point, Diamond
from JPGPainter import JPGPainter


def draw(img: Image.Image):
    """ 図形描画本体 """
    lines = [Line(Point(1.0, 1.0), Point(1.0, 511.0)),
             Line(Point(1.0, 1.0), Point(511.0, 1.0)),
             Line(Point(511.0, 511.0), Point(511.0, 1.0)),
             Line(Point(511.0, 511.0), Point(1.0, 511.0))]
    p = JPGPainter(img)
    for l in lines:
        p.draw(l)
    p.draw(Diamond(Point(256.0, 256.0), 200.0, 16))


def prompt() -> None:
    """ メイン処理 """
    filename = os.path.join("test", "generated__image")
    if not os.path.exists("test"):
        os.mkdir("test")

    # JPGPainter
    width, height = 512, 512
    img = Image.new("RGB", (width + 1, height + 1), "white")
    draw(img)
    img.save(filename + ".jpg")
    os.startfile(filename + ".jpg")

if __name__ == "__main__":
    prompt()
