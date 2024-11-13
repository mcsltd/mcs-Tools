def separate_string(string):
    return string[::-1].replace(";", "\n", 2)[::-1]


def read_txt(path_to_txt: str):
    with open(path_to_txt, "r", encoding="utf-8") as file:
        lines = file.readlines()
        lines = list(filter(lambda x: x != "\n", lines))
        lines = [l.replace("\n", "").split(";") for l in lines]
    return lines