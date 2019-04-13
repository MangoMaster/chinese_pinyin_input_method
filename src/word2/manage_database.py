import os
import sqlite3


def create_database(database_path):
    """
    Create a database with a table named PinyinPinyinWordWord to database_path.

    Args:
        database_path: Path to the destination sqlite database file.
    """
    try:
        connection = sqlite3.connect(database_path)
        cursor = connection.cursor()
        cursor.execute("""
            create table PinyinPinyinWordWord(
                pinyin1 varchar(96) not null,
                pinyin2 varchar(96) not null,                
                word1 varchar(16) not null,
                word2 varchar(16) not null,
                count integer not null,
                primary key(pinyin1, pinyin2, word1, word2)
            )""")
        connection.commit()
    finally:
        cursor.close()
        connection.close()


def check_database(database_path):
    """
    Check the sqlite database is properly set.

    Args:
        database_path: Path to a sqlite database file.
    """
    try:
        connection = sqlite3.connect(database_path)
        cursor = connection.cursor()
        cursor.execute("""
            select * from PinyinPinyinWordWord
            """)
        data = cursor.fetchall()
        print(data, len(data))
    finally:
        cursor.close()
        connection.close()


"""
Create or check sqlite database PinyinPinyinWordWord.
"""
if __name__ == "__main__":
    database_path = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), os.path.pardir, os.path.pardir, "data", "pinyin_pinyin_word_word.db")
    # create_database(database_path)
    check_database(database_path)
