import configparser
from datetime import datetime
from tkinter import filedialog as fd
from tkinter.messagebox import *
from ParserSMD.editor import *
from file_processing import *
from tkinter import ttk

import os

PATH_TO_DIR_CONFIG = os.environ["HOMEDRIVE"] + os.environ["HOMEPATH"] + f"\\.mcs-tools"
PATH_TO_CONFIG = os.environ["HOMEDRIVE"] + os.environ["HOMEPATH"] + f"\\.mcs-tools\\config.ini"


def set_config(path_to_config, path_to_template):
    """
    Setting the path to the file with .txt templates.
    :param template_file_name: name of input file
    :return:
    """
    # Create config
    config = configparser.ConfigParser()
    config.add_section("Settings - CSV Handler App")
    config.set("Settings - CSV Handler App", "path", path_to_template)

    # Save config into file
    with open(path_to_config, "w") as config_file:
        config.write(config_file)
def get_config(path_to_config):
    """
    Retrieving data from a configuration file.
    :return:
    """
    config = configparser.ConfigParser()
    # read config file
    config.read(path_to_config)
    # get config data
    file_name = config.get("Settings - CSV Handler App", "path")
    return file_name
def load_preference():
    """
    load txt file from config.ini.
    :return: str path to txt input file.
    """
    # create dir config is not exists
    if not os.path.exists(PATH_TO_DIR_CONFIG):
        os.mkdir(PATH_TO_DIR_CONFIG)

    # check if file with config exists
    if not os.path.exists(PATH_TO_CONFIG):

        result = askyesno(
            title="Поиск TXT файла с шаблонами",
            message="Найти TXT файл с шаблонами?"
        )

        if result:
            path_to_template = fd.askopenfilename(
                title="Выберите TXT файл с шаблонами",
                filetypes=[('text files', 'txt')]
            )
        else:
            path_to_template = None
            return path_to_template

        # get file .txt input
        path_to_template = path_to_template
        # create config file and set path to txt input file
        set_config(PATH_TO_CONFIG, path_to_template)

    # get path to txt input
    path_to_template = get_config(PATH_TO_CONFIG)
    return path_to_template


