from dotenv import load_dotenv
import os
import re
import logging
import asyncpg
import asyncio
from aiogram_dialog import setup_dialogs
#aiogram
from aiogram import Bot, Dispatcher
from aiogram import F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandObject, CommandStart
from aiogram.fsm.context import FSMContext
#Handlers
from core.handlers.basic import (get_start_ref, get_start, get_help,
                                 get_rate, get_ref, cancel,
                                 com_list_out_gold, get_out_gold, get_recruit_balance,
                                 com_list_recruit_balance, create_promocode, admin_panel)
from core.handlers.keyboardhandlers import (rate_kb,profile, income, support)
from core.handlers.callback import choice_weapon, choice_card
from core.handlers.callbackcanotk import choice_otk_odob, choice_app_dec_recruit
from core.handlers import selectamount as selamo
#Middlewares 
from core.middlewares.dbmiddleware import DbSession
from core.middlewares.start_middleware import CheckBanUser
#KeyBoard
from core.keydoard.markup import main_kb
from core.keydoard import inlineweapon as inweapon
from core.keydoard.inline_game import games_kb
#Utils
from core.utils.dbconnect import Request
from core.utils.commands import set_commands
from core.utils.shopstates import SelectAmount, Promocode, GetStavka
from core.utils.callbackdata import WeapInfo, ApprovedDeclined, RecruitData, CardData
#Games
from core.games.games import slot_machine

load_dotenv()

main_kb_text = {
    "💳Купить золото🍯" : 1,
    '📨Вывести золото🍯': 2,
    'Курс📈': 3,
    'Продать золото💵': 4,
    'Пополнить баланс💳': 5,
    'Профиль👤': 6,
    'Заработок💰': 7,
    'Поддержка📧': 8,
    'Промокод': 9,
    'Игры🕹️': 10,
    'Главное меню↩️': 11
    }

TOKEN = os.getenv("TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DATABASE_NAME = os.getenv("DATABASE_NAME")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT"))

async def start_bot(bot: Bot):
    await set_commands(bot)
    await bot.send_message(ADMIN_ID, text='Я запустился')



async def main():
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s - [%(levelname)s] -  %(name)s - "
                               "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
                        )
    bot = Bot(token=TOKEN, parse_mode="html")
    dp = Dispatcher()
    
    pool_connect = await asyncpg.create_pool(user=DB_USER, password=DB_PASSWORD, database=DATABASE_NAME, host=DB_HOST, port=DB_PORT, command_timeout=60)
    
    dp.startup.register(start_bot)
    
    dp.update.middleware.register(CheckBanUser())
    dp.update.middleware.register(DbSession(pool_connect))
    
    dp.message.register(cancel, F.text.lower() == 'главное меню↩️')
    dp.callback_query.register(cancel, F.data == 'cancel')
    
    dp.message.register(get_start_ref, CommandStart(deep_link=True, magic=F.args.regexp(re.compile(r'ref_(\d+)'))))
    dp.message.register(get_start, Command(commands='start'))
    dp.message.register(get_help, Command(commands='help'))
    dp.message.register(get_rate, Command(commands='rate'))
    dp.message.register(get_ref, Command(commands='ref'))

    dp.callback_query.register(cancel, F.data == 'cancel_weapon')
    dp.callback_query.register(choice_weapon, WeapInfo.filter())
    dp.callback_query.register(choice_otk_odob, ApprovedDeclined.filter())
    dp.callback_query.register(choice_card, CardData.filter())
    dp.callback_query.register(choice_app_dec_recruit, RecruitData.filter())
    dp.callback_query.register(selamo.get_stavka, F.data == 'slot-machine')
    
    dp.message.register(admin_panel, Command(commands='panel'))
    dp.message.register(create_promocode, Command(commands='create_promocode'))
    dp.message.register(com_list_out_gold, Command(commands='out_gold'))
    dp.message.register(com_list_recruit_balance, Command(commands='recruit'))

    dp.message.register(slot_machine, GetStavka.GET_SLOTS)
    dp.message.register(selamo.get_promocode, Promocode.GET_PROMO, F.text)
    dp.message.register(get_recruit_balance, SelectAmount.GET_RECRUIT_BALANCE_PHOTO, F.photo)
    dp.message.register(selamo.recruit_balance_sum, SelectAmount.GET_RECRUIT_BALANCE, F.text)
    dp.message.register(get_out_gold, SelectAmount.GET_PHOTO_GOLD, F.photo)
    dp.message.register(selamo.sshet_buy_gold, SelectAmount.GET_BUY_GOLD, F.text)
    dp.message.register(selamo.out_gold_weapon, SelectAmount.GET_OUT_GOLD, F.text)
    
    
    @dp.message(F.text)
    async def choose_kb(message: Message, state: FSMContext, request: Request, bot: Bot):
        try:
            value = main_kb_text[message.text]
        except KeyError:
            await message.answer("Не понял вас! Используйте команду /help\nИли воспользуйтесь меню↓")
            return

        match value:
            case 1:
                await selamo.get_buy_gold(message, state, request)
            case 2:
                await selamo.out_gold(message, state, request)
            case 3:
                await rate_kb(message, bot, request)
            case 4:
                await message.answer("Напишите менеджеру @magic779 с хештегом #SELL")
            case 5:
                await selamo.recruit_balance(message, state, request)
            case 6:
                await profile(message, bot, request)
            case 7:
                await income(message, bot)
            case 8:
                await support(message, bot)
            case 9:
                await selamo.promocode(message, state)
            case 10:
                await message.answer("На данный момент доступна 1 игра\n"
                                     "Слоты🎰 \n"
                                     "Подробное описание игр можно узнать по ссылке\n"
                                     "https://telegra.ph/Igra-Sloty-12-23\n"
                                     "Выберите игру: ",
                                     reply_markup=games_kb())
            case 11:
                await cancel(message, state, request, bot)
            case _:
                await message.answer("Не понял вас! Используйте команду /help\nИли воспользуйтесь меню↓")
    
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
        
if __name__ == '__main__':
    asyncio.run(main())