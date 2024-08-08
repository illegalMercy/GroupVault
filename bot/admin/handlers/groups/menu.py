from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from database import async_session
from database.crud.read import get_free_groups as db_get_free_groups
from bot.static.texts.admin import groups as admin_text
from ...keyboards import inline
from ...filters.enums import CancelButton
from ...filters.callback_data import Menu, MenuButton


router = Router()


@router.callback_query(Menu.filter(F.button == MenuButton.GROUPS))
async def groups(call: CallbackQuery):
    groups = await db_get_free_groups(async_session)
    
    await call.message.edit_text(
        admin_text.MENU.format(total_groups=len(groups)), 
        reply_markup=inline.groups()
    )


@router.callback_query(F.data == CancelButton.GROUPS)
async def cancel_action(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await groups(call)