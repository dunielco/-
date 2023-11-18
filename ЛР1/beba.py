import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt
from PIL import Image

class ChannelViewerApp(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        self.setWindowTitle("Лабораторная работа №1")
        self.setWindowIcon(QIcon("temp/meme.png"))
        self.setFixedSize(800, 800)
        
        layout = QVBoxLayout()

        self.load_image_button = QPushButton("Load Image")
        self.load_image_button.clicked.connect(self.load_image)
        layout.addWidget(self.load_image_button)
    
        self.red_channel_button = QPushButton("Red Channel")
        self.red_channel_button.clicked.connect(self.show_red_channel)
        self.red_channel_button.setEnabled(False)
        layout.addWidget(self.red_channel_button)

        self.green_channel_button = QPushButton("Green Channel")
        self.green_channel_button.clicked.connect(self.show_green_channel)
        self.green_channel_button.setEnabled(False)
        layout.addWidget(self.green_channel_button)

        self.blue_channel_button = QPushButton("Blue Channel")
        self.blue_channel_button.clicked.connect(self.show_blue_channel)
        self.blue_channel_button.setEnabled(False)
        layout.addWidget(self.blue_channel_button)

        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.image_label)

        self.setLayout(layout)
        self.image_path = ""
        self.current_channel = None
        self.red_image_path = ""
        self.green_image_path = ""
        self.blue_image_path = ""

    def load_image(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly

        file_dialog = QFileDialog()
        file_dialog.setNameFilter("Images (*.png *.jpg *.jpeg *.bmp *.gif)")
        selected_file, _ = file_dialog.getOpenFileName(self, "Open Image File", "", "Images (*.png *.jpg *.jpeg *.bmp *.gif);;All Files (*)", options=options)

        if selected_file:
            self.image_path = selected_file
            image = Image.open(self.image_path)

            # Разбиваем изображение на каналы RGB
            red_channel, green_channel, blue_channel = image.split()

            # Создаем цветные изображения для каждого канала
            self.red_image_path = "temp/red_image.png"
            self.green_image_path = "temp/green_image.png"
            self.blue_image_path = "temp/blue_image.png"

            red_image = Image.merge("RGB", (red_channel, Image.new('L', red_channel.size, 0), Image.new('L', red_channel.size, 0)))
            green_image = Image.merge("RGB", (Image.new('L', green_channel.size, 0), green_channel, Image.new('L', green_channel.size, 0)))
            blue_image = Image.merge("RGB", (Image.new('L', blue_channel.size, 0), Image.new('L', blue_channel.size, 0), blue_channel))

            red_image.save(self.red_image_path)
            green_image.save(self.green_image_path)
            blue_image.save(self.blue_image_path)

            self.current_channel = 'red'
            self.show_red_channel()

            self.red_channel_button.setEnabled(True)
            self.green_channel_button.setEnabled(True)
            self.blue_channel_button.setEnabled(True)

    def show_red_channel(self):
        if self.red_image_path:
            pixmap = QPixmap(self.red_image_path)
            pixmap = pixmap.scaled(self.image_label.size(), aspectRatioMode=1)
            self.image_label.setPixmap(pixmap)
            self.current_channel = 'red'

    def show_green_channel(self):
        if self.green_image_path:
            pixmap = QPixmap(self.green_image_path)
            pixmap = pixmap.scaled(self.image_label.size(), aspectRatioMode=1)
            self.image_label.setPixmap(pixmap)
            self.current_channel = 'green'

    def show_blue_channel(self):
        if self.blue_image_path:
            pixmap = QPixmap(self.blue_image_path)
            pixmap = pixmap.scaled(self.image_label.size(), aspectRatioMode=1)
            self.image_label.setPixmap(pixmap)
            self.current_channel = 'blue'

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ChannelViewerApp()
    window.show()
    sys.exit(app.exec_())