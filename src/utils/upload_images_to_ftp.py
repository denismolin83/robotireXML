import os
from src.config import settings
from src.utils.save_to_ftp import save_to_ftp

# Загрузка изображений на FTP-сервер
def upload_images_to_ftp(local_path: str) -> None:
    image_files = os.listdir(local_path)
    image_files_with_path = []

    for file_name in image_files:
        image_files_with_path.append(os.path.join(local_path, file_name))

    save_to_ftp(file_parth_local=image_files_with_path,
                remote_path=settings.REMOTE_IMAGES_PATH,
                remote_file_name=image_files)


folder_path = os.path.abspath('../images_info')
upload_images_to_ftp(folder_path)