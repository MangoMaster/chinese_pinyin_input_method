import os

import jieba
import pypinyin

# Destination file, pinyin
input_file_path = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), os.path.pardir, "data", "input3.txt")
# Source file, Chinese sentence
std_output_file_path = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), os.path.pardir, "data", "output_std3.txt")

# Convert Chinese sentences to pinyin for test
with open(std_output_file_path, 'r') as sentence_file, open(input_file_path, 'w') as pinyin_file:
    for sentence in sentence_file:
        pinyins = []
        segments = jieba.cut(sentence)
        for word in segments:
            pinyin = pypinyin.lazy_pinyin(
                word, style=pypinyin.Style.NORMAL, errors='ignore')
            pinyins.extend(pinyin)
        pinyin_file.write(' '.join(pinyins))
        pinyin_file.write('\n')
