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
    words = []
    pinyin_start = 0
    pinyin_stop = len(pinyin)
    while pinyin_start < pinyin_stop:
        while pinyin[pinyin_start: pinyin_stop] not in pinyin_word_table:
            # Pop the last character's pinyin.
            while pinyin[pinyin_stop] != ' ':
                pinyin_stop -= 1
                # If all the possible pinyin of a single Chinese character
                # is in pinyin_word_table, pinyin will never underflow.
                assert pinyin_start < pinyin_stop, "Pinyin underflow: " + \
                    pinyin + '(' + str(pinyin_start) + \
                    ',' + str(pinyin_stop) + ')'
        # TODO: Optimize it by using a threshold
        words.append(pinyin_word_table[pinyin[pinyin_start:pinyin_stop]])
        # Pop (from the front) pinyin of the characters that are already in the sentence.
        pinyin_start = pinyin_stop + 1
        pinyin_stop = len(pinyin)
    return ''.join(words)
