from aiogram.filters.callback_data import CallbackData

class WeapInfo(CallbackData, prefix='weap'):
    stattrack: str | None = None
    types: str | None=None
    name: str | None = None
    skin: str | None=None

class ApprovedDeclined(CallbackData, prefix='appdec'):
    """Описание:
        Value: принимает в себя транслит одобрено и отказ
        Ids: принимает id пользователя
    """
    value: str
    ids: int

class CardData(CallbackData, prefix='card'):
    bank: str
    number: str

class RecruitData(CallbackData, prefix='recruit'):
    value: str
    sum: int
    ids: int