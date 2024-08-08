from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from database import async_session
from database.crud.read import get_sessions as db_get_sessions
from database.crud.delete import delete_session as db_delete_session
from bot.static.texts.admin import accounts as admin_text
from ...keyboards import inline
from ...states.admin import Accounts as AccountsFSM
from ...filters.callback_data import Account, AccountButton


router = Router()


@router.callback_query(Account.filter(F.button == AccountButton.DEL_ACCOUNT))
async def send_session_ids(call: CallbackQuery, state: FSMContext):
    sessions = await db_get_sessions(async_session)
    accounts_str = '\n'.join([f'{s.id}: <code>{s.name}</code>' for s in sessions])

    await call.message.edit_text(
        admin_text.DEL_ACCOUNT.format(accounts=accounts_str), 
        reply_markup=inline.cancel_button('accounts')
    )
    await state.set_state(AccountsFSM.del_account)


@router.message(AccountsFSM.del_account)
async def del_account(msg: Message, state: FSMContext):
    await db_delete_session(async_session, msg.text)
    await msg.answer(
        admin_text.DEL_ACCOUNT_SUCCESS, 
        reply_markup=inline.to_keyboard('accounts')
    )
    await state.clear()


    
