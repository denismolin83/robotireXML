from gspread.worksheet import Worksheet as Wor
from xml.etree import ElementTree as ET
from src.utils.save_to_ftp import save_to_ftp


def delete_elements(worksheet: Wor, tree: ET.ElementTree, filename_local: str):
    data = worksheet.get_all_records()
    root = tree.getroot()

    need_ids = []
    #получаем список нужных элементов (которые надо передавать)
    for item in data:
        if item['status_ya'] == 'YES':
            need_ids.append(item['id'])

    print(need_ids)

    offers = root.findall('.//offer')
    offers_to_delete = []
    for offer in offers:
        if int(offer.get('id')) not in need_ids:
            offers_to_delete.append(offer)


    for offer in offers_to_delete:
        root.find('.//offers').remove(offer)

    tree.write(filename_local, encoding='UTF-8', xml_declaration=True)

