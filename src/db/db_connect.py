import sqlite3
from pathlib import Path
from typing import Dict, Any
from src.utils.get_yandexgpt_description import get_yandexgpt_description

from gspread.worksheet import Worksheet as Wor

from src.config import settings


# Создание подключения к БД
def db_connect(db_name: str) -> sqlite3.connect:
    script_dir = Path(__file__).parent
    db_path = script_dir / db_name
    return sqlite3.connect(db_path)


# Создание таблицы и БД если ее нет
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

#Вставка позиции в таблицу
def db_insert_item(connection: sqlite3.Connection, table_name: str, data: Dict[str, Any]) -> None:
    cursor = connection.cursor()
    try:
        id_item = data.get('id')
        #Проверяем наличие item в БД
        if id_item is not None:
            cursor.execute(f"SELECT 1 FROM {table_name} WHERE id = ?", (id_item, ))
            exists = cursor.fetchone() is not None
        else:
            exists = False

        #Если item существует обновляем его, если нет - добавляем
        if exists:
            #Обновление записи
            set_clause = ", ".join([f"{col} = ?" for col in data.keys() if col != 'id'])
            values_data = [v for k, v in data.items() if k != 'id']
            values_data.append('id')
            query = f"UPDATE {table_name} SET {set_clause} WHERE id = ?"
            cursor.execute(query, values_data)
            print(f"Данные с id={id_item} обновлены в таблице {table_name}")
        else:
            columns = ", ".join(data.keys())
            placeholders = ", ".join(["?" for _ in data.values()])
            values_data = tuple(data.values())
            query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
            cursor.execute(query, values_data)
            print(f"Данные добавлены в таблицу {table_name}")

        connection.commit()

    except sqlite3.Error as e:
        print("Ошибка при вставке данных в БД", e)
        connection.rollback()
    finally:
        cursor.close()


#Добавть или обновить все данные в БД из Гугл таблиц
def db_add_all_items_from_sheet(worksheet: Wor) ->None:
    data = worksheet.get_all_records()
    conn = db_connect(db_name=settings.DB_NAME)

    try:
        db_create(conn)  # Создаем таблицу

        for item in data:
            db_insert_item(connection=conn, table_name='items', data=item)
    finally:
        conn.close()  # Закрываем соединение только после всех операций


#Создаем описание для позиций и заносим в бд, параметр regenerate_desc - указываем TRUE если надо
#перегенерировать описание, FALSE если только для тех позиций у которых еще нет описания
def db_generate_description_gtp(table_name: str, regenerate_desc: bool = False) -> None:
    conn = db_connect(db_name=settings.DB_NAME)

    cursor = conn.cursor()

    try:

        if regenerate_desc: #Если нужно перегенерировать описание у всех items
            query = f"""
            SELECT * FROM {table_name}
            WHERE status_ya = 'YES';
            """
        else: #генерируем у тех похиций у кого пока нет описания
            query = f"""
            SELECT * FROM {table_name}
            WHERE description IS NULL OR description = '' AND status_ya = 'YES';
            """

        cursor.execute(query)

        rows = cursor.fetchall()

        #для перевода кортежа в словарь берем названия столбцов из таблицы БД
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = [col[1] for col in cursor.fetchall()]

        #обходим полученные строки запрашиваем у GPT описание и записывае в БД
        for row in rows[:2]:
            row_data = dict(zip(columns, row))
            print(row_data)
            data_key_words = [row_data['season']]
            description =get_yandexgpt_description(name=row_data['name'], key_words=data_key_words)
            query_add_description = f"""
                                    UPDATE {table_name} SET description = ? WHERE id = ?
                                    """
            cursor.execute(query_add_description, (description, row_data['id']))

        conn.commit()

    except sqlite3.Error as e:
        print("Ошибка при получении/записи данных из БД: ", e)
        conn.rollback()
    finally:
        cursor.close()






