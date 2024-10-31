from reportlab.lib.pagesizes import A3
from reportlab.lib.units import mm
from reportlab.pdfgen.canvas import Canvas

import svglib
from svglib.svglib import svg2rlg

from cutter import read_data
from cutter.sticker import Sticker, Annotation
from cutter.draw import draw_sticker, draw_hline_ref_points
from cutter.read_data import read_txt


def main(
        stickers,
        dx, dy,
        point_radius,
        annotation="TASK_0001 PAGE 1"
):
    # new pdf file
    pdf = Canvas("output.pdf", pagesize=A3)
    # new dxf file
    ...

    x, y = point_radius * 2 + mm, 2 * mm

    ind_sticker = 0
    cnt_row = 1

    # draw two ref point in below
    draw_hline_ref_points(
        canvas=pdf,
        x1_cen=point_radius, x2_cen=A3[0]-point_radius, y_cen=point_radius,
        radius=point_radius
    )
    Annotation().draw_annotation_pdf(canvas=pdf, x=point_radius, y=A3[1]/2, text=annotation)
    while ind_sticker < len(stickers):

        # check filling on x
        if x + stickers[ind_sticker].width + 2 * point_radius > A3[0]:
            x = point_radius * 2 + mm
            y += stickers[ind_sticker].height + dy

            # check filling on y
            if y + stickers[ind_sticker].height > A3[1]:
                draw_hline_ref_points(
                    canvas=pdf,
                    x1_cen=point_radius, x2_cen=A3[0] - point_radius,
                    y_cen=cnt_row * stickers[ind_sticker].height + (cnt_row - 1) * dy - point_radius,
                    radius=point_radius
                )  # draw line ref point in upstairs

                pdf.showPage()  # create new page

                cnt_row = 1
                x, y = point_radius * 2 + mm, 2 * mm
                # draw two ref point in below on new page
                draw_hline_ref_points(
                    canvas=pdf,
                    x1_cen=point_radius, x2_cen=A3[0] - point_radius, y_cen=point_radius,
                    radius=point_radius
                )
                continue
            cnt_row += 1

        stickers[ind_sticker].draw_sticker_pdf(canvas=pdf, x=x, y=y)

        x += stickers[ind_sticker].width + dx
        ind_sticker += 1

    if cnt_row > 1:
        draw_hline_ref_points(
            canvas=pdf,
            x1_cen=point_radius, x2_cen=A3[0] - point_radius,
            y_cen=cnt_row * stickers[ind_sticker - 1].height + (cnt_row - 1) * dy - point_radius,
            radius=point_radius
        )  # draw line ref point in upstairs

    pdf.save()


if __name__ == "__main__":
    paths_to_sticker = ["template/sticker_sn.svg", "template/reverse_sticker_sn.svg"]
    path_to_sn = "template/sn.svg"
    path_to_lot = "template/lot.svg"

    path_to_data = "input/sample.txt"

    # example for read data
    # t = {"text": ..., "x": ..., "y": ..., "rotate": True, }
    # text = [
    #     {"text": "MCScap PROFESSIONAL, L,\n Mod: 15E-03M25\n mks.ru\n", "x": 132, "y": "fsdf", "rotate": 1},
    #     {"text": "24123", "x":123, "y": 234}
    # ]

    # read data for stickers
    text = read_txt("input/sample.txt")

    sticks = []
    cnt = 1
    for t in text:
        if cnt % 2 == 0:

            sticks.append(Sticker(
                path_to_sticker="template/reverse_sticker_sn.svg",
                path_to_dxf="template/reverse_sticker.dxf",
                width=46 * mm, height=28 * mm,
                text=[
                        {"text": t[0], "x": 0, "y": 24*mm,},
                        {"text": t[1], "x": 0, "y": 21*mm,},
                        {"text": t[2], "x": 0, "y": 18*mm,},
                        {"text": t[3], "x": 2.5*mm, "y": 11.5*mm,}
                    ],
                inverted=True)
            )
        else:
            sticks.append(Sticker(
                path_to_sticker="template/sticker_sn.svg",
                path_to_dxf="template/reverse_sticker.dxf",
                width=46 * mm, height=28 * mm,
                text=[
                        {"text": t[0], "x": 0, "y": 24*mm,},
                        {"text": t[1], "x": 0, "y": 21*mm,},
                        {"text": t[2], "x": 0, "y": 18*mm,},
                        {"text": t[3], "x": 2.5*mm, "y": 11.5*mm,}
                    ])
            )
        cnt += 1

    main(
        stickers=sticks,
        dx=-7*mm,
        dy=2*mm,
        point_radius=3.5*mm,
    )



