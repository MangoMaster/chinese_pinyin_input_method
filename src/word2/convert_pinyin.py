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
        pinyin_word_table: pinyin-word table, a dict, key->pinyin, value->[[word, log(probability)].
        word_word_table: word-word table, a dict, key->str(word1-word2), value->log(probability)

    Returns:
        A string of Chinese characters converted from pinyin.
    """
    # Dynamic programming strategy.
    pinyin_list = pinyin.split(' ')
    if not pinyin_list or pinyin_list == ['']:
        return ""
    # 'lue' should be 'lve' and 'nue' should be 'nve' in standard Chinese pinyin.
    pinyin_list = ['lve' if pinyin_single == 'lue'
                   else 'nve' if pinyin_single == 'nue'
                   else pinyin_single
                   for pinyin_single in pinyin_list]
    dynamic_programming_table = [[] for _ in range(len(pinyin_list))]
    # dynamic_programming_table:二维数组，记录pinyin_list[:stop_index+1]的所有可能尾词的分别最优解
    # 第一维为stop_index，第二维为list(尾词，尾词probability，总句，总句probability)
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
                    # Pushes one sentence for every word_back
                    max_sentence = [word_back,
                                    word_probability_back, "", float("-inf")]
                    for word_front, word_probability_front, sentence_front, sentence_probability_front in dynamic_programming_table[mid_stop_index]:
                        word_pair = '-'.join((word_front, word_back))
                        # log(probability), so * => + , / => -
                        if word_pair in word_word_table:
                            sentence_probability = (
                                sentence_probability_front + word_word_table[word_pair] - word_probability_front)
                        else:
                            # Add a punishment to increase accuracy
                            sentence_probability = sentence_probability_front + word_probability_back - 0.5
                        if sentence_probability > max_sentence[3]:
                            max_sentence[2] = sentence_front + word_back
                            max_sentence[3] = sentence_probability
                    assert max_sentence[2] != ""
                    dynamic_programming_table[stop_index].append(max_sentence)
    max_sentence = ("", float("-inf"))
    for dp_node in dynamic_programming_table[-1]:
        if dp_node[3] > max_sentence[1]:
            max_sentence = (dp_node[2], dp_node[3])
    assert max_sentence[0] != ""
    return max_sentence[0]
