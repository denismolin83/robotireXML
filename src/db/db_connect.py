import sqlite3
from pathlib import Path
from typing import Dict, Any

from gspread.worksheet import Worksheet as Wor


# Создание подключения к БД
def db_connect(db_name: str) -> sqlite3.connect:
    return sqlite3.connect(db_name)

# Создание таблициы и БД если ее нет
def db_create(connection: sqlite3.connect):
    cursor = connection.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS items(
                    itemid INTEGER PRIMARY KEY AUTOINCREMENT,
                    id INTEGER, 
                    name TEXT,
                    count INTEGER,
                    price INTEGER,
                    status_ya TEXT,
                    picture TEXT,
                    year INTEGER,
                    country TEXT,
                    season TEXT,
                    description TEXT);""")

    connection.commit()
    cursor.close()


def db_insert_item(connection: sqlite3.Connection, table_name: str, data: Dict[str, Any]) -> None:
    cursor = connection.cursor()
    try:
        columns = ', '.join(data.keys())
        placeholders = ", ".join(["?" for _ in data.values()])
        values = tuple(data.values())
        query = f"""INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"""

        cursor.execute(query, values)

        connection.commit()

        print(f"Данные успешно добавлены в таблицу {table_name}")

    except sqlite3.Error as error:
        print("Ошибка при вставке данных в БД", error)
        connection.rollback()
    finally:
        cursor.close()



def db_add_all_items_from_sheet(worksheet: Wor):
    data = worksheet.get_all_records()
    script_dir = Path(__file__).parent

    conn = db_connect('items.db')
    try:
        db_create(conn)  # Создаем таблицу

        for item in data[:25]:
            db_insert_item(conn, 'items', item)
    finally:
        conn.close()  # Закрываем соединение только после всех операций



