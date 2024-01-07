from aiogram.utils.keyboard import InlineKeyboardBuilder
from core.utils.jsonget import get_kurs

def games_kb():
    game_kb = InlineKeyboardBuilder()
    game_kb.button(text='Слоты🎰', callback_data='slot-machine')
    game_kb.adjust(1)
    return game_kb.as_markup()