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
    # Dynamic programming strategy.
    pinyin_list = pinyin.split(' ')
    dynamic_programming_table = [[] for _ in range(len(pinyin_list))]
    # dynamic_programming_table: 二维数组，记录pinyin_list[start_index:stop_index+1]的最优解
    # 第一维为stop_index，第二维为(整句, 整句probability)
    for stop_index in range(len(pinyin_list)):
        pinyin_whole = ' '.join(pinyin_list[:stop_index + 1])
        if pinyin_whole in pinyin_word_table:
            max_now = pinyin_word_table[pinyin_whole]
        else:
            max_now = ["", 0]
        for mid_stop_index in range(stop_index):
            pinyin_back = ' '.join(
                pinyin_list[mid_stop_index + 1:stop_index + 1])
            if pinyin_back in pinyin_word_table:
                word, word_probability = pinyin_word_table[pinyin_back]
                sentence, sentence_probability = dynamic_programming_table[mid_stop_index]
                probability = word_probability * sentence_probability
                if probability > max_now[1]:
                    max_now = [sentence + word, probability]
        assert max_now[0] != ""
        dynamic_programming_table[stop_index] = max_now
    return dynamic_programming_table[-1][0]
    # # Greedy stategy.
    # words = []
    # pinyin_start = 0
    # pinyin_stop = len(pinyin)
    # while pinyin_start < pinyin_stop:
    #     while pinyin[pinyin_start: pinyin_stop] not in pinyin_word_table:
    #         # Pop the last character's pinyin.
    #         pinyin_stop -= 1
    #         while pinyin[pinyin_stop] != ' ':
    #             pinyin_stop -= 1
    #             # If all the possible pinyin of a single Chinese character
    #             # is in pinyin_word_table, pinyin will never underflow.
    #             assert pinyin_start < pinyin_stop, "Pinyin underflow: " + \
    #                 pinyin + '(' + str(pinyin_start) + \
    #                 ',' + str(pinyin_stop) + ')'
    #     # TODO: Optimize it by using a threshold
    #     words.append(pinyin_word_table[pinyin[pinyin_start:pinyin_stop]][0])
    #     # Pop (from the front) pinyin of the characters that are already in the sentence.
    #     pinyin_start = pinyin_stop + 1
    #     pinyin_stop = len(pinyin)
    # return ''.join(words)
