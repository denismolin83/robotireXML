from src.config import settings
from src.utils.get_worksheet import get_worksheet
from src.utils.get_xml_tree import get_xml_tree
from src.utils.delete_elements import delete_elements
from src.utils.save_to_ftp import save_to_ftp
from src.utils.update_data_in_worksheet import update_data_in_worksheet


#получаем корневой элемент xml роботайра по ссылке
tree = get_xml_tree(settings.URL_XML)
root = tree.getroot()

#получаем лист с данными шин из Гугл таблиц, для
#сравнения с данными из роботайра
worksheet = get_worksheet(name_sheet=settings.SPREADSHEET)

#Обновляем данные в листе и добавляем новый элемент если его нет в листе
update_data_in_worksheet(worksheet=worksheet, root=root)

#Формируем файла output.xml с только нужными шинами и выкладываем на FTP shopkolesa.ru
delete_elements(worksheet=worksheet, tree=tree, filename_local='output.xml')

#и выкладываем на FTP shopkolesa.ru
save_to_ftp(file_parth='output.xml')
