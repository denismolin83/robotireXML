from ftplib import FTP
from src.config import settings

def save_to_ftp(file_parth: str) -> None:
    ftp = FTP(settings.FTP_HOST)
    ftp.login(settings.FTP_USER, settings.FTP_PASSWORD)

    ftp.cwd(settings.REMOTE_FILE_PARTH)

    with open(file_parth, 'rb') as file:
        ftp.storbinary('STOR ' +settings.REMOTE_FILE_NAME, file)

    ftp.quit()
