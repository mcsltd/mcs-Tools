import datetime
import os.path
import logging
import ezdxf

from reportlab.lib.pagesizes import A3
from reportlab.lib.units import mm
from reportlab.pdfgen.canvas import Canvas

from StickerCutter.sticker import Sticker, Annotation
from StickerCutter.draw import draw_hline_ref_points, draw_hline_ref_points_dxf
from StickerCutter.read_data import read_txt

logging.basicConfig(level=logging.INFO)


def main(
        stickers,
        dx, dy,
        point_radius,
        dir_to_save,
        annotation="TASK_0001",
):
    # new pdf file
    pdf = Canvas(f"{dir_to_save}/output.pdf", pagesize=A3)

    # new dxf file
    dxf = ezdxf.new(stickers[0].doc_dxf.dxfversion)
    msp = dxf.modelspace()

    # pad for draw annotate
    x_pad, y_pad = 2 * point_radius + mm, point_radius
    x, y = x_pad, y_pad

    ind_sticker = 0
    cnt_row = 1

    # draw two ref point in below
    draw_hline_ref_points(
        canvas=pdf,
        x1_cen=point_radius, x2_cen=A3[0] - point_radius,
        y_cen=point_radius,  # problem with draw?
        radius=point_radius,
    )

    # offsets for the contour in the dxf file
    dx_inner, dy_inner = 0.49, 0.52
    # initial coordinates for sticker outlines
    x_, y_ = x_pad / mm + dx_inner, y_pad / mm + dy_inner

    # draw two ref point in below in pdf file
    draw_hline_ref_points_dxf(
        modelspace=msp,
        x1_cen=point_radius / mm, x2_cen=(A3[0] - point_radius) / mm,
        y_cen=point_radius / mm,
        radius=point_radius / mm,
    )

    cnt_page = 1
    annotation += " " + datetime.datetime.now().isoformat()[:-7].replace("T", " ")

    # draw annotation
    Annotation().draw_annotation_pdf(
        canvas=pdf, x=A3[0] / 2, y=point_radius / 2, text=annotation + f" PAGE {cnt_page}")

    logging.info(f"Drawing stickers on the page: {cnt_page}.")

    while ind_sticker < len(stickers):

        # check filling on x and y
        if x + stickers[ind_sticker].width + x_pad > A3[0]:
            # carriage return to new line (pfd)
            x = x_pad
            y += stickers[ind_sticker].height + dy

            # carriage return to new line (dxf)
            x_ = x_pad / mm + dx_inner
            y_ += (stickers[ind_sticker].height + dy) / mm

            # check filling on y
            if y + stickers[ind_sticker].height + y_pad > A3[1]:
                draw_hline_ref_points(
                    canvas=pdf,
                    x1_cen=point_radius, x2_cen=A3[0] - point_radius,
                    y_cen=cnt_row * stickers[ind_sticker].height + (cnt_row - 1) * dy - point_radius,
                    radius=point_radius
                )  # draw line ref point in upstairs (pdf)

                # draw annotation upstairs
                Annotation().draw_annotation_pdf(
                    canvas=pdf,
                    x=A3[0] / 2, y=cnt_row * stickers[ind_sticker - 1].height + cnt_row * dy + y_pad + 2 * mm,
                    text=annotation + f" PAGE {cnt_page}"
                )

                pdf.showPage()  # create new page
                cnt_page += 1

                logging.info(f"Drawing stickers on the page: {cnt_page}.")

                # draw annotation below
                Annotation().draw_annotation_pdf(
                    canvas=pdf, x=A3[0] / 2, y=point_radius / 2, text=annotation + f" PAGE {cnt_page}")

                cnt_row = 1
                y = y_pad
                # draw two ref point in below
                draw_hline_ref_points(
                    canvas=pdf,
                    x1_cen=point_radius, x2_cen=A3[0] - point_radius,
                    y_cen=point_radius,  # problem with draw?
                    radius=point_radius,
                )
                continue
            cnt_row += 1

        # draw stickers
        stickers[ind_sticker].draw_sticker_pdf(canvas=pdf, x=x, y=y)
        stickers[ind_sticker].draw_sticker_dxf(modelspace=msp, x=x_ + dx_inner, y=y_ + dy_inner)

        x += stickers[ind_sticker].width + dx                           # pdf file
        x_ += (stickers[ind_sticker].width + dx) / mm        # dxf file
        ind_sticker += 1

    if cnt_row > 1:
        draw_hline_ref_points(
            canvas=pdf,
            x1_cen=point_radius, x2_cen=A3[0] - point_radius,
            y_cen=cnt_row * stickers[ind_sticker - 1].height + (cnt_row - 1) * dy - point_radius,
            radius=point_radius
        )  # draw line ref point in upstairs
        draw_hline_ref_points_dxf(
            modelspace=msp, x1_cen=point_radius / mm, x2_cen=(A3[0] - point_radius) / mm,
            y_cen=(cnt_row * stickers[ind_sticker - 1].height + (cnt_row - 1) * dy - point_radius) / mm,
            radius=point_radius / mm
        )

    # add annotation upstairs
    Annotation().draw_annotation_pdf(
        canvas=pdf,
        x=A3[0] / 2, y=cnt_row * stickers[ind_sticker - 1].height + cnt_row * dy + y_pad + 2 * mm,
        text=annotation + f" PAGE {cnt_page}"
    )

    if ind_sticker == len(stickers):
        logging.info(f"The program worked well. Number of drawn stickers: {ind_sticker}."
                     f" Total number of stickers: {len(stickers)}")
        logging.info(f"The result is saved to file: {dir_to_save}/output.pdf.")
        logging.info(f"Сutting file saved in {dir_to_save}/output.dxf.")
    else:
        logging.error(f"The number of stickers drawn does not correspond to the number of transferred ones.")

    pdf.save()
    dxf.saveas(f"{dir_to_save}/output.dxf")


