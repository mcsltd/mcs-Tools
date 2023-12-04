from tkinter.ttk import *
from tkinter import *

from tkinter.messagebox import showerror

class Editor:
    def __init__(self, master, name_file):
        self.master = master

        # name txt file
        self.name_file = name_file

        # setup UI app
        self._set_ui()

        # show content template file in text panel
        self._get_file_content()
        pass

    def _set_ui(self):
        # Add Buttons
        self.btn_save = Button(self.master, text="Сохранить", command=self._save_modify_file)

        # Add panel info
        self.text = Text(self.master)
        self.scroll = Scrollbar(self.master, command=self.text.yview)
        self.text.config(yscrollcommand=self.scroll.set)

        # Place button
        self.btn_save.grid(row=0, column=0, padx=10, pady=10, sticky=W)

        # Place Text
        self.text.grid(row=1, rowspan=6, column=0, columnspan=3, padx=10, pady=10, sticky=E)

        # Place
        self.scroll.grid(row=1, rowspan=6, column=4, columnspan=3, pady=2, padx=2, sticky="wns")

    def _get_file_content(self):
        """
        Get the text of the replacement templates and output it to the text field for modification.
        :return:
        """
        try:
            with open(self.name_file, "r") as file:
                t = "".join(file.readlines())
                self.text.insert(1.0, t)
        except Exception as err:
            showerror(
                title="Обработчик .CSV файлов",
                message="Файл c шаблонами .txt не существует!\n self.name_file"
            )

    def _save_modify_file(self):
        """
        Saving modified file.
        :return:
        """
        with open(self.name_file, "w") as file:
            file.write(self.text.get(1.0, END))


if __name__ == "__main__":
    root = Tk()

    app = Editor(root, name_file="template_new.txt")

    root.mainloop()
