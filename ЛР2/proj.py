import sys
import numpy as np
import heapq
from collections import defaultdict
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog, QTextEdit, QVBoxLayout

# Чтение двумерного массива из файла
def read_array_from_file(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        array = [list(map(int, line.strip().split())) for line in lines]
        return np.array(array)

def write_in_file(result_text):
    with open('out.txt', 'w') as file:
        file.write(result_text)

# Обход решетками с параметрами M=N=2
def grid_traversal(array):
    M, N = 2, 2
    flattened_array = []
    for passes in range(0, 4):
        match passes:
            case 0:        
                for i in range(0, array.shape[0],M):
                    for j in range(0, array.shape[0],N):
                        flattened_array.extend(array[i,j].flatten())   
            case 1:     
                for i in range(0, array.shape[0],M):
                    for j in range(1, array.shape[0],N):
                        flattened_array.extend(array[i,j].flatten())
            case 2:
                for i in range(1, array.shape[0],M):
                    for j in range(0, array.shape[0],N):
                        flattened_array.extend(array[i,j].flatten())
            case 3:
                for i in range(1, array.shape[0],M):
                    for j in range(1, array.shape[0],N):
                        flattened_array.extend(array[i,j].flatten())

    return np.array(flattened_array)

# Метод RLE сжатия
def rle_compress(array):
    compressed_array = []
    count = 1
    for i in range(1, len(array)):
        if array[i] == array[i - 1]:
            count += 1
        else:
            compressed_array.append((count, array[i - 1]))
            count = 1
    compressed_array.append((count, array[-1]))
    return compressed_array

# Метод Хаффмана для сжатия данных
def huffman_compress(array):
    freq = defaultdict(int)
    for num in array:
        freq[num] += 1
    
    heap = [[weight, [num, ""]] for num, weight in freq.items()]
    heapq.heapify(heap)
    
    while len(heap) > 1:
        lo = heapq.heappop(heap)
        hi = heapq.heappop(heap)
        for pair in lo[1:]:
            pair[1] = '0' + pair[1]
        for pair in hi[1:]:
            pair[1] = '1' + pair[1]
        heapq.heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])
    
    huffman_codes = dict(heap[0][1:])
    compressed_array = ''.join(huffman_codes[num] for num in array)
    return compressed_array, huffman_codes

# Функция для обработки файла и вывода результатов
def process_file():
    options = QFileDialog.Options()
    file_name, _ = QFileDialog.getOpenFileName(None, "Выберите файл", "", "Text Files (*.txt);;All Files (*)", options=options)
    if file_name:
        array = read_array_from_file(file_name)
        flattened_array = grid_traversal(array)
        rle_compressed_array = rle_compress(flattened_array)
        huffman_compressed_array, huffman_codes = huffman_compress(flattened_array)
        
        result_text = "Исходный массив:\n{}\n\nОбход решетками и сжатие RLE:\n{}\n{}\n\nСжатие методом Хаффмана:\n{}\n\nТаблица кодирования Хаффмана:\n".format(
            array, flattened_array, rle_compressed_array, huffman_compressed_array
        )
        for num, code in huffman_codes.items():
            result_text += f"{num}: {code}\n"
        
        text_output.setText(result_text)
        write_in_file(result_text)

app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("Лабораторная работа №2")
window.setGeometry(100, 100, 600, 400)

btn_open = QPushButton("Открыть файл")
btn_open.clicked.connect(process_file)

text_output = QTextEdit()
text_output.setReadOnly(True)

layout = QVBoxLayout()
layout.addWidget(btn_open)
layout.addWidget(text_output)

window.setLayout(layout)
window.show()

sys.exit(app.exec_())