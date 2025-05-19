from xml.etree import ElementTree as ET
import requests

def get_xml_tree(url: str) -> ET.ElementTree:
    response = requests.get(url=url)
    tree = ET.ElementTree(ET.fromstring(response.content))
    return tree
