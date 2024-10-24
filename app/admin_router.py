# admin_router.py

from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from keyboards import *
from states import *
from db_request import *

admin_router = Router()

@admin_router.message(F.text == "Админ меню")
async def admin_menu(message: Message):
    if is_user_admin(message.from_user.id):
        telegram_id = message.from_user.id
        keyboard = get_menu_keyboard(telegram_id)
        await message.answer("Выберите действие:")
    else:
        await message.answer("У вас нет прав администратора!")
