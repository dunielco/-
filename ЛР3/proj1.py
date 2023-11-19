import pickle
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QTextEdit, QVBoxLayout

AlphPower = 2550
FirstCode = 0
CodingLength = 5

# forms an array of AlphPower elements
# each of which stores the number of occurrences of the corresponding character in the file
# returns a tuple of the number of characters and this array
def count_file_symbols(filename):
    symbol_count = 0
    ents = [0] * AlphPower
    input_file = open(filename, 'r', encoding="utf-8")

    for line in input_file:
        for char in line:
            char_code = ord(char)
            ents[char_code] = ents[char_code] + 1
            symbol_count = symbol_count + 1

    input_file.close()
    return symbol_count, ents


# calculates the probability of each symbol.
# Saves it to a file (needed for decoding).
# Stored as a dictionary. The file is binary,
# and for writing and reading from it - the pickle module.
def init_model(inputFilename, outputFilename):
    (symbol_count, ents) = count_file_symbols(inputFilename)

    for char_code in range(FirstCode, 2550):
        ents[char_code] = 1.0 * ents[char_code] / symbol_count

    result_text = ''
    low = 0.0
    dict = {}
    for char_code in range(FirstCode, 2550):
        if ents[char_code] > 0:
            high = low + ents[char_code]
            dict[char_code] = (low, high)
            low = high

            result_text += f"{char_code}:\t{dict[char_code]}\n"

    model_file = open(outputFilename, 'wb')
    pickle.dump(dict, model_file)
    model_file.close()

    return result_text


def read_model(modelFilename):
    input_file = open(modelFilename, 'rb')
    dict = pickle.load(input_file)
    input_file.close()
    return dict


def char_low_high(char, dict):
    char_code = ord(char)
    (low, high) = dict[char_code]
    return (low, high)


def add_symbol_to_coding_sequence(seq_low, seq_high, dict, symbol):
    (symbol_low, symbol_high) = char_low_high(symbol, dict)
    return (seq_low + (seq_high - seq_low) * symbol_low,
            seq_low + (seq_high - seq_low) * symbol_high)


def AriphCoding(input_filename, dict, outputfilename):
    input_file = open(input_filename, 'r', encoding="utf-8")
    output_file = open(outputfilename, 'wb')

    coding_result = []

    count = CodingLength + 1
    for line in input_file:
        for char in line:
            if count >= CodingLength:
                (low, high) = char_low_high(char, dict)
                count = 1
            else:
                (low, high) = add_symbol_to_coding_sequence(low, high, dict, char)
                count = count + 1
            if count >= CodingLength:
                coding_result.append((count, low+(high-low)/2))
    if count != 0:
        coding_result.append((count, low + (high - low) / 2))

    pickle.dump(coding_result, output_file)
    input_file.close()
    output_file.close()

def reverse_map(char_to_range):
    range_to_char = {}

    for key in char_to_range:
        range = char_to_range[key]
        range_to_char[range] = key

    return range_to_char

def get_first_char_range(value, range_to_char):
    for key in range_to_char:
        (low, high) = key
        if low <= value <= high:
            return (low, high)

    return [-1,-1]

def AriphDecoding(input_filename, range_to_char, outputfilename):
    input_file = open(input_filename, 'rb')
    codes = pickle.load(input_file)
    input_file.close()

    output_file = open(outputfilename, 'w', encoding="utf-8")

    for (length, code) in codes:
        for number in range(length):
            char_range = get_first_char_range(code, range_to_char)
            char = range_to_char[char_range]
            output_file.write(chr(char))
            (low, high) = char_range
            code = (code-low)/(high-low)

    output_file.close()



app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle('Лабораторная работа №3.1')
window.setGeometry(100, 100, 600, 800)

text_code = QTextEdit()
text_decode = QTextEdit()
btn_code = QPushButton('Закодировать')
btn_decode = QPushButton('Декодировать')

def code():
    result_text = init_model('in.txt', 'ents.txt')
    char_to_range = read_model('ents.txt')
    #print(char_to_range)

    range_to_char = reverse_map(char_to_range)
    #print(range_to_char)

    AriphCoding('in.txt', char_to_range, 'code.txt')
    AriphDecoding('code.txt', range_to_char, 'decode.txt')

    layout.addWidget(text_code)
    text_code.setReadOnly(True)
    text_code.setText(result_text)
    layout.addWidget(btn_decode)
    text_decode.hide()

def decode():
    layout.addWidget(text_decode)
    text_decode.show()
    text_decode.setReadOnly(True)    
    input_file = open('decode.txt', 'r', encoding='utf-8')
    input_text = input_file.read()
    text_decode.setText(input_text)
    input_file.close()

btn_code.clicked.connect(code)
btn_decode.clicked.connect(decode)

layout = QVBoxLayout()
layout.addWidget(btn_code)


window.setLayout(layout)
window.show()

sys.exit(app.exec_())