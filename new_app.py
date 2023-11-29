import configparser
from tkinter import *
from tkinter.ttk import *

from tkinter import filedialog as fd

from editor import *


def set_config(template_file_name):
    """
    Setting the path to the file with .txt templates.
    :param template_file_name: name of template file
    :return:
    """
    # Create config
    config = configparser.ConfigParser()
    config.add_section("Settings")
    config.set("Settings", "path", template_file_name)

    # Save config into file
    with open("config.ini", "w") as config_file:
        config.write(config_file)


class App:

    def __init__(self, master):
        self.master = master

        # setup UI for application
        self._set_ui()

        # parse config file
        self.config_file = "config.ini"
        self.template_txt = self.get_config()
        pass

    def get_config(self):
        """
        Retrieving data from a configuration file.
        :return:
        """
        config = configparser.ConfigParser()
        # read config file
        config.read('config.ini')
        # get config data
        file_name = config.get("Settings", "path")
        return file_name

    def _set_ui(self):
        """
        Setup UI application
        :return:
        """
        self.notebook = Notebook(self.master)

        # Create menu
        self.main_menu = Menu(self.master)
        self.master.config(menu=self.main_menu)

        # tab edit
        self.edit_menu = Menu(self.main_menu, tearoff=0)
        self.edit_menu.add_command(label="Изменить .txt шаблон", command=self.change_template_txt)
        self.main_menu.add_cascade(label="Изменить", menu=self.edit_menu)

        # tab help
        self.help_menu = Menu(self.main_menu, tearoff=0)
        # self.help_menu.add_command(label="О программе",
        #                            command=self._get_info_about)
        # self.help_menu.add_command(label="Порядок работы c программой",
        #                            command=self._get_info_procedure)
        # self.help_menu.add_command(label="Правила оформления шаблона .txt для обработки файла",
        #                            command=self._get_info_template)
        self.main_menu.add_cascade(label="Справка", menu=self.help_menu)

        # Excel file processing
        self.frame_excel = Frame(self.notebook)
        self.btn_processed_excel = Button(
            self.frame_excel,
            text="Выбрать файл(-ы) для обработки",
            width=45,
            command=self._get_processed_files
        )
        self.btn_template_excel = Button(
            self.frame_excel,
            text="Выберите шаблон для обработки Excel файлом",
            width=45,
            command=self._get_template
        )
        self.btn_save_excel = Button(
            self.frame_excel,
            text="Cохранить в ...",
            width=45,
            command=self._get_save_location
        )
        self.btn_start_excel = Button(
            self.frame_excel,
            text="Обработать выбранные файлы",
            width=45
        )

        # .txt file processing
        self.frame_txt = Frame(self.notebook)
        self.btn_processed_txt = Button(
            self.frame_txt,
            text="Выбрать файл(-ы) для обработки",
            width=45,
            command=self._get_processed_files
        )
        self.btn_save_txt = Button(
            self.frame_txt,
            text="Cохранить в ...",
            width=45,
            command=self._get_save_location
        )
        self.btn_start_txt = Button(
            self.frame_txt,
            text="Обработать выбранные файлы",
            width=45,
            command=self._start_processing
        )

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

        # Place info panel
        self.info.grid(row=0, column=2, rowspan=6, columnspan=2, padx=10, pady=10, sticky=E)

        # Place scroll bar
        self.scroll.grid(row=0, rowspan=6, column=4, pady=2, padx=2, sticky="wns")

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
            title="Выберите Excel файл с шаблонами",
            filetypes=(
                ("Excel files", ".xlsx .xls")
            )
        )

    def change_template_txt(self):
        """
        Open txt editor window.
        :return:
        """
        win = Toplevel()
        editor = Editor(
            master=win,
            name_file=self.template_txt
        )
        win.grab_set()

    def _start_processing(self):
        pass


if __name__ == "__main__":
    root = Tk()

    app = App(root)

    root.mainloop()

    # set path to template txt file
    # set_config(
    #     template_file_name="./template_new.txt"
    # )
