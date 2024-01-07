from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject
from typing import Callable, Dict, Any, Awaitable

from core.utils.dbconnect import Request

from datetime import datetime

# def ban_list(request: Request, user_id: int):
    
    
class CheckBanUser(BaseMiddleware):
    # def __init__(self, request):
        # ban_list = Request.check_ban(user_id)
        # return ban_list
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        user = data['event_from_user']
        ban_info = Request.check_ban(user.id)
        # ban_info = await ban_list(request, int(user.id))
        if ban_info:
            datas_ban = ban_info['ban_date']
            datas_unban = ban_info['unban_date']
            await event.answer(f'Вы заблокированы за нарушение правил!\nЕсли вы считает что произошла ошибка напишите сюда:\n@magic779')
            await event.answer(f'Блокировка закончится: {datas_unban}\nЧерез {datas_unban - datetime.now()}')
        else:
            await event.answer(f'Ok')
            return await handler(event, data)