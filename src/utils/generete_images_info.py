from src.utils.add_text_to_image import add_text_to_image
from gspread.worksheet import Worksheet as Wor

#Функция генерирует информацию для добавления на изображение, и в конце создает эти изображения
def generate_images_info(worksheet: Wor):
    data = worksheet.get_all_records()

    bags = 'пакеты в подарок'

    for item_data in data[:25]:
        image_texts  = []

        name_to_image = item_data['name'].replace('Шина ', '')
        image_texts.append(name_to_image)

        if item_data['year']:
            image_texts.append(f'{str(item_data['year'])} год')

        image_texts.append(bags)

        if item_data['season']:
            season = item_data['season']
            if season == 'зима':
                season = 'зима липучка'
            image_texts.append(season)

        if item_data['country']:
            image_texts.append(item_data['country'])


        add_text_to_image(image_url=item_data['picture'],
                          texts=image_texts,
                          output_filename=str(item_data['id']))
