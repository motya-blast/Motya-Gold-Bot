import asyncio
import re

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandObject, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder

from aiogram_dialog import DialogManager, StartMode

from core.utils.jsonget import get_kurs
from core.keydoard.markup import main_kb
from core.utils.commands import set_commands, all_commands
from core.utils.callbackdata import ApprovedDeclined, RecruitData
from core.utils.dbconnect import Request

from dotenv import load_dotenv
import os
load_dotenv()
ADMIN_ID = os.getenv("ADMIN_ID")



async def get_start_ref(message: Message, command: CommandObject, bot: Bot, request: Request):
    names_a = message.from_user.username
    idsa = message.from_user.id
    ids = command.args.split("_")[1]
    if await request.check_user(idsa):
        await request.add_data(message.from_user.id, message.from_user.first_name, message.from_user.username)
        await message.answer(f"Добро пожаловать!", reply_markup=main_kb)
        await bot.send_message(ids, text=f"Пользователь @{names_a} уже был ранее зарегистрирован", parse_mode="MarkdownV2")
    else:
        await request.add_data(message.from_user.id, message.from_user.first_name, message.from_user.username)
        await message.answer(f"Добро пожаловать", reply_markup=main_kb)
        await request.add_ref(ids, idsa)
        await bot.send_message(ids, text=f"У вас новый реферал @{names_a}!", parse_mode="MarkdownV2")
    
async def get_start(message: Message, bot: Bot, request: Request):
    await request.add_data(message.from_user.id, message.from_user.first_name, message.from_user.username)
    await message.answer("Добро пожаловать", reply_markup=main_kb)
    await request.check_ban(123)

async def get_rate(message: Message, bot: Bot):
    rate = get_kurs()
    await message.answer(f'Курс:\n1 Gold - {rate}\n'
                        f'100 Gold - {rate*100}\n'
                        f'500 gold - {rate*500}')
    await message.answer(f'Курс считается так:\n'
                        f'500 * {rate} = {rate*500}', reply_markup=main_kb)

async def get_help(message: Message, bot: Bot):
    await message.answer(f'{all_commands}', reply_markup=main_kb)
    
async def get_ref(message: Message, bot: Bot, request: Request):
    ref_href = 't.me/motya_gold_bot?start=ref_' + str(message.from_user.id)
    data_ref = await request.get_data_ref(message.from_user.id)
    invite = data_ref['ref_users']
    sum = data_ref['ref_sum']
    ref_level = data_ref['ref_level']
    if ref_level == 1:
        ref_percent = 3
            
    elif ref_level == 2:
        ref_percent = 5
        
    if ref_level == 3:
        ref_percent = 7
    await message.answer(f'Информация о рефералах:\n'
                         f'Ваш реферальный уровень : {ref_level}\n'
                         f'Приглашенно: {invite}\n'
                         f'Заработано: {sum}\n'
                         f'Процент от пополнений рефералов: {ref_percent}%\n'
                         f'Ваша реф. ссылка:\n<code>{ref_href}</code>\n', parse_mode='HTML', reply_markup=main_kb)

async def get_out_gold(message: Message, bot: Bot, request: Request, state: FSMContext):
    amount_out = await state.get_data()
    amount_out = amount_out['amount']
    amount_out = int(amount_out)
    file_id = message.photo[-1].file_id
    id = message.from_user.id
    await request.save_photo(id, file_id, amount_out, message.from_user.username)
    await message.answer("Заявка подана!")
    await request.add_balance_gold(message.from_user.id, -amount_out)
    data = await request.all_admins()
    for row in data:
        admin_id = row['user_id']
        await bot.send_message(admin_id, f'Новая заявка на вывод голды!!\nИспользуйте команду /out_gold')

