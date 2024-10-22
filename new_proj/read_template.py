import pandas as pd


def read_xl(path_to_xl: str):
    xl = pd.ExcelFile(path_to_xl)
    df = xl.parse(xl.sheet_names[0])
    d = df.to_dict("index")
    template = [d[i] for i in d.keys()]
    return template


if __name__ == "__main__":
    read_xl(path_to_xl="template/template_sn.xlsx")
