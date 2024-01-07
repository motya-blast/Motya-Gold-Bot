from aiogram import Bot
from aiogram.types import Message, CallbackQuery, LabeledPrice, PreCheckoutQuery
from aiogram.fsm.context import FSMContext
from core.utils.shopstates import SelectAmount, Promocode, GetStavka
from core.utils.dbconnect import Request
from core.keydoard import inlineweapon as inweapon
from core.keydoard.inlinecard import choice_card
from core.keydoard.markup import glav_menu, main_kb
from dotenv import load_dotenv
import os

load_dotenv()
ADMIN_ID = os.getenv("ADMIN_ID")





async def get_buy_gold(message: Message, state: FSMContext,  request: Request):
    global sum_gold
    kurs = await request.get_kurs()
    balance = await request.check_balance_rub(message.from_user.id)
    sum_gold = balance/kurs
    sum_gold = round(sum_gold, 0)
    if balance == 0:
        await message.answer(f'На вашем балансе нету денег, вы можете его пополнить!', reply_markup=main_kb)
    else:
        await message.answer(f"У вас {balance} рублей, на них вы можете купить: {sum_gold} G\nВыберите количество золота которое хотите купить: ", reply_markup=glav_menu)
        await state.set_state(SelectAmount.GET_BUY_GOLD)
    
async def sshet_buy_gold(message: Message, state: FSMContext, request: Request, bot: Bot):
    kurs = await request.get_kurs()
    balance = await request.check_balance_rub(message.from_user.id)
    try:
        if int(message.text) in ([i for i in range(30, 50001)]):
            if int(message.text) <= sum_gold:
                await state.update_data(amount_gold=int(message.text))
                await message.answer(f'Вы купили {message.text} золота')
                await request.add_sum_ref(message.from_user.id, int(message.text))
                await request.add_balance_gold(message.from_user.id, int(message.text))
                rub = int(message.text)*kurs
                await request.change_balance_rub(message.from_user.id, -rub)
                balance_rub = await request.check_balance_rub(message.from_user.id)
                balance_gold = await request.check_balance_gold(message.from_user.id)
                await message.answer(f'На вашем балансе:\n'
                                    f'Золото: {balance_gold}\n'
                                    f'Рублей: {balance_rub}', reply_markup=glav_menu)
                await state.clear()
            else:
                await message.answer(f'Вы не можете купить больше чем {sum_gold}', reply_markup=glav_menu)
                
        else:
            await message.answer(f'Введите сумму от 30 голды', reply_markup=glav_menu)
    except ValueError:
        await message.answer(f'Введите число!', reply_markup=glav_menu)
        return
        

async def out_gold(message: Message, state: FSMContext, request: Request):
    global balance_gold
    balance_gold = await request.check_balance_gold(message.from_user.id)
    if balance_gold == 0:
        await message.answer(f'На вашем балансе нету золота, вы можете его приобрести!', reply_markup=main_kb)
    else:
        if not (await request.get_user_out(message.from_user.id)):
            await message.answer(f"У вас есть {balance_gold} голды\nВыберите сколько вы хотите вывести:", reply_markup=glav_menu)
            await state.set_state(SelectAmount.GET_OUT_GOLD)
        else:
            await message.answer(f"У вас уже есть заявка на вывод, дождитесь ее закрытия\nПока можете сыграть в игры!", reply_markup=main_kb)
            await state.clear()
    
async def out_gold_weapon(message: Message, state: FSMContext, request: Request, bot: Bot):
    print(await state.get_data())
    try:
        if int(message.text) > balance_gold:
            await message.answer(f'На вашем балансе нету такой суммы!\nУ вас {balance_gold} G', reply_markup=glav_menu)
        else:
            if int(message.text) in ([i for i in range(29, 150000)]):
                await state.update_data(amount=message.text)
                amount = await state.get_data()
                amount = amount['amount']
                amount = int(amount)
                await message.answer(f'Выберите оружие для вывода!\nВы хотите вывести {message.text} голды',
                                    reply_markup=inweapon.get_inline_keyboard())
            else:
                await message.answer('Ввывод от 29 до 149.999 голды', reply_markup=glav_menu)
    except ValueError:
        await message.answer('Введите число!', reply_markup=glav_menu)

async def recruit_balance(message: Message, state: FSMContext, request: Request):
    if not (await request.get_user_recruit(message.from_user.id)):
        await message.answer(f'Введите сумму на которую хотите пополнить: ', reply_markup=glav_menu)
        await state.set_state(SelectAmount.GET_RECRUIT_BALANCE)
    else:
        await message.answer(f"У вас уже есть заявка на пополнение, дождитесь ее закрытия\nПока можете сыграть в игры!", reply_markup=main_kb)
        await state.clear()

async def recruit_balance_sum(message: Message, state: FSMContext, request: Request, bot: Bot):
    kurs = await request.get_kurs()
    try:
        if int(message.text) in ([i for i in range(25, 1_000_000)]):
            await state.update_data(sum_rub=message.text)
            sum = await state.get_data()
            sum = sum['sum_rub']
            sum = int(sum)
            await message.answer(f'За {sum} вы можете приобрести {round((sum/kurs), 2)}\n'
                                 f'Выберите куда вам будет удобно отправить\n'
                                 f'В описание оплаты напишите ваш TG тег!\n',
                                 reply_markup=choice_card())

        else:
            await message.answer('Минимальная сумма пополнения 25 рублей')
    except ValueError as e:
        print(e)
        await message.answer('Введите число!')
    
async def promocode(message: Message, state: FSMContext):
    await message.answer(f'Введите промокод:')
    await state.set_state(Promocode.GET_PROMO)
    
async def get_promocode(message: Message, state: FSMContext, request: Request, bot: Bot):
    data = await request.get_promocode(message.text)
    try:
        gold = data['amount_gold']
        use = data['use']
        if gold != 0:
            if use == 0:
                await request.delete_promocode(message.text)
                await message.answer('Промокод не активен(', reply_markup=main_kb)
            else:
                await request.add_balance_gold(message.from_user.id, gold)
                await request.dec_activate_promo(message.text)
                await message.answer(f'Поздравляю!\nВам начислено {gold} G', reply_markup=main_kb)
                use -= 1
                await bot.send_message(ADMIN_ID, f'Пользователь @{message.from_user.username} ввел промокод {message.text}, и получил {gold} G\nАктивций осталось: {use}')
                await state.clear()
    except TypeError:
        await message.answer('Промокод не найден', reply_markup=main_kb)
        await state.clear()
        

async def get_stavka(call: CallbackQuery, state: FSMContext, request: Request):
    balance = await request.check_balance_gold(call.from_user.id)
    if balance != 0:
        await call.message.answer(f'Введите сумму ставки\nБаланс: {balance}', reply_markup=glav_menu)
        await state.set_state(GetStavka.GET_SLOTS)
    else:
        await call.answer('На ваше балансе нету золота!\nВы можете его пополнить', reply_markup=main_kb)
        await state.clear()