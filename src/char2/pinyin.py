import os
import sys

from convert_pinyin import load_table, convert_pinyin


"""
main() of the pinyin program.
"""
pinyin_char_table_path = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), os.path.pardir, os.path.pardir, "data", "char2_pinyin_char_table.json")
char_char_table_path = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), os.path.pardir, os.path.pardir, "data", "char2_char_char_table.json")
if len(sys.argv) == 1:
    # Interactive mode
    print("Initializing...")
    pinyin_char_table = load_table(pinyin_char_table_path)
    char_char_table = load_table(char_char_table_path)
    print("Initialization finished.")
    while True:
        pinyin = input("全拼拼音，音与音之间用空格隔开：")
        pinyin = pinyin.strip().lower()
        sentence = convert_pinyin(pinyin, pinyin_char_table, char_char_table)
        print(sentence)
elif len(sys.argv) == 3:
    # File input-output mode
    print("Initializing...")
    pinyin_char_table = load_table(pinyin_char_table_path)
    char_char_table = load_table(char_char_table_path)
    print("Initialization finished.")
    with open(sys.argv[1], 'r') as input_file, open(sys.argv[2], 'w') as output_file:
        for pinyin in input_file:
            pinyin = pinyin.strip().lower()
            sentence = convert_pinyin(
                pinyin, pinyin_char_table, char_char_table)
            output_file.write(sentence)
            output_file.write('\n')
else:
    # Help
    print("拼音输入法使用方法：")
    print("1.提供输入文件名和输出文件名并运行程序，例如: ")
    print("  pinyin ../data/input.txt ../data/output.txt")
    print("2.交互模式，直接运行程序即可")
