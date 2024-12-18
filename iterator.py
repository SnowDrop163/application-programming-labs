import csv

class ImageIterator:
    def __init__(self, annotation_file: str):
        """
        Инициализация объекта ImageIterator с заданным файлом аннотаций.

        Args:
            annotation_file (str): Путь к файлу аннотаций.
        """
        self.annotation_file = annotation_file
        self.image_paths = []
        self.current_index = 0
        self.load_annotations()

    def load_annotations(self) -> None:
        """
        Метод для загрузки путей к изображениям из файла аннотаций.
        Пути сохраняются в список self.image_paths.
        """
        with open(self.annotation_file, mode='r') as f:
            reader = csv.reader(f)
            next(reader)  # Пропускаем заголовок
            self.image_paths = [row[0] for row in reader]

    def __iter__(self) -> 'ImageIterator':
        """
        Метод, который возвращает сам объект ImageIterator при итерации над ним.

        Returns:
            ImageIterator: Сам объект итератора.
        """
        return self

    def __next__(self) -> str:
        """
        Метод, который возвращает следующий путь к изображению при итерации.

        Returns:
            str: Путь к следующему изображению.

        Raises:
            StopIteration: Если все пути уже пройдены.
        """
        if self.current_index < len(self.image_paths):
            image_path = self.image_paths[self.current_index]
            self.current_index += 1
            return image_path
        else:
            raise StopIteration
