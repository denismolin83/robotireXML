from gspread.worksheet import Worksheet as Wor
from xml.etree import ElementTree as ET


def delete_elements(worksheet: Wor, tree: ET.ElementTree, filename_local: str):
    data = worksheet.get_all_records()
    root = tree.getroot()

    need_ids = []
    #получаем список нужных элементов (которые надо передавать)
    for item in data:
        if item['status_ya'] == 'YES':
            need_ids.append(item['id'])

    print(len(need_ids), need_ids)

    offers = root.findall('.//offer')
    offers_to_delete = []
    for offer in offers:
        #disabled - тег отвечающий за возврат/скрытие товара с витрины
        disable_element = ET.SubElement(offer, 'disabled')
        disable_element.text = 'false'

        #Добавляем зачеркнутую цену
        old_price = ET.SubElement(offer, 'oldprice')
        old_price.text = str(round(int(offer.find('price').text) * 1.1))

        #Диаметр - привод в соответствие с требованиями
        diameter_param = offer.find('.//param[@name="Диаметр"]')
        if diameter_param is not None:
            diameter_param.text = 'R' + str(int(float(diameter_param.text)))

        #Ширину профиля - привод в соответствие с требованиями
        width_param = ET.SubElement(offer, 'param')
        width_param.set('name', 'Ширина профиля')
        width_param.text = str(int(float(offer.find('param[@name="Ширина"]').text)))

        # Высоту профиля - привод в соответствие с требованиями
        height_param = ET.SubElement(offer, 'param')
        height_param.set('name', 'Высота профиля')
        height_param.text = str(int(float(offer.find('param[@name="Высота"]').text)))

        # Камерные
        height_param = ET.SubElement(offer, 'param')
        height_param.set('name', 'Камерные')
        height_param.text = 'Нет'

        if int(offer.get('id')) not in need_ids:
            offers_to_delete.append(offer)


    for offer in offers_to_delete:
        root.find('.//offers').remove(offer)


    tree.write(filename_local, encoding='UTF-8', xml_declaration=True)