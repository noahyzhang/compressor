import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QGridLayout, QFileDialog, QPushButton, QComboBox
from PyQt5.QtGui import QPixmap
from PIL import Image

class ImageCompressor(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Image Compressor'
        self.left = 10
        self.top = 10
        self.width = 800
        self.height = 800
        # self.formatComboBox = QComboBox(self)
        # self.formatComboBox.addItems(['JPEG', 'PNG', 'BMP', 'GIF'])
        self.image_path = None
        self.image_size_label = QLabel()
        self.image_size_label.setText('Image Size: ')
        self.image_size_value = QLabel()
        self.image_size_value.setText('')
        self.image_pixel_label = QLabel()
        self.image_pixel_label.setText('Image Pixel: ')
        self.image_pixel_value = QLabel()
        self.image_pixel_value.setText('')
        self.compress_button = QPushButton('Compress')
        self.compress_button.clicked.connect(self.compress_image)
        self.open_file_button = QPushButton('Open Image')
        self.open_file_button.clicked.connect(self.open_file_dialog)
        self.image_label = QLabel()
        self.image_label.setFixedSize(800, 800)
        layout = QGridLayout()
        layout.addWidget(self.image_label, 0, 0, 1, 2)
        layout.addWidget(self.image_size_label, 1, 0)
        layout.addWidget(self.image_size_value, 1, 1)
        layout.addWidget(self.image_pixel_label, 2, 0)
        layout.addWidget(self.image_pixel_value, 2, 1)
        layout.addWidget(self.open_file_button, 3, 0)
        layout.addWidget(self.compress_button, 3, 1)
        self.setLayout(layout)
        # self.setGeometry(300, 300, 800, 400)
        self.setWindowTitle('熊熊的图片压缩器')
        self.show()

    def open_file_dialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.image_path, _ = QFileDialog.getOpenFileName(self,"Open Image File", "","Image Files (*.png *.jpg *.jpeg *.bmp *.gif)", options=options)
        if self.image_path:
            pixmap = QPixmap(self.image_path)
            self.image_label.setPixmap(pixmap)
            self.image_label.setScaledContents(True)
            self.update_image_info()

    def update_image_info(self):
        if self.image_path:
            image = Image.open(self.image_path)
            width, height = image.size
            size = os.path.getsize(self.image_path)
            size_kb = size / 1024
            self.image_size_value.setText('{:.2f} KB'.format(size_kb))
            self.image_pixel_value.setText('{} x {}'.format(width, height))

    def compress_image(self):
        if self.image_path:
            image = Image.open(self.image_path)
            width, height = image.size
            new_width = int(width * 0.5)
            new_height = int(height * 0.5)
            new_image = image.resize((new_width, new_height))
            # 保存图像，根据选择的格式自动确定保存的文件类型
            # format = self.formatComboBox.currentText()
            # 保存图像，根据文件的后缀自动确定保存的文件类型
            image_path_prefix = os.path.splitext(self.image_path)[0]
            image_path_suffix = os.path.splitext(self.image_path)[1]
            new_image_path = image_path_prefix + '_compressed' + image_path_suffix
            new_image.save(new_image_path)
            self.image_path = new_image_path
            pixmap = QPixmap(new_image_path)
            self.image_label.setPixmap(pixmap)
            self.image_label.setScaledContents(True)
            self.update_image_info()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    image_compressor = ImageCompressor()
    sys.exit(app.exec_())
