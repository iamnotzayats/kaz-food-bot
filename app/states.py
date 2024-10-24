# states.py

from aiogram.fsm.state import State, StatesGroup

class RegistrationStates(StatesGroup):
    waiting_for_department_number = State()

class ReviewStates(StatesGroup):
    waiting_for_canteen_name = State()
    waiting_for_rating = State()
    waiting_for_comment = State()