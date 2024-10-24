# user_router.py

from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from keyboards import *
from states import *
from db_request import *
from decorators import *

user_router = Router()

# user_router.py

@user_router.message(CommandStart())
@check_ban
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
            "<b>Нажимая кнопку ниже, вы соглашаетесь на обработку персональных данных</b>",
            reply_markup=get_keyboard_register()
        )

@user_router.callback_query(F.data == 'register')
@check_ban
async def process_callback_register(callback_query: CallbackQuery, state: FSMContext):
    telegram_id = callback_query.from_user.id
    if check_account(telegram_id):
        await callback_query.message.answer('Вы уже зарегистрированы!')
    else:
        await callback_query.message.answer("Введите номер отдела:")
        await state.set_state(RegistrationStates.waiting_for_department_number)

@user_router.message(RegistrationStates.waiting_for_department_number)
@check_ban
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
        await message.answer("Пользователь успешно зарегистрирован.", reply_markup=get_canteens_keyboard())
    except IntegrityError as e:
        session.rollback()
        session.close()
        await message.answer(f"Ошибка при регистрации пользователя. {str(e)}")

    await state.clear()

@user_router.message(F.text.in_(get_all_canteens()))
@check_ban
@check_account_exists
async def process_canteen_selection(message: Message, state: FSMContext):
    selected_canteen = message.text
    await state.update_data(selected_canteen=selected_canteen)
    await message.answer(f"Рейтинг данной столовой: {get_average_rating(selected_canteen)}", reply_markup= get_menu_keyboard())

@user_router.message(F.text == "Меню на сегодня")
@check_ban
@check_account_exists
async def process_menu_request(message: Message, state: FSMContext):
    data = await state.get_data()
    selected_canteen = data.get('selected_canteen')
    if not selected_canteen:
        await message.answer("Пожалуйста, сначала выберите столовую.")
        return

    menu = get_menu_for_today(selected_canteen)
    await message.answer(menu, parse_mode='HTML')

@user_router.message(F.text == "Главное меню")
@check_ban
@check_account_exists
async def process_main_menu_request(message: Message):
    await message.answer("Вы вернулись в главное меню.", reply_markup=get_canteens_keyboard())

@user_router.message(F.text == "Оставить отзыв")
@check_ban
@check_account_exists
async def process_review_request(message: Message, state: FSMContext):
    data = await state.get_data()
    selected_canteen = data.get('selected_canteen')
    if not selected_canteen:
        await message.answer("Пожалуйста, сначала выберите столовую.")
        return

    await message.answer(f"Вы выбрали столовую {selected_canteen}. Введите рейтинг столовой (от 1 до 5):")
    await state.set_state(ReviewStates.waiting_for_rating)

@user_router.message(ReviewStates.waiting_for_rating)
@check_ban
@check_account_exists
async def process_rating(message: Message, state: FSMContext):
    try:
        rating = int(message.text)
        if rating < 1 or rating > 5:
            raise ValueError
    except ValueError:
        await message.answer("Пожалуйста, введите корректный рейтинг (от 1 до 5):")
        return

    await state.update_data(rating=rating)
    await message.answer("Введите комментарий к отзыву:")
    await state.set_state(ReviewStates.waiting_for_comment)

@user_router.message(ReviewStates.waiting_for_comment)
@check_ban
@check_account_exists
async def process_comment(message: Message, state: FSMContext):
    comment = message.text
    data = await state.get_data()
    selected_canteen = data.get('selected_canteen')
    rating = data.get('rating')
    telegram_id = message.from_user.id

    result = add_review(telegram_id, selected_canteen, rating, comment)
    await message.answer(result, reply_markup=get_canteens_keyboard())
    await state.clear()
