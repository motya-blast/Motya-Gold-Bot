from aiogram.fsm.state import StatesGroup, State

class SelectAmount(StatesGroup):
    GET_BUY_GOLD = State()
    GET_OUT_GOLD = State()
    GET_PHOTO_GOLD = State()
    GET_SELL_GOLD = State()
    GET_RECRUIT_BALANCE = State()
    GET_RECRUIT_BALANCE_PHOTO = State()

class Promocode(StatesGroup):
    GET_PROMO = State()
    GET_CREATE_PROMO = State()

class GetStavka(StatesGroup):
    GET_SLOTS = State()
    GET_DICE = State()
    