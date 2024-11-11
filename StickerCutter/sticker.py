import numpy as np
import reportlab.pdfbase.pdfmetrics

from ezdxf import select
from ezdxf.layouts import Modelspace
from reportlab.graphics import renderPDF
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas
from svglib.svglib import svg2rlg

import ezdxf

pdfmetrics.registerFont(TTFont('Arial', 'arial.ttf'))


class Sticker:

    def __init__(
            self,
            # actual sticker sizes
            width, height,

            # paths to external files
            path_to_sticker,
            path_to_dxf,

            # information on the sticker
            text,
            inverted=False
    ):
        # read file with pic sticker
        self.image = svg2rlg(path_to_sticker)

        # work with dxf file
        self.doc_dxf = ezdxf.readfile(path_to_dxf)
        self.msp_dxf = self.doc_dxf.modelspace()

        self.width = width
        self.height = height
        self.text = text

        self.inverted = inverted

        # get entities and left-down point
        window = select.Window(
            (float("-inf"), float("-inf")),
            (float("inf"), float("inf"))
        )
        self.entities = select.bbox_outside(window, self.msp_dxf.entity_space.entities)     # elements in dxf file
        self.min_pt = None      # left-down point (using for draw dxf cutting file)
        for entity in self.entities:
            pt = np.min(np.array(entity.control_points), axis=0)
            if self.min_pt is None or np.all(pt < self.min_pt):
                self.min_pt = pt    # anchor point

    # function for draw in pdf

    def draw_sticker_pdf(self, canvas: Canvas, x, y, font_name="Arial", font_size=7,):
        canvas.setFillColorCMYK(0.03, 0.02, 0.03, 0)
        canvas.setFont(psfontname=font_name, size=font_size)
        # draw sticker
        renderPDF.draw(self.image, canvas, x, y)
        # draw text on sticker
        if self.text is not None:
            if self.inverted:
                canvas.saveState()

                canvas.translate(x + self.width - 0.5 * mm, y + self.height + 0.25 * mm)
                canvas.rotate(180)

                # draw text
                for t in self.text:
                    self.draw_text_pdf(canvas=canvas, x=t["x"], y=t["y"], text=t["text"], align=t["align"])

                canvas.restoreState()
            else:
                # draw text
                for t in self.text:
                    self.draw_text_pdf(canvas=canvas, x=x+t["x"], y=y+t["y"], text=t["text"], align=t["align"])

    def draw_text_pdf(self, canvas, x, y, text, align="center"):
        if align == "left":
            canvas.drawString(x, y, text)

        if align == "center":
            text_width = canvas.stringWidth(text)
            canvas.drawString(x + int((self.width - text_width)) / 2, y, text)

        if align == "right":
            canvas.drawRightString(x, y, text)

    # function for draw in dxf
    def draw_sticker_dxf(self, modelspace: Modelspace, x: float, y: float):
        # draw the cutting outline in dxf
        for entity in self.entities:
            cp_entity = entity.copy()
            cp_entity.translate(-self.min_pt[0] + x, -self.min_pt[1] + y, 0)
            modelspace.add_foreign_entity(cp_entity)


class RefPoint:
    def __init__(self, radius):
        pass

    def draw_ref_point_pdf(self, canvas: Canvas, x_cen, y_cen):
        pass

    def draw_ref_point_dxf(self, canvas: Canvas, x_cen, y_cen):
        pass


class Annotation:
    def __init__(self):
        pass

    def draw_annotation_pdf(self, canvas, x, y, text, font_name="Arial", font_size=9):
        str_width = reportlab.pdfbase.pdfmetrics.stringWidth(text, font_name, font_size)
        canvas.setFillColorCMYK(0.4, 0.4, 0.4, 1)
        canvas.setFont(psfontname=font_name, size=font_size)
        canvas.drawString(x - str_width / 2, y - font_size / 2, text)



