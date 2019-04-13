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


def convert_pinyin(pinyin, pinyin_word_table, word_word_table):
    """
    Convert pinyin to Chinese sentence.

    Args:
        pinyin: A string, a sentence of pinyin separated by space.
        pinyin_word_table: pinyin-word table, a dict, key->pinyin, value->[(word, probability)].
        word_word_table: word-word table, a dict, key->(word1, word2), value->probability

    Returns:
        A string of Chinese characters converted from pinyin.
    """
    # Dynamic programming strategy.
    pinyin_list = pinyin.split(' ')
    dynamic_programming_table = [[] for _ in range(len(pinyin_list))]
    # dynamic_programming_table:
    # 第一维为stop_index，第二维为(尾词，尾词probability，总句，总句probability)
    for stop_index in range(len(pinyin_list)):
        pinyin_whole = ' '.join(pinyin_list[:stop_index + 1])
        if pinyin_whole in pinyin_word_table:
            for word_whole, probability_whole in pinyin_word_table[pinyin_whole]:
                dynamic_programming_table[stop_index].append(
                    [word_whole, probability_whole, word_whole, probability_whole])
        for mid_stop_index in range(stop_index):
            pinyin_back = ' '.join(
                pinyin_list[mid_stop_index + 1:stop_index + 1])
            if pinyin_back in pinyin_word_table:
                for word_back, word_probability_back in pinyin_word_table[pinyin_back]:
                    for word_front, word_probability_front, sentence_front, sentence_probability_front in dynamic_programming_table[mid_stop_index]:
                        if (word_front, word_back) in word_word_table:
                            sentence_probability = sentence_probability_front * word_word_table[(word_front, word_back)] / word_probability_front
                        else:
                            sentence_probability = sentence_probability_front * word_probability_back
                        dynamic_programming_table[stop_index].append(
                            [word_back, word_probability_back, sentence_front + word_back, sentence_probability])
    return dynamic_programming_table[-1][-1][2]
