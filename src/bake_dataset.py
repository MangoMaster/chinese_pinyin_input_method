import gc
import json
import os
import re
import sqlite3

import jieba
import pypinyin


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


def get_words(text):
    """
    Cut text into words.

    Arg:
        text: A Chinese sentence.

    Returns:
        A list of words cut from text.
    """
    words = []
    # 只考虑中文字符
    chinese_words = re.compile(u"[\u4e00-\u9fa5]+")
    segments = jieba.cut(text)
    for word in segments:
        if re.match(chinese_words, word):
            words.append(word)
    return words


def get_pinyin(words):
    """
    Get Chinese pinyin of words.

    Arg:
        words: A list of words.

    Returns:
        A list of pair [pinyin, word].
    """
    pinyin_word_pairs = []
    for word in words:
        pinyin = pypinyin.lazy_pinyin(
            word, style=pypinyin.Style.NORMAL, errors='ignore')
        pinyin_word_pairs.append([pinyin, word])
    return pinyin_word_pairs


def count_pinyin_words(pinyin_word_pairs, database_path):
    """
    Count how many times the same pinyin-word pair appears.

    Args:
        pinyin_word_pairs: A list of pair (pinyin, word).
        database_path: Path to a sqlite database file.
    """
    try:
        connection = sqlite3.connect(database_path, isolation_level=None)
        cursor = connection.cursor()
        # 关闭写同步以加速
        cursor.execute("""pragma synchronous = off""")
        # 显式开启事务以加速
        cursor.execute("""begin transaction;""")
        for pinyin, word in pinyin_word_pairs:
            pinyin = ' '.join(pinyin)
            cursor.execute("""
                update PinyinWord
                set count = count + 1
                where pinyin = '%s' and word = '%s';
                """ % (pinyin, word))
            if cursor.rowcount == 0:
                cursor.execute("""
                    insert into PinyinWord (pinyin, word, count)
                    values ('%s', '%s', 1);
                    """ % (pinyin, word))
        cursor.execute("""commit transaction;""")
        connection.commit()
    finally:
        cursor.close()
        connection.close()


def bake_dataset_pinyin_word():
    # 无自定义拼音库，控制pypinyin不做copy操作, 以减少内存占用
    os.environ['PYPINYIN_NO_DICT_COPY'] = 'true'
    # 设置文件和数据库路径
    news_dirname = os.path.join(os.path.pardir, "data", "sina_news_utf8")
    news_filenames = os.listdir(news_dirname)
    database_path = os.path.join(os.path.pardir, "data", "counter.db")
    for news_filename in news_filenames:
        with open(os.path.join(news_dirname, news_filename), 'r') as f:
            print("Reading " + news_filename + "...")
            news_texts = get_news_text(f)
            # 逐条分析新闻以减少内存占用
            for news_text in news_texts:
                news_words = get_words(news_text)
                news_pinyin_word_pairs = get_pinyin(news_words)
                count_pinyin_words(news_pinyin_word_pairs, database_path)


"""
Convert sina news to pinyin-word counts
"""
if __name__ == "__main__":
    bake_dataset_pinyin_word()
