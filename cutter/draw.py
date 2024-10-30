from reportlab.graphics import renderPDF
from reportlab.pdfgen.canvas import Canvas


def draw_sticker(
        canvas: Canvas, image,
        x, y,
        # text_label, text_sign
):
    # draw sticker
    renderPDF.draw(image, canvas, x, y)


def draw_hline_ref_points(canvas: Canvas, x1_cen, x2_cen, y_cen, radius):
    canvas.setFillColorCMYK(0.07, 0.03, 0.0, 0.13)
    canvas.circle(x_cen=x1_cen, y_cen=y_cen, r=radius, fill=1)
    canvas.circle(x_cen=x2_cen, y_cen=y_cen, r=radius, fill=1)
