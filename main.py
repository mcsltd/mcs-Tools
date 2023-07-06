import csv
import os

SYMBOLS = ["\'", "\"", "\n"]

TEMPLATE_NAME_1 = "Designator"
TEMPLATE_NAME_2 = "~FV"

NAME_BUFFER_FILE = "temp.csv"



def preprocess_data(name_data):

    with open(name_data, "r") as txt_file, open(NAME_BUFFER_FILE, "w") as temp:
        flag = False
        for line in txt_file.readlines():

            # looking for the beginning of the cap
            if TEMPLATE_NAME_1 in line:
                flag = True

            if flag:
                if not(TEMPLATE_NAME_2 in line):
                    print(line.replace("\"", ""), file=temp, end="")


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


def process_data(data, template):
    # remove unwanted lines and symbols
    preprocess_data(data)

    # get templates
    templates = get_templates(template)

    file_output = "output_" + data

    with open(NAME_BUFFER_FILE) as csv_file, open(file_output, "w", newline="") as out_csv_file:

        csv_reader = list(csv.DictReader(csv_file))
        name_keys = list(csv_reader[0].keys())

        csv_writer = csv.DictWriter(out_csv_file, fieldnames=name_keys.copy())
        csv_writer.writeheader()

        proc_data = []
        name_keys.append(None)

        for row in csv_reader:
            for sign in name_keys:

                if sign == "Rotation":
                    row[sign] = templates[row[sign]]

                if sign == "Layer":
                    row[sign] = templates[row[sign]]

                if sign == "Footprint":
                    if row[sign] in templates:
                        if templates[row[sign]] == "delete":
                            row[sign] = ""
                        else:
                            row[sign] = templates[row[sign]]

                if sign == "Comment":
                    row[sign] = row[sign].replace(" ", "_").replace("\n", "")

                if sign in row and sign == None:
                    row[name_keys[len(name_keys) - 2]] = row[name_keys[len(name_keys) - 2]] + row[sign][0].replace("\n", "")
                    row.pop(sign)
            proc_data.append(row.copy())

        csv_writer.writerows(proc_data)



def main():
    inpt = input("Input data: ")
    template = input("Input name template: ")
    process_data(inpt, template)

    try:
        os.remove(NAME_BUFFER_FILE)
    except Exception as err:
        print(f"Cannot remove file {err}")


if __name__ == "__main__":
    main()