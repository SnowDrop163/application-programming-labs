import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QFileDialog, QVBoxLayout, QWidget, QMessageBox
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from iterator import ImageIterator

class MainWindow(QMainWindow):
    def __init__(self):
        """
        Инициализация главного окна приложения.
        """
        super().__init__()
        self.setWindowTitle("Image Viewer")
        self.setGeometry(100, 100, 800, 600)

        self.layout = QVBoxLayout()
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.image_label)

        self.load_button = QPushButton("Load Annotation File", self)
        self.load_button.clicked.connect(self.load_annotations)
        self.layout.addWidget(self.load_button)

        self.next_button = QPushButton("Next Image", self)
        self.next_button.clicked.connect(self.show_next_image)
        self.next_button.setEnabled(False)
        self.layout.addWidget(self.next_button)

        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

        self.image_iterator = None

    def load_annotations(self) -> None:
        """
        Загружает файл аннотаций и инициализирует итератор изображений.
        """
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Select Annotation CSV File", "", "CSV Files (*.csv);;All Files (*)", options=options)
        if file_name:
            try:
                self.image_iterator = ImageIterator(file_name)
                self.next_button.setEnabled(True)
                self.show_next_image()
            except Exception as e:
                self.show_error_message(f"Error loading annotations: {str(e)}")

    def show_next_image(self) -> None:
        """
        Отображает следующее изображение из итератора.
        """
        if self.image_iterator:
            try:
                image_path = next(self.image_iterator)
                pixmap = QPixmap(image_path)
                self.image_label.setPixmap(pixmap.scaled(self.image_label.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
            except StopIteration:
                self.image_label.setText("No more images to display.")
            except Exception as e:
                self.show_error_message(f"Error displaying image: {str(e)}")

    def show_error_message(self, message: str) -> None:
        """
        Отображает сообщение об ошибке.

        Args:
            message (str): Сообщение об ошибке для отображения.
        """
        QMessageBox.critical(self, "Error", message)

def main() -> None:
    """
    Главная функция для запуска приложения.
    """
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
