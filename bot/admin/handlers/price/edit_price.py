from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from database import async_session
from database.crud.read import get_prices as db_get_prices
from database.crud.update import update_price as db_update_price
from bot.static.texts.admin import price as admin_text
from ...keyboards import inline
from ...filters.enums import CancelButton
from ...states.admin import Price as PriceFSM
from ...filters.callback_data import Price, PriceButton, EditPrice


router = Router()


@router.callback_query(Price.filter(F.button == PriceButton.EDIT_PRICE))
async def select_group_age(call: CallbackQuery):
    prices = await db_get_prices(async_session)

    price_dict = {price.age: price.price for price in prices}

    await call.message.edit_text(
        admin_text.SELECT_GROUP_AGE, 
        reply_markup=inline.group_age_for_price_editing(price_dict)
    )


@router.callback_query(EditPrice.filter())
async def handle_group_age_selection(call: CallbackQuery, 
                                     callback_data: EditPrice, 
                                     state: FSMContext):
    await call.message.edit_text(
        admin_text.EDIT_PRICE, 
        reply_markup=inline.cancel_button('edit_price')
    )
    await state.update_data(age=callback_data.age, price=callback_data.price)
    await state.set_state(PriceFSM.edit_price)


@router.message(PriceFSM.edit_price)
async def edit_price(msg: Message, state: FSMContext):
    try:
        new_price = float(msg.text)
    except ValueError:
        await msg.answer(
            admin_text.ERROR_EDIT_PRICE, 
            reply_markup=inline.cancel_button('edit_price')
        )
        return

    state_data = await state.get_data()
    await db_update_price(async_session, state_data['age'], new_price)

    await msg.answer(
        admin_text.SUCCESS_EDIT_PRICE.format(old_price=int(state_data['price']), 
                                             new_price=int(new_price)), 
        reply_markup=inline.to_keyboard('edit_price')
    )
    await state.clear()


@router.callback_query(F.data == CancelButton.EDIT_PRICE)
async def cancel_action(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await select_group_age(call)