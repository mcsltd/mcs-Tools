import csv
import datetime
import os.path
from pprint import pprint

import pandas as pd

from app import *

TEMPLATE_NAME_1 = "Designator"
TEMPLATE_NAME_2 = "~FV"

TEMPLATE_REPEAT_1 = "MCS_WORK/MECH/"
TEMPLATE_REPEAT_2 = "MCS_WORK/COMMON/FIDUCIAL_MARK"
# TEMPLATE_REPEAT_2 = "MCS_WORK/COMMON/"

NAME_BUFFER_FILE = "temp.csv"

SYMBOLS = ["\'", "\"", "\n"]


def preprocess_data(name_data):
    with open(name_data, "r") as txt_file, open(NAME_BUFFER_FILE, "w") as temp:
        flag = False
        cnt_str = 0
        cap = []
        for line in txt_file.readlines():
            # looking for the beginning of the cap
            if TEMPLATE_NAME_1 in line:
                flag = True
            if flag:
                cnt_str += 1
                print(line.replace("\"", ""), file=temp, end="")
            else:
                cap.append(line)
        return cap, cnt_str - 1


def get_template_txt_file(template):
    t = {}
    with open(template, "r") as file_t:
        lines = file_t.readlines()
        for l in lines:
            if l != "\n":
                for el in SYMBOLS:
                    l = l.replace(el, "")
                l = l.split()
                t.update({l[0]: l[1]})
    return t


def create_dir(name_dir):
    if os.path.exists(name_dir):
        return
    else:
        os.mkdir(name_dir)
        # app.info.insert(END,
        #                 f"Обработанные .csv файлы сохраняются в папке {name_dir}\n"
        #                 )


def processing_txt_file(csvfile, template, name_save_dir):
    """
    A function that processes a .csv file with a .txt file
    :param csvfile:
    :param template:
    :param name_save_dir:
    :return:
    """

    name_csv_file = csvfile[csvfile.rfind("/") + 1:]
    log = f"Общее количество строк в обрабатываемом файле {name_csv_file}"

    # remove unwanted lines and symbols
    cap, cnt = preprocess_data(csvfile)
    log += f" - {cnt}\n"

    # get templates
    templates = get_template_txt_file(template)

    # create dir for save processed file
    create_dir(name_save_dir)

    name_top_file = f"{name_save_dir}/TOP_{name_csv_file}"
    name_bot_file = f"{name_save_dir}/BOT_{name_csv_file}"
    name_del_file = f"{name_save_dir}/DELETE_{name_csv_file}"

    # app.info.insert(END, f"Созданы три файла для вывода обработанных значений:\n"
    #                      f" 1){name_top_file};\n"
    #                      f" 2){name_bot_file};\n"
    #                      f" 3){name_del_file}.")

    with open(NAME_BUFFER_FILE) as r_file, \
            open(name_top_file, "w", newline="") as top_file, \
            open(name_bot_file, "w", newline="") as bot_file, \
            open(name_del_file, "w", newline="") as del_file:

        csv_reader = list(csv.DictReader(r_file))
        name_keys = list(csv_reader[0].keys())

        csv_writer_top = csv.DictWriter(top_file, fieldnames=name_keys.copy())
        csv_writer_top.writeheader()

        csv_writer_bot = csv.DictWriter(bot_file, fieldnames=name_keys.copy())
        csv_writer_bot.writeheader()

        # write cap in delete file
        print(*cap, file=del_file)

        csv_writer_del = csv.DictWriter(del_file, fieldnames=name_keys.copy())
        csv_writer_del.writeheader()

        proc_data_top = []
        proc_data_bot = []
        proc_data_del = []

        name_keys.append(None)

        footprint_prev_top = ""
        footprint_prev_bot = ""
        buffer_top = ""
        buffer_bot = ""
        i = 0
        j = 0

        for row in csv_reader:
            flag_top = False
            flag_bot = False
            flag_del = False

            for sign in name_keys:

                if sign == "Designator":
                    if TEMPLATE_NAME_2 in row[sign]:
                        flag_del = True

                if sign == "Footprint":
                    if row[sign] in templates:
                        if templates[row[sign]] == "delete":
                            flag_del = True
                        else:
                            row[sign] = templates[row[sign]]
                    elif TEMPLATE_REPEAT_1 in row[sign]:
                        if row["Layer"] == "TopLayer":
                            buffer_top = row[sign]
                            if TEMPLATE_REPEAT_1 in footprint_prev_top:
                                i += 1
                                row[sign] = f"M{i}"
                            else:
                                i = 1
                                row[sign] = f"M{i}"
                        elif sign["Layer"] == "BottomLayer":
                            buffer_bot = row[sign]
                            if TEMPLATE_REPEAT_1 in footprint_prev_bot:
                                j += 1
                                row[sign] = f"M{i}"
                            else:
                                j = 1
                                row[sign] = f"M{i}"
                    elif TEMPLATE_REPEAT_2 in row[sign]:
                        if row["Layer"] == "TopLayer":
                            buffer_top = row[sign]
                            if TEMPLATE_REPEAT_2 in footprint_prev_top:
                                i += 1
                                row[sign] = f"F{i}"
                            else:
                                i = 1
                                row[sign] = f"F{i}"
                        elif row["Layer"] == "BottomLayer":
                            buffer_bot = row[sign]
                            if TEMPLATE_REPEAT_2 in footprint_prev_bot:
                                j += 1
                                row[sign] = f"F{i}"
                            else:
                                j = 1
                                row[sign] = f"F{i}"
                    else:
                        flag_del = True

                if sign == "Rotation":
                    row[sign] = templates[row[sign]]

                if sign == "Layer":
                    if row[sign] == "TopLayer" and not flag_del:
                        if buffer_top != "":
                            footprint_prev_top = buffer_top
                            buffer_top = ""
                        else:
                            footprint_prev_top = row["Footprint"]
                        flag_top = True
                    elif row[sign] == "BottomLayer" and not flag_del:
                        if buffer_bot != "":
                            footprint_prev_bot = buffer_bot
                            buffer_bot = ""
                        else:
                            footprint_prev_bot = row["Footprint"]
                        flag_bot = True
                    row[sign] = templates[row[sign]]

                if sign == "Comment":
                    row[sign] = row[sign].replace(" ", "_").replace("\n", "")

                if sign in row and sign is None:
                    row[name_keys[len(name_keys) - 2]] = row[name_keys[len(name_keys) - 2]] \
                                                         + row[sign][0].replace("\n", "")
                    row.pop(sign)

            if flag_bot:
                proc_data_bot.append(row.copy())
            elif flag_top:
                proc_data_top.append(row.copy())
            elif flag_del:
                proc_data_del.append(row.copy())

        csv_writer_top.writerows(proc_data_top)
        csv_writer_bot.writerows(proc_data_bot)
        csv_writer_del.writerows(proc_data_del)

    log += f"В обработанном файле TOP_{name_csv_file} - {len(proc_data_top)}\n"
    log += f"В обработанном файле BOT_{name_csv_file} - {len(proc_data_bot)}\n"
    log += f"В обработанном файле DELETE_{name_csv_file} - {len(proc_data_del)}\n\n"

    try:
        os.remove(NAME_BUFFER_FILE)
    except Exception as err:
        print(f"Cannot remove buffer file {err}")

    return log


