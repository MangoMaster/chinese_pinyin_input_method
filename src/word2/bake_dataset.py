import gc
import itertools
import json
import os
import re
import sqlite3

import jieba
import pypinyin


def pairwise(iterable):
    """
    Iterate as pair (current, next).
    s -> (s0,s1), (s1,s2), (s2, s3), ...

    Args:
        iterable: A list or something as a iterable
    """
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)


def get_news_text(news_file):
    """
    Retrieve text from news file.

    Args:
        news_file: A file containing news.
            Every line contains a piece of news in json
            Json keys include: title-新闻标题 html-新闻正文.

    Returns:
        A list of texts in news.
    """
    news_texts = []
    for news in news_file:
        news_data = json.loads(news)
        news_texts.append(news_data['title'])
        news_texts.append(news_data['html'])
    return news_texts


def get_neighbor_words(text):
    """
    Cut text into words and group neighbor words into pairs.

    Arg:
        text: A Chinese sentence.

    Returns:
        A list of (word1, word2) pairs cut from text.
    """
    neighbor_words = []
    # 只考虑中文字符
    chinese_words = re.compile(u"[\u4e00-\u9fa5]+")
    segments = jieba.cut(text)
    for word1, word2 in pairwise(segments):
        if re.match(chinese_words, word1) and re.match(chinese_words, word2):
            neighbor_words.append([word1, word2])
    return neighbor_words


def get_pinyin(neighbor_words):
    """
    Get Chinese pinyin of words.

    Arg:
        words: A list of (word1, word2) pairs.

    Returns:
        A list of pair [pinyin1, pinyin2, word1, word2].
    """
    pinyin_pinyin_word_word_pairs = []
    for word1, word2 in neighbor_words:
        pinyin1 = pypinyin.lazy_pinyin(
            word1, style=pypinyin.Style.NORMAL, errors='ignore')
        pinyin2 = pypinyin.lazy_pinyin(
            word2, style=pypinyin.Style.NORMAL, errors='ignore')
        pinyin_pinyin_word_word_pairs.append([pinyin1, pinyin2, word1, word2])
    return pinyin_pinyin_word_word_pairs


def count_pinyin_pinyin_word_words(pinyin_pinyin_word_word_pairs, database_path):
    """
    Count how many times the same (pinyin-word pair, pinyin-word pair) pair appears.

    Args:
        pinyin_pinyin_word_word_pairs: A list of pair (pinyin1, pinyin2, word1, word2).
        database_path: Path to a sqlite database file.
    """
    try:
        connection = sqlite3.connect(database_path, isolation_level=None)
        cursor = connection.cursor()
        # 关闭写同步以加速
        cursor.execute("""pragma synchronous = off""")
        # 显式开启事务以加速
        cursor.execute("""begin transaction;""")
        for pinyin1, pinyin2, word1, word2 in pinyin_pinyin_word_word_pairs:
            pinyin1 = ' '.join(pinyin1)
            pinyin2 = ' '.join(pinyin2)
            cursor.execute("""
                update PinyinPinyinWordWord
                set count = count + 1
                where pinyin1 = '%s' and pinyin2 = '%s' and word1 = '%s' and word2 = '%s';
                """ % (pinyin1, pinyin2, word1, word2))
            if cursor.rowcount == 0:
                cursor.execute("""
                    insert into PinyinPinyinWordWord (pinyin1, pinyin2, word1, word2, count)
                    values ('%s', '%s', '%s', '%s', 1);
                    """ % (pinyin1, pinyin2, word1, word2))
        cursor.execute("""commit transaction;""")
        connection.commit()
    finally:
        cursor.close()
        connection.close()


def bake_dataset_pinyin_pinyin_word_word():
    # 无自定义拼音库，控制pypinyin不做copy操作, 以减少内存占用
    os.environ['PYPINYIN_NO_DICT_COPY'] = 'true'
    # 设置文件和数据库路径
    news_dirname = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), os.path.pardir, os.path.pardir, "data", "sina_news_utf8")
    news_filenames = os.listdir(news_dirname)
    database_path = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), os.path.pardir, os.path.pardir, "data", "pinyin_pinyin_word_word.db")
    for news_filename in news_filenames:
        with open(os.path.join(news_dirname, news_filename), 'r') as f:
            print("Reading " + news_filename + "...")
            news_texts = get_news_text(f)
            # 逐条分析新闻以减少内存占用
            for news_text in news_texts:
                news_neighbor_words = get_neighbor_words(news_text)
                news_pinyin_pinyin_word_word_pairs = get_pinyin(
                    news_neighbor_words)
                count_pinyin_pinyin_word_words(
                    news_pinyin_pinyin_word_word_pairs, database_path)


if __name__ == "__main__":
    bake_dataset_pinyin_pinyin_word_word()
