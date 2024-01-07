from aiogram import Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from core.utils.shopstates import SelectAmount
from core.utils.dbconnect import Request
from core.utils.callbackdata import WeapInfo, CardData
from core.keydoard.markup import main_kb
from core.keydoard.inlinecancel import cancel_kb



async def choice_weapon(callback: CallbackQuery, callback_data: WeapInfo, request: Request, state: FSMContext):
    amount_out_gold = await state.get_data()
    amount_out_gold = amount_out_gold['amount']
    amount_out_gold = int(amount_out_gold)
    
    one_pre_cent = amount_out_gold/100
    plus = one_pre_cent*25
    amount_out_gold = amount_out_gold + plus
    
    print(callback.from_user.id)
    
    stattrack = callback_data.stattrack
    types = callback_data.types
    name = callback_data.name
    skin = callback_data.skin


    if types == 'cancel_weapon':
        await callback.message.edit_text('Отмена', reply_markup=main_kb)
        await request.gold_freeze(callback.from_user.id, 0)
    else:
        if stattrack:
            print("call 1 ", amount_out_gold)
            answer = f'Хорошо выставляйте {stattrack} {name} {skin} за {amount_out_gold}\nЗатем отправьте скриншот выставленнного скина'
            await callback.message.edit_text(answer, reply_markup=cancel_kb())
            await state.set_state(SelectAmount.GET_PHOTO_GOLD)
        elif stattrack == None or stattrack == "None":
            print("call 2 ", amount_out_gold)
            answer = f'Хорошо выставляйте {name} {skin} за {amount_out_gold}\nЗатем отправьте скриншот выставленнного скина'
            await callback.message.edit_text(answer, reply_markup=cancel_kb())
            await state.set_state(SelectAmount.GET_PHOTO_GOLD)
            
async def choice_card(callback: CallbackQuery, callback_data: CardData, request: Request, state: FSMContext):
    card = callback_data.bank
    number = callback_data.number
    await state.update_data(bank=card)
    
    if card.lower in ['тинькофф']:
        await callback.message.edit_text(f'Реквизиты для перевода\n'
                                      f'- - - - - - - - - - - - - - -\n'
                                      f'{number}\n'
                                      f'- - - - - - - - - - - - - - -\n'
                                      f'В описание перевода добавьте ваш тег @{callback.from_user.username}\n'
                                      f'После совершения переводая\n'
                                      f'Пришлите скриншот оплаты\n',
                                      reply_markup=cancel_kb())
        await state.set_state(SelectAmount.GET_RECRUIT_BALANCE_PHOTO)
    else:
        await callback.message.edit_text(f'Реквизиты для перевода\n'
                                      f'- - - - - - - - - - - -\n'
                                      f'{number}\n'
                                      f'- - - - - - - - - - - -\n'
                                      f'В описание перевода добавьте ваш тег @{callback.from_user.username}\n'
                                      f'После совершения переводая\n'
                                      f'Пришлите скриншот оплаты\n',
                                      reply_markup=cancel_kb())
        await state.set_state(SelectAmount.GET_RECRUIT_BALANCE_PHOTO)