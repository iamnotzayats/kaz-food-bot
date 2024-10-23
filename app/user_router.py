from aiogram import Router, F
from aiogram.filters import CommandStart, Command

from aiogram.types import Message

user_router = Router()

@user_router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(
        f"<b>Приветствуем тебя, <i>{message.from_user.full_name}</i></b>\n\n" +
        "Представляем вам нашего КАЗ.Столовые — вашего верного помощника в мире вкусной и здоровой пищи!" +
        "С нашим ботом вы всегда будете в курсе самых свежих и аппетитных предложений в ближайших столовых.\n\n" +
        "<b>Что может наш Чат-Бот?</b>\n\n" +
        "🍽️ <i>Меню на каждый день:</i> Узнайте, что приготовлено сегодня и завтра в вашей любимой столовой.\n" +
        "💸 <i>Акции:</i> Будьте в курсе всех скидок и специальных предложений.\n" +
        "📅 <i>Отзывы:</i> Оставить отзыв о наших столовых\n\n" +
        "<b>Почему выбирают нас?</b>\n\n" +
        "🌟 <i>Удобство:</i> Все необходимое в одном месте — не нужно переключаться между приложениями\n" +
        "🌟 <i>Скорость:</i> Мгновенные ответы на все ваши вопросы.\n" +
        "🌟 <i>Персонализация:</i> Индивидуальный подход к каждому пользователю.\n\n" +
        "Присоединяйтесь к нам и наслаждайтесь вкусной и полезной едой каждый день! 🍔🍟\n\n" +
        "Для работы с чат-ботом пройдите небольшую регистрацию, нажав кнопку ниже\n\n"+
        "<b>Нажимая кнопку ниже, вы соглашаетесь на обработку персональных данных</b>"
    )