# user_router.py

from functools import wraps
from aiogram.types import Message, CallbackQuery
from db_request import is_banned

def check_ban(func):
    @wraps(func)
    async def wrapper(message_or_callback: Message | CallbackQuery, *args, **kwargs):
        user_id = message_or_callback.from_user.id
        if is_banned(user_id):
            await message_or_callback.answer("Вы забанены.")
            return
        return await func(message_or_callback, *args, **kwargs)
    return wrapper
