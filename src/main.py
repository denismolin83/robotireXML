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


#Обновляем данные в листе и добавляем новый элемент если его нет в листе
update_data_in_worksheet(worksheet=worksheet, root=root)
