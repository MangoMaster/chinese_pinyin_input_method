import sqlite3
import json


def build_table(database_path):
    """
    Build pinyin-word table using database_path.
        table: pinyin -> (most frenquent word, count).

    Args:
        database_path: Path to a sqlite database file.

    Returns:
        pinyin-word table: A dict, key->pinyin, value->(word, count)
    """
    pinyin_word_table = dict()
    try:
        connection = sqlite3.connect(database_path)
        cursor = connection.cursor()
        cursor.execute("""
            select pinyin, word, count from PinyinWord
            """)
        while True:
            data_list = cursor.fetchmany()
            if not data_list:
                break
            for (pinyin, word, count) in data_list:
                if pinyin in pinyin_word_table:
                    if count > pinyin_word_table[pinyin][1]:
                        pinyin_word_table[pinyin] = (word, count)
                else:
                    pinyin_word_table[pinyin] = (word, count)
    finally:
        cursor.close()
        connection.close()
    return pinyin_word_table


def save_table(pinyin_word_table, pinyin_word_table_path):
    """
    Save pinyin_word_table to pinyin_word_table_path.

    Args:
        pinyin_word_table: A dict
        pinyin_word_table_path: Path to the destination pinyin-word-table json file.
    """
    with open(pinyin_word_table_path) as f:
        json.dump(pinyin_word_table, f)


"""
Build and save pinyin-word table.
"""
if __name__ == "__main__":
    database_path = "../data/counter.db"
    pinyin_word_table_path = "../data/pinyin_word_table.json"
    pinyin_word_table = build_table(database_path)
    save_table(pinyin_word_table, pinyin_word_table_path)
