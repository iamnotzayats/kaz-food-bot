from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from keyboards import *
from states import *
from db_request import *

user_router = Router()

@user_router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    if check_account(message.from_user.id) == False:
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
            "<b>Нажимая кнопку ниже, вы соглашаетесь на обработку персональных данных</b>",
            reply_markup=get_keyboard_register()
        )
    else:
        await message.answer('Вы уже зарегистрированы!')

@user_router.callback_query(F.data == 'register')
async def process_callback_register(callback_query: CallbackQuery, state: FSMContext):
    telegram_id = callback_query.from_user.id
    if check_account(telegram_id):
        await callback_query.message.answer('Вы уже зарегистрированы!')
    else:
        await callback_query.message.answer("Введите номер отдела:")
        await state.set_state(RegistrationStates.waiting_for_department_number)

@user_router.message(RegistrationStates.waiting_for_department_number)
async def process_department_number(message: Message, state: FSMContext):
    telegram_id = message.from_user.id
    sp_number = message.text
    username = message.from_user.username
    department = session.query(Department).filter_by(number=sp_number).first()

    if not department:
        await message.answer("Отдел с таким номером не существует. Пожалуйста, введите номер отдела снова:")
        return

    new_user = User(telegram_id=telegram_id, username=username, department_id=department.id)
    session.add(new_user)
    try:
        session.commit()
        session.close()
        await message.answer("Пользователь успешно зарегистрирован.")
    except IntegrityError as e:
        session.rollback()
        session.close()
        await message.answer(f"Ошибка при регистрации пользователя. {str(e)}")

    await state.clear()
