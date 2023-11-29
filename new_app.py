from tkinter import *
from tkinter.ttk import *


class App:

    def __init__(self, master):
        self.master = master

        # setup UI for application
        self._set_ui()
        pass

    def _set_ui(self):
        """
        Setup UI application
        :return:
        """
        self.notebook = Notebook(self.master)

        # Excel file processing
        self.frame_excel = Frame(self.notebook)
        self.btn_processed_excel = Button(self.frame_excel, text="Выбрать файл(-ы) для обработки", width=45, padding=6)
        self.btn_template_excel = Button(self.frame_excel, text="Выберите шаблон для обработки Excel файлом", width=45, padding=6)
        self.btn_save_excel = Button(self.frame_excel, text="Cохранить в ...", width=45, padding=6)
        self.btn_start_excel = Button(self.frame_excel, text="Обработать выбранные файлы", width=45, padding=6)

        # .txt file processing
        self.frame_txt = Frame(self.notebook)
        self.btn_processed_txt = Button(self.frame_txt, text="Выбрать файл(-ы) для обработки", width=45, padding=6)
        self.btn_save_txt = Button(self.frame_txt, text="Cохранить в ...", width=45, padding=6)
        self.btn_start_txt = Button(self.frame_txt, text="Обработать выбранные файлы", width=45, padding=6)

        # Add File Processing tabs
        self.notebook.add(self.frame_excel, text="Обработка Excel файлом", padding=7)
        self.notebook.add(self.frame_txt, text="Обработка .txt файлом", padding=7)

        # Add panel info
        self.info = Text()
        self.scroll = Scrollbar(command=self.info.yview)
        self.info.config(yscrollcommand=self.scroll.set)

        # Place notebook
        self.notebook.grid(row=0, column=0)

        # Place button for processing .txt file in notebook
        self.btn_processed_txt.grid(row=1, column=0, sticky=W, padx=10, pady=10)
        self.btn_save_txt.grid(row=2, column=0, sticky=W, padx=10, pady=10)
        self.btn_start_txt.grid(row=3, column=0, sticky=W, padx=10, pady=10)

        # Place button for processing Excel file in notebook
        self.btn_processed_excel.grid(row=1, column=0, sticky=W, padx=10, pady=10)
        self.btn_template_excel.grid(row=2, column=0, sticky=W, padx=10, pady=10)
        self.btn_save_excel.grid(row=3, column=0, sticky=W, padx=10, pady=10)
        self.btn_start_excel.grid(row=4, column=0, sticky=W, padx=10, pady=10)

        # place info
        self.info.grid(row=0, column=2, rowspan=6, columnspan=2, pady=10, sticky=E)

        # Place scroll bar
        self.scroll.grid(row=0, rowspan=6, column=4, pady=1, sticky="wns")


if __name__ == "__main__":
    root = Tk()

    app = App(root)

    root.mainloop()
