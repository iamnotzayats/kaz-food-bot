import os
from dotenv import load_dotenv
from datetime import datetime
from sqlalchemy.orm import sessionmaker, relationship, DeclarativeBase
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, create_engine

# Загрузка переменных окружения
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path)
db_path = os.getenv('DB_PATH')

engine = create_engine(db_path)
Session = sessionmaker(bind=engine)
session = Session()

# Определение моделей
class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    department_id = Column(Integer, ForeignKey('departments.id'))

    department = relationship('Department', back_populates='users')
    reviews = relationship('Review', back_populates='user')

class Department(Base):
    __tablename__ = 'departments'

    id = Column(Integer, primary_key=True, autoincrement=True)
    number = Column(Integer, nullable=False)

    users = relationship('User', back_populates='department')

class Cafeteria(Base):
    __tablename__ = 'cafeterias'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    time_from = Column(String(20), nullable=False)
    time_to = Column(String(20), nullable=False)

    menus = relationship('Menu', back_populates='cafeteria')
    reviews = relationship('Review', back_populates='cafeteria')

class Menu(Base):
    __tablename__ = 'menus'

    id = Column(Integer, primary_key=True, autoincrement=True)
    cafeteria_id = Column(Integer, ForeignKey('cafeterias.id'))
    soups = Column(String(255), nullable=True)
    dish = Column(String(255), nullable=False)
    drinks = Column(String(255), nullable=False)
    additional = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    cafeteria = relationship('Cafeteria', back_populates='menus')

class Review(Base):
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    cafeteria_id = Column(Integer, ForeignKey('cafeterias.id'))
    rating = Column(Integer, nullable=False)
    comment = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship('User', back_populates='reviews')
    cafeteria = relationship('Cafeteria', back_populates='reviews')

# Создание таблиц в базе данных
Base.metadata.create_all(engine)

