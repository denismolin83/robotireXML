import requests
from src.config import settings

def get_yandexgpt_description(name: str, key_words: list[str]) -> str:
    key_words_sting = ', '.join(key_words)



    messages = [
        {
            "role": "system",
            "text": "Ты — маркетолог. Напиши описание товара для маркетплейса. Используй заданные название товара, категорию и ключевые слова.",
        },
        {
            "role": "user",
            "text": f"Название товара: '{name}'. Категория: Авто - Шины и диски - Шины. Ключевые слова: {key_words_sting}.",
        }
    ]

    str_name_keywords = f"Название товара: {name}. Категория: Авто - Шины и диски - Шины. Ключевые слова: {key_words_sting}."

    prompt = {
            "modelUri": f"gpt://{settings.FOLDER_ID_YANDEX}/yandexgpt-lite",
            "completionOptions": {
            "stream": False,
            "temperature": 0.4,
            "maxTokens": "2000",
            "reasoningOptions": {
              "mode": "DISABLED"
            }
          },
        "messages": [
            {
                "role": "system",
                "text": "Ты — маркетолог. Напиши описание товара для маркетплейса Яндеккс Маркет. Используй заданные название товара, категорию и ключевые слова. "
                        "Длинна от 500 символов"
            },

            {
                "role": "system",
                "text": "Для генерации используй следующий пример и сделай по примеру: Шина 185/65 15 88H Yokohama Bluearth ES32 - это летняя шина, разработанная для легковых автомобилей. "
                        "Шина имеет ширину профиля 185 мм, высоту профиля 65 и диаметр R15. Индекс нагрузки составляет 88, что означает, что шина способна выдерживать нагрузку до 560 кг. Индекс максимальной скорости H (до 210 км/ч), что позволяет использовать шину на дорогах с высокими скоростями."
                        "Уровень внешнего шума составляет всего 68 дБ, что соответствует 1 низкому классу. Это означает, что шина обеспечивает низкий уровень шума, что делает поездку более комфортной."
                        "Шина обладает высокой износостойкостью, достигающей 400.0. Это означает, что шина прослужит долго и сохранит свои характеристики на протяжении всего срока эксплуатации."
                        "Симметричный тип рисунка протектора обеспечивает отличное сцепление на мокрой дороге и гарантирует безопасность на дороге в любую погоду."
                        "Шина не оснащена технологией RunFlat, Seal, направленным протектором, технологией 'тихие шины', шипами и камерной технологией."
                        "Выбирая шину 185/65 15 88H Yokohama Bluearth ES32, вы получаете надежный и качественный продукт, который обеспечит безопасность и комфорт на дороге."
            },

            {
                "role": "user",
                "text": f"Название товара: {name}. Категория: Авто - Шины и диски - Шины. Ключевые слова: {key_words_sting}."
            }
        ]
    }

    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Api-Key {settings.API_KEY_YANDEX}",
    }

    response = requests.post(url, headers=headers, json=prompt)
    result = response.json()
    #print(result['result']['alternatives'][0]['message']['text'])
    return result['result']['alternatives'][0]['message']['text']


get_yandexgpt_description(name='Шина 165/65 14 79H Triangle TE301', key_words=['Размер 165/65 14', 'Летние', 'Индексы скорости и нагрузки: 79H'])