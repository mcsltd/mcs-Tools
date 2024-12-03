import json
import os
import datetime


from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from copy import deepcopy

from constants import RADIUS_REF_POINT
from stickers.create_pdf_dxf import create_pdf_dxf
from stickers.db25_var1.sticker import StickerDB25

pdfmetrics.registerFont(TTFont('Arial', 'arial.ttf'))
pdfmetrics.registerFont(TTFont('Arial-Bold', 'arialbd.ttf'))

PATH_TO_METADATA_DB25_VAR2 = r".\stickers\db25_var2\metadata.json"


def db25var2_create_pdf_dxf(input_file, sign):
    with open(PATH_TO_METADATA_DB25_VAR2, "r") as file:
        metadata = json.load(file)

    # создание шаблона
    template_stickers = []
    for stc in metadata["stickers"]:
        s = StickerDB25()
        for attr in stc.keys():
            if attr == "sn" and sign == "sn":
                setattr(s, "path_to_svg", stc[attr])
            if attr == "lot" and sign == "lot":
                setattr(s, "path_to_svg", stc[attr])
            if attr == "mm_width" or attr == "mm_height":
                setattr(s, attr, stc[attr] * mm)
            if attr == "dxf":
                setattr(s, "path_to_dxf", stc[attr])
            if attr == "inverted":
                setattr(s, attr, stc[attr])
            if attr == "labels":
                setattr(s, attr, stc[attr])
        template_stickers.append(deepcopy(s))

    # чтение данных и генерация стикеров
    with open(input_file, "r") as file:
        stickers = []
        ind_s = 0
        for data in file.readlines():

            if data == "\n":
                continue

            data = data.replace("\n", "").split(";")

            # the data must match the labels in the metadata
            if len(data) != len(template_stickers[ind_s].labels):
                raise Exception("The data does not match the settings.")

            s = deepcopy(template_stickers[ind_s])
            s.initialize()
            s.set_label(data)
            stickers.append(s)

            if ind_s == len(template_stickers) - 1:
                ind_s = 0
            else:
                ind_s += 1

    # create dir with time processing for saving the result
    name = datetime.datetime.now().isoformat()[:-7].replace('-', ' ').replace(':', '-')
    idx_sep = name.find("T")
    to_save = f"./output/{name[:idx_sep]} - {metadata['name']} {name[idx_sep:]}"
    if not os.path.exists(to_save):
        os.makedirs(to_save)

    if len(stickers) > 0:
        create_pdf_dxf(
            dx_inner=0.4,
            stickers=stickers,
            dx=-3 * mm, dy=1 * mm,
            x_pad=2 * RADIUS_REF_POINT + mm, y_pad=RADIUS_REF_POINT,
            dir_to_save=to_save, skip_dxf=False, skip_rpoints=False
        )


if __name__ == "__main__":
    db25var2_create_pdf_dxf(
        input_file=r"C:\Users\andmo\OneDrive\Desktop\my-dev-work\mcs-Tools\mcs_StickerCreator\input\db25_input_full_page.txt",
        sign="sn"
    )