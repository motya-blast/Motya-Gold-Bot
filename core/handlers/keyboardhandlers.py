import asyncio
import re

from aiogram import Bot, Dispatcher
from aiogram import F
from aiogram.types import Message
from aiogram.filters import Command, CommandObject, CommandStart

from core.utils.jsonget import get_kurs
from core.utils.dbconnect import Request
from core.keydoard.markup import main_kb


async def rate_kb(message: Message, bot: Bot, request: Request):
    rate =await request.get_kurs()
    rate = round(rate, 2)
    await message.answer(f'Курс:\n1 Gold - {rate}\n'
                        f'100 Gold - {rate*100}\n'
                        f'500 gold - {rate*500}')
    await message.answer(f'Курс считается так:\n'
                         f'500 * {rate} = {rate*500}', reply_markup=main_kb)

async def sell_gold(message: Message, bot: Bot):
    await message.answer(f'Золото продается по курсу 0.30\nНапишите менеджеру @magic779:')

async def recruit_balance(message: Message, bot: Bot):
    await message.answer(f'Введите сумму на которую хотите полонить баланс:')
    
async def profile(message: Message, bot: Bot, request: Request):
    await message.answer(f'Имя: {message.from_user.first_name}\n'
                         f'ID: {message.from_user.id}\n'
                         f'Баланс: {await request.check_balance_rub(message.from_user.id)}\n'
                         f'Баланс золота: {await request.check_balance_gold(message.from_user.id)}\n'
                         f'Рефералов: {await request.check_user_ref(message.from_user.id)}\n'
                         f'Заработано голды: 0\n')

async def income(message: Message, bot: Bot):
    await message.answer(f'Есть 2 способа заработка:\n'
                            f'1. Заработок голды:\n'
                            f'Вам нужно приглашать рефералов и когда они будут покупать золото\n'
                            f'Вы будете получать процент от их кол-ва золота\n'
                            f'В зависимости от вашего уровня\n'
                            f'Например: Ваш реферал купил 1000 золото вы получите 3%\n'
                            f'Т.е. 30 золота\n\n'
                            f'2. Заработок рублей:\n'
                            f'Если вы ютубер, тик токер или еще кто-либо\n'
                            f'Вы можете написать мне в личку(@magic779) и отправить свой аккаунт соц сети\n'
                            f'И мы с вами обусдим условия вашего заработка\n'
                            f'Подробнее можете прочитать в этой статье ↓\n'
                            f'https://telegra.ph/Zarabotok-Motya-Gold-12-16')

async def support(message: Message, bot: Bot):
    await message.answer('Напишите нашему менеджеру он ответит на любые ваши вопросы!\n@magic779')