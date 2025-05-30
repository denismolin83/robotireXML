from PIL import Image, ImageDraw, ImageFont
import os
import requests
from io import BytesIO
from pathlib import Path
import re

# функция проверяет есть ли файлы содержащие имя, удаляеи такие файлы и формирует
# новое нименовние
def get_next_filename(folder: Path, name: str) -> str:
    # Проверяем, есть ли файлы с таким наименованием
    pattern = re.compile(rf"^{name}(?:_(\d+))?\.png$")
    max_num = 0
    files_to_delete = []

    # Перебираем все файлы в папке
    for filename in os.listdir(folder):
        match = pattern.match(filename)
        if match:
            # Добавляем файл в список для удаления
            files_to_delete.append(filename)

            # Определяем номер файла (если есть)
            num_str = match.group(1)
            if num_str:
                current_num = int(num_str)
                if current_num > max_num:
                    max_num = current_num

    # Удаляем все найденные файлы
    for filename in files_to_delete:
        filepath = os.path.join(folder, filename)
        if os.path.exists(filepath):
            os.remove(filepath)

    # Формируем новое имя
    if max_num > 0 or files_to_delete:
        return f"{name}_{max_num + 1}.png"
    else:
        return f"{name}.png"


#Функция для добавления текста на изображение
def add_text_to_image(image_url: str, texts: list[str], output_filename: str):
    """Добавляет текст с закруглёнными прямоугольниками на изображение"""
    script_dir = Path(__file__).parent.parent  # Поднимаемся на уровень выше из utils
    output_dir = script_dir / 'images_info'

    # Создаем папку, если её нет
    output_dir.mkdir(exist_ok=True)

    # Загрузка изображения
    response = requests.get(image_url)
    response.raise_for_status()
    image = Image.open(BytesIO(response.content)).convert('RGBA')
    draw = ImageDraw.Draw(image)

    # Настройка шрифта
    try:
        font = ImageFont.truetype('arial.ttf', 32)
    except IOError:
        font = ImageFont.load_default(size=12)

    # Параметры отрисовки
    x_start = image.width - 20
    y_start = 20
    padding = 6
    radius = 10
    bg_color = (235, 247, 23, 255)
    text_color = (0, 0, 0)

    for i, text in enumerate(texts):
        if i < 2:
            smaller_font = ImageFont.truetype(font.path, font.size - 8)
            current_font = smaller_font
        else:
            current_font = font

        # Получаем размеры текста
        text_bbox = draw.textbbox((0, 0), text, font=current_font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]

        # Вычисляем координаты прямоугольника
        rect_x1 = x_start - text_width - 2 * padding
        rect_y1 = y_start - padding
        rect_x2 = x_start + padding
        rect_y2 = y_start + text_height + padding

        # Рисуем прямоугольник с закруглёнными углами (новая функция)
        draw.rounded_rectangle(
            (rect_x1, rect_y1, rect_x2, rect_y2),
            radius=radius,
            fill=bg_color
        )

        # Рисуем текст
        text_x = x_start - text_width - padding
        text_y = rect_y1
        draw.text((text_x, text_y), text, font=current_font, fill=text_color)

        # Смещаем позицию для следующего блока
        y_start += text_height + 2 * padding + 10

    # Сохраняем результат
    next_file_name = get_next_filename(folder=output_dir, name=output_filename)
    output_path = output_dir / f"{next_file_name}"
    image.save(output_path)

