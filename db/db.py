from models.models import User
from passlib.context import CryptContext

from models.models import User, Role

USER_DATA = {}


# Функция для получения пользовательских данных на основе имени пользователя
def get_user(username: str):
    if username in USER_DATA:
        user_data = USER_DATA[username]
        return User(**user_data)
    return None