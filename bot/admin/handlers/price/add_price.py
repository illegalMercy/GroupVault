from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from database import async_session
from database.crud.read import get_prices as db_get_prices
from database.crud.create import create_price as db_create_price
from bot.static.texts.admin import price as admin_text
from ...keyboards import inline
from ...states.admin import Price as PriceFSM
from ...filters.callback_data import Price, PriceButton


router = Router()


@router.callback_query(Price.filter(F.button == PriceButton.ADD_PRICE))
async def enter_group_age(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text(
        admin_text.ENTER_GROUP_AGE, 
        reply_markup=inline.cancel_button('price')
    )
    await state.set_state(PriceFSM.add_group_age)


@router.message(PriceFSM.add_group_age)
async def handle_group_age(msg: Message, state: FSMContext):
    try:
        group_age = int(msg.text)
    except ValueError:
        await msg.answer(
            admin_text.ERROR_GROUP_AGE, 
            reply_markup=inline.cancel_button('price')
        )
        return
    
    prices = await db_get_prices(async_session)

    is_group_age_exist = next((True for price in prices if group_age == price.age), None)
    if is_group_age_exist:
        await msg.answer(
            admin_text.ERROR_GROUP_AGE_EXIST, 
            reply_markup=inline.cancel_button('price')
        )
        return
    
    await msg.answer(
        admin_text.ENTER_GROUP_PRICE, 
        reply_markup=inline.cancel_button('price')
    )
    await state.update_data(group_age=group_age)
    await state.set_state(PriceFSM.add_group_price)


@router.message(PriceFSM.add_group_price)
async def handle_group_price(msg: Message, state: FSMContext):
    try:
        price = float(msg.text)
    except ValueError:
        await msg.answer(
            admin_text.ERROR_ADD_PRICE, 
            reply_markup=inline.cancel_button('price')
        )
        return
    
    state_data = await state.get_data()
    group_age = state_data['group_age']

    await db_create_price(async_session, group_age, price)

    await msg.answer(
        admin_text.SUCCESS_ADD_PRICE.format(group_age=group_age, price=price), 
        reply_markup=inline.to_keyboard('price')
    )
    await state.clear()