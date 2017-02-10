# -*- coding: utf-8 -*-
""" 図形描画のテスト """
import os
import random
from PIL import Image
from Figure import Line, Point, Diamond
from JPGPainter import JPGPainter

width, height = 4096, 4096
center = [width / 2, height / 2]


def draw(img: Image.Image):
    """ 図形描画本体 """
    white = 50.0
    lines = [Line(Point(white, white), Point(white, height - white)),
             Line(Point(white, white), Point(width - white, white)),
             Line(Point(width - white, height - white), Point(width - white, white)),
             Line(Point(width - white, height - white), Point(white, height - white))]
    p = JPGPainter(img)
    for l in lines:
        p.draw(l)
    p.draw(Diamond(Point(center[0], center[1]), min(width, height) / 2, 16, lambda t: [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]))


def prompt() -> None:
    """ メイン処理 """
    filename = os.path.join("test", "generated__image")
    if not os.path.exists("test"):
        os.mkdir("test")

    # JPGPainter
    img = Image.new("RGB", (width + 1, height + 1), "white")
    draw(img)
    img.save(filename + ".bmp")
    os.startfile(filename + ".bmp")

if __name__ == "__main__":
    prompt()
