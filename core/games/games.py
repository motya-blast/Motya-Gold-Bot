import asyncio
from aiogram.types.dice import Dice, DiceEmoji
from aiogram.methods.send_dice import SendDice
from aiogram import Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from core.games.get_slot_result import get_result_text
from core.utils.dbconnect import Request



async def slot_machine(message: Message, bot: Bot, request: Request):
    balance = await request.check_balance_gold(message.from_user.id)
    try:
        if int(message.text) <= balance:
            if int(message.text) >= 10:
                result_dice = await message.answer_dice(emoji='🎰')
                await asyncio.sleep(2)
                answer, gold, super_pres = get_result_text(result_dice=result_dice.dice.value, bid=int(message.text))
                await request.add_balance_gold(message.from_user.id, gold)
                balance = await request.check_balance_gold(message.from_user.id)
                answer = answer+f'Ваш баланс: {balance} G'
                if super_pres == False:
                    await message.answer(answer)
                else:
                    await message.answer(answer)
                    await bot.send_photo(chat_id="-1002129409161", photo='AgACAgIAAxkBAAIMgGWN4ShUerFDWbo0OoxlQKHoOrOqAAKU1zEb38xwSFB5kwIGdKkyAQADAgADeQADMwQ',
                                         caption=f'У нас есть СУПЕР победитель!\nИ это @{message.from_user.username} !\nОн выиграл {gold} G!\nПоздравим в коментариях!')
            else:
                await message.answer(f'Ставка должна быть не меньше 10!')        
        else:
            await message.answer(f'У вас нет столько золота!\nНа вашем балансе {balance}')
    except ValueError:
        await message.answer('Введите число!')
