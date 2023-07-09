import csv
import datetime
import os.path

from new_app import *

TEMPLATE_NAME_1 = "Designator"
NAME_BUFFER_FILE = "temp.csv"
TEMPLATE_NAME_2 = "~FV"
SYMBOLS = ["\'", "\"", "\n"]


def preprocess_data(name_data):
    with open(name_data, "r") as txt_file, open(NAME_BUFFER_FILE, "w") as temp:
        flag = False
        i = 0
        j = 0
        for line in txt_file.readlines():

            # looking for the beginning of the cap
            if TEMPLATE_NAME_1 in line:
                flag = True
                # if i != 0:
                #     # app.info.insert(END, "  Шапка до \"Designator\" удалена!\n")
                # else:
                #     # app.info.insert(END, "  В файле не была найдена шапка!\n")

            if flag:
                if not(TEMPLATE_NAME_2 in line):
                    print(line.replace("\"", ""), file=temp, end="")
                else:
                    j += 1
            if j > 0:
                pass
                # app.info.insert(END, f" {j} строк содержащих {TEMPLATE_NAME_2} было удалено\n")
            i += 1


def get_templates(template):
    t = {}
    with open(template, "r") as file_t:
        lines = file_t.readlines()
        for l in lines:
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
    # remove unwanted lines and symbols
    preprocess_data(csvfile)

    # get templates
    templates = get_templates(template)

    name_top_file = f"{name_save_dir}/TOP_{csvfile}"
    name_bot_file = f"{name_save_dir}/BOT_{csvfile}"
    name_del_file = f"{name_save_dir}/DELETE_{csvfile}"

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

        flag_top = False
        flag_bot = False
        flag_del = False

        for row in csv_reader:
            for sign in name_keys:

                if sign == "Footprint":
                    if row[sign] in templates:
                        row[sign] = templates[row[sign]]
                    else:
                        flag_del = True

                if sign == "Rotation":
                    row[sign] = templates[row[sign]]

                if sign == "Layer":
                    if row[sign] == "TopLayer" and not flag_del:
                        flag_top = True
                    elif row[sign] == "BotLayer" and not flag_del:
                        flag_bot = True
                    row[sign] = templates[row[sign]]

                if sign == "Comment":
                    row[sign] = row[sign].replace(" ", "_").replace("\n", "")

                if sign in row and sign == None:
                    row[name_keys[len(name_keys) - 2]] = row[name_keys[len(name_keys) - 2]] + row[sign][0].replace("\n",
                                                                                                                   "")
                    row.pop(sign)

            if flag_bot:
                proc_data_bot.append(row)
            elif flag_top:
                proc_data_top.append(row)
            elif flag_del:
                proc_data_del.append(row.copy())

        top_file.writerows(proc_data_top)
        bot_file.writerows(proc_data_bot)
        del_file.writerows(proc_data_top)


def main():
    root = Tk()
    app = App(root, process_csvfile)
    root.mainloop()


if __name__ == "__main__":
    main()
