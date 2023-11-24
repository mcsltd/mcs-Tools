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

        # create menu
        self.main_menu = Menu(self.master)
        self.master.config(menu=self.main_menu)

        self.help_menu = Menu(self.main_menu, tearoff=0)
        self.help_menu.add_command(label="О программе",
                                   command=self._get_info_about)
        self.help_menu.add_command(label="Порядок работы c программой",
                                   command=self._get_info_procedure)
        self.help_menu.add_command(label="Правила оформления шаблона для обработки .csv файла",
                                   command=self._get_info_template)
        self.main_menu.add_cascade(label="Справка", menu=self.help_menu)


        # buttons for action
        self.btn_processed = Button(self.master, text="Выберите файл(-ы) для обработки")
        self.btn_template = Button(self.master, text="Выберите шаблон")
        self.btn_save = Button(self.master, text="Сохранить как")
        self.btn_start = Button(self.master, text="Обработать")

        # button click event binding
        self.btn_processed["command"] = self._get_processed_files
        self.btn_template["command"] = self._get_template
        self.btn_save["command"] = self._get_save_location
        self.btn_start["command"] = self._press_start

        self.info = Text()
        self.scroll = Scrollbar(command=self.info.yview)
        self.info.config(yscrollcommand=self.scroll.set)

        self._set_ui()

    def _get_info_about(self):
        sub_master = Tk()
        sub_master.geometry("+500+300")
        sub_master.title("О программе ...")
        text = "Программа служит для обработки .csv файла(-ов) с заголовком:\n" \
               "Designator,Footprint,Center-X(mm),Center-Y(mm),Layer,Rotation,Comment\n\n" \
               "Обработка файла включает в себя удаление символов \" , а также замену слов\n" \
               "по файлу, в котором указаны шаблоны замены.\n\n" \
               "Обработанные  строки для  файла(-ов) в  зависимости  от столбца \"Rotation\"\n" \
               "и информации, указанной в  файле с шаблонами  замены, распределяются по трём\n" \
               "файлам:\n" \
               " 1)Top;\n 2)Bottom;\n 3)Delete.\n\n" \
               "В файл \"Delete\" отправляются файлы для которых не указан  шаблон  замены и\n" \
               "строки содержащие шаблон \"~FV\".\n" \
               "Для  обработанных  файлов  генерируется  папка с  именем \"Output\" и  временем \n" \
               "начала обработки .csv файлов."
        info = Label(sub_master, text=text, justify="left").pack()
        sub_master.mainloop()

    def _get_info_procedure(self):
        sub_master = Tk()
        sub_master.geometry("+500+300")
        sub_master.title("Порядок работы с программой")
        text = "1) Программе указываются необработанные файл или файлы только в формате\n" \
               "    .csv и только с заголовком:\n\n" \
               "   Designator,Footprint,Center-X(mm),Center-Y(mm),Layer,Rotation,Comment\n\n" \
               "2) Программе указывает шаблон со  словами на  которые нужно заменить те,\n" \
               "    что в необработанном .csv файле.  Этот файл обязательно  должен  быть\n" \
               "    в формате .txt.\n\n" \
               "3) Программе обязательно указывается место сохранения файлов.\n\n" \
               "4) Программа начинает  обработку  файлов  после  нажатия кнопки \"Старт\"\n" \
               "    Информация об обработке отображается в поле справа от кнопок.\n\n" \
               "5) Если Вы хотите обработать другие необработанные файлы .сsv, тогда\n" \
               "    нужно повторить пункты 1 - 4."
        info = Label(sub_master, text=text, justify="left").pack()
        sub_master.mainloop()

    def _get_info_template(self):
        sub_master = Tk()
        sub_master.geometry("+500+300")
        sub_master.title("Правила оформления шаблона для обработки .csv файла")
        text = "Файл с шаблоном замены должен иметь формат .txt. Он может иметь\n" \
               "любое  название.  Главное,  чтобы  данные в  этом  файле  были \n" \
               "организованы следующим образом:\n\n" \
               "   'что_менять'   'на_что_менять'\n\n " \
               "Пример:\n" \
               "\'IPC-7351/CAPC1005M\' \'0402C_501\'\n\n" \
               "ГЛАВНОЕ: файл с шаблонами замены должен содержать ТОЛЬКО шаблоны\n" \
               "замены, не допускаются комментарии,  одиночные  слова в  строках,\n" \
               "пустые строки, повторение слов, которые нужно заменить по шаблону.\n\n" \
               "Слова шаблоны должны быть атомарными (не должны присутствовать пробелы):\n\n" \
               "'MCS_WORK/LATTICE/CM36A-ICE40 #2' - CM36A_503\n\n" \
               "Здесь пустая строка не допускается и приведёт к ошибке. Не допускается\n" \
               "также повторное использование слов, которые нужно заменить:\n\n" \
               "'MCS_WORK/LATTICE/CM36A-ICE40 #2' - CM36A_503\n" \
               "'MCS_WORK/LATTICE/CM36A-ICE40 #2' - CH3A_511\n"
        info = Label(sub_master, text=text, justify="left").pack()
        sub_master.mainloop()

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
            filetypes=(
                ("CSV Files", ".csv"),
            )
        )

    def _get_template(self):
        self.template_file = fd.askopenfile(
            title="Выберите файл-шаблон подстановки",
            filetypes=(
                ("TXT Files", "*.txt"),
                ("Excel files", ".xls")
            )
        )

        # show info about selected files
        if self.template_file is not None:
            fn = self.template_file.name[self.template_file.name.rfind("/") + 1:]

            if ".xls" in self.template_file.name[-4:]:
                self.info.insert(END, f"Выбран файл {fn} c шаблонами.\n")
                self.btn_start.configure(text="Обработать .xls файлом")

            if ".txt" in self.template_file.name[-4:]:
                self.info.insert(END, f"Выбран файл {fn} c шаблонами.\n")
                self.btn_start.configure(text="Обработать .txt файлом")

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



