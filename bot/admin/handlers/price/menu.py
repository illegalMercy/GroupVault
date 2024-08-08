from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from database import async_session
from database.crud.read import get_prices as db_get_prices
from bot.static.texts.admin import price as admin_text
from ...keyboards import inline
from ...filters.enums import CancelButton
from ...filters.callback_data import Menu, MenuButton


router = Router()


@router.callback_query(Menu.filter(F.button == MenuButton.PRICE))
async def price(call: CallbackQuery):
    prices = await db_get_prices(async_session)
    
    prices_str = '\n'.join([f'<b>{price.age} мес.</b> - {int(price.price)} ₽' 
                            for price in prices])
    await call.message.edit_text(
        admin_text.MENU.format(prices=prices_str), 
        reply_markup=inline.price()
    )


@router.callback_query(F.data == CancelButton.PRICE)
async def cancel_action(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await price(call)