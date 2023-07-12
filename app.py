import datetime

from tkinter import *
from tkinter import filedialog as fd


class App:

    def __init__(self, master, func):
        self.master = master
        self.func = func

        self.processed_files = ""
        self.template_file = ""
        self.save_location = ""

        # buttons for action
        self.btn_processed = Button(self.master, text="Выберите файл(-ы) для обработки")
        self.btn_template = Button(self.master, text="Выберите шаблон")
        self.btn_save = Button(self.master, text="Сохранить как")
        self.btn_start = Button(self.master, text="Cтарт")

        # button click event binding
        self.btn_processed["command"] = self._get_processed_files
        self.btn_template["command"] = self._get_template
        self.btn_save["command"] = self._get_save_location
        self.btn_start["command"] = self._press_start

        self.info = Text()
        self.scroll = Scrollbar(command=self.info.yview)
        self.info.config(yscrollcommand=self.scroll.set)

        self._set_ui()

    def _set_ui(self):
        # name of application
        self.master.title("Обработчик .csv файлов")

        # place button
        self.btn_processed.grid(row=1, column=0, sticky=W, padx=10, pady=10)
        self.btn_template.grid(row=2, column=0, sticky=W, padx=10, pady=10)
        self.btn_save.grid(row=3, column=0, sticky=W, padx=10, pady=10)
        self.btn_start.grid(row=4, column=0, sticky=W, padx=10, pady=10)

        # place info
        self.info.grid(row=0, column=2, rowspan=6, columnspan=2, pady=10, sticky=E)

        # scroll bar
        self.scroll.grid(row=0, rowspan=6, column=4, pady=1, sticky="wns")

    def _get_save_location(self):
        self.save_location = fd.askdirectory(
            title="Выбор места сохранения обработанных файлов"
        )

    def _get_processed_files(self):
        self.processed_files = fd.askopenfilenames(
            title="Выберите файл(-ы) для обработки",
            filetypes=(("CSV Files", "*.csv"),)
        )

    def _get_template(self):
        self.template_file = fd.askopenfile(
            title="Выберите файл-шаблон подстановки",
            filetypes=(("TXT Files", "*.txt"),)
        )

    def _press_start(self):

        self.info.delete(1.0, END)

        if self.template_file == "":
            self.info.insert(END, "ОШИБКА! Не выбран шаблон .txt для замены значений в .csv файле!\n")
            return

        if self.processed_files == "":
            self.info.insert(END, "ОШИБКА! Не выбраны .csv файлы для обработки!\n")
            return

        if self.save_location == "":
            self.info.insert(END, "ОШИБКА! Не выбрана папка для сохранения файлов!\n")
            return

        self.save_location += f"/output_{str(datetime.datetime.now())}".replace(":", ".")
        self.info.insert(END, "Начало обработки файлов...\n")

        for fn in self.processed_files:
            try:
                self.info.insert(END, f"Обрабатывается файл {fn}\n\n")
                # print(self.template_file.name)
                log = self.func(fn, self.template_file.name, self.save_location)
                self.info.insert(END, log)
            except Exception as err:
                self.info.insert(END, f"Возникла ошибка обработки файла {err}\n")
            else:
                self.info.insert(END, f"Обработка файла \"{fn}\" завершена\n")

        self.save_location = ""
        self.template_file = ""
        self.processed_files = ""



