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

def arithmetic_decoding(encoded_data, original_length, frequencies, precision):
    decoded_text = []
    low = 0.0
    high = 1.0
    range_size = high - low
    value = encoded_data[0]

    for _ in range(original_length):
        for symbol, freq in frequencies.items():
            symbol_low = low + range_size * sum(frequencies[c] for c in frequencies if c < symbol) / original_length
            symbol_high = low + range_size * sum(frequencies[c] for c in frequencies if c <= symbol) / original_length

            if symbol_low <= value < symbol_high:
                decoded_text.append(symbol)
                range_size = symbol_high - symbol_low
                value = (value - symbol_low) / (symbol_high - symbol_low)
                low = symbol_low
                high = symbol_high
                break

    decoded_text = ''.join(decoded_text)
    return decoded_text if precision is None else decoded_text[:precision]

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

        decode_button = QPushButton('Decode Text')
        decode_button.clicked.connect(self.decode_text)
        layout.addWidget(decode_button)

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

        self.encoded_data = encoded_sequence
        self.original_length = len(text)
        self.frequencies = dict(Counter(text))

    def decode_text(self):
        if hasattr(self, 'encoded_data') and hasattr(self, 'original_length') and hasattr(self, 'frequencies'):
            precision = None  # Здесь можно установить точность декодирования
            decoded_text = arithmetic_decoding(self.encoded_data, self.original_length, self.frequencies, precision)
            self.result_label.setText(f"Decoded text: {decoded_text}")
        else:
            self.result_label.setText("Please encode text first.")

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
