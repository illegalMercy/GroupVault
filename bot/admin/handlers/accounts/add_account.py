from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from database import async_session
from database.crud.create import create_session as db_create_session
from bot.client_api import TelethonClient
from bot.client_api.functions import get_password_hash
from bot.static.texts.admin import accounts as admin_text
from ...keyboards import inline
from ...states.admin import Accounts as AccountsFSM
from ...filters.callback_data import Account, AccountButton


router = Router()


@router.callback_query(Account.filter(F.button == AccountButton.ADD_ACCOUNT))
async def add_account(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text(
        admin_text.ADD_ACCOUNT, 
        reply_markup=inline.cancel_button('accounts')
    )
    await state.set_state(AccountsFSM.add_session_str)


@router.message(AccountsFSM.add_session_str)
async def handle_session_string(msg: Message, state: FSMContext):
    await msg.answer(
        admin_text.ADD_2FA_PASSWORD, 
        reply_markup=inline.cancel_button('accounts')
    )
    await msg.delete()

    await state.update_data(session_str=msg.text)
    await state.set_state(AccountsFSM.add_password)


@router.message(AccountsFSM.add_password)
async def handle_password(msg: Message, state: FSMContext):
    state_data = await state.get_data()

    try:
        async with TelethonClient(state_data['session_str']) as client:
            pwd_hash = await get_password_hash(client, msg.text)
    except (ValueError, ConnectionError):
        await msg.answer(
            admin_text.ACCOUNT_ACCESS_ERROR, 
            reply_markup=inline.to_keyboard('accounts')
        )
        await state.clear()
        return
        
    await msg.answer(
        admin_text.ADD_ACCOUNT_NAME, 
        reply_markup=inline.cancel_button('accounts')
    )
    await msg.delete()
 
    await state.update_data(password=pwd_hash)
    await state.set_state(AccountsFSM.add_account_name)


@router.message(AccountsFSM.add_account_name)
async def handle_name(msg: Message, state: FSMContext):
    state_data = await state.get_data()
    await db_create_session(async_session, state_data['session_str'], 
                            state_data['password'], msg.text)
    await msg.answer(
        admin_text.ADD_ACCOUNT_SUCCESS,
        reply_markup=inline.to_keyboard('accounts')
    )
    await state.clear()

