from aiogram import Bot
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.types import BotCommand, BotCommandScopeDefault


def create_bot(bot_token: str) -> Bot:
    return Bot(
        token=bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    
async def set_commands(bot: Bot):
    commands = [
        BotCommand(
            command='start',
            description='Меню'
        )
    ]
    await bot.set_my_commands(commands, BotCommandScopeDefault())