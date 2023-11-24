from pprint import pprint

import pandas as pd

FILENAME = "BOM.xls"

# head of columns in excel file
COLUMN_REFERENCE = "Reference"
COLUMN_FOOTPRINT = "Footprint"
COLUMN_PART = "Part"

# head of columns in csv file
CSV_COLUMN_FOOTPRINT = "Footprint"
CSV_COLUMN_COMMENT = "Comment"


def _get_references(ref):
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
    xl = pd.ExcelFile(filename)

    # get first sheet in excel file
    df = xl.parse(xl.sheet_names[0])

    template = {}
    last_foot = ""
    last_part = ""

    for ref, foot, part in zip(df[COLUMN_REFERENCE], df[COLUMN_FOOTPRINT], df[COLUMN_PART]):
        # print(ref, " - ", part, " - ", foot)

        # get list of references
        ref = _get_references(ref)

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


def main():
    pprint(get_template_excel_file(filename=FILENAME))


if __name__ == "__main__":
    main()
