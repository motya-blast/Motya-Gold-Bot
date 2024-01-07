from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault

all_commands = '''
/start - Начало работы
/help - Помощь
/rate - Информация о курсе
/ref - Получить реф. ссылку
'''

async def set_commands(bot: Bot):
    commands = [
        BotCommand(
            command='start',
            description='Начало работы'
        ),
        BotCommand(
            command='help',
            description='Помощь'
        ),
        BotCommand(
            command='rate',
            description='Узнать актуальный курс'
        ),
        BotCommand(
            command='ref',
            description='Получит реф. ссылку'
        )
    ]

    await bot.set_my_commands(commands, BotCommandScopeDefault())
    
async def set_admins_commands(bot: Bot):
    commands = [
        BotCommand(
            command='panel',
            description='Начало работы'
        ),
        BotCommand(
            command='help',
            description='Помощь'
        ),
        BotCommand(
            command='rate',
            description='Узнать актуальный курс'
        ),
        BotCommand(
            command='ref',
            description='Получит реф. ссылку'
        )
    ]

    await bot.set_my_commands(commands, BotCommandScopeDefault())