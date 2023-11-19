import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QTextEdit, QVBoxLayout

def bwt_transform(text):
    # Получаем все циклические перестановки фразы
    rotations = [text[i:] + text[:i] for i in range(len(text))]

    # Сортируем циклические перестановки в лексикографическом порядке
    sorted_rotations = sorted(rotations)

    # Получаем последнюю букву каждой сортированной циклической перестановки
    bwt_transformed = ''.join([rotation[-1] for rotation in sorted_rotations])

    return bwt_transformed

def mtf_transform(text):
    list_text = set([text[i] for i in range(len(text))])
    # Создаем список всех символов в тексте
    alphabet = sorted(list_text)
    # Создаем список для хранения результата
    mtf_text = []
    for char in text:
        # Получаем индекс символа в алфавите
        index = alphabet.index(char)
        # Добавляем индекс символа в результат
        mtf_text.append(index)
        # Перемещаем символ в начало алфавита
        alphabet.pop(index)
        alphabet.insert(0, char)
    # Возвращаем полученный результат как список чисел
    return mtf_text

class BWTTransformApp(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.text_input = QTextEdit(self)
        self.result_bwt_output = QTextEdit(self)
        self.result_bwt_output.setReadOnly(True)

        self.result_mtf_output = QTextEdit(self)
        self.result_mtf_output.setReadOnly(True)

        button_bwt = QPushButton('Преобразовать BWT и MTF', self)
        button_bwt.clicked.connect(self.transform_bwt)
        button_bwt.clicked.connect(self.transform_mtf)
 

        layout = QVBoxLayout()
        layout.addWidget(self.text_input)
        layout.addWidget(button_bwt)
        layout.addWidget(self.result_bwt_output)
        layout.addWidget(self.result_mtf_output)

        self.result_bwt_output.hide()
        self.result_mtf_output.hide()
        self.setLayout(layout)

        self.setGeometry(300, 300, 400, 50)
        self.setWindowTitle('Лабораторная работа 3.2')
        self.show()

    def transform_bwt(self):
        bwt_result = bwt_transform(self.text_input.toPlainText())
        self.result_bwt_output.setPlainText(str(bwt_result))

        self.result_bwt_output.show()

    def transform_mtf(self):
        mtf_result = mtf_transform(bwt_transform(self.text_input.toPlainText()))
        self.result_mtf_output.setPlainText(str(mtf_result))

        self.result_mtf_output.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = BWTTransformApp()
    sys.exit(app.exec_())