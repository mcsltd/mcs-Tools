from reportlab.lib.units import mm
from reportlab.pdfgen.canvas import Canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

pdfmetrics.registerFont(TTFont('Arial', 'arial.ttf'))


def draw_sticker(plot: Canvas, path_to_stick, x, y, width, height):
    plot.drawImage(
        image=path_to_stick,
        x=x, y=y,
        width=width, height=height,
        preserveAspectRatio=True
    )


def draw_serial(plot: Canvas, x: int, y: int, serial: str):
    plot.setFillColorCMYK(0.03, 0.02, 0.03, 0)
    plot.setFont(psfontname='Arial', size=7)
    plot.setLineWidth(width=7)
    plot.drawString(x + 15.75 * mm, y + 10.5 * mm, "SN")
    plot.drawString(x + 22 * mm, y + 10.5 * mm, serial)
    plot.setLineWidth(width=1)


def draw_lot(plot: Canvas, x: int, y: int, lot: str):
    plot.setFillColorCMYK(0.03, 0.02, 0.03, 0)
    plot.setFont(psfontname='Arial', size=7)
    plot.setLineWidth(width=7)
    plot.drawString(x + 15 * mm, y + 10.5 * mm, "LOT")
    plot.drawString(x + 22 * mm, y + 10.5 * mm, lot)
    plot.setLineWidth(width=1)


def draw_center_text(
        plot: Canvas,
        x: int, y: int,
        text: str, max_width: int,
        font_name: str = "Arial", font_size=7,
        line_spacing=3 * mm
):
    plot.setFillColorCMYK(0.03, 0.02, 0.03, 0)
    text = text.split(sep="\n")

    for t in text:
        text_width = plot.stringWidth(t, font_name, font_size)
        plot.setFont(psfontname='Arial', size=7)
        plot.drawString(x + int((max_width - text_width)) / 2, y, t)
        y -= line_spacing


def draw_ref_circle(plot: Canvas, x_cen, y_cen, radius):
    plot.setFillColorCMYK(0.07, 0.03, 0.0, 0.13)
    plot.circle(
        x_cen=x_cen,
        y_cen=y_cen,
        r=radius,
        fill=1
    )


def draw_ref_point_horizontal(plot: Canvas, x_cen_1, x_cen_2, y_cen, radius):
    draw_ref_circle(plot=plot, x_cen=x_cen_1, y_cen=y_cen, radius=radius)
    draw_ref_circle(plot=plot, x_cen=x_cen_2, y_cen=y_cen, radius=radius)