def get_references(ref):
    """
    Converts a string with references to a list of references
    :param ref: str have format "smth1,smth2,smth3,"
    :return: list
    """
    ref = ref.replace(",", " ").split()
    return ref


def get_template_excel_file(filename):
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

        # get list of references
        ref = get_references(ref)

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


def get_data_csv_file(csvfilename):
    data = []
    with open(csvfilename) as read_file:
        file_reader = csv.DictReader(read_file, delimiter=",")
        for d in file_reader:
            data.append(d)
    return data


# Column names in the processed file.
COL_DESIGNATOR = "Designator"
COL_FOOTPRINT = "Footprint"
COL_COMMENT = "Comment"


def processing_xls_file(csvfile, file_xls_template, name_save_dir=None):
    """
    A function that processes a .csv file with a .xls file
    :param csvfile:
    :param template:
    :param name_save_dir:
    :return:
    """
    log = ""

    template = get_template_excel_file(file_xls_template)
    data = get_data_csv_file(csvfile)  # data for processing

    sink = []  # lines from the processed csv file that differ from the template

    name_csv_file = csvfile[csvfile.rfind("/") + 1:]
    # the name of the new file with changes
    name_new_file = f"{name_save_dir}/NEW_{name_csv_file}"
    # the names of the new file with old lines that have differences
    name_sink_file = f"{name_save_dir}/SINK_{name_csv_file}"

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

    if len(sink) != 0:
        # create dir for save processed file
        create_dir(name_save_dir)

        with open(name_new_file, "w", newline="") as new_file, open(name_sink_file, "w", newline="") as sink_file:
            # name of columns
            name_keys = list(sink[0].keys())

            csv_writer_new = csv.DictWriter(new_file, fieldnames=name_keys.copy())
            csv_writer_new.writeheader()
            csv_writer_new.writerows(data)

            csv_writer_sink = csv.DictWriter(sink_file, fieldnames=name_keys.copy())
            csv_writer_sink.writeheader()
            csv_writer_sink.writerows(sink)

        # create log for App
        log += f"В обрабатываемом файле\n {csvfile}\nбыло найдено {len(sink)} различий с файлом\n {file_xls_template}.\n"
        log += f"Все строки, в которых было найдено отличие по колонкам \"Footprint\" " \
               f"и \"Comment\", были заменены на значения из файла\n{file_xls_template}.\n"
    else:
        # create log for App
        log += f"Обрабатываемый файл\n{csvfile}\nи файл со шаблонами\n{file_xls_template}\nне имеет различий.\n"

    return log


def main():
    processing_funcs = [
        processing_txt_file,
        processing_xls_file
    ]

    # idle run function
    # pprint(processing_xls_file(
    #     csvfile="BOT_input.csv",
    #     file_xls_template="BOM.xls",
    #     name_save_dir="./"
    # ))

    root = Tk()
    # ToDo: add help in main window
    app = App(root, processing_funcs)
    root.mainloop()


if __name__ == "__main__":
    main()
