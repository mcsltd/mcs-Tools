import reportlab.pdfbase.pdfmetrics
from reportlab.graphics import renderPDF
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas
from svglib.svglib import svg2rlg

import ezdxf

pdfmetrics.registerFont(TTFont('Arial', 'arial.ttf'))


class Sticker:

    def __init__(self, width, height, path_to_sticker, text, inverted=False):
        self.image = svg2rlg(path_to_sticker)

        self.width = width
        self.height = height
        self.text = text

        self.inverted = inverted

    # function for draw in pdf

    def draw_sticker_pdf(self, canvas: Canvas, x, y, font_name="Arial", font_size=7,):
        canvas.setFillColorCMYK(0.03, 0.02, 0.03, 0)
        canvas.setFont(psfontname=font_name, size=font_size)
        # draw sticker
        renderPDF.draw(self.image, canvas, x, y)
        if self.text is not None:

            if self.inverted:
                canvas.saveState()

                # ToDo: figure out - why are there offsets?
                canvas.translate(x + self.width - 0.5 * mm, y + self.height + 0.25 * mm)
                canvas.rotate(180)

                # draw text
                for t in self.text:
                    self.draw_text_pdf(canvas=canvas, x=t["x"], y=t["y"] , text=t["text"])

                canvas.restoreState()
            else:
                # draw text
                for t in self.text:
                    self.draw_text_pdf(canvas=canvas, x=x+t["x"], y=y+t["y"], text=t["text"])

    def draw_text_pdf(self, canvas, x, y, text):
        text_width = canvas.stringWidth(text)
        canvas.drawString(x + int((self.width - text_width)) / 2, y, text)

    # function for draw in dxf
    ...


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



