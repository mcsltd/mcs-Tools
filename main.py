import csv
import datetime
import os.path

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
        for line in txt_file.readlines():
            # looking for the beginning of the cap
            if TEMPLATE_NAME_1 in line:
                flag = True
            if flag:
                cnt_str += 1
                print(line.replace("\"", ""), file=temp, end="")
        return cnt_str - 1


def get_templates(template):
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


def process_csvfile(csvfile, template, name_save_dir):
    name_csv_file = csvfile[csvfile.rfind("/") + 1:]
    log = f"Общее количество строк в обрабатываемом файле {name_csv_file}"

    # remove unwanted lines and symbols
    log += f" - {preprocess_data(csvfile)}\n"

    # get templates
    templates = get_templates(template)

    # create dir for save processed file
    create_dir(name_save_dir)


    name_top_file = f"{name_save_dir}/TOP_{name_csv_file}"
    name_bot_file = f"{name_save_dir}/BOT_{name_csv_file}"
    name_del_file = f"{name_save_dir}/DELETE_{name_csv_file}"

    # app.info.insert(END, f"Созданы три файла для вывода обработанных значений:\n"
    #                      f" 1){name_top_file};\n"
    #                      f" 2){name_bot_file};\n"
    #                      f" 3){name_del_file}.")

    with open(NAME_BUFFER_FILE) as r_file,\
            open(name_top_file, "w", newline="") as top_file,\
            open(name_bot_file, "w", newline="") as bot_file,\
            open(name_del_file, "w", newline="") as del_file:

        csv_reader = list(csv.DictReader(r_file))
        name_keys = list(csv_reader[0].keys())

        csv_writer_top = csv.DictWriter(top_file, fieldnames=name_keys.copy())
        csv_writer_top.writeheader()

        csv_writer_bot = csv.DictWriter(bot_file, fieldnames=name_keys.copy())
        csv_writer_bot.writeheader()

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
                    row[name_keys[len(name_keys) - 2]] = row[name_keys[len(name_keys) - 2]]\
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


def main():
    root = Tk()
    app = App(root, process_csvfile)
    root.mainloop()


if __name__ == "__main__":
    main()

