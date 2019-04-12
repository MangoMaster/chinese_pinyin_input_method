import sqlite3


def create_database(database_path):
    """
    Create a database to database_path.

    Args:
        database_path: Path to a sqlite database file.
    """
    try:
        connection = sqlite3.connect(database_path)
        cursor = connection.cursor()
        cursor.execute("""
            create table PinyinWord(
                pinyin varchar(50) not null,
                word varchar(10) not null,
                count integer not null,
                primary key(pinyin, word)
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
            select * from PinyinWord
            """)
        data = cursor.fetchall()
        print(data, len(data))
    finally:
        cursor.close()
        connection.close()


"""
Create or check sqlite database.
"""
if __name__ == "__main__":
    database_path = "../data/counter.db"
    # create_database(database_path)
    check_database(database_path)
