from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_keyboard_register():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Регистрация', callback_data='register')]
    ])
    return keyboard