import xml.etree.ElementTree as ET
import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

url = 'https://lk.robotyre.ru/Shop/MarketUnloadings/GetYandexMarketUnloading?customerId=48691'
response = requests.get(url=url)
xml_data = response.content

root = ET.fromstring(xml_data)

#Установка соединения с Гугл таблицами
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('robotyrexml-97b85c8843b9.json', scope)
client = gspread.authorize(creds)
spreadsheet = client.open('robotire_XML')
worksheet = spreadsheet.get_worksheet(0)

data = []

for index, offer in enumerate(root.findall('.//offer')):
    name = offer.find('name').text
    count = offer.find('count').text
    price = offer.find('price').text
    id_offer = offer.get('id')
    print(index, id_offer, name, count, price)
    data.append([id_offer, name, count, price])


df = pd.DataFrame(data, columns=["ID", "Name", "Count", "Price"])
worksheet.update([df.columns.values.tolist()] + df.values.tolist())