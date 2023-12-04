from csv import *
import os

import pandas as pd

# buffer name file
NAME_BUFFER_FILE = "temp.csv"

TABLE_START_TEMPLATE = "Designator"

TEMPLATE_REPEAT_1 = "MCS_WORK/MECH/"
TEMPLATE_REPEAT_2 = "MCS_WORK/COMMON/FIDUCIAL_MARK"
TEMPLATE_REPEAT_3 = "~FV"


def create_dir(name_dir):
    if os.path.exists(name_dir):
        return
    else:
        os.mkdir(name_dir)


def get_data_csv_file(csvfilename):
    data = []
    with open(csvfilename) as read_file:
        file_reader = DictReader(read_file, delimiter=",")
        for d in file_reader:
            data.append(d)
    return data


class csvFile:
    def __init__(self, name_csv_file):
        self.name_csv_file = name_csv_file
        pass

    def delete_header(self):
        """
        Delete and return header in csv file.
        :return: list[str]
        """
        flag = False
        header = []

        log = ""
        with open(self.name_csv_file, "r") as file, open(NAME_BUFFER_FILE, "w") as temp_file:
            lines = file.readlines()
            log = f"Выбранный файл .CSV {self.name_csv_file} \n" \
                  f"имеет {len(lines)} строк. \n\n"
            for l in lines:

                if TABLE_START_TEMPLATE in l:
                    # add begin of table in file DELETE
                    header.append(l)
                    flag = True

                # the beginning of the column names was encountered
                if flag:
                    temp_file.write(l)
                else:
                    header.append(l)

        return log, header

    def delete_template_repeat(self):

        delete = []
        data = []

        # read data in buffer file and separate it
        with open(NAME_BUFFER_FILE, "r") as file:
            for line in file.readlines():
                if TEMPLATE_REPEAT_1 in line:
                    delete.append(line)
                elif TEMPLATE_REPEAT_2 in line:
                    delete.append(line)
                elif TEMPLATE_REPEAT_3 in line:
                    delete.append(line)
                else:
                    data.append(line)

        # write cleaned data in buffer file
        with open(NAME_BUFFER_FILE, "w") as file:
            file.writelines(data)

        return delete

    def preprocessing(self, name_delete_file):
        try:
            # get header
            log, delete = self.delete_header()

            # get delete string in table
            delete.extend(self.delete_template_repeat())

            # save delete data
            self._create_delete_file(name_delete_file, delete)

            ok = True
            log += "Сделана предобработка файла:\n"\
                   "- удалена шапка .CSV файла;\n"\
                   f"- удалены строки со символами:\n "\
                   f"{TEMPLATE_REPEAT_1, TEMPLATE_REPEAT_2, TEMPLATE_REPEAT_3}\n"\
                   f"Все удалённые строки сохранены в файле с префиксом DELETE_.\n" \
                   f"Всего удалённых строк: {len(delete)}.\n\n"
        except Exception as err:
            ok, log = (False, err)

        return ok, log

    def _create_delete_file(self, file_name, data):
        with open(file_name, "w") as file:
            file.writelines(data)

    def txt_file_processing(self, name_save_dir, name_template):
        # create dir for save processed file
        create_dir(name_save_dir)

        # name of create file
        name_csv_file = self.name_csv_file[self.name_csv_file.rfind("/") + 1:]

        # the name of the new file with changes
        name_top_file = f"{name_save_dir}/TOP_{name_csv_file}"
        # the names of the new file with old lines that have differences
        name_bot_file = f"{name_save_dir}/BOT_{name_csv_file}"
        # the names of the new file with old lines that have differences
        name_del_file = f"{name_save_dir}/DELETE_{name_csv_file}"

        # preprocess CSV data
        # create save dir, temp file, save delete data in file with prefix DELETE_
        ok, log = self.preprocessing(name_del_file)

        if not ok:
            log += "ВОЗНИКЛА ОШИБКА! Обработка .CSV файла не удалась!\n"
            return log

        # get templates
        template = self._get_template_txt_file(name_template)

        # for file top
        data_top = []
        # for file bottom
        data_bot = []
        # for file delete
        data_del = []

        with open(NAME_BUFFER_FILE) as data_file, \
                open(name_top_file, "w", newline="") as top_file, \
                open(name_bot_file, "w", newline="") as bot_file, \
                open(name_del_file, "a", newline="") as del_file:

            csv_data = list(DictReader(data_file))
            name_col = list(csv_data[0].keys())

            for row in csv_data:

                flag_bot = False
                flag_top = False
                flag_del = False

                for col in name_col:

                    if col == "Footprint":
                        if row[col] in template:
                            if str(template[row[col]]).lower() == "delete":
                                data_del.append(row.copy())
                                flag_del = True
                                break
                            else:
                                row[col] = template[row[col]]

                    if col == "Rotation" and row[col] in template:
                        row[col] = template[row[col]]

                    if col == "Comment":
                        row[col] = row[col].replace(" ", "_").replace("\n", "")

                    if col == "Layer":
                        if row[col] == "BottomLayer":
                            row[col] = "B"
                            flag_bot = True

                        elif row[col] == "TopLayer":
                            row[col] = "T"
                            flag_top = True

                # save processing data
                if flag_bot:
                    data_bot.append(row.copy())
                elif flag_top:
                    data_top.append(row.copy())
                elif flag_del:
                    data_del.append(row.copy())

            csv_writer_top = DictWriter(top_file, fieldnames=name_col.copy())
            csv_writer_top.writeheader()
            csv_writer_top.writerows(data_top)

            csv_writer_bot = DictWriter(bot_file, fieldnames=name_col.copy())
            csv_writer_bot.writeheader()
            csv_writer_bot.writerows(data_bot)

            csv_writer_del = DictWriter(del_file, fieldnames=name_col.copy())
            # csv_writer_del.writeheader()
            csv_writer_del.writerows(data_del)

            log += f"В обработанном файле TOP_{name_csv_file} - {len(data_top)}\n"
            log += f"В обработанном файле BOT_{name_csv_file} - {len(data_bot)}\n"
            log += f"В обработанном файле DELETE_{name_csv_file} - {len(data_del)}\n\n"

        os.remove(NAME_BUFFER_FILE)
        log += "Обработка .csv файла TXT файлом завершена."
        return log

    def _get_template_txt_file(self, name_template):
        """
        Get template from txt file.
        :param name_template: str
        :return: dict
        """
        t = {}
        symbols = ["\'", "\"", "\n"]
        log = ""
        try:
            with open(name_template, "r") as file_template:
                lines = file_template.readlines()
                for ln in lines:
                    if ln != "\n":
                        for el in symbols:
                            ln = ln.replace(el, "")
                        ln = ln.split()
                        t.update({ln[0]: ln[1]})
        except Exception:
            log += f"Отсуствует файл:\n {name_template}.\n\n"
        return t

    def excel_file_processing(self, file_excel_template, name_save_dir):
        # create dir for save processed file
        create_dir(name_save_dir)

        # name of create file
        name_csv_file = self.name_csv_file[self.name_csv_file.rfind("/") + 1:]
        # the name of the new file with changes
        name_new_file = f"{name_save_dir}/NEW_{name_csv_file}"
        # the names of the new file with old lines that have differences
        name_sink_file = f"{name_save_dir}/ZAMENA_{name_csv_file}"
        # the names of the new file with old lines that have differences
        name_delete_file = f"{name_save_dir}/DELETE_{name_csv_file}"

        # preprocess CSV data
        # create save dir, temp file, save delete data in file with prefix DELETE_
        ok, log = self.preprocessing(name_delete_file)

        if not ok:
            log += "ВОЗНИКЛА ОШИБКА! Обработка не удалась!\n"
            return log

        # Column names in the processed file.
        COL_DESIGNATOR = "Designator"
        COL_FOOTPRINT = "Footprint"
        COL_COMMENT = "Comment"

        # get template from Excel file
        template = self._get_template_excel_file(file_excel_template)

        data = get_data_csv_file(NAME_BUFFER_FILE)  # data for processing
        sink = []  # lines from the processed csv file that differ from the template

        for row in data:
            if row[COL_DESIGNATOR] in template:
                # name in column Designator
                dsg = row[COL_DESIGNATOR]

                if template[dsg][COL_FOOTPRINT] != row[COL_FOOTPRINT]:
                    # if there are differences, keep them
                    sink.append(row.copy())

                    # change the value in the Footprint column to the value in the same column from the template
                    row[COL_FOOTPRINT] = template[dsg][COL_FOOTPRINT]

                    if template[dsg][COL_COMMENT] != row[COL_COMMENT]:
                        # change the value in the Footprint column to the value in the same column from the template
                        row[COL_COMMENT] = template[dsg][COL_COMMENT]

        with open(name_new_file, "w", newline="") as new_file, \
                open(name_sink_file, "w", newline="") as sink_file:

            if len(data) == 0:
                name_keys = ""
                log += "Файл .CSV пустой!\n"
            else:
                # name of columns
                name_keys = list(sink[0].keys())

            # save new data in file with prefix NEW_
            csv_writer_new = DictWriter(new_file, fieldnames=name_keys)
            csv_writer_new.writeheader()
            csv_writer_new.writerows(data)

            # save old version changed data in file with prefix ZAMENA_
            csv_writer_sink = DictWriter(sink_file, fieldnames=name_keys)
            csv_writer_sink.writeheader()
            csv_writer_sink.writerows(sink)

            log += f"В обработанном файле NEW_{name_csv_file} - {len(data)}\n"
            log += f"В обработанном файле ZAMENA_{name_csv_file} - {len(sink)}\n"

        os.remove(NAME_BUFFER_FILE)

        log += "Обработка .csv файла Excel файлом завершена.\n"
        return log

    def _get_template_excel_file(self, filename):
        """
        Getting replacement templates for Designator in a CSV file
        :param filename: Excel file str
        :return: substitution template dict
        """
        # head of columns in excel file
        COLUMN_REFERENCE = "Reference"
        COLUMN_FOOTPRINT = "Footprint"
        COLUMN_PART = "Part"

        # head of columns in csv file
        CSV_COLUMN_FOOTPRINT = "Footprint"
        CSV_COLUMN_COMMENT = "Comment"

        xl = pd.ExcelFile(filename)

        # get first sheet in excel file
        df = xl.parse(xl.sheet_names[0])

        template = {}
        last_foot = ""
        last_part = ""

        for ref, foot, part in zip(df[COLUMN_REFERENCE], df[COLUMN_FOOTPRINT], df[COLUMN_PART]):
            # print(ref, " - ", part, " - ", foot)

            # check empty string in row
            if str(ref) == "nan":
                continue

            # get list of references
            ref = ref.replace(",", " ").split()

            # update value of Footprint and Part
            if str(foot) != "nan":
                last_foot = foot
            if str(part) != "nan":
                last_part = part

            # generating a template from an Excel file
            for r in ref:
                template[r] = {
                    CSV_COLUMN_FOOTPRINT: last_foot,
                    CSV_COLUMN_COMMENT: last_part
                }
        return template


def ex_proc_excel_file():
    import datetime
    d = csvFile(name_csv_file="file.csv")

    time = f"\EXCEL_output_{str(datetime.datetime.now())}".replace(":", ".")
    name_save_dir = rf"C:\Users\andmo\OneDrive\Desktop\my-dev-work\mcs-Tools\{time}"

    d.excel_file_processing(
        file_excel_template="BOM.xlsx",
        name_save_dir=name_save_dir
    )


def ex_proc_txt_file():
    import datetime
    d = csvFile(name_csv_file="file.csv")

    time = f"\TXT_output_{str(datetime.datetime.now())}".replace(":", ".")
    name_save_dir = rf"C:\Users\andmo\OneDrive\Desktop\my-dev-work\mcs-Tools\{time}"

    d.txt_file_processing(
        name_save_dir=name_save_dir,
        name_template="template_new.txt"
    )


if __name__ == "__main__":
    # ex_proc_excel_file()
    ex_proc_txt_file()
