import os
import sys
import subprocess
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QPushButton, QLabel, QVBoxLayout, QMessageBox, QComboBox, QListWidget, QListWidgetItem
import pkg_resources

class PDFCompressor(QWidget):
    def __init__(self):
        super().__init__()
        self.selected_files = []
        self.compression_level = None
        self.init_ui()

    def init_ui(self):
        # 创建选择文件按钮
        select_btn = QPushButton('选择文件', self)
        select_btn.clicked.connect(self.open_file_dialog)

        # 创建展示文件路径的标签
        self.file_path_list = QListWidget(self)

        # 创建压缩级别下拉框
        compression_level_label = QLabel('压缩级别:', self)
        self.compression_level_combo = QComboBox(self)
        self.compression_level_combo.addItems(['低（屏幕）', '中（ ebook）', '高（打印）'])

        # 创建压缩文件按钮
        compress_btn = QPushButton('压缩文件', self)
        compress_btn.clicked.connect(self.compress_files)

        # 创建垂直布局，并将按钮、标签和下拉框加入其中
        vbox = QVBoxLayout()
        vbox.addWidget(select_btn)
        vbox.addWidget(self.file_path_list)
        vbox.addWidget(compression_level_label)
        vbox.addWidget(self.compression_level_combo)
        vbox.addWidget(compress_btn)

        # 设置窗口布局
        self.setLayout(vbox)

        # 设置窗口大小
        self.setGeometry(300, 300, 800, 400)

        self.setWindowTitle('熊熊的 PDF 压缩器')
        self.show()

    def open_file_dialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(self, "选择文件", "", "PDF 文件 (*.pdf)", options=options)
        if files:
            self.selected_files = files
            for file in files:
                item = QListWidgetItem(file)
                self.file_path_list.addItem(item)

    def compress_files(self):
        if self.selected_files:
            # 获取压缩级别
            if self.compression_level_combo.currentText() == '低（屏幕）':
                self.compression_level = '/screen'
            elif self.compression_level_combo.currentText() == '中（ ebook）':
                self.compression_level = '/ebook'
            elif self.compression_level_combo.currentText() == '高（打印）':
                self.compression_level = '/printer'

            # 循环压缩每一个文件
            for file in self.selected_files:
                # 获取压缩后的文件名
                output_file_name = os.path.splitext(file)[0] + '_compressed.pdf'

                gs_path = pkg_resources.resource_filename(__name__, "")
                # 构造 Ghostscript 压缩命令
                cmd = ['gs', '-sDEVICE=pdfwrite', '-dCompatibilityLevel=1.4', '-dPDFSETTINGS={}'.format(self.compression_level), '-dNOPAUSE', '-dQUIET', '-dBATCH', '-sOutputFile={}'.format(output_file_name), file]

                # 调用 Ghostscript 进行 PDF 压缩
                try:
                    subprocess.run(cmd, check=True)
                except subprocess.CalledProcessError:
                    QMessageBox.critical(self, "错误", "压缩文件时发生错误！")
                    return

            QMessageBox.information(self, "提示", "文件压缩完成！")
        else:
            QMessageBox.warning(self, "警告", "请选择要压缩的 PDF 文件！")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    pdf_compressor = PDFCompressor()
    sys.exit(app.exec_())