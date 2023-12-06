from tkinter.ttk import *
from tkinter import *

from tkinter.messagebox import showerror, showinfo


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
        self.btn_add = Button(self.master, text="Добавить", width=10, command=self._add_template_to_file)
        self.btn_del = Button(self.master, text="Удалить", width=10, command=self._delete_template_in_file)

        # Add Entries
        self.entry_add = Entry(self.master)
        self.entry_del = Entry(self.master)

        # Add panel info
        self.text = Text(self.master)
        self.scroll = Scrollbar(self.master, command=self.text.yview)
        self.text.config(yscrollcommand=self.scroll.set)

        # Place button
        self.btn_add.grid(row=0, column=0, padx=10, pady=10, sticky=W)
        self.btn_del.grid(row=1, column=0, padx=10, pady=10, sticky=W)

        self.entry_add.grid(row=0, column=1, columnspan=3, pady=10, padx=10, sticky=NSEW)
        self.entry_del.grid(row=1, column=1, columnspan=3, pady=10, padx=10, sticky=NSEW)

        # Place Text
        self.text.grid(row=2, rowspan=6, column=0, columnspan=3, padx=10, pady=10, sticky=NSEW)
        # add text box stretching
        self.master.columnconfigure(index=2, weight=1)
        self.master.rowconfigure(index=2, weight=1)

        # Place
        self.scroll.grid(row=2, rowspan=6, column=4, columnspan=3, pady=2, padx=2, sticky="wns")

    def _get_file_content(self):
        """
        Get the text of the replacement templates and output it to the text field for modification.
        :return:
        """
        try:
            with open(self.name_file, "r") as file:
                t = "".join(file.readlines())
                self.text.configure(state=NORMAL)
                self.text.insert(1.0, t)
                self.text.configure(state=DISABLED)
        except Exception as err:
            showerror(
                title="Обработчик .CSV файлов",
                message="Файл c шаблонами .txt не существует!\n self.name_file"
            )

    def _add_template_to_file(self):
        """
        Saving modified file.
        :return:
        """
        template = self.entry_add.get()
        text = self.text.get(1.0, END).split("\n")

        template = template.split()
        if len(template) == 2:
            for t in text:
                if t.split() != [] and template[0] == t.split()[0]:
                    showerror(
                        title="Найден похожий шаблон",
                        message=f"Для {template[0]} найден похожий элемент в файле шаблонов template.txt"
                    )
                    return

            self.text.configure(state=NORMAL)
            # insert template in Text widget
            self.text.insert(END, "\n" + " ".join(template))
            self.text.configure(state=DISABLED)

            # save template in txt
            with open(self.name_file, "w") as file:
                file.write(self.text.get(1.0, END))

            self.entry_add.delete(0, END)

        else:
            showerror(
                title="Введен неправильный шаблон",
                message=f"Введен неправильный шаблон. Вводите шаблон по следующему образцу:\n"
                        f"  \'то-что-меняется\' то-на-что-меняется"
            )

    def _delete_template_in_file(self):
        new_text = []
        template = self.entry_del.get()
        text = self.text.get(1.0, END).split("\n")

        flag_del = False
        for t in text:
            _t = t.replace("\n", "")
            if template != _t:
                new_text.append(t)
            else:
                flag_del = True

        if flag_del:
            self.text.configure(state=NORMAL)
            self.text.delete(1.0, END)
            self.text.insert(1.0, "\n".join(new_text)[:-2])
            self.text.configure(state=DISABLED)
            self.entry_del.delete(0, END)

            # save new templates in txt
            with open(self.name_file, "w") as file:
                file.write(self.text.get(1.0, END))
        else:
            showinfo(
                title="Шаблон не найден",
                message="Шаблон не найден в файле template.txt"
            )


if __name__ == "__main__":
    root = Tk()

    app = Editor(root, name_file="template.txt")

    root.mainloop()
