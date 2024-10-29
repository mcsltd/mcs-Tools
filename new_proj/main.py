import os.path
from datetime import datetime

import ezdxf
import numpy as np
import argparse as ap

from ezdxf import select

from reportlab.lib.pagesizes import A3
from reportlab.lib.units import mm, cm
from reportlab.pdfgen.canvas import Canvas

from draw_pdf import draw_sticker, draw_center_text, draw_serial, draw_lot, draw_ref_point_horizontal
from read_txt import read_txt

# sticker size
WIDTH_STICKER = 4.4 * cm
HEIGHT_STICKER = 2.645 * cm

# size of reference point
DIAMETER_POINT = 7 * mm

# indent sizes
X_DISTANCE = 2 * mm
Y_DISTANCE = 3 * mm

# size indent
X_PAD = 14 * mm
Y_PAD = 3 * mm


def main(
        path_to_stick: str,
        path_to_cutout: str,
        sign: str,
        path_to_save: str,
        data: list[list[str, str]],
):
    # read counter dxf
    doc = ezdxf.readfile(path_to_cutout)
    msp = doc.modelspace()

    # create new dxf
    new_doc = ezdxf.new(doc.dxfversion)
    new_msp = new_doc.modelspace()

    # get entities and left-down point
    window = select.Window(
        (float("-inf"), float("-inf")),
        (float("inf"), float("inf"))
    )
    entities = select.bbox_outside(window, msp.entity_space.entities)
    min_pt = None
    for entity in entities:
        pt = np.min(np.array(entity.control_points), axis=0)
        if min_pt is None or np.all(pt < min_pt):
            min_pt = pt

    # create pdf for drawing stickers
    c = Canvas(f"{path_to_save}/output.pdf", pagesize=A3)

    cnt_sticker = 0     # sticker counter in pdf
    cnt_page = 0        # page counter in pdf
    cnt_row = 1         # row counter in pdf
    max_cnt_col = 6     # max sticker column in pdf

    x, y = X_PAD, Y_PAD     # for pdf file
    x_, y_ = 0, 0           # for dxf file
    while cnt_sticker < len(data):

        # check for height filling
        if (A3[1] - y) < HEIGHT_STICKER:
            # draw a reference point in below of horizontally
            draw_ref_point_horizontal(
                plot=c,
                x_cen_1=X_PAD - Y_DISTANCE - DIAMETER_POINT / 2,
                x_cen_2=X_PAD + max_cnt_col * WIDTH_STICKER + (max_cnt_col - 1) * X_DISTANCE + Y_DISTANCE + DIAMETER_POINT / 2,
                y_cen=Y_PAD + Y_DISTANCE + DIAMETER_POINT / 2,
                radius=DIAMETER_POINT / 2
            )

            if cnt_row > 1:
                # draw a reference point in upper of horizontally
                draw_ref_point_horizontal(
                    plot=c,
                    x_cen_1=X_PAD - Y_DISTANCE - DIAMETER_POINT / 2,
                    x_cen_2=X_PAD + max_cnt_col * WIDTH_STICKER + (max_cnt_col - 1) * X_DISTANCE + Y_DISTANCE + DIAMETER_POINT / 2,
                    y_cen=(HEIGHT_STICKER + Y_PAD) * (cnt_row - 2) + HEIGHT_STICKER - DIAMETER_POINT + Y_PAD,
                    radius=DIAMETER_POINT / 2
                )

            c.showPage()            # create new page
            x, y = X_PAD, Y_PAD     # update current coordinates for new page in pdf
            x_, y_ = 0, 0           # update current coordinates for dxf
            cnt_row = 1

            cnt_page += 1

        # check for width filling
        if WIDTH_STICKER > (A3[0] - x):
            x = X_PAD
            x_ = 0
            y += Y_DISTANCE + HEIGHT_STICKER
            y_ += (Y_DISTANCE + HEIGHT_STICKER) / mm
            cnt_row += 1
            continue

        # draw the cutting outline in dxf
        for entity in entities:
            cp_entity = entity.copy()
            _ = cp_entity.translate(x_, y_, 0)
            new_msp.add_foreign_entity(cp_entity)

        draw_sticker(
            plot=c, x=x, y=y,
            path_to_stick=path_to_stick, height=HEIGHT_STICKER, width=WIDTH_STICKER
        )

        draw_center_text(
            plot=c, x=x, y=y + 22 * mm, text=data[cnt_sticker][0], max_width=WIDTH_STICKER
        )

        if sign == "sn":
            draw_serial(plot=c, x=x, y=y, serial=data[cnt_sticker][1])
        if sign == "lot":
            draw_lot(plot=c, x=x, y=y, lot=data[cnt_sticker][1])

        cnt_sticker += 1
        x_ += (X_DISTANCE + WIDTH_STICKER) / mm
        x += X_DISTANCE + WIDTH_STICKER

    # draw a reference point in below of horizontally
    draw_ref_point_horizontal(
        plot=c,
        x_cen_1=X_PAD - Y_DISTANCE - DIAMETER_POINT / 2,
        x_cen_2=X_PAD + 6 * WIDTH_STICKER + 5 * X_DISTANCE + Y_DISTANCE + DIAMETER_POINT / 2,
        y_cen=Y_PAD + Y_DISTANCE + DIAMETER_POINT / 2,
        radius=DIAMETER_POINT / 2)

    new_msp.add_circle(
        center=(
            min_pt[0] - (2 * Y_DISTANCE + 0.5 * mm) / mm,
            min_pt[1] + (2 * Y_DISTANCE - 0.5 * mm) / mm
        ),
        radius=DIAMETER_POINT / (2 * mm)
    )

    new_msp.add_circle(
        center=(
            min_pt[0] + (A3[0] - X_PAD - Y_DISTANCE + 0.5 * mm) / mm,
            min_pt[1] + (2 * Y_DISTANCE - 0.5 * mm) / mm
        ),
        radius=DIAMETER_POINT / (2 * mm)
    )

    if cnt_row > 1:
        # draw a reference point in upper of horizontally
        draw_ref_point_horizontal(
            plot=c,
            x_cen_1=X_PAD - Y_DISTANCE - DIAMETER_POINT / 2,
            x_cen_2=X_PAD + 6 * WIDTH_STICKER + 5 * X_DISTANCE + Y_DISTANCE + DIAMETER_POINT / 2,
            y_cen=(HEIGHT_STICKER + Y_PAD) * (cnt_row - 1) + HEIGHT_STICKER - DIAMETER_POINT + Y_PAD,
            radius=DIAMETER_POINT / 2
        )

        new_msp.add_circle(
            center=(
                min_pt[0] - (2 * Y_DISTANCE + 0.5 * mm) / mm,
                min_pt[1] + ((HEIGHT_STICKER + Y_PAD) * (cnt_row - 1) + HEIGHT_STICKER - DIAMETER_POINT) / mm
            ),
            radius=DIAMETER_POINT / (2 * mm)
        )

        new_msp.add_circle(
            center=(
                min_pt[0] + (A3[0] - X_PAD - Y_DISTANCE) / mm,
                min_pt[1] + ((HEIGHT_STICKER + Y_PAD) * (cnt_row - 1) + HEIGHT_STICKER - DIAMETER_POINT) / mm
            ),
            radius=DIAMETER_POINT / 2 / mm
        )

    # save pdf with stickers
    c.save()
    # save dxf file
    new_doc.saveas(f"{path_to_save}/output.dxf")

    print(f"Программа успешно отработала.\n"
          f"Сгенерированы 2 файла \"output.dxf\" и \"output.pdf\" в папку {path_to_save}.")


