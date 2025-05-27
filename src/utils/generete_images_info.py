from src.utils.add_text_to_image import add_text_to_image
from gspread.worksheet import Worksheet as Wor


def generate_images_info(worksheet: Wor):
    data = worksheet.get_all_records()

    test_data = data[0]

    print(test_data)
    season = 'зима шипы'
    bags = 'пакеты в подарок'
    year_to_image = f'{str(test_data['year'])} год'

    add_text_to_image(image_url=test_data['picture'],
                      texts=[year_to_image, bags, season, test_data['country']],
                      output_filename=str(test_data['id']))


    # add_text_to_image(image_url='https://images.robotyre.ru/productimages/c67a709e1482451991fb5dc9a324019b/Big.png',
    #                   texts=['165/65 14 79H Triangle TE301', '2025 год', 'пакеты в подарок', 'зима шипы', 'Россия'], output_filename='../test/output.png')
