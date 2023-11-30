from csv import *

# buffer name file
NAME_BUFFER_FILE = "temp.csv"

TABLE_START_TEMPLATE = "Designator"

TEMPLATE_REPEAT_1 = "MCS_WORK/MECH/"
TEMPLATE_REPEAT_2 = "MCS_WORK/COMMON/FIDUCIAL_MARK"
TEMPLATE_REPEAT_3 = "~FV"


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

    def preprocessing(self):

        # get header
        delete = self.delete_header().copy()

        # get delete string in table
        delete.extend(self.delete_template_repeat())

        # ToDo: make function that create file DELETE_
        # self.create_delete_file(delete)

    def txt_file_processing(self, name_template):
        # get templates
        # templates = self._get_template_txt_file(name_template)
        pass

    # def _get_template_txt_file(self, name_template):
    #     """
    #     Get template from txt file.
    #     :param name_template: str
    #     :return: dict
    #     """
    #     t = {}
    #     symbols = ["\'", "\"", "\n"]
    #
    #     with open(name_template, "r") as file_template:
    #         lines = file_template.readlines()
    #         for ln in lines:
    #             if ln != "\n":
    #                 for el in symbols:
    #                     ln = ln.replace(el, "")
    #                 ln = ln.split()
    #                 t.update({ln[0]: ln[1]})
    #     return t

    def excel_file_processing(self, name_template):
        pass


if __name__ == "__main__":
    d = csvFile(name_csv_file="file.csv")
    d.preprocessing()
