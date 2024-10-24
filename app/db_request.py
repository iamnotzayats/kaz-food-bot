# db_requests.py

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from sqlalchemy import create_engine, func
import os
from datetime import datetime, date

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

def get_all_canteens():
    session = Session()
    canteens = session.query(Cafeteria).all()
    session.close()
    return [canteen.name for canteen in canteens]

def get_menu_for_today(canteen_name):
    session = Session()
    today = date.today()
    cafeteria = session.query(Cafeteria).filter_by(name=canteen_name).first()
    if not cafeteria:
        session.close()
        return "Столовая не найдена."

    menu = session.query(Menu).filter(
        Menu.cafeteria_id == cafeteria.id,
        func.date(Menu.created_at) == today
    ).first()
    session.close()
    if not menu:
        return "Меню на сегодня не найдено."

    return (
        f"<b>Меню на сегодня в столовой {canteen_name}:</b>\n\n"
        f"<b>Супы:</b> {menu.soups}\n"
        f"<b>Основное блюдо:</b> {menu.dish}\n"
        f"<b>Напитки:</b> {menu.drinks}\n"
        f"<b>Дополнительно:</b> {menu.additional}"
    )

def add_menu(canteen_name, soups, dish, drinks, additional):
    session = Session()
    cafeteria = session.query(Cafeteria).filter_by(name=canteen_name).first()
    if not cafeteria:
        session.close()
        return "Столовая не найдена."

    new_menu = Menu(
        cafeteria_id=cafeteria.id,
        soups=soups,
        dish=dish,
        drinks=drinks,
        additional=additional,
        created_at=datetime.utcnow()
    )
    session.add(new_menu)
    try:
        session.commit()
        session.close()
        return "Меню успешно добавлено."
    except IntegrityError as e:
        session.rollback()
        session.close()
        return f"Ошибка при добавлении меню. {str(e)}"

def add_review(telegram_id, canteen_name, rating, comment):
    session = Session()
    user = session.query(User).filter_by(telegram_id=telegram_id).first()
    cafeteria = session.query(Cafeteria).filter_by(name=canteen_name).first()
    if not user or not cafeteria:
        session.close()
        return "Пользователь или столовая не найдены."

    new_review = Review(
        user_id=user.id,
        cafeteria_id=cafeteria.id,
        rating=rating,
        comment=comment,
        created_at=datetime.utcnow()
    )
    session.add(new_review)
    try:
        session.commit()
        session.close()
        return "Отзыв успешно добавлен."
    except IntegrityError as e:
        session.rollback()
        session.close()
        return f"Ошибка при добавлении отзыва. {str(e)}"

def get_average_rating(canteen_name):
    session = Session()
    cafeteria = session.query(Cafeteria).filter_by(name=canteen_name).first()
    if not cafeteria:
        session.close()
        return "Столовая не найдена."

    average_rating = session.query(func.avg(Review.rating)).filter_by(cafeteria_id=cafeteria.id).scalar()
    session.close()
    if average_rating is None:
        return "отзывов пока нет."

    return f" ⭐️{average_rating:.1f}"

def is_user_admin(telegram_id):
    session = Session()
    user = session.query(User).filter_by(telegram_id=telegram_id).first()
    return user.is_admin if user else False