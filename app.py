from tkinter import *


class App:
    def __init__(self, master, func):
        """
        Constructor
        :param master:
        :param func:
        """
        self.master = master

        # function processing csv file
        self.func = func

        # text file names for saving, processing
        self.input_file = None
        self.template_file = "template.txt"
        self.save_location = None

        # input field for the name of processed files
        self.lab_input = Label(master, text="Введите файл или папку для обработки: ")
        self.ent_input = Entry(master, width=20)

        # substitution template file
        self.lab_template = Label(master, text="Введите название файла-шаблона: ")
        self.ent_template = Entry(master, width=20)

        # where to save processed files
        self.lab_save = Label(master, text="Введите место сохранения обработанного файлов: ")
        self.ent_save = Entry(master, width=20)

        # button start process
        self.btn_start = Button(master, text="Cтарт")

        # button click event binding
        self.btn_start["command"] = self.press_start

        self._setUI()

    def _setUI(self):
        """
        Сustomization and arrangement of elements in the application
        :return:
        """
        # name of application
        self.master.title("Обработчик .csv файлов")

        # get width and height of main screen
        width = self.master.winfo_screenwidth()
        height = self.master.winfo_screenheight()
        width_app = 575
        heght_app = 180

        # set application location
        loc = f'{width_app}x{heght_app}+{height // 2 + heght_app // 2}+{width // 2 + width_app // 2}'
        self.master.geometry(loc)

        self.lab_input.grid(row=0, column=0, sticky=W, padx=10, pady=10)
        self.ent_input.grid(row=0, column=1, sticky=E, padx=10, pady=10)

        self.lab_template.grid(row=1, column=0, sticky=W, padx=10, pady=10)
        self.ent_template.grid(row=1, column=1, sticky=E, padx=10, pady=10)

        self.lab_save.grid(row=2, column=0, sticky=W, padx=10, pady=10)
        self.ent_save.grid(row=2, column=1, sticky=E, padx=10, pady=10)

        self.btn_start.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    def press_start(self):
        """
        Button click handler
        :return:
        """
        # getting data from a field
        self.input_file = self.ent_input.get()
        self.template_file = self.ent_template.get()
        self.save_location = self.ent_save.get()

        self.func(self.input_file, self.template_file, self.save_location)



