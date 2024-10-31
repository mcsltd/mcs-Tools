from reportlab.lib.pagesizes import A3
from reportlab.lib.units import cm, mm

WIDTH_STICKER = 4.4 * cm
HEIGHT_STICKER = 2.645 * cm

from reportlab.graphics import renderPDF
from reportlab.pdfgen import canvas
from svglib.svglib import svg2rlg


def scale(drawing, scaling_factor):
    """
    Scale a reportlab.graphics.shapes.Drawing()
    object while maintaining the aspect ratio
    """
    scaling_x = scaling_factor
    scaling_y = scaling_factor

    drawing.width = drawing.minWidth() * scaling_x
    drawing.height = drawing.height * scaling_y
    drawing.scale(scaling_x, scaling_y)
    return drawing


def add_image(image_path, scaling_factor):
    my_canvas = canvas.Canvas('svg_scaled_on_canvas.pdf', pagesize=A3)
    y, x = 0, 0
    for ind in range(1, 8):
        drawing = svg2rlg(image_path)
        scaled_drawing = scale(drawing, scaling_factor=scaling_factor)
        if ind % 2 == 0:
            scaled_drawing.rotate(180)
            renderPDF.draw(scaled_drawing, my_canvas, x, y + HEIGHT_STICKER)
            x += -5 * mm
        else:
            renderPDF.draw(scaled_drawing, my_canvas, x, y)
            x += 2 * WIDTH_STICKER - 5 * mm
        y = 0
        # my_canvas.drawString(50, 30, 'My SVG Image')
    my_canvas.save()


if __name__ == '__main__':
    image_path = 'template/sticker.svg'
    add_image(image_path, scaling_factor=1)