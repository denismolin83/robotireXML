from ftplib import FTP
from src.config import settings

# сохраняем список файлов на ФПТ передаем список фалов которые надо отправить и список файлов которые надо создать на ФПТ
def save_to_ftp(file_parth_local: list[str], remote_path: str, remote_file_name: list[str]) -> None:
    ftp = FTP(settings.FTP_HOST)
    ftp.login(settings.FTP_USER, settings.FTP_PASSWORD)

    ftp.cwd(remote_path)

    for item_file_remote, item_file_parth_local in zip(remote_file_name, file_parth_local):
        with open(item_file_parth_local, 'rb') as file:
            ftp.storbinary('STOR ' + item_file_remote, file)

    ftp.quit()
