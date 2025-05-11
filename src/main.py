import pandas as pd
from src.config import settings
from src.utils.get_worksheet import get_worksheet
from src.utils.get_xml_root import get_xml_root
from src.utils.update_data_in_worksheet import update_data_in_worksheet

#получаем корневой элемент xml роботайра по ссылке
root = get_xml_root(settings.URL_XML)

#получаем лист с данными шин из Гугл таблиц, для
#сравнения с данными из роботайра
worksheet = get_worksheet(name_sheet=settings.SPREADSHEET)

# data = []
#
# for index, offer in enumerate(root.findall('.//offer')):
#     name = offer.find('name').text
#     count = offer.find('count').text
#     price = offer.find('price').text
#     id_offer = offer.get('id')
#     print(index, id_offer, name, count, price)
#     data.append([id_offer, name, count, price])


# df = pd.DataFrame(data, columns=["ID", "Name", "Count", "Price"])
# worksheet.update([df.columns.values.tolist()] + df.values.tolist())

update_data_in_worksheet(worksheet=worksheet, root=root)
