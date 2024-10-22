import argparse
import re


def get_file() -> str:
    """

    Извлекает путь к файлу из командной строки.

    Return:
    str: Имя файла.

    """
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', type=str, help='name of your file')
    args = parser.parse_args()
    return args.filename


def read_file(filename: str) -> str:
    """

    Открывает файл и читает содержимое файла.

    Arg:
    filename (str): Имя файла.

    Return:
    str: Содержимое файла.

    """
    try:
        with open(filename, "r", encoding="UTF-8") as file:
            return file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл '{filename}' не найден.")


def find_female_names(content: str) -> set:
    """
    
    Находит все женские имена, начинающиеся с буквы A, в заданном тексте.

    Arg:
    content (str): Текст, в котором нужно выполнить поиск.

    Return:
    set: Множество женских имен, начинающихся с буквы A.

    """
    pattern = r'Имя: (А\w+)\sПол: Женский'
    matches = re.findall(pattern, content)
    female_names = set(match for match in matches)
    return female_names


def print_female_names(names: set) -> None:
    """

    Выводит все найденные женские имена, начинающиеся с буквы А.

    Arg:
    names (set): Множество женских имен, начинающихся с буквы А.

    """
    if names:
        print("Женские имена, начинающиеся с буквы А:")
        for name in names:
            print(name)
    else:
        print("Нет женских имен, начинающихся с буквы А.")

def main() -> None:
    try:
        filename = get_file()
        file_content = read_file(filename)
        female_names = find_female_names(file_content)
        print_female_names(female_names)
    except ValueError as exc:
        print(f"Ошибка: {exc}")


if __name__ == '__main__':
    main()
