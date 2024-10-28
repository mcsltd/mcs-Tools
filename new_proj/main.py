import os.path
from datetime import datetime

import ezdxf
import numpy as np
import argparse as ap

from ezdxf import select

from reportlab.lib.pagesizes import A3
from reportlab.lib.units import mm, cm
from reportlab.pdfgen.canvas import Canvas

from draw import draw_sticker, draw_center_text, draw_serial, draw_ref_circle, draw_lot
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

    x, y = X_PAD, Y_PAD     # for pdf file
    x_, y_ = 0, 0           # for dxf file

    number_sticker = 0
    number_row = 1

    while (A3[1] - y) > HEIGHT_STICKER:

        if number_sticker == len(data):
            break

        if WIDTH_STICKER > (A3[0] - x):
            x = X_PAD
            x_ = 0

            y += Y_DISTANCE + HEIGHT_STICKER
            y_ += (Y_DISTANCE + HEIGHT_STICKER) / mm

            number_row += 1
            continue

        draw_sticker(
            plot=c, x=x, y=y,
            path_to_stick=path_to_stick, height=HEIGHT_STICKER, width=WIDTH_STICKER
        )

        if number_sticker < len(data):
            draw_center_text(
                plot=c, x=x, y=y + 22 * mm, text=data[number_sticker][0], max_width=WIDTH_STICKER
            )

        if sign == "sn":
            draw_serial(plot=c, x=x, y=y, serial=data[number_sticker][1])
        if sign == "lot":
            draw_lot(plot=c, x=x, y=y, lot=data[number_sticker][1])

        for entity in entities:
            cp_entity = entity.copy()
            _ = cp_entity.translate(x_, y_, 0)
            new_msp.add_foreign_entity(cp_entity)

        x_ += (X_DISTANCE + WIDTH_STICKER) / mm
        x += X_DISTANCE + WIDTH_STICKER
        number_sticker += 1

    # down left circle in pdf
    draw_ref_circle(
        plot=c,
        x_cen=X_PAD - Y_DISTANCE - DIAMETER_POINT / 2,
        y_cen=Y_PAD + Y_DISTANCE + DIAMETER_POINT / 2,
        radius=DIAMETER_POINT / 2
    )
    # down left circle in dxf
    new_msp.add_circle(
        center=(
            min_pt[0] - (2 * Y_DISTANCE) / mm,
            min_pt[1] + (2 * Y_DISTANCE) / mm
        ),
        radius=DIAMETER_POINT / (2 * mm)
    )

    # down right circle in pdf
    draw_ref_circle(
        plot=c,
        x_cen=X_PAD + 6 * WIDTH_STICKER + 5 * X_DISTANCE + Y_DISTANCE + DIAMETER_POINT / 2,
        y_cen=Y_PAD + Y_DISTANCE + DIAMETER_POINT / 2,
        radius=DIAMETER_POINT / 2
    )
    # down right circle in dxf
    new_msp.add_circle(
        center=(
            min_pt[0] + (A3[0] - X_PAD - Y_DISTANCE) / mm,
            min_pt[1] + (2 * Y_DISTANCE) / mm
        ),
        radius=DIAMETER_POINT / (2 * mm)
    )

    if number_row > 1:
        # up left circle in pdf
        draw_ref_circle(
            plot=c,
            x_cen=X_PAD - Y_DISTANCE - DIAMETER_POINT / 2,
            y_cen=(HEIGHT_STICKER + Y_PAD) * (number_row - 1) + HEIGHT_STICKER - DIAMETER_POINT + Y_PAD,
            radius=DIAMETER_POINT / 2
        )
        # up left circle in dxf
        new_msp.add_circle(
            center=(
                min_pt[0] - (2 * Y_DISTANCE) / mm,
                min_pt[1] + ((HEIGHT_STICKER + Y_PAD) * (number_row - 1) + HEIGHT_STICKER - DIAMETER_POINT) / mm
            ),
            radius=DIAMETER_POINT / (2 * mm)
        )

        # up right circle in pdf
        draw_ref_circle(
            plot=c,
            x_cen=X_PAD + 6 * WIDTH_STICKER + 5 * X_DISTANCE + Y_DISTANCE + DIAMETER_POINT / 2,
            y_cen=(HEIGHT_STICKER + Y_PAD) * (number_row - 1) + HEIGHT_STICKER - DIAMETER_POINT + Y_PAD,
            radius=DIAMETER_POINT / 2,
        )
        # up right circle in dxf
        new_msp.add_circle(
            center=(
                min_pt[0] + (A3[0] - X_PAD - Y_DISTANCE) / mm,
                min_pt[1] + ((HEIGHT_STICKER + Y_PAD) * (number_row - 1) + HEIGHT_STICKER - DIAMETER_POINT) / mm
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
    parse = ap.ArgumentParser()
    parse.add_argument("file", type=str, help="Файл с данными для стикеров.")
    parse.add_argument("sign", type=str, help="Имя символа - SN, LOT.")
    args = parse.parse_args()

    sticker = "./template/sticker.jpg"
    cutout = "./template/counter.dxf"
    file_txt = args.file
    sign = args.sign.lower()

    try:
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
    except Exception as ex:
        print(f"Возникла ошибка обработки: {ex}")

