from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup
from db_request import *

def get_keyboard_register():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Регистрация', callback_data='register')]
    ])
    return keyboard

def get_canteens_keyboard():
    canteens = get_all_canteens()
    kb = [
        [KeyboardButton(text=f"{canteen}")] for canteen in canteens
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

    return keyboard



def get_menu_keyboard():
    kb = [
        [KeyboardButton(text="Меню на сегодня")],
        [KeyboardButton(text="Оставить отзыв")],
        [KeyboardButton(text="Главное меню")]
    ]


    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

    return keyboard

