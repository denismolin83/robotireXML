from gspread.worksheet import Worksheet as Wor
from xml.etree import ElementTree as ET


def add_or_update_element(lst: list[dict], element: dict) -> list[dict]:
    for item in lst:
        if item['id'] == element['id']:
            item.update(element)
            return lst
    lst.append(element.copy())
    return lst


def update_data_in_worksheet(worksheet: Wor, root: ET.Element):
    data = worksheet.get_all_records()
    new_element = {}

    for index, offer in enumerate(root.findall('.//offer')):
        new_element['id'] = offer.get('id')
        new_element['name'] = offer.find('name').text
        new_element['count'] = offer.find('count').text
        new_element['price'] = offer.find('price').text
        data = add_or_update_element(data, new_element)

