import pandas as pd
import cv2
import matplotlib.pyplot as plt
import argparse



def get_image_dimensions(image_path: str) -> tuple:

    """
    Функция для получения размеров изображения.

    Arg:
    image_path: Путь к изображению для чтения.

    Return:
    tuple: Кортеж, содержащий высоту, ширину и количество каналов изображения.
    """

    try:
        img = cv2.imread(image_path)
        if img is not None:
            height, width, depth = img.shape
            return height, width, depth
        else:
            raise ValueError(f"Не удалось открыть изображение -> {image_path}")
    except Exception as e:
        print(f"Ошибка при обработке изображения -> {image_path}: {e}")
        return None, None, None


def filter_images(df: pd.DataFrame, max_width: int, max_height: int) -> pd.DataFrame:

    """
    Функция для фильтрации DataFrame по максимальным значениям ширины и высоты.

    Arg:
    df: DataFrame с данными изображений.
    max_width: Максимальная ширина для фильтрации.
    max_height: Максимальная высота для фильтрации.

    Return:
    DataFrame: Отфильтрованный DataFrame.
    """

    return df[(df['width'] <= max_width) & (df['height'] <= max_height)]


def read_annotations(annotation_file: str) -> pd.DataFrame:

    """
    Функция для чтения аннотаций из файла.

    Arg:
    annotation_file: Путь к файлу аннотаций (CSV).

    Return:
    DataFrame: DataFrame с аннотациями изображений.
    """

    try:
        df = pd.read_csv(annotation_file, header=None, names=['absolute_path', 'relative_path'])
        return df
    except Exception as e:
        raise ValueError(f"Ошибка при чтении файла аннотаций -> {e}")


def add_image_dimensions(df: pd.DataFrame) -> pd.DataFrame:

    """
    Функция для добавления размеров изображений в DataFrame.

    Arg:
    df: DataFrame с путями к изображениям.

    Return:
    DataFrame: DataFrame с добавленными размерами изображений.
    """

    df[['height', 'width', 'depth']] = df['absolute_path'].apply(get_image_dimensions).apply(pd.Series)
    df.dropna(inplace=True)
    return df


def compute_statistics(df: pd.DataFrame) -> pd.DataFrame:

    """
    Функция для вычисления статистической информации по размерам изображений.

    Arg:
    df: DataFrame с размерами изображений.

    Return:
    DataFrame: Статистическая информация о размерах изображений.
    """

    return df[['height', 'width', 'depth']].describe()


def plot_area_distribution(df: pd.DataFrame) -> None:

    """
    Функция для создания гистограммы распределения площадей изображений.

    Arg:
    df: DataFrame с данными изображений, включая площади.
    """

    plt.figure(figsize=(10, 6))
    plt.hist(df['area'], bins=30, color='blue', alpha=0.7)
    plt.title('Распределение площадей изображений')
    plt.xlabel('Площадь (пиксели)')
    plt.ylabel('Частота')
    plt.grid(axis='y', alpha=0.75)
    plt.show()

def main() -> None:
    parser = argparse.ArgumentParser(description='Анализ изображений из файла аннотаций.')
    parser.add_argument('annotation_file', type=str, help='Путь к файлу')
    parser.add_argument('--max_width', type=int, default=1920, help='Максимальная ширина для фильтра')
    parser.add_argument('--max_height', type=int, default=1080, help='Максимальная высота для фильтра')
    args = parser.parse_args()

    try:
        df = read_annotations(args.annotation_file)
        df = add_image_dimensions(df)
        stats = compute_statistics(df)
        print("Статистическая информация:\n", stats)
        df['area'] = df['height'] * df['width']
        print("Не отфильтрованный DataFrame:\n", df)
        filtered_df = filter_images(df, max_width=args.max_width, max_height=args.max_height)
        print("Отфильтрованный DataFrame:\n", filtered_df)
        df_sorted = df.sort_values(by='area')
        plot_area_distribution(df_sorted)

    except Exception as e:
        print(f"Произошла ошибка -> {e}")

if __name__ == "__main__":
    main()