class App:

    def __init__(self, master, path_to_txt_template):
        self.master = master

        # parse config file
        self.template_txt = path_to_txt_template

        # name of application
        self.master.title("Обработчик .CSV файлов для станка")

        # state of saving file together or separate
        self.mode_save_file = IntVar()

        # setup UI for application
        self._set_ui()

        self.save_location = ""
        self.template_excel_file = ""
        self.processed_file = ""
        pass

    def _set_ui(self):
        """
        Setup UI application
        :return:
        """
        self.notebook = Notebook(self.master)

        # checkbox for selecting file saving mode
        self.checkbox_sep = ttk.Checkbutton(
            text="Сохранять строки c BOT и TOP в разные файлы",
            variable=self.mode_save_file,
            # command=self.test_checkbox
        )

        # Create menu
        self.main_menu = Menu(self.master)
        self.master.config(menu=self.main_menu)

        # tab file
        self.file_menu = Menu(self.main_menu, tearoff=0)
        self.file_menu.add_command(label="Выход", command=self._close_app)
        # self.edit_menu.add_command(label="Выбрать новый .txt шаблон", command=self.choose_template_txt)
        self.main_menu.add_cascade(label="Файл", menu=self.file_menu)

        # tab edit
        self.edit_menu = Menu(self.main_menu, tearoff=0)
        self.edit_menu.add_command(label="Изменить .txt шаблон", command=self.change_template_txt)
        # self.edit_menu.add_command(label="Выбрать новый .txt шаблон", command=self.choose_template_txt)
        self.main_menu.add_cascade(label="Изменить", menu=self.edit_menu)

        # tab help
        self.help_menu = Menu(self.main_menu, tearoff=0)
        self.help_menu.add_command(
            label="Работа с программой ...",
            command=self._get_info_processing_file
        )
        # self.help_menu.add_command(
        #     label="Правила оформления шаблона .txt для обработки файла",
        #     # command=self._get_info_template
        # )
        self.main_menu.add_cascade(label="Справка", menu=self.help_menu)

        # Excel file processing
        self.frame_excel = Frame(self.notebook)
        self.btn_processed_excel = Button(
            self.frame_excel,
            text="Выбрать файл(-ы) для обработки",
            width=45,
            command=self._get_processed_file
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
            text="Обработать ...",
            width=45,
            command=self._start_processing
        )

        # .txt file processing
        self.frame_txt = Frame(self.notebook)
        self.btn_processed_txt = Button(
            self.frame_txt,
            text="Выбрать файл(-ы) для обработки",
            width=45,
            command=self._get_processed_file
        )
        self.btn_save_txt = Button(
            self.frame_txt,
            text="Cохранить в ...",
            width=45,
            command=self._get_save_location
        )
        self.btn_start_txt = Button(
            self.frame_txt,
            text="Обработать ...",
            width=45,
            command=self._start_processing,
        )

        # Add File Processing tabs
        self.notebook.add(
            self.frame_excel,
            text="Обработка Excel файлом",
            padding=7, )
        self.notebook.add(
            self.frame_txt,
            # text="Обработка TXT файлом",
            text="Обработка .CSV файла шаблоном",
            padding=7)

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

        # place checkbox
        self.checkbox_sep.grid(row=5, column=0, sticky=W, padx=10, pady=10)

        # Place info panel
        self.info.grid(row=0, column=2, rowspan=6, columnspan=2, padx=10, pady=10, sticky=NSEW)
        # add text box stretching
        self.master.columnconfigure(index=2, weight=1)
        self.master.rowconfigure(index=1, weight=1)

        # Place scroll bar
        self.scroll.grid(row=0, rowspan=6, column=4, pady=2, padx=2, sticky="ns")

    # def test_checkbox(self):
    #     print(f"Состояние checkbox'а:{self.mode_save_file.get()}")

    def _get_info_processing_file(self):
        sub_master = Tk()
        sub_master.geometry("+500+300")
        sub_master.title("Порядок обработки .CSV файлов")
        text = "Программа служит для обработки .csv файла.\n\n" \
               "Обрабатываемые .csv файлы должны обязательно иметь заголовок:\n" \
               "Designator,Footprint,Center-X(mm),Center-Y(mm),Layer,Rotation,Comment\n\n" \
               "Обработка .сsv файла включает в себя удаление шапки, а также замену слов\n" \
               "по файлу, в котором указаны шаблоны замены.\n\n" \
               "Существует два типа файлов со шаблонами: .txt и Excel файлы\n\n" \
               "  -  Если выбран файл .txt с шаблонами:\n" \
               "Обработанные  строки для  файла(-ов) в  зависимости  от столбца \"Rotation\"\n" \
               "и информации, указанной в  файле с шаблонами  замены, распределяются по трём\n" \
               "файлам:\n" \
               " 1)Top;\n 2)Bottom;\n 3)Delete.\n\n" \
               "В файл \"Delete\" отправляются строки для которых в файле шаблона указано delete,\n" \
               f"строки содержащие шаблон \"~FV\", \"{TEMPLATE_REPEAT_1}\", \"{TEMPLATE_REPEAT_2}\"\n\n" \
               "  -  Если выбран файл Excel с шаблонами:\n" \
               "Данные из .csv файла проверяются на равенство по шаблону из Excel файла.\n" \
               "Равенство проверяется по значениям из колонок \"Footprint\" и \"Comment\".\n" \
               "Если были найдены неравенства, то создаются два файла с префиками ZAMENA_ и NEW_.\n\n" \
               " 1) ZAMENA_ - файл содержит строки, в которых программа нашла отличия;\n" \
               " 2) NEW_ - обновленные строки в соответствии со шаблоном.\n\n" \
               "Для  обработанных  файлов  генерируется  папка с  именем \"Output\" и  временем \n" \
               "начала обработки .csv файлов."
        info = Label(sub_master, text=text, justify="left").pack()
        sub_master.mainloop()

    def _get_save_location(self):
        self.save_location = fd.askdirectory(
            title="Выбор место сохранения обработанного файла"
        )

    def _get_processed_file(self):
        self.processed_file = fd.askopenfilename(
            title="Выберите файл для обработки",
            filetypes=(
                ("CSV Files", ".csv"),
            )
        )

    def _get_template(self):
        self.template_excel_file = fd.askopenfilename(
            title="Выберите Excel файл с шаблонами",
            filetypes=[("Excel files", ".xlsx .xls")]
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

    def choose_template_txt(self):
        new_template_txt = fd.askopenfilename(
            title="Выберите TXT файл с шаблонами",
            filetypes=[('text files', 'txt')]
        )

        if new_template_txt != "":
            self.template_txt = new_template_txt
            # set new path to txt input file in config.ini
            set_config(
                path_to_config=PATH_TO_CONFIG,
                path_to_template=self.template_txt
            )

    def _start_processing(self):

        self.info.delete(1.0, END)

        if self.processed_file == "":
            self.info.insert(END, "ОШИБКА! Не выбраны .CSV файл для обработки!\n")
            return
        self.info.insert(END, f"Выбран .CSV файл для обработки:\n{self.processed_file}\n\n")

        if self.save_location == "":
            self.info.insert(END, "ОШИБКА! Не выбрана папка для сохранения файлов!\n")
            return
        self.info.insert(END, f"Выбрано место для сохранения обработанных файлов:\n{self.processed_file}\n\n")

        csv_file = csvFile(
            name_csv_file=self.processed_file
        )

        ind = self.notebook.select()
        # ind == 0: Excel file processing
        # ind == 1: TXT file processing

        if self.notebook.tabs().index(ind) == 0:
            self.save_location += f"/EXCEL_output_{str(datetime.now())[:-6]}".replace(":", ".")

            if self.template_excel_file == "":
                self.info.insert(END, "ОШИБКА! Не выбран шаблон Excel для замены значений в .csv файле!\n")
                return

            self.info.insert(END, f"Выбран шаблон Excel файла для обработки:\n{self.template_excel_file}\n\n")
            self.info.insert(END, "Выбрана обработка Excel файлом.\n\n")

            log = csv_file.excel_file_processing(
                file_excel_template=self.template_excel_file,
                name_save_dir=self.save_location
            )

        elif self.notebook.tabs().index(ind) == 1:
            self.save_location += f"/TXT_output_{str(datetime.now())}".replace(":", ".")
            self.info.insert(END, f"Автоматически выбран шаблон .txt для обработки:\n{self.template_txt}.\n\n")
            self.info.insert(END, "Выбрана обработка TXT файлом.\n\n")

            log = csv_file.txt_file_processing(
                name_save_dir=self.save_location,
                name_template=self.template_txt,
                mode=self.mode_save_file.get()
            )

        self.info.insert(END, log)

    def _close_app(self):
        if askokcancel("Выход", "Вы хотите выйти из программы?"):
            root.destroy()


if __name__ == "__main__":
    # path_to_template = load_preference()
    path_to_template = os.getcwd() + rf"\template.txt"

    if os.path.exists(path_to_template):

        root = Tk()
        app = App(
            root,
            path_to_template
        )
        root.mainloop()
    else:
        showwarning(
            title="Не найден .txt файл с шаблонами замены",
            message="Не найден файл input.txt."
                    " Поместите в ту же директорию, в которой запущена программа файл input.txt.\n"
                    "Работа программы прекращена."
        )

    # set path to input txt file
    # set_config(
    #     template_file_name="./input.txt"
    # )

