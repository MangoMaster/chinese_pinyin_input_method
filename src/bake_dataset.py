import json
import re
import jieba
import pypinyin
import sqlite3


def get_news_text(news_file):
    """
    Retrieve text from news file.

    Args:
        news_file: A file containing news.
            Every line contains a piece of news in json, title:新闻标题 html:新闻正文.

    Returns:
        A list of texts in news.
    """
    news_texts = []
    for news in news_file:
        news_data = json.loads(news)
        news_texts.append(news_data['title'])
        news_texts.append(news_data['html'])
    return news_texts


def get_words(texts):
    """
    Cut text into words.

    Arg:
        texts: A list of text, each text is a Chinese sentence.

    Returns:
        A list of words cut from texts.
    """
    words = []
    # 只考虑中文字符
    chinese_words = re.compile(u"[\u4e00-\u9fa5]+")
    for text in texts:
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
    Count how many times pinyin-word pair happen.

    Args:
        pinyin_word_pairs: A list of pair (pinyin, word).
        database_path: Path to a sqlite database file.
    """
    try:
        connection = sqlite3.connect(database_path, isolation_level=None)
        cursor = connection.cursor()
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
        connection.commit()
    finally:
        cursor.close()
        connection.close()


"""
Convert sina news to pinyin-word counts
"""
if __name__ == "__main__":
    import os
    news_dirname = "../data/sina_news_utf8"
    news_filenames = os.listdir(news_dirname)
    database_path = "../data/counter.db"
    for news_filename in news_filenames:
        print("Reading " + news_filename)
        with open(os.path.join(news_dirname, news_filename), 'r') as f:
            news_texts = get_news_text(f)
            news_words = get_words(news_texts)
            news_pinyin_word_pairs = get_pinyin(news_words)
            count_pinyin_words(news_pinyin_word_pairs, database_path)
