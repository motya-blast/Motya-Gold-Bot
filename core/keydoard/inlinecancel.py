from aiogram import Bot
from aiogram.utils.keyboard import InlineKeyboardBuilder

def cancel_kb():
    cancel_kb = InlineKeyboardBuilder()
    cancel_kb.button(text='Отмена', callback_data='cancel')
    cancel_kb.adjust(1)
    return cancel_kb.as_markup()