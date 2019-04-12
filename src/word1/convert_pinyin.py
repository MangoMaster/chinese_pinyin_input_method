import copy
import json


def load_table(pinyin_word_table_path):
    """
    Load pinyin-word table from pinyin_word_table_path.

    Args:
        pinyin_word_table_path: Path to the source pinyin-word table json file.

    Returns:
        pinyin-word table, a dict, key->pinyin, value->(word, count).
    """
    with open(pinyin_word_table_path, 'r') as f:
        return json.load(f)


def convert_pinyin(pinyin, pinyin_word_table):
    """
    Convert pinyin to Chinese sentence.

    Args:
        pinyin: A string, a sentence of pinyin separated by space.
        pinyin_word_table: pinyin-word table, a dict, key->pinyin, value->(word, count).

    Returns:
        A string of Chinese characters converted from pinyin.
    """
    # # Dynamic programming strategy.
    # pinyin_list = pinyin.split(' ')
    # dynamic_programming_table = [[] for _ in range(len(pinyin_list))]
    # # dynamic_programming_table: 二维数组，记录pinyin_list[start_index:start_index+slice_length]的最优解
    # # 第一维为start_index，第二维为slice_length-1
    # for slice_length in range(1, len(pinyin_list) + 1):
    #     for start_index in range(0, len(pinyin_list) + 1 - slice_length):
    #         pinyin_now = ' '.join(
    #             pinyin_list[start_index: start_index + slice_length])
    #         if pinyin_now in pinyin_word_table:
    #             max_now = pinyin_word_table[pinyin_now]
    #         else:
    #             max_now = ["", 0]
    #         for slice_mid_length in range(1, slice_length):
    #             count = (dynamic_programming_table[start_index][slice_mid_length - 1][1] *
    #                      dynamic_programming_table[start_index + slice_mid_length][slice_length - slice_mid_length - 1][1]) ** 0.5
    #             if count > max_now[1]:
    #                 max_now = [(dynamic_programming_table[start_index][slice_mid_length - 1][0] +
    #                             dynamic_programming_table[start_index + slice_mid_length][slice_length-slice_mid_length-1][0]),
    #                            count]
    #         assert max_now[0] != ""
    #         dynamic_programming_table[start_index].append(max_now)
    # return dynamic_programming_table[0][-1][0]
    # Greedy stategy.
    words = []
    pinyin_start = 0
    pinyin_stop = len(pinyin)
    while pinyin_start < pinyin_stop:
        while pinyin[pinyin_start: pinyin_stop] not in pinyin_word_table:
            # Pop the last character's pinyin.
            pinyin_stop -= 1
            while pinyin[pinyin_stop] != ' ':
                pinyin_stop -= 1
                # If all the possible pinyin of a single Chinese character
                # is in pinyin_word_table, pinyin will never underflow.
                assert pinyin_start < pinyin_stop, "Pinyin underflow: " + \
                    pinyin + '(' + str(pinyin_start) + \
                    ',' + str(pinyin_stop) + ')'
        # TODO: Optimize it by using a threshold
        words.append(pinyin_word_table[pinyin[pinyin_start:pinyin_stop]][0])
        # Pop (from the front) pinyin of the characters that are already in the sentence.
        pinyin_start = pinyin_stop + 1
        pinyin_stop = len(pinyin)
    return ''.join(words)
