from ezdxf.layouts import Modelspace
from reportlab.graphics import renderPDF
from reportlab.pdfgen.canvas import Canvas


def draw_hline_ref_points(canvas: Canvas, x1_cen, x2_cen, y_cen, radius):
    canvas.setFillColorCMYK(0.07, 0.03, 0.0, 0.13)
    canvas.circle(x_cen=x1_cen, y_cen=y_cen, r=radius, fill=1)
    canvas.circle(x_cen=x2_cen, y_cen=y_cen, r=radius, fill=1)


def draw_hline_ref_points_dxf(modelspace: Modelspace, x1_cen, x2_cen, y_cen, radius):
    modelspace.add_circle(
        center=(x1_cen, y_cen),
        radius=radius,
    )
    modelspace.add_circle(
        center=(x2_cen, y_cen),
        radius=radius,
    )

