from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from database import async_session
from database.crud.read import get_prices as db_get_prices
from database.crud.delete import delete_price as db_delete_price
from bot.static.texts.admin import price as admin_text
from ...keyboards import inline
from ...states.admin import Price as PriceFSM
from ...filters.callback_data import Price, PriceButton


router = Router()


@router.callback_query(Price.filter(F.button == PriceButton.DEL_PRICE))
async def enter_group_age(call: CallbackQuery, state: FSMContext):
    prices = await db_get_prices(async_session)
    prices_str = '\n'.join([f'<code>{price.age}</code> мес. - {int(price.price)} ₽' 
                            for price in prices])
    
    await call.message.edit_text(
        admin_text.ENTER_GROUP_AGE_FOR_DEL.format(prices=prices_str), 
        reply_markup=inline.cancel_button('price')
    )
    await state.set_state(PriceFSM.del_group_age)


@router.message(PriceFSM.del_group_age)
async def handle_group_age(msg: Message, state: FSMContext):
    try:
        group_age = int(msg.text)
    except ValueError:
        await msg.answer(
            admin_text.ERROR_GROUP_AGE, 
            reply_markup=inline.cancel_button('price')
        )
        return
    
    await db_delete_price(async_session, group_age)

    await msg.answer(
        admin_text.DEL_PRICE_SUCCESS, 
        reply_markup=inline.to_keyboard('price')
    )
    await state.clear()