async def com_list_out_gold(message: Message, bot: Bot, request: Request):
    admin_data = await request.check_admins(message.from_user.id)
    admin_level = int(admin_data['level'])
    admin_id = int(admin_data['user_id'])
    if admin_level == 1:
        print('1 lvl')
        try:
            data = await request.get_file(29, 70)
            print(data)
            file_id = data['file_id']
            sum_out = data['sum_out']
            tg_tag = data['tg_tag']
            user_id = data['user_id']
            sum_kom = sum_out
            one_per_cent = sum_kom/100
            sum_kom = sum_kom + (one_per_cent*25)
            await bot.send_photo(admin_id, file_id, caption=f"Заявка от {tg_tag}\n"
                                                            f"Сумма вывода: {sum_out}\n"
                                                            f"Сумма вывода с учетом комиссии: {sum_kom}")
            await bot.send_message(admin_id, f"Выберите действие:", reply_markup=build_can(user_id))
        except IndexError:
            await bot.send_message(admin_id, f"Заявки отсутствуют!", reply_markup=main_kb)
    elif admin_level == 2:
        print('2 lvl')
        try:
            data = await request.get_file(71, 230)
            print(data)
            file_id = data['file_id']
            sum_out = data['sum_out']
            tg_tag = data['tg_tag']
            user_id = data['user_id']
            sum_kom = sum_out
            one_per_cent = sum_kom/100
            sum_kom = sum_kom + (one_per_cent*25)
            await bot.send_photo(admin_id, file_id, caption=f"Заявка от {tg_tag}\n"
                                                            f"Сумма вывода: {sum_out}\n"
                                                            f"Сумма вывода с учетом комиссии: {sum_kom}")
            await bot.send_message(admin_id, f"Выберите действие:", reply_markup=build_can(user_id))
        except IndexError:
            await bot.send_message(admin_id, f"Заявки отсутствуют!", reply_markup=main_kb)
            
    elif admin_level == 3:
        print('3 lvl')
        try:
            data = await request.get_file(231, 400)
            print(data)
            file_id = data['file_id']
            sum_out = data['sum_out']
            tg_tag = data['tg_tag']
            user_id = data['user_id']
            sum_kom = sum_out
            one_per_cent = sum_kom/100
            sum_kom = sum_kom + (one_per_cent*25)
            await bot.send_photo(admin_id, file_id, caption=f"Заявка от {tg_tag}\n"
                                                            f"Сумма вывода: {sum_out}\n"
                                                            f"Сумма вывода с учетом комиссии: {sum_kom}")
            await bot.send_message(admin_id, f"Выберите действие:", reply_markup=build_can(user_id))
        except IndexError:
            await bot.send_message(admin_id, f"Заявки отсутствуют!", reply_markup=main_kb)
    
    elif admin_level == 4:
        print('4 lvl')
        try:
            data = await request.get_file(0, 888888)
            print(data)
            file_id = data['file_id']
            sum_out = data['sum_out']
            tg_tag = data['tg_tag']
            user_id = data['user_id']
            sum_kom = sum_out
            one_per_cent = sum_kom/100
            sum_kom = sum_kom + (one_per_cent*25)
            await bot.send_photo(admin_id, file_id, caption=f"Заявка от {tg_tag}\n"
                                                            f"Сумма вывода: {sum_out}\n"
                                                            f"Сумма вывода с учетом комиссии: {sum_kom}")
            await bot.send_message(admin_id, f"Выберите действие:", reply_markup=build_can(user_id))
        except IndexError:
            await bot.send_message(admin_id, f"Заявки отсутствуют!", reply_markup=main_kb)

def build_can(id):
    kb_builder = InlineKeyboardBuilder()
    kb_builder.button(text="Одобрено", callback_data=ApprovedDeclined(value='odobreno', ids=id))
    kb_builder.button(text='Отказано', callback_data=ApprovedDeclined(value='otkaz', ids=id))
    kb_builder.adjust(2)
    return kb_builder.as_markup()

