from ftplib import FTP
from src.config import settings

# сохраняем список файлов на ФПТ передаем список фалов которые надо отправить, и список файлов которые надо создать на ФПТ
def get_files_list_from_ftp(remote_path: str) -> list[str]:
    ftp = FTP(settings.FTP_HOST)
    ftp.login(settings.FTP_USER, settings.FTP_PASSWORD)
    files = []

    ftp.cwd(remote_path)
    files = ftp.nlst()
    ftp.quit()

    return files
