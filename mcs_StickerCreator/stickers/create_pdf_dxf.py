import datetime
import os.path
import logging
import ezdxf


from mcs_StickerCreator.constants import mm, A3, RADIUS_REF_POINT, Sign
from mcs_StickerCreator.stickers.db25.sticker import Sticker, Annotation
from mcs_StickerCreator.draw import draw_hline_ref_points, draw_hline_ref_points_dxf


from reportlab.pdfgen.canvas import Canvas

# custom logger
logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.INFO)


def create_pdf_dxf(
        stickers: list[Sticker],
        dx: float, dy: float,
        dir_to_save: str,
        x_pad: float, y_pad: float,
        dx_inner: float = 0.49, dy_inner: float = 0.52,
        annotation: str | None = None,
        skip_dxf: bool = True, skip_rpoints=True
) -> None:
    logger.info(f"The data file has been read. Total stickers: {len(stickers)}.")

    # new pdf file
    pdf = Canvas(f"{dir_to_save}/output.pdf", pagesize=A3)

    # pad for draw annotate
    x, y = x_pad, y_pad

    # draw two ref point in below
    draw_hline_ref_points(
        canvas=pdf,
        x1_cen=RADIUS_REF_POINT, x2_cen=A3[0] - RADIUS_REF_POINT,
        y_cen=RADIUS_REF_POINT,  # problem with draw?
        radius=RADIUS_REF_POINT, skip=skip_rpoints
    )

    if not skip_dxf:
        # new dxf file
        dxf = ezdxf.new(stickers[0].doc_dxf.dxfversion)
        msp = dxf.modelspace()

        # initial coordinates for sticker outlines
        x_, y_ = x_pad / mm + dx_inner, y_pad / mm + dy_inner

        # draw two ref point in below in pdf file
        draw_hline_ref_points_dxf(
            modelspace=msp,
            x1_cen=RADIUS_REF_POINT / mm, x2_cen=(A3[0] - RADIUS_REF_POINT) / mm,
            y_cen=RADIUS_REF_POINT / mm,
            radius=RADIUS_REF_POINT / mm, skip=skip_rpoints
        )

    # initialization of counters
    cnt_page = 1
    ind_sticker = 0
    cnt_row = 1

    if annotation is not None:
        annotation += " " + datetime.datetime.now().isoformat()[:-7].replace("T", " ")
        # draw annotation
        Annotation().draw_annotation_pdf(
            canvas=pdf, x=A3[0] / 2, y=RADIUS_REF_POINT / 2, text=annotation + f" PAGE {cnt_page}")

    logger.info(f"Drawing stickers on the page: {cnt_page}.")

    while ind_sticker < len(stickers):

        # check filling on x and y
        if x + stickers[ind_sticker].mm_width + x_pad > A3[0]:
            # carriage return to new line (pfd)
            x = x_pad
            y += stickers[ind_sticker].mm_height + dy

            if not skip_dxf:
                # carriage return to new line (dxf)
                x_ = x_pad / mm + dx_inner
                y_ += (stickers[ind_sticker].mm_height + dy) / mm

            # check filling on y (end of page)
            if y + stickers[ind_sticker].mm_height + y_pad > A3[1]:
                # draw line ref point in upstairs (pdf)
                draw_hline_ref_points(
                    canvas=pdf,
                    x1_cen=RADIUS_REF_POINT, x2_cen=A3[0] - RADIUS_REF_POINT,
                    y_cen=cnt_row * stickers[ind_sticker].mm_height + (cnt_row - 1) * dy - RADIUS_REF_POINT,
                    radius=RADIUS_REF_POINT, skip=skip_rpoints
                )

                if not skip_dxf:
                    # add ref points upstairs dxf file
                    draw_hline_ref_points_dxf(
                        modelspace=msp, x1_cen=RADIUS_REF_POINT / mm, x2_cen=(A3[0] - RADIUS_REF_POINT) / mm,
                        y_cen=(cnt_row * stickers[ind_sticker - 1].mm_height + (cnt_row - 1) * dy - RADIUS_REF_POINT) / mm,
                        radius=RADIUS_REF_POINT / mm, skip=skip_rpoints
                    )

                    # save the completely completed dxf file
                    if not os.path.exists(f"{dir_to_save}/output.dxf"):
                        dxf.saveas(f"{dir_to_save}/output.dxf")

                    # create new dxf file
                    dxf = ezdxf.new(stickers[0].doc_dxf.dxfversion)
                    msp = dxf.modelspace()
                    y_ = y_pad / mm + dy_inner  # reset variable y (dxf)

                if annotation is not None:
                    # draw annotation upstairs
                    Annotation().draw_annotation_pdf(
                        canvas=pdf,
                        x=A3[0] / 2, y=cnt_row * stickers[ind_sticker - 1].mm_height + cnt_row * dy + y_pad + 2 * mm,
                        text=annotation + f" PAGE {cnt_page}"
                    )

                y = y_pad  # reset variable y (pdf)
                cnt_row = 1

                pdf.showPage()  # create new page
                cnt_page += 1

                logger.info(f"Drawing stickers on the page: {cnt_page}.")

                if annotation is not None:
                    # draw annotation below
                    Annotation().draw_annotation_pdf(
                        canvas=pdf, x=A3[0] / 2, y=RADIUS_REF_POINT / 2, text=annotation + f" PAGE {cnt_page}")

                # draw two ref point in below
                draw_hline_ref_points(
                    canvas=pdf,
                    x1_cen=RADIUS_REF_POINT, x2_cen=A3[0] - RADIUS_REF_POINT,
                    y_cen=RADIUS_REF_POINT,  # problem with draw?
                    radius=RADIUS_REF_POINT, skip=skip_rpoints
                )

                if not skip_dxf:
                    # draw two ref point in below in dxf file
                    draw_hline_ref_points_dxf(
                        modelspace=msp,
                        x1_cen=RADIUS_REF_POINT / mm, x2_cen=(A3[0] - RADIUS_REF_POINT) / mm,
                        y_cen=RADIUS_REF_POINT / mm,
                        radius=RADIUS_REF_POINT / mm, skip=skip_rpoints
                    )
                continue
            cnt_row += 1

        # draw stickers in pdf and dxf file
        stickers[ind_sticker].draw_sticker_pdf(canvas=pdf, x=x, y=y)

        if not skip_dxf:
            stickers[ind_sticker].draw_sticker_dxf(modelspace=msp, x=x_ + dx_inner, y=y_ + dy_inner)
            x_ += (stickers[ind_sticker].mm_width + dx) / mm  # dxf file

        x += stickers[ind_sticker].mm_width + dx  # pdf file
        ind_sticker += 1

    if cnt_row > 1:
        draw_hline_ref_points(
            canvas=pdf,
            x1_cen=RADIUS_REF_POINT, x2_cen=A3[0] - RADIUS_REF_POINT,
            y_cen=cnt_row * stickers[ind_sticker - 1].mm_height + (cnt_row - 1) * dy - RADIUS_REF_POINT,
            radius=RADIUS_REF_POINT, skip=skip_rpoints
        )  # draw line ref point in upstairs

        if not skip_dxf:
            draw_hline_ref_points_dxf(
                modelspace=msp, x1_cen=RADIUS_REF_POINT / mm, x2_cen=(A3[0] - RADIUS_REF_POINT) / mm,
                y_cen=(cnt_row * stickers[ind_sticker - 1].mm_height + (cnt_row - 1) * dy - RADIUS_REF_POINT) / mm,
                radius=RADIUS_REF_POINT / mm, skip=skip_rpoints
            )

    if annotation is not None:
        # add annotation upstairs
        Annotation().draw_annotation_pdf(
            canvas=pdf,
            x=A3[0] / 2, y=cnt_row * stickers[ind_sticker - 1].mm_height + cnt_row * dy + y_pad + 2 * mm,
            text=annotation + f" PAGE {cnt_page}"
        )

    if ind_sticker == len(stickers):
        logger.info(f"The program worked well. Number of drawn stickers: {ind_sticker}."
                    f" Total number of stickers: {len(stickers)}")
        logger.info(f"The result is saved to file: {dir_to_save}/output.pdf.")
        logger.info(f"Сutting file saved in {dir_to_save}/output.dxf.")
    else:
        logger.error(f"The number of stickers drawn does not correspond to the number of transferred ones.")

    pdf.save()

    if not skip_dxf:
        # save as output.dxf
        if os.path.exists(f"{dir_to_save}/output.dxf"):
            if not ((x + stickers[ind_sticker - 1].mm_width + dx + x_pad > A3[0])
                    and (y + 2 * stickers[ind_sticker - 1].mm_height + dy + y_pad > A3[1])):
                # the output.dxf file already exists (it is assumed that it is completely filled)
                dxf.saveas(f"{dir_to_save}/output_last_page.dxf")
        else:
            dxf.saveas(f"{dir_to_save}/output.dxf")


