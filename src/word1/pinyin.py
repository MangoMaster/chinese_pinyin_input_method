import os
import sys

from convert_pinyin import load_table, convert_pinyin


"""
main() of the pinyin program.
"""
pinyin_word_table_path = os.path.join(
    os.path.pardir, os.path.pardir, "data", "pinyin_word_table.json")
if len(sys.argv) == 1:
    # Interactive mode
    pinyin_word_table = load_table(pinyin_word_table_path)
    while True:
        pinyin = input("全拼拼音，每个音之间用空格隔开：")
        pinyin = pinyin.strip().lower()
        sentence = convert_pinyin(pinyin, pinyin_word_table)
        print(sentence)
elif len(sys.argv) == 3:
    # File input-output mode
    pinyin_word_table = load_table(pinyin_word_table_path)
    with open(sys.argv[1], 'r') as input_file, open(sys.argv[2], 'w') as output_file:
        for pinyin in input_file:
            pinyin = pinyin.strip().lower()
            sentence = convert_pinyin(pinyin, pinyin_word_table)
            output_file.write(sentence)
            output_file.write('\n')
else:
    # Help
    print("拼音输入法使用方法：")
    print("1.提供输入文件名和输出文件名并运行程序，例如: ")
    print("  pinyin ../data/input.txt ../data/output.txt")
    print("2.交互模式，直接运行程序即可")