async def get_recruit_balance(message: Message, bot: Bot, request: Request, state: FSMContext):
    data = await state.get_data()
    sum_rub = data['sum_rub']
    bank = data['bank']
    sum_rub = int(sum_rub)
    file_id = message.photo[-1].file_id
    id = message.from_user.id
    await request.save_photo_recruit(file_id, sum_rub, bank, message.from_user.id, message.from_user.username)
    await message.answer("Заявка подана!")
    await bot.send_message(ADMIN_ID, f'Новая заявка на пополнение!\nИспользуйте команду /recruit')

async def com_list_recruit_balance(message: Message, bot: Bot, request: Request):
    if int(message.from_user.id) == int(ADMIN_ID):
        try:
            data = await request.get_recruit_file()
            file_id = data['file_id']
            sum_rub = data['sum_rub']
            tg_tag = data['tg_tag']
            bank = data['bank']
            user_id = data['user_id']

            await bot.send_photo(ADMIN_ID, file_id, caption=f"Заявка от {tg_tag}\n"
                                                            f"Сумма пополнения: {sum_rub}\n"
                                                            f"Перевод на {bank}")
            await bot.send_message(ADMIN_ID, f"Выберите действие:", reply_markup=build_recruit(user_id, sum_rub))
        except IndexError:
            await bot.send_message(ADMIN_ID, f"Заявки отсутствуют!", reply_markup=main_kb)
    
def build_recruit(id, sum):
    kb_builder = InlineKeyboardBuilder()
    kb_builder.button(text="Одобрено", callback_data=RecruitData(value='odobreno', sum=sum, ids=id))
    kb_builder.button(text='Отказано', callback_data=RecruitData(value='otkaz', sum=sum, ids=id))
    kb_builder.adjust(2)
    return kb_builder.as_markup()

async def cancel(message: Message, state: FSMContext, request: Request, bot: Bot):
    #await message.answer('Главное меню:', reply_markup=main_kb)
    await bot.send_message(message.from_user.id, "Главное меню:", reply_markup=main_kb)
    print(await state.get_data())
    await state.clear()
    print(await state.get_data())
    print(message.from_user.id)
    await request.gold_freeze(message.from_user.id, 0)
    

async def create_promocode(message: Message, command: CommandObject, request: Request):
    if int(message.from_user.id) == int(ADMIN_ID):
        try:
            name = command.args.split(' ')[0]
            try:
                gold = command.args.split(' ')[1]
                try:
                    activate = command.args.split(' ')[2]
                    print(name, gold, activate)
                    await request.create_promocode(name, int(gold), activate)
                    await message.answer("Промокод успешно создан!")
                except IndexError:
                    await message.answer(f"Введите имя, кол-во голды и кол-во активаций через пробел")
            except IndexError:
                await message.answer(f"Введите имя, кол-во голды и кол-во активаций через пробел")
        except AttributeError:
            await message.answer(f"Введите имя, кол-во голды и кол-во активаций через пробел")
        
async def admin_panel(message: Message, request: Request):
    data_adm = await request.check_admins(message.from_user.id)
    if data_adm == False:
        await message.answer(f'Не понял вас! Используйте команду /help\nИли воспользуйтесь меню↓')
    else:
        level = data_adm['level']
        answer = ''
        match (level):
            case 1:
                answer = f'Вам доступны команды:\n/panel - админ паенль\n/out_gold - просмотр заявок на вывод'
            case 2:
                answer = f'Вам доступны команды:\n/panel - админ паенль\n/out_gold - просмотр заявок на вывод'
            case 3:
                answer = f'Вам доступны команды:\n/panel - админ паенль\n/out_gold - просмотр заявок на вывод'
            case 4:
                answer = f'Вам доступны команды:\n/panel - админ паенль\n\
                /out_gold - просмотр заявок на вывод\n\
                    /recruit - пополнение баланса\n\
                        /create_promocode - создать промокод\n\
                            /ban - заблокировать пользователя'
        await message.answer(answer)