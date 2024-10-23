from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from sqlalchemy import create_engine
import os

from models import *


dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path)
db_path = os.getenv('DB_PATH')

# Создание движка и сессии
engine = create_engine(db_path)
Session = sessionmaker(bind=engine)
session = Session()


def check_account(telegram_id):
    user = session.query(User).filter_by(telegram_id=telegram_id).first()
    if user:
        session.close()
        return True
    else:
        return False

def registration(telegram_id, username, sp_number):
    department = session.query(Department).filter_by(number=sp_number).first()
    if not department:
        session.close()
        return "Отдел с таким номером не существует."

    new_user = User(telegram_id=telegram_id, username=username, department_id=department.id)
    session.add(new_user)
    try:
        session.commit()
        session.close()
        return "Пользователь успешно зарегистрирован."
    except IntegrityError as e:
        session.rollback()
        session.close()
        return f"Ошибка при регистрации пользователя. {str(e)}"

