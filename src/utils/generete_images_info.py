from src.utils.add_text_to_image import add_text_to_image
from gspread.worksheet import Worksheet as Wor

# Готовим наименовние, разбиваем на 2 строки
def process_string(input_string: str) -> list[str]:
    # Разбиваем строку на части по пробелам
    parts = input_string.split()

    # Удаляем первое слово (индекс 0) и четвертое слово (индекс 3 после удаления первого)
    if len(parts) >= 4:
        del parts[0]  # Удаляем первое слово
        del parts[2]  # Теперь четвертое слово стало третьим (индекс 2)

    # Собираем оставшиеся части обратно в строку
    modified_string = ' '.join(parts)

    # Находим позицию третьего пробела в новой строке
    space_positions = [i for i, char in enumerate(modified_string) if char == ' ']
    if len(space_positions) >= 3:
        third_space_pos = space_positions[2]
        # Разделяем строку на две части по третьему пробелу
        first_part = modified_string[:third_space_pos]
        second_part = modified_string[third_space_pos + 1:]
        return [first_part, second_part]
    else:
        return [modified_string, '']


#Функция генерирует информацию для добавления на изображение, и в конце создает эти изображения
def generate_images_info(worksheet: Wor):
    data = worksheet.get_all_records()

    bags = 'пакеты в подарок'

    for item_data in data[:25]:
        image_texts  = []

        image_texts = process_string(item_data['name'])

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
