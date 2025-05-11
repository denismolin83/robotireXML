import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials

from src.config import settings


def get_worksheet(name_sheet: str):
    current_dir = os.path.dirname(__file__)
    parent_dir = os.path.dirname(current_dir)
    file_path = os.path.join(os.path.dirname(parent_dir), settings.CREDENTIALS_FILE)
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(file_path, scope)
    client = gspread.authorize(creds)
    spreadsheet = client.open(name_sheet)
    return spreadsheet.get_worksheet(0)



