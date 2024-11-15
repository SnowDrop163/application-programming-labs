import cv2
import numpy as np
import matplotlib.pyplot as plt
import argparse
import os

def read_image(image_path: str) -> tuple:

    """
    Функция для чтения изображения из указанного пути.

    Arg:
    image_path: Путь к изображению для чтения.

    Return:
    tuple: Кортеж, содержащий изображение, ширину и высоту изображения.
    """

    try:
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError("The image could not be uploaded.")
        return image, image.shape[1], image.shape[0]
    except Exception as e:
        raise RuntimeError(f"Error (image reader): {e}")

def plot_histogram(image: np.ndarray) -> None:

    """
    Функция для построения гистограммы цветовых каналов изображения.

    Arg:
    image: Изображение, для которого будет построена гистограмма.
    """

    colors = ('b', 'g', 'r')
    plt.figure(figsize=(10, 5))
    for i, color in enumerate(colors):
        hist = cv2.calcHist([image], [i], None, [256], [0, 256])
        plt.plot(hist, color=color)
        plt.xlim([0, 256])
    plt.title("Image Histogram")
    plt.xlabel("Intensity")
    plt.ylabel("Frequency")
    plt.legend(['Blue', 'Green', 'Red'])
    plt.show()

def split_and_save_channels(image: np.ndarray, output_dir: str) -> list:

    """
    Функция для разделения цветовых каналов изображения и сохранения их в указанной директории.

    Arg:
    image: Исходное изображение для разделения.
    output_dir : Директория для сохранения отдельных каналов.

    Returns:
    saved_channels: Список кортежей, содержащих имена и массивы сохраненных каналов.
    """

    try:
        channels = cv2.split(image)
        channel_names = ['blue', 'green', 'red']
        saved_channels = []
        for i, channel in enumerate(channels):
            save_path = os.path.join(output_dir, f"{channel_names[i]}_channel.png")
            cv2.imwrite(save_path, channel)
            saved_channels.append((channel_names[i], channel))
        return saved_channels
    except Exception as e:
        raise RuntimeError(f"Error (save channel): {e}")

def display_image(image: np.ndarray, title: str = "Original image", width: str = None, height: int = None) -> None:

    """
    Функция для отображения изображения с заданным заголовком и его размером.

    Arg:
    image: Изображение для отображения.
    title: Заголовок для изображения.
    width: Ширина изображения.
    height: Высота изображения.
    """

    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.title(f"{title} (Size: {width} x {height})" if width and height else title)
    plt.axis('off')
    plt.show()

def main(image_path: str, output_dir: str) -> None:

    """
    Основная функция для обработки изображения: чтение, построение гистограммы,
    отображение изображения и сохранение цветовых каналов.

    Arg:
    image_path: Путь к изображению для обработки.
    output_dir: Директория для сохранения результатов.
    """

    try:
        image, width, height = read_image(image_path)
        plot_histogram(image)
        display_image(image, title="Original image", width=width, height=height)
        saved_channels = split_and_save_channels(image, output_dir)
        for channel_name, channel in saved_channels:
            display_image(channel, title=f"Channel: {channel_name}", width=channel.shape[1], height=channel.shape[0])

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Image Processing.")
    parser.add_argument("image_path", type=str, help="Path to the image for processing")
    parser.add_argument("output_dir", type=str, help="Directory to save results")

    args = parser.parse_args()
    os.makedirs(args.output_dir, exist_ok=True)
    main(args.image_path, args.output_dir)
