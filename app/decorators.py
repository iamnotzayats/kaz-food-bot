# user_router.py

from functools import wraps
from aiogram.types import Message, CallbackQuery
from db_request import is_banned, check_account

def check_ban(func):
    @wraps(func)
    async def wrapper(message_or_callback: Message | CallbackQuery, *args, **kwargs):
        user_id = message_or_callback.from_user.id
        if is_banned(user_id):
            await message_or_callback.answer("Вы забанены.")
            return
        return await func(message_or_callback, *args, **kwargs)
    return wrapper
# decorators.py

from functools import wraps
from aiogram.types import Message, CallbackQuery
from db_request import check_account
from keyboards import get_keyboard_register

def check_account_exists(func):
    @wraps(func)
    async def wrapper(message_or_callback: Message | CallbackQuery, *args, **kwargs):
        user_id = message_or_callback.from_user.id
        if not check_account(user_id):
            if isinstance(message_or_callback, CallbackQuery):
                await message_or_callback.message.answer("Вы не зарегистрированы. Пожалуйста, пройдите регистрацию.", reply_markup=get_keyboard_register())
            else:
                await message_or_callback.answer("Вы не зарегистрированы. Пожалуйста, пройдите регистрацию.", reply_markup=get_keyboard_register())
            return
        return await func(message_or_callback, *args, **kwargs)
    return wrapper

