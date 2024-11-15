import os
import csv
import argparse
from icrawler.builtin import GoogleImageCrawler
from iterator import ImageIterator


def download_images(keyword: str, download_folder: str, num_images: int = 100) -> list[str]:

    """
    Функция для скачивания изображений по заданному ключевому слову в указанную папку.
    Arg:
    keyword (str): Ключевое слово для поиска изображений.
    download_folder (str): Папка для загрузки изображений.
    num_images (int, необязательно): Максимальное количество изображений для скачивания. По умолчанию 100.
    Returns:
    image_paths (list): Список путей к скачанным изображениям.
    """

    crawler = GoogleImageCrawler(storage={"root_dir": download_folder})
    crawler.crawl(keyword=keyword, max_num=num_images)

    image_paths = []
    for dirname, _, filenames in os.walk(download_folder):
        for filename in filenames:
            if filename.endswith(('.jpg', '.jpeg', '.png')):
                image_paths.append(os.path.join(dirname, filename))

    return image_paths


def save_annotation(image_paths: list[str], annotation_file: str):

    """
        Функция для сохранения аннотаций (абсолютный и относительный пути) к изображениям в CSV-файл.
        Arg:
        image_paths (list): Список путей к изображениям.
        annotation_file (str): Путь к файлу для сохранения аннотаций.
    """

    with open(annotation_file, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['absolute_path', 'relative_path'])

        for image_path in image_paths:
            absolute_path = os.path.abspath(image_path)
            relative_path = os.path.relpath(image_path, start=os.path.dirname(annotation_file))
            writer.writerow([absolute_path, relative_path])


def main():

    """
    Основная функция, которая управляет скачиванием изображений и сохранением аннотаций.
    """

    parser = argparse.ArgumentParser(description="Скачивание изображений по ключевому слову.")
    parser.add_argument("keyword", type=str, help="Ключевое слово для поиска изображений")
    parser.add_argument("download_folder", type=str, help="Папка для загрузки изображений")
    parser.add_argument("annotation_file", type=str, help="Файл для сохранения аннотаций")
    args = parser.parse_args()
    keyword = args.keyword
    download_folder = args.download_folder
    annotation_file = args.annotation_file
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)
    image_paths = download_images(keyword, download_folder)
    save_annotation(image_paths, annotation_file)
    image_iterator = ImageIterator(annotation_file)
    for image_path in image_iterator:
        print(image_path)


if __name__ == "__main__":
    main()