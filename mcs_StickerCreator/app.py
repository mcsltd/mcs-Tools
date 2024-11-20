from tkinter import filedialog as fd, Tk, Listbox, Variable
from tkinter.constants import SINGLE, SOLID, DISABLED, NORMAL
from tkinter.messagebox import *
from tkinter import ttk

import constants
from main import db25var1_create_pdf_dxf


class Maker:
    NAME_STICKERS = ["DB25 var.1", ]

    def __init__(self, master):
        self.master = master

        self.input_file = None
        self.list_sign = [constants.Sign.sn, constants.Sign.lot]
        self.selected_sign = Variable(value=self.list_sign)
        self.selected_sign.set(constants.Sign.sn)

        self.setUi()

    def setUi(self):
        self.text = ttk.Label(text="Стикеры:")
        self.text.grid(row=0, column=0, padx=5, pady=5)

        self.lb_sticker = Listbox(listvariable=Variable(value=Maker.NAME_STICKERS), selectmode=SINGLE)
        self.lb_sticker.bind("<<ListboxSelect>>", self.select_sticker)
        self.lb_sticker.grid(row=1, column=0, padx=5, pady=5)
        self.lb_sticker.select_set(0)

        # self.sticker_btn = ttk.Button(self.master, text="Ок", command=self._select_sticker)
        # self.sticker_btn.grid(row=2, column=0, padx=10, pady=10)
        self.sticker_fr = ttk.Frame(self.master, relief=SOLID, padding=[8, 10])
        self.sticker_fr.grid(
            row=0, rowspan=3,
            column=1, columnspan=3,
            padx=10, pady=10
        )
        self.setUiFrame()

    def select_sticker(self, event):
        ind_v, = self.lb_sticker.curselection()

        if not (isinstance(ind_v, int) and ind_v < len(Maker.NAME_STICKERS)):
            return

        v = Maker.NAME_STICKERS[ind_v]
        if v == Maker.NAME_STICKERS[0]:
            self.maker_db25()

    # function for sticker generation
    def maker_db25(self):
        self.setUiFrame()

    def setUiFrame(self):
        self.in_btn = ttk.Button(self.sticker_fr, text="Выбрать файл для обработки", command=self.get_input,
                            width=30, padding=6)
        self.in_btn.grid(row=0, column=0)

        ind_row = 0
        for sg in self.list_sign:
            sgn_btn = ttk.Radiobutton(self.sticker_fr, text=sg, value=sg, variable=self.selected_sign)
            sgn_btn.grid(row=1 + ind_row, column=0)
            ind_row += 1

        self.ok_btn = ttk.Button(self.sticker_fr, text="Сгенерировать", command=self.make_db25var1_create_pdf_dxf,
                            width=30, padding=6, state=DISABLED)
        self.ok_btn.grid(row=len(self.list_sign) + 1, column=0)

    def get_input(self):
        self.input_file = fd.askopenfilename(
            title="Выберите файл для обработки",
            filetypes=(
                ("TXT Files", ".txt"),
            )
        )
        self.ok_btn["state"] = NORMAL

    def make_db25var1_create_pdf_dxf(self):
        try:
            db25var1_create_pdf_dxf(self.input_file, self.selected_sign.get())
        except:
            showwarning(
                title="Возникла ошибка!",
                message="В результате работы программы возникла ошибка!"
                        "Проверьте файл TXT подаваемый на вход, а также есть ли файлы SVG для стикеров."
            )
        finally:
            self.ok_btn["state"] = DISABLED


if __name__ == "__main__":
    root = Tk()
    app = Maker(root)
    root.geometry("425x225")
    root.mainloop()
