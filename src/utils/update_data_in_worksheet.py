from gspread.worksheet import Worksheet as Wor
from xml.etree import ElementTree as ET
from src.utils.status_ya_enum import StatusYa
import pandas as pd


def add_or_update_element(lst: list[dict], element: dict) -> list[dict]:
    for item in lst:
        if item['id'] == element['id']:
            element['status_ya'] = item['status_ya']
            item.update(element)
            return lst

    element['status_ya'] = StatusYa.NEW.value
    lst.append(element.copy())
    return lst

#Обновляем данные в листе и добавляем новый элемент если его нет в листе
def update_data_in_worksheet(worksheet: Wor, root: ET.Element):
    data = worksheet.get_all_records()
    new_element = {}
    print(len(data), data)
    print('------------------')


    for index, offer in enumerate(root.findall('.//offer')):
        new_element['id'] = int(offer.get('id'))
        new_element['name'] = offer.find('name').text
        new_element['count'] = int(offer.find('count').text)
        new_element['price'] = int(offer.find('price').text)
        data = add_or_update_element(data, new_element)

    print(len(data), data)

    df = pd.DataFrame(data, columns=['id', 'name', 'count', 'price', 'status_ya'])
    worksheet.update([df.columns.values.tolist()] + df.values.tolist())
