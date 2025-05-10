from xml.etree import ElementTree as ET
import requests

def get_xml_root(url: str):
    response = requests.get(url=url)
    xml_data = response.content
    return ET.fromstring(xml_data)
