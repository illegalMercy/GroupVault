from aiogram import Router, F
from aiogram.filters.command import Command
from aiogram.types import Message, CallbackQuery
from database import async_session
from database.crud.create import create_user as db_create_user
from database.crud.read import get_free_groups as db_get_free_groups
from ..keyboards import inline
from ..static.texts import user as user_text
from ..filters.callback_data import Menu, MenuButton


router = Router()


@router.message(Command('start'))
async def start(msg: Message):
    await db_create_user(async_session, msg.from_user.id)
    await handle_menu(msg.answer)


@router.callback_query(Menu.filter(F.button == MenuButton.MENU))
async def menu(call: CallbackQuery):
    await handle_menu(call.message.edit_text)


async def handle_menu(msg_method):
    groups = await db_get_free_groups(async_session)    
    await msg_method(user_text.MENU.format(total_groups=len(groups)), 
                     reply_markup=inline.menu())


@router.callback_query(F.data.startswith('#keyboard-divider'))
async def keyboard_divider(call: CallbackQuery):
    await call.answer()
    