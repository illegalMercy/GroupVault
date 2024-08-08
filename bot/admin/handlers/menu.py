from aiogram import Router, F
from aiogram.filters.command import Command
from aiogram.types import Message, CallbackQuery
from database import async_session
from database.crud.read import get_admin as db_get_admin
from bot.static.texts.admin import menu as admin_text
from ..keyboards import inline
from ..filters.callback_data import Menu, MenuButton


router = Router()


@router.message(Command('admin_panel'))
async def start(msg: Message):
    if not await db_get_admin(async_session, msg.from_user.id):
        return

    await msg.delete()
    await handle_menu(msg.answer)


@router.callback_query(Menu.filter(F.button == MenuButton.MENU))
async def menu(call: CallbackQuery):
    await handle_menu(call.message.edit_text)


async def handle_menu(msg_method):
    await msg_method(admin_text.MENU, reply_markup=inline.menu())
