from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import (CallbackQuery, InlineKeyboardButton,
                           InlineKeyboardMarkup, Message)

storage: MemoryStorage = MemoryStorage()
user_dict: dict[int, dict[str, str | int | bool]] = {}
class FSMFillForm(StatesGroup):
    # Создаем экземпляры класса State, последовательно
    # перечисляя возможные состояния, в которых будет находиться
    # бот в разные моменты взаимодейтсвия с пользователем
    fill_departure = State()        # Состояние ожидания ввода места отправления
    fill_arrival = State()         # Состояние ожидания ввода места прибытия
    fill_date_departure = State()      # Состояние ожидания выбора даты отправления
    fill_price = State()     # Состояние ожидания ввода цены
fill_pri="123"
   