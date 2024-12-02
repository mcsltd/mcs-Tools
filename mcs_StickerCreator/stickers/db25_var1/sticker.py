import ezdxf
import numpy as np
import reportlab
from ezdxf import select
from ezdxf.layouts import Modelspace
from reportlab.graphics import renderPDF
from reportlab.lib.units import mm
from reportlab.pdfgen.canvas import Canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from mcs_StickerCreator._svglib.svglib.svglib import svg2rlg


pdfmetrics.registerFont(TTFont('Arial', 'arial.ttf'))
pdfmetrics.registerFont(TTFont('Arial-Bold', 'arialbd.ttf'))

class StickerDB25:

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
            font_name: str = "Arial",
            font_size: int = 7
    ) -> None:

        canvas.setFillColorCMYK(0.03, 0.02, 0.03, 0)
        canvas.setFont(psfontname=font_name, size=font_size)
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
                    self.draw_text_pdf(canvas=canvas, x=t["mm_x"], y=t["mm_y"], text=t["text"], align=t["align"])

                canvas.restoreState()
            else:
                # draw text
                for t in self.labels:
                    self.draw_text_pdf(canvas=canvas, x=x + t["mm_x"], y=y + t["mm_y"], text=t["text"], align=t["align"])

    def draw_text_pdf(self, canvas: Canvas, x: float, y: float, text: str, align: int = "center"):
        if align == "left":
            canvas.drawString(x, y, text)

        if align == "center":
            text_width = canvas.stringWidth(text)
            canvas.drawString(x + int((self.mm_width - text_width)) / 2, y, text)

        if align == "right":
            canvas.drawRightString(x, y, text)

    # function for draw in dxf
    def draw_sticker_dxf(self, modelspace: Modelspace, x: float, y: float):
        # draw the cutting outline in dxf
        for entity in self.entities:
            cp_entity = entity.copy()
            cp_entity.translate(-self.min_pt[0] + x, -self.min_pt[1] + y, 0)
            modelspace.add_foreign_entity(cp_entity)



class Annotation:
    def __init__(self):
        pass

    def draw_annotation_pdf(
            self, canvas: Canvas,
            x: float, y: float, text: str, font_name: float = "Arial", font_size: int = 9) -> None:
        str_width = reportlab.pdfbase.pdfmetrics.stringWidth(text, font_name, font_size)
        canvas.setFillColorCMYK(0.4, 0.4, 0.4, 1)
        canvas.setFont(psfontname=font_name, size=font_size)
        canvas.drawString(x - str_width / 2, y - font_size / 2, text)