from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

        
main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="💳Купить золото🍯"),
            KeyboardButton(text='📨Вывести золото🍯'),
            KeyboardButton(text='Пополнить баланс💳')
        ],
        [
            KeyboardButton(text='Игры🕹️'),
            KeyboardButton(text='Курс📈'),
            KeyboardButton(text='Промокод')
        ],
        [
            KeyboardButton(text='Продать золото💵'),
            KeyboardButton(text='Заработок💰')
        ],
        [
            KeyboardButton(text='Профиль👤'),
            KeyboardButton(text='Поддержка📧')
        ]
    ],
    resize_keyboard=True
)

glav_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Главное меню↩️')
        ]
    ],
    resize_keyboard=True
)
