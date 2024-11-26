import datetime
import json
import os
from copy import deepcopy

import ezdxf
import numpy as np
from ezdxf import select
from reportlab.graphics import renderPDF
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas

from mcs_StickerCreator._svglib.svglib.svglib import svg2rlg
from mcs_StickerCreator.stickers.create_pdf_dxf import create_pdf_dxf

PATH_TO_METADATA_KEL50 = r"C:\Users\andmo\OneDrive\Desktop\my-dev-work\mcs-Tools\mcs_StickerCreator\stickers\kel50\metadata.json"


pdfmetrics.registerFont(TTFont('Arial', 'arial.ttf'))
pdfmetrics.registerFont(TTFont('Arial-Bold', 'arialbd.ttf'))


class StickerKel50:

    def __init__(
            self,
            # actual sticker sizes
            mm_width: float = None, mm_height: float = None,

            # paths to external files
            path_to_svg: str = None,
            path_to_dxf: str = None,

            # information on the sticker
            text: list[dict] = None,
            inverted: bool = None
    ):

        self.path_to_svg = path_to_svg
        self.path_to_dxf = path_to_dxf

        self.mm_width = mm_width
        self.mm_height = mm_height

        self.labels = text
        self.inverted = inverted

    def set_label(self, data: list[str]):
        for label, text in zip(self.labels, data):
            if text != "":
                label["text"] = text
                label["mm_x"] = label["mm_x"] * mm
                label["mm_y"] = label["mm_y"] * mm

    def initialize(self):
        # read file with pic sticker
        self.image = svg2rlg(self.path_to_svg)

        if self.path_to_dxf:
            # work with dxf file
            self.doc_dxf = ezdxf.readfile(self.path_to_dxf)
            self.msp_dxf = self.doc_dxf.modelspace()

            # get entities and left-down point
            window = select.Window(
                (float("-inf"), float("-inf")),
                (float("inf"), float("inf"))
            )

            self.entities = select.bbox_outside(window, self.msp_dxf.entity_space.entities)  # elements in dxf file
            self.min_pt = None  # left-down point (using for draw dxf cutting file)
            for entity in self.entities:
                pt = np.min(np.array(entity.control_points), axis=0)
                if self.min_pt is None or np.all(pt < self.min_pt):
                    self.min_pt = pt  # anchor point

    # function for draw in pdf
    def draw_sticker_pdf(
            self,
            canvas: Canvas,
            x: float, y: float,
    ) -> None:

        # draw sticker
        renderPDF.draw(self.image, canvas, x, y)
        # draw text on sticker
        if self.labels is not None:
            if self.inverted:
                canvas.saveState()

                canvas.translate(x + self.mm_width - 0.5 * mm, y + self.mm_height + 0.25 * mm)
                canvas.rotate(180)

                # draw text
                for t in self.labels:
                    self.draw_text_pdf(
                        canvas=canvas,
                        x=x + t["mm_x"], y=y + t["mm_y"],
                        text=t["text"], font_name=t["font"], size=t["size"],
                        align=t["align"])

                canvas.restoreState()
            else:
                # draw text
                for t in self.labels:
                    self.draw_text_pdf(
                        canvas=canvas,
                        x=x + t["mm_x"], y=y + t["mm_y"],
                        text=t["text"], font_name=t["font"], size=t["size"],
                        align=t["align"])

    def draw_text_pdf(
            self, canvas: Canvas,
            x: float, y: float,
            text: str,
            font_name: str = "Arial", size: int = 7,
            align: int = "center"):

        canvas.setFillColorCMYK(0.03, 0.02, 0.03, 0)
        # canvas.setFillColorCMYK(0.4, 0.4, 0.4, 1)

        canvas.setFont(psfontname=font_name, size=size)

        if align == "left":
            canvas.drawString(x, y, text)

        if align == "center":
            text_width = canvas.stringWidth(text=text, fontName=font_name, fontSize=size)
            canvas.drawString(x + int((self.mm_width - text_width)) / 2, y, text)

        if align == "right":
            canvas.drawRightString(x, y, text)


def kel50_create_pdf(input_file, sign="sn"):
    with open(PATH_TO_METADATA_KEL50, "r") as file:
        metadata = json.load(file)

    # создание шаблона
    template_stickers = []
    for stc in metadata["stickers"]:
        s = StickerKel50()
        for attr in stc.keys():
            if attr == "sn" and sign == "sn":
                setattr(s, "path_to_svg", stc[attr])
            if attr == "lot" and sign == "lot":
                setattr(s, "path_to_svg", stc[attr])
            if attr == "mm_width" or attr == "mm_height":
                setattr(s, attr, stc[attr] * mm)
            if attr == "dxf":
                setattr(s, "path_to_dxf", stc[attr])
            if attr == "inverted":
                setattr(s, attr, stc[attr])
            if attr == "labels":
                setattr(s, attr, stc[attr])
        template_stickers.append(deepcopy(s))

    # чтение данных и генерация стикеров
    with open(input_file, "r") as file:
        stickers = []
        ind_s = 0
        for data in file.readlines():

            if data == "\n":
                continue

            data = data.replace("\n", "").split(";")
            s = deepcopy(template_stickers[ind_s])
            s.initialize()
            s.set_label(data)
            stickers.append(s)

            if ind_s == len(template_stickers) - 1:
                ind_s = 0
            else:
                ind_s += 1

    # create dir with time processing for saving the result
    to_save = f"./output/kel50_{datetime.datetime.now().isoformat()[:-7].replace('-', ' ').replace(':', '-')}"
    if not os.path.exists(to_save):
        os.makedirs(to_save)

    if len(stickers) > 0:
        create_pdf_dxf(
            stickers=stickers,
            dx=10 * mm, dy=10 * mm,
            x_pad=27 * mm, y_pad=16 * mm,
            dir_to_save=to_save, annotation=None
        )


if __name__ == "__main__":
    kel50_create_pdf(input_file="input.txt")

