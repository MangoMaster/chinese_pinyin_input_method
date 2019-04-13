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


def get_pinyin_chars(text):
    """
    Get pinyin-char pairs and pinyin-pinyin-char-char pairs from text

    Arg:
        text: A Chinese sentence.

    Returns:
        A list of pair [pinyin, char], a list of pair [pinyin1, pinyin2, char1, char2].
    """
    pinyin_char_pairs = []
    pinyin_pinyin_char_char_pairs = []
    # 记录上一个词语末尾的char以及它是否与下一个词语相连
    old_char_pinyin = ''
    old_char = ''
    old_char_is_neighbor = False
    # 只考虑中文字符
    chinese_words = re.compile(u"[\u4e00-\u9fa5]+")
    # 进行jieba分词以提高拼音准确率
    segments = jieba.cut(text)
    for word in segments:
        if re.match(chinese_words, word):
            pinyin = pypinyin.lazy_pinyin(
                word, style=pypinyin.Style.NORMAL, errors='ignore')
            pinyin_char_pair_list = list(zip(pinyin, word))
            pinyin_char_pairs.extend(pinyin_char_pair_list)
            # Neighbor with old char
            if old_char_is_neighbor:
                pinyin_pinyin_char_char_pairs.append(
                    [old_char_pinyin, pinyin[0], old_char, word[0]])
            # Neighbor within word
            for (pinyin1, char1), (pinyin2, char2) in pairwise(pinyin_char_pair_list):
                pinyin_pinyin_char_char_pairs.append(
                    [pinyin1, pinyin2, char1, char2])
            # Update old_char
            old_char_pinyin = pinyin[-1]
            old_char = word[-1]
            old_char_is_neighbor = True
        else:
            old_char_is_neighbor = False
    return (pinyin_char_pairs, pinyin_pinyin_char_char_pairs)


def count_pinyin_chars(pinyin_char_pairs, database_path):
    """
    Count how many times the same pinyin-char pair appears.

    Args:
        pinyin_char_pairs: A list of pair (pinyin, char).
        database_path: Path to a sqlite database file.
    """
    try:
        connection = sqlite3.connect(database_path, isolation_level=None)
        cursor = connection.cursor()
        # 关闭写同步以加速
        cursor.execute("""pragma synchronous = off""")
        # 显式开启事务以加速
        cursor.execute("""begin transaction;""")
        for pinyin, char in pinyin_char_pairs:
            cursor.execute("""
                update PinyinChar
                set count = count + 1
                where pinyin = '%s' and char = '%c';
                """ % (pinyin, char))
            if cursor.rowcount == 0:
                cursor.execute("""
                    insert into PinyinChar (pinyin, char, count)
                    values ('%s', '%c', 1);
                    """ % (pinyin, char))
        cursor.execute("""commit transaction;""")
        connection.commit()
    finally:
        cursor.close()
        connection.close()


def count_pinyin_pinyin_char_chars(pinyin_pinyin_char_char_pairs, database_path):
    """
    Count how many times the same (pinyin-char pair, pinyin-char pair) pair appears.

    Args:
        pinyin_pinyin_char_char_pairs: A list of pair (pinyin1, pinyin2, char1, char2).
        database_path: Path to a sqlite database file.
    """
    try:
        connection = sqlite3.connect(database_path, isolation_level=None)
        cursor = connection.cursor()
        # 关闭写同步以加速
        cursor.execute("""pragma synchronous = off""")
        # 显式开启事务以加速
        cursor.execute("""begin transaction;""")
        for pinyin1, pinyin2, char1, char2 in pinyin_pinyin_char_char_pairs:
            cursor.execute("""
                update PinyinPinyinCharChar
                set count = count + 1
                where pinyin1 = '%s' and pinyin2 = '%s' and char1 = '%c' and char2 = '%c';
                """ % (pinyin1, pinyin2, char1, char2))
            if cursor.rowcount == 0:
                cursor.execute("""
                    insert into PinyinPinyinCharChar (pinyin1, pinyin2, char1, char2, count)
                    values ('%s', '%s', '%c', '%c', 1);
                    """ % (pinyin1, pinyin2, char1, char2))
        cursor.execute("""commit transaction;""")
        connection.commit()
    finally:
        cursor.close()
        connection.close()


def bake_dataset_pinyin_pinyin_char_char():
    # 无自定义拼音库，控制pypinyin不做copy操作, 以减少内存占用
    os.environ['PYPINYIN_NO_DICT_COPY'] = 'true'
    # 设置文件和数据库路径
    news_dirname = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), os.path.pardir, os.path.pardir, "data", "sina_news_utf8")
    news_filenames = os.listdir(news_dirname)
    pinyin_char_database_path = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), os.path.pardir, os.path.pardir, "data", "pinyin_char.db")
    pinyin_pinyin_char_char_database_path = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), os.path.pardir, os.path.pardir, "data", "pinyin_pinyin_char_char.db")
    for news_filename in news_filenames:
        with open(os.path.join(news_dirname, news_filename), 'r') as f:
            print("Reading " + news_filename + "...")
            news_texts = get_news_text(f)
            # 逐条分析新闻以减少内存占用
            for news_text in news_texts:
                news_pinyin_char_pairs, news_pinyin_pinyin_char_char_pairs \
                    = get_pinyin_chars(news_text)
                count_pinyin_chars(
                    news_pinyin_char_pairs, pinyin_char_database_path)
                count_pinyin_pinyin_char_chars(
                    news_pinyin_pinyin_char_char_pairs, pinyin_pinyin_char_char_database_path)


if __name__ == "__main__":
    bake_dataset_pinyin_pinyin_char_char()
