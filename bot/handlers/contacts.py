from aiogram import Router, F
from aiogram.types import CallbackQuery
from bot.keyboards import inline
from ..static.texts import user as user_text
from ..filters.callback_data import Menu, MenuButton


router = Router()


@router.callback_query(Menu.filter(F.button == MenuButton.CONTACTS))
async def contacts(call: CallbackQuery):
    await call.message.edit_text(user_text.CONTACTS, 
                                 reply_markup=inline.to_keyboard('menu'))