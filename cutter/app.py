from reportlab.lib.pagesizes import A3
from reportlab.lib.units import mm
from reportlab.pdfgen.canvas import Canvas

import svglib
from svglib.svglib import svg2rlg

from cutter import read_data
from cutter.draw import draw_sticker, draw_hline_ref_points
from cutter.read_data import read_txt


def main(
        # data for sticker
        path_to_sign, path_to_sticker,
        width_sticker, height_sticker,
        data, dx, dy,
        point_radius,
):
    pdf = Canvas("new.pdf", pagesize=A3)

    x, y = point_radius * 2 + mm, 2 * mm

    cnt_sticker = 1
    cnt_row = 1

    # read the svg file for draw in a pdf
    sticker_image = svg2rlg(path_to_sticker)
    m_sticker_image = svg2rlg("template/modify_sticker.svg")

    # draw two ref point in below
    draw_hline_ref_points(
        canvas=pdf,
        x1_cen=point_radius, x2_cen=A3[0]-point_radius, y_cen=point_radius,
        radius=point_radius
    )

    while cnt_sticker <= len(data):

        # check filling on x
        if x + width_sticker + 2 * point_radius > A3[0]:
            x = point_radius * 2 + mm
            y += height_sticker + dy

            # check filling on y
            if y + height_sticker > A3[1]:
                draw_hline_ref_points(
                    canvas=pdf,
                    x1_cen=point_radius, x2_cen=A3[0] - point_radius,
                    y_cen=cnt_row * height_sticker + (cnt_row - 1) * dy - point_radius,
                    radius=point_radius
                )  # draw line ref point in upstairs

                pdf.showPage()  # create new page

                cnt_row = 1
                x, y = point_radius * 2 + dx, 2 * mm
                # draw two ref point in below on new page
                draw_hline_ref_points(
                    canvas=pdf,
                    x1_cen=point_radius, x2_cen=A3[0] - point_radius, y_cen=point_radius,
                    radius=point_radius
                )
                continue
            cnt_row += 1

        if cnt_sticker % 2 == 0:
            draw_sticker(canvas=pdf, image=m_sticker_image, x=x+width_sticker, y=y-height_sticker)
        else:
            draw_sticker(canvas=pdf, image=sticker_image, x=x, y=y)

        x += width_sticker + dx
        cnt_sticker += 1

    if cnt_row > 1:
        draw_hline_ref_points(
            canvas=pdf,
            x1_cen=point_radius, x2_cen=A3[0] - point_radius,
            y_cen=cnt_row * height_sticker + (cnt_row - 1) * dy - point_radius,
            radius=point_radius
        )  # draw line ref point in upstairs

    pdf.save()


if __name__ == "__main__":
    path_to_sticker = "template/sticker.svg"
    path_to_sn = "template/sn.svg"
    path_to_lot = "template/lot.svg"

    path_to_data = "input/sample.txt"

    main(
        path_to_sign=path_to_sn,
        path_to_sticker=path_to_sticker,

        data=read_txt(path_to_data),
        dx=-7*mm, dy=2*mm, point_radius=3.5*mm,
        width_sticker=46*mm, height_sticker=28*mm,
    )



