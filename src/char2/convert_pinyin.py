import copy
import json


def load_table(table_path):
    """
    Load table from table_path.

    Args:
        table_path: Path to the source table json file.

    Returns:
        table, a datastructure converted from json file.
    """
    with open(table_path, 'r') as f:
        return json.load(f)


def convert_pinyin(pinyin, pinyin_char_table, char_char_table):
    """
    Convert pinyin to Chinese sentence.

    Args:
        pinyin: A string, a sentence of pinyin separated by space.
        pinyin_char_table: pinyin-char table, a dict, key->pinyin, value->[[char, log(probability)].
        char_char_table: char-char table, a dict, key->str(char1-char2), value->log(probability)

    Returns:
        A string of Chinese characters converted from pinyin.
    """
    # Dynamic programming strategy.
    pinyin_list = pinyin.split(' ')
    if not pinyin_list:
        return ""
    dynamic_programming_table = [[] for _ in range(len(pinyin_list))]
    # dynamic_programming_table:二维数组，记录pinyin_list[:stop_index+1]的最优解
    # 第一维为stop_index，第二维为list(总句，总句probability，尾字probability)
    dynamic_programming_table[0] = pinyin_char_table[pinyin_list[0]]
    for stop_index in range(1, len(pinyin_list)):
        pinyin_back = pinyin_list[stop_index]
        # Single pinyin will never fall out of pinyin_char_table
        assert pinyin_back in pinyin_char_table
        for char_back, char_probability_back in pinyin_char_table[pinyin_back]:
            # Pushes one sentence for every char_back
            max_sentence = ["", float("-inf"), char_probability_back]
            for sentence_front, sentence_probability_front, char_probability_front in dynamic_programming_table[stop_index - 1]:
                char_pair = '-'.join((sentence_front[-1], char_back))
                # log(probability), so * => + , / => -
                if char_pair in char_char_table:
                    sentence_probability = (
                        sentence_probability_front + char_char_table[char_pair] - char_probability_front)
                else:
                    sentence_probability = sentence_probability_front + char_probability_back
                if sentence_probability > max_sentence[1]:
                    max_sentence[0] = sentence_front + char_back
                    max_sentence[1] = sentence_probability
            assert max_sentence[0] != ""
            dynamic_programming_table[stop_index].append(max_sentence)

    max_sentence = ("", float("-inf"))
    for dp_node in dynamic_programming_table[-1]:
        if dp_node[1] > max_sentence[1]:
            max_sentence = (dp_node[0], dp_node[1])
    assert max_sentence[0] != ""
    return max_sentence[0]
