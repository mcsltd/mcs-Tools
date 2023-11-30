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

        with open(self.name_csv_file, "r") as file, open(NAME_BUFFER_FILE, "w") as temp_file:
            for line in file.readlines():

                if TABLE_START_TEMPLATE in line:
                    # add begin of table in file DELETE
                    header.append(line)
                    flag = True

                # the beginning of the column names was encountered
                if flag:
                    temp_file.write(line)
                else:
                    header.append(line)

        return header

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

        # get header
        delete = self.delete_header().copy()

        # get delete string in table
        delete.extend(self.delete_template_repeat())

        # save delete data
        self._create_delete_file(name_delete_file, delete)

    def _create_delete_file(self, file_name, data):
        with open(file_name, "w") as file:
            file.writelines(data)

    def txt_file_processing(self, name_template):
        # get templates
        # templates = self._get_template_txt_file(name_template)
        pass

    def _get_template_txt_file(self, name_template):
        """
        Get template from txt file.
        :param name_template: str
        :return: dict
        """
        t = {}
        symbols = ["\'", "\"", "\n"]

        with open(name_template, "r") as file_template:
            lines = file_template.readlines()
            for ln in lines:
                if ln != "\n":
                    for el in symbols:
                        ln = ln.replace(el, "")
                    ln = ln.split()
                    t.update({ln[0]: ln[1]})
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
        self.preprocessing(name_delete_file)

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

        with open(name_new_file, "w", newline="") as new_file, open(name_sink_file, "w", newline="") as sink_file:
            # name of columns
            name_keys = list(sink[0].keys())

            # save new data in file with prefix NEW_
            csv_writer_new = DictWriter(new_file, fieldnames=name_keys.copy())
            csv_writer_new.writeheader()
            csv_writer_new.writerows(data)

            # save old version changed data in file with prefix ZAMENA_
            csv_writer_sink = DictWriter(sink_file, fieldnames=name_keys.copy())
            csv_writer_sink.writeheader()
            csv_writer_sink.writerows(sink)


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


if __name__ == "__main__":
    ex_proc_excel_file()
