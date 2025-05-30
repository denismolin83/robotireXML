import os
from ftplib import FTP

from src.config import settings
from src.utils.save_to_ftp import save_to_ftp


def delete_images_from_ftp(folder: str):
    """
    Удаляет все файлы в указанной папке на FTP-сервере.
    """

    try:
        # Подключаемся к FTP-серверу
        with FTP(settings.FTP_HOST) as ftp:
            ftp.login(settings.FTP_USER, settings.FTP_PASSWORD)

            # Переходим в нужную папку
            ftp.cwd(folder)

            # Получаем список файлов
            files = ftp.nlst()

            # Удаляем каждый файл
            for file in files:
                try:
                    ftp.delete(file)
                except Exception as e:
                    print(f"Ошибка при удалении {file}: {e}")

    except Exception as e:
        print(f"Ошибка подключения к FTP: {e}")


# Загрузка изображений на FTP-сервер
def upload_images_to_ftp(local_path: str) -> None:
    image_files = os.listdir(local_path)
    image_files_with_path = []

    delete_images_from_ftp(settings.REMOTE_IMAGES_PATH)

    for file_name in image_files:
        image_files_with_path.append(os.path.join(local_path, file_name))

    save_to_ftp(file_parth_local=image_files_with_path,
                remote_path=settings.REMOTE_IMAGES_PATH,
                remote_file_name=image_files)


folder_path = os.path.abspath('../images_info')
upload_images_to_ftp(folder_path)