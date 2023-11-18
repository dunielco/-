import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QTextEdit, QFileDialog
from collections import Counter

def arithmetic_coding(data):
    frequencies = dict(Counter(data))  # Подсчет частоты появления символов
    total_symbols = len(data)  # Общее количество символов
    low = 0.0
    high = 1.0
    encoded_data = []

    for symbol in data:
        # Вычисляем новые значения low и high на основе частоты символов
        range_size = high - low
        high = low + range_size * sum(frequencies[c] for c in frequencies if c < symbol) / total_symbols
        low = low + range_size * sum(frequencies[c] for c in frequencies if c <= symbol) / total_symbols

    # Кодирование последнего символа
    code = (low + high) / 2
    encoded_data.append(code)

    return encoded_data

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.text_edit = QTextEdit()
        layout.addWidget(self.text_edit)

        load_button = QPushButton('Load Text from File')
        load_button.clicked.connect(self.load_text)
        layout.addWidget(load_button)

        encode_button = QPushButton('Encode Text')
        encode_button.clicked.connect(self.encode_text)
        layout.addWidget(encode_button)

        self.result_label = QLabel()
        layout.addWidget(self.result_label)

        self.setLayout(layout)
        self.setWindowTitle('Arithmetic Coding')

    def load_text(self):
        file_dialog = QFileDialog()
        file_dialog.setNameFilter("Text Files (*.txt)")
        if file_dialog.exec_():
            file_path = file_dialog.selectedFiles()[0]
            with open(file_path, 'r') as file:
                text = file.read()
                self.text_edit.setPlainText(text)

    def encode_text(self):
        text = self.text_edit.toPlainText()
        encoded_sequence = arithmetic_coding(text)
        self.result_label.setText(f"Encoded sequence: {encoded_sequence}")

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
