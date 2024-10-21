from reportlab.lib.pagesizes import A3
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas

WIDTH_STICKER = 44 * mm
HEIGHT_STICKER = 26.45 * mm

# DPI = 198
# WIDTH_STICKER = 4.4 / 2.54 * DPI
# HEIGHT_STICKER = 2.645 / 2.54 * DPI

DIAMETER_POINT = 7 * mm

X_DISTANCE = 2 * mm
Y_DISTANCE = X_DISTANCE * 2


def read_xls(path_to_xls):
    template = {
        "names": [],
        "numbers": [],
        "serial": []
    }
    return template


def draw_stickers(plot, string, path_to_stick):
    pass

def create_stickers(
        path_to_stick: str,
        num_stickers: int,
        path_to_save: str | None,
):
    c = canvas.Canvas(path_to_save, pagesize=A3)

    # draw reference points
    c.setFillColorCMYK(0.07, 0.03, 0.0, 0.13)
    c.circle(
        x_cen=2 * X_DISTANCE + DIAMETER_POINT // 2,
        y_cen=2 * X_DISTANCE + DIAMETER_POINT,
        r=DIAMETER_POINT // 2, fill=1)
    c.circle(
        x_cen=11 * X_DISTANCE + DIAMETER_POINT + 6 * WIDTH_STICKER,
        y_cen=2 * X_DISTANCE + DIAMETER_POINT,
        r=DIAMETER_POINT // 2, fill=1)

    max_cnt_rows = num_stickers // 6
    if max_cnt_rows != 0:

        c.circle(
            x_cen=2 * X_DISTANCE + DIAMETER_POINT // 2,
            y_cen=2 * X_DISTANCE + 2 * DIAMETER_POINT + max_cnt_rows * (3 * X_DISTANCE + HEIGHT_STICKER),
            r=DIAMETER_POINT // 2, fill=1)

        c.circle(
            x_cen=11 * X_DISTANCE + DIAMETER_POINT + 6 * WIDTH_STICKER,
            y_cen=2 * X_DISTANCE + 2 * DIAMETER_POINT + max_cnt_rows * (3 * X_DISTANCE + HEIGHT_STICKER),
            r=DIAMETER_POINT // 2, fill=1)

    # draw stickers
    x, y = 4 * X_DISTANCE + DIAMETER_POINT, Y_DISTANCE
    for idx in range(max_cnt_rows):
        for idj in range(6):
            c.drawImage(image=path_to_stick, x=x, y=y, width=WIDTH_STICKER, height=HEIGHT_STICKER)
            x += X_DISTANCE + WIDTH_STICKER
        x = 4 * X_DISTANCE + DIAMETER_POINT
        y += Y_DISTANCE + HEIGHT_STICKER

    for idx in range(num_stickers % 6):
        c.drawImage(image=path_to_stick, x=x, y=y, width=WIDTH_STICKER, height=HEIGHT_STICKER)
        x += X_DISTANCE + WIDTH_STICKER

    c.save()


if __name__ == "__main__":
    create_stickers(
        path_to_stick="sticker.jpg",
        path_to_save="output.pdf",
        num_stickers=23,

    )