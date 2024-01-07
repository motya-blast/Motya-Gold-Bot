from aiogram import Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from core.utils.shopstates import SelectAmount
from core.utils.dbconnect import Request
from core.utils.callbackdata import ApprovedDeclined, RecruitData
from core.keydoard.markup import main_kb


async def choice_otk_odob(callback: CallbackQuery, callback_data: ApprovedDeclined, request: Request, state: FSMContext, bot: Bot):
    value = callback_data.value
    ids = callback_data.ids
    if value == 'odobreno':
        data = await request.get_file_user(ids)
        file_id = data['file_id']
        sum_out = data['sum_out']
        tg_tag = data['tg_tag']
        user_id = data['user_id']
        await bot.send_message(user_id, "Ваш вывод завершен!")
        await request.add_balance_gold(ids, -sum_out)
        await callback.message.edit_text(f"Одобрено!\nUser_id: {user_id}\nShort Name: {tg_tag}\nСумма вывода: {sum_out}")
        await request.delete_out_gold(user_id)
        await state.clear()
        
    else:
        data = await request.get_file_user(ids)
        print(data)
        file_id = data['file_id']
        sum_out = data['sum_out']
        tg_tag = data['tg_tag']
        user_id = data['user_id']
        await bot.send_message(ids, 'В выводе отказано!\nСверьте правильность следующих факторов:\n1. Цена должна быть такой же как и указана\n2.Аватарку нельзя менять!\n3.Возможно были дубликаты создайте заявку заново')
        await callback.message.edit_text(f"Отказано!\nUser_id: {user_id}\nShort Name: {tg_tag}\nСумма вывода: {sum_out}")
        await request.add_balance_gold(user_id, sum_out)
        await request.delete_out_gold(user_id)
        await state.clear()
    

async def choice_app_dec_recruit(callback: CallbackQuery, callback_data: RecruitData, request: Request, state: FSMContext, bot: Bot):
    value = callback_data.value
    sum = callback_data.sum
    ids = callback_data.ids
    if value == 'odobreno':
        data = await request.get_recruit_file_user(ids)
        file_id = data['file_id']
        sum_rub = data['sum_rub']
        bank = data['bank']
        user_id = data['user_id']
        print(file_id)
        await bot.send_message(ids, "Ваш баланс пополнен!")
        await request.change_balance_rub(ids, sum_rub)
        await request.delete_recruit(user_id)
        await callback.message.edit_text("Одобрено!")
        await state.clear()
        
    else:
        data = await request.get_recruit_file_user(ids)
        file_id = data['file_id']
        sum_rub = data['sum_rub']
        bank = data['bank']
        user_id = data['user_id']
        await bot.send_message(ids, 'В пополнение отказано!\nВозможно вы пополнили меньше или больше чем нужно было в этом случае напишите менеджеру @magic779')
        await callback.message.edit_text(f"Отазано!\nID: {ids}")
        await request.delete_recruit(user_id)
        await state.clear()