if __name__ == "__main__":
    # create dir with time processing for saving the result
    to_save = f"./output/{datetime.datetime.now().isoformat()[:-7].replace(':', '-')}"
    if not os.path.exists(to_save):
        os.makedirs(to_save)
        logging.info(f"A directory has been created for saving files with stickers: {to_save}")

    # read data for stickers
    text = read_txt("./input/sample.txt")
    if len(text) == 0:
        logging.warning(f"Data file is empty.")

    logging.info(f"The data file has been read. Total stickers: {len(text)}.")

    sticks = []
    cnt = 1
    for t in text:
        if cnt % 2 == 0:
            sticks.append(Sticker(
                path_to_sticker="template/combo sn reverse.svg",
                path_to_dxf="template/sticker_reverse.dxf",
                width=46 * mm, height=28 * mm,
                text=[
                    {"text": t[0], "x": 0, "y": 24 * mm}, {"text": t[1], "x": 0, "y": 21 * mm},
                    {"text": t[2], "x": 0, "y": 18 * mm},
                    {"text": t[3], "x": 4 * mm, "y": 11.5 * mm}     # ToDo: place text on sticker without alignment
                ],
                inverted=True)
            )
        else:
            sticks.append(Sticker(
                path_to_sticker="template/combo sn.svg",
                path_to_dxf="template/sticker.dxf",
                width=46 * mm, height=28 * mm,
                text=[
                    {"text": t[0], "x": 0, "y": 24 * mm}, {"text": t[1], "x": 0, "y": 21 * mm},
                    {"text": t[2], "x": 0, "y": 18 * mm},
                    {"text": t[3], "x": 4 * mm, "y": 11.5 * mm}     # ToDo: place text on sticker without alignment
                ])
            )
        cnt += 1

    if len(sticks) > 0:
        logging.info("Start program...")
        main(
            stickers=sticks,
            dx=-7 * mm,
            dy=1 * mm,
            point_radius=3.5 * mm,
            dir_to_save=to_save,
        )
    else:
        logging.info("Empty file data. Stop program.")
