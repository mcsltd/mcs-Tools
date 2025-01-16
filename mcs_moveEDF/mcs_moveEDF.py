import os
import shutil
import argparse

def get_eeg_file_names_in_dir(path_to_dir) -> list:
    try:
        files = os.listdir(path_to_dir)
        file_names = [
            f for f in files if os.path.isfile(os.path.join(path_to_dir, f)) and ".edf" in f
        ]
        return file_names
    except FileNotFoundError:
        print(f"Ошибка: Директория '{path_to_dir}' не найдена.")
        return []
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return []


def read_txt(path_to_txt) -> list:

    with open(path_to_txt, "r", encoding="utf-8") as txt:
        file_names = [f.replace(".EEG", ".edf").replace("\n", "") for f in txt.readlines()]

    return file_names


def move_files(files: list, save_dir: str):
    """
    Перемещает указанные файлы в указанную директорию.

    :param files: Список файлов для перемещения.
    :param save_dir: Директория, в которую будут перемещены файлы.
    """
    if not os.path.exists(save_dir):
        print(f"Ошибка: Директория '{save_dir}' не существует.")
        return

    for file in files:
        try:
            if os.path.isfile(file):
                shutil.move(file, save_dir)
        except Exception as e:
            print(f"Произошла ошибка при перемещении файла '{file}': {e}")


if __name__ == "__main__":
    # inp = "./input"
    # txt = "list.txt"
    # out = "./output"

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", type=str,
                        # default=inp
                        )
    parser.add_argument("-t", "--txt", type=str,
                        # default=txt
                        )
    parser.add_argument("-o", "--output", type=str,
                        # default=out
                        )
    args = parser.parse_args()

    # read all files in dir
    dir_edf_files: list = get_eeg_file_names_in_dir(path_to_dir=args.input)

    # read TXT file and get name edf files
    edf_files: list = read_txt(path_to_txt=args.txt)

    moved_files = set(dir_edf_files) - set(edf_files)
    moved_files = [f"{args.input}/{f}" for f in moved_files]
    print(f"Всего будет перемещено EDF файлов {len(moved_files)} в папку с названием {args.output}")

    # move edf files which not in list
    move_files(files=moved_files, save_dir=args.output)
