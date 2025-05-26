from PIL import Image, ImageDraw, ImageFont, ImageOps
import os
import requests
from io import BytesIO


def add_rounded_rectangle(draw, bbox, radius, fill):
    """Рисует прямоугольник с закруглёнными углами"""
    x1, y1, x2, y2 = bbox

    # Рисуем 4 угловых эллипса
    draw.ellipse((x1, y1, x1 + 2 * radius, y1 + 2 * radius), fill=fill)
    draw.ellipse((x2 - 2 * radius, y1, x2, y1 + 2 * radius), fill=fill)
    draw.ellipse((x1, y2 - 2 * radius, x1 + 2 * radius, y2), fill=fill)
    draw.ellipse((x2 - 2 * radius, y2 - 2 * radius, x2, y2), fill=fill)

    # Рисуем прямоугольные части
    draw.rectangle((x1 + radius, y1, x2 - radius, y2), fill=fill)
    draw.rectangle((x1, y1 + radius, x2, y2 - radius), fill=fill)


def add_text_to_image(image_url: str, texts: list[str], output_filename: str):
    os.makedirs('output', exist_ok=True)

    response = requests.get(image_url)
    response.raise_for_status()

    image = Image.open(BytesIO(response.content)).convert('RGBA')
    draw = ImageDraw.Draw(image)

    try:
        font = ImageFont.truetype('arial.ttf', 24)
    except IOError:
        font = ImageFont.load_default(size=12)

    x_start = image.width - 20
    y_start = 20
    padding = 6  # Отступ от текста до края прямоугольника
    radius = 10  # Радиус закругления углов
    bg_color = (235, 247, 23, 255)  # Цвет фона с прозрачностью

    for text in texts:
        # Получаем размеры текста
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]

        # Вычисляем координаты прямоугольника
        rect_x1 = x_start - text_width - 2 * padding
        rect_y1 = y_start - padding
        rect_x2 = x_start + padding
        rect_y2 = y_start + text_height + padding

        # Рисуем прямоугольник с закруглёнными углами
        add_rounded_rectangle(
            draw,
            (rect_x1, rect_y1, rect_x2, rect_y2),
            radius=radius,
            fill=bg_color
        )

        # Рисуем текст
        text_x = x_start - text_width - padding
        text_y = y_start
        draw.text((text_x, text_y), text, font=font, fill=(0, 0, 0))

        # Смещаем Y для следующей строки
        y_start += text_height + 2 * padding + 10  # Отступ между блоками

    output_path = os.path.join('output', output_filename)
    image.save(output_path)


# def add_text_to_image(image_url: str, texts: list[str], output_filename: str):
    # os.makedirs('output', exist_ok=True)
    #
    # response = requests.get(image_url)
    # response.raise_for_status()
    #
    # image = Image.open(BytesIO(response.content)).convert('RGBA')
    # draw = ImageDraw.Draw(image)
    #
    # try:
    #     font = ImageFont.truetype('arial.ttf', 26)
    # except IOError:
    #     font = ImageFont.load_default(size=12)
    #
    # x = image.width - 20
    # y = 20
    #
    # for text in texts:
    #     text_bbox = draw.textbbox((0, 0), text, font=font)
    #     text_width = text_bbox[2] - text_bbox[0]
    #     text_height = text_bbox[3] - text_bbox[1]
    #
    #     text_x = x - text_width
    #     text_y = y
    #
    #     #draw.text((x, y), text, font=font, fill=(0, 0, 0))
    #     draw.rectangle((text_x-2, text_y-2, text_x+text_width+5, text_y+text_height+5), fill=(235, 247, 23, 50))
    #     draw.text((text_x, text_y), text, font=font, fill=(0, 0, 0))
    #
    #     y += text_height + 15
    #
    # output_path = os.path.join('output', output_filename)
    # image.convert('RGB').save(output_path)


add_text_to_image(image_url='https://images.robotyre.ru/productimages/c67a709e1482451991fb5dc9a324019b/Big.png',
                  texts=['2025 год', 'пакеты в подарок', 'зима шипы'], output_filename='output.png')