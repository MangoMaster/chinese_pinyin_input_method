import os
import sqlite3


def create_database(database_path, name):
    """
    Create a database with a table named PinyinChar or PinyinPinyinCharChar to database_path.

    Args:
        database_path: Path to the destination sqlite database file.
        name: Name of the table, PinyinChar or PinyinPinyinCharChar
    """
    try:
        connection = sqlite3.connect(database_path)
        cursor = connection.cursor()
        if name == "PinyinChar":
            cursor.execute("""
                create table PinyinChar(
                    pinyin varchar(8) not null,
                    char character(1) not null,
                    count integer not null,
                    primary key(pinyin, char)
                )""")
        elif name == "PinyinPinyinCharChar":
            cursor.execute("""
                create table PinyinPinyinCharChar(
                    pinyin1 varchar(8) not null,
                    pinyin2 varchar(8) not null,                
                    char1 character(1) not null,
                    char2 character(1) not null,
                    count integer not null,
                    primary key(pinyin1, pinyin2, char1, char2)
                )""")
        else:
            raise ValueError("Database table name is not properly given")
        connection.commit()
    finally:
        cursor.close()
        connection.close()


def check_database(database_path, name):
    """
    Check the sqlite database is properly set.

    Args:
        database_path: Path to a sqlite database file.
        name: Name of the table, PinyinChar or PinyinPinyinCharChar
    """
    try:
        connection = sqlite3.connect(database_path)
        cursor = connection.cursor()
        if name == "PinyinChar":
            cursor.execute("""
                select * from PinyinChar
                """)
        elif name == "PinyinPinyinCharChar":
            cursor.execute("""
                select * from PinyinPinyinCharChar
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
    pinyin_char_database_path = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), os.path.pardir, os.path.pardir, "data", "pinyin_char.db")
    pinyin_pinyin_char_char_database_path = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), os.path.pardir, os.path.pardir, "data", "pinyin_pinyin_char_char.db")
    # create_database(pinyin_char_database_path, "PinyinChar")
    # create_database(pinyin_pinyin_char_char_database_path, "PinyinPinyinCharChar")
    # check_database(pinyin_char_database_path, "PinyinChar")
    check_database(pinyin_pinyin_char_char_database_path, "PinyinPinyinCharChar")