if __name__ == "__main__":
    parse = ap.ArgumentParser(description="Программа для генерации pdf и dxf файлов для резки стикеров.")
    parse.add_argument("-f", "--file", type=str, help="Файл с данными для стикеров.")
    parse.add_argument("-s", "--sign", type=str, help="Имя символа - SN, LOT.")
    args = parse.parse_args()

    sticker = "./template/sticker.jpg"
    cutout = "./template/cut_contour.dxf"
    file_txt = "./input/sample.txt"
        # args.file
    sign = "sn"
        # args.sign.lower()

    # try:
    if not os.path.exists(sticker):
        raise Exception("Sticker file not found.")

    if not os.path.exists(cutout):
        raise Exception("Cutout .dxf file not found.")

    if not os.path.exists(file_txt):
        raise Exception("TXT file with sticker data not found.")

    if sign not in ["lot", "sn"]:
        raise Exception("An incorrect value was passed to the sign parameter. Should be \'sn\' or \'lot\'")

    stickers_data = read_txt(path_to_txt=file_txt)

    path_to_save = f"output_{datetime.now().isoformat().replace(':', '-')[:-7]}"
    os.mkdir(path=f"{path_to_save}")

    main(
        path_to_save=path_to_save,
        path_to_stick=sticker,
        sign=sign,
        path_to_cutout=cutout,
        data=stickers_data
    )
    # except Exception as ex:
    #     print(f"Возникла ошибка обработки: {ex}")

