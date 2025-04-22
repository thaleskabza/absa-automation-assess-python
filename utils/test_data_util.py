import csv
from models.user_data import UserData

_latest_user: UserData = None


def get_user_data_from_csv(file_name: str, row_index: int) -> UserData:
    path = f"resources/testdata/{file_name}"
    with open(path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        rows = list(reader)
    data = rows[row_index]
    return UserData(
        first_name=data['FirstName'].strip(),
        last_name=data['LastName'].strip(),
        username=data['UserName'].strip(),
        password=data['Password'].strip(),
        company=data['Company'].strip(),
        role=data['Role'].strip(),
        email=data['Email'].strip(),
        mobile_phone=data['Mobilephone'].strip()
    )


def set_latest_user(user: UserData):
    global _latest_user
    _latest_user = user


def get_latest_user() -> UserData:
    return _latest_user