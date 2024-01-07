from aiogram.utils.keyboard import InlineKeyboardBuilder
from core.utils.callbackdata import CardData

def choice_card():
    card_kb = InlineKeyboardBuilder()
    card_kb.button(text='🟡Тинькофф', callback_data=CardData(bank='Tinkoff', number='2200 0000 0000 0000'))
    card_kb.button(text='🟢Сбербанк', callback_data=CardData(bank='Sberbank', number='1100 0000 0000 0000'))
    card_kb.button(text='Отмена', callback_data='cancel')
    card_kb.adjust(1)
    return card_kb.as_markup()