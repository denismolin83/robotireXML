from xml.etree import ElementTree as ET
import requests

#Получаем дерево из xml файла по ссылке robotyre
def get_xml_tree(url: str) -> ET.ElementTree:
    response = requests.get(url=url)
    tree = ET.ElementTree(ET.fromstring(response.content))
    return tree
