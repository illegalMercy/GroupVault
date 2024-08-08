from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from database import async_session
from database.crud.create import create_groups as db_create_groups
from database.crud.read import (get_sessions as db_get_sessions, 
                                get_session as db_get_session)
from bot.client_api import TelethonClient
from bot.static.texts.admin import groups as admin_text
from bot.client_api.functions import get_folders, get_groups_from_folders
from ...keyboards import inline
from ...states.admin import Groups as GroupsFSM
from ...filters.callback_data import Groups, GroupButton


router = Router()


@router.callback_query(Groups.filter(F.button == GroupButton.ADD_GROUPS))
async def add_groups(call: CallbackQuery, state: FSMContext):
    sessions = await db_get_sessions(async_session)
    accounts_str = '\n'.join([f'{s.id}: <code>{s.name}</code>' for s in sessions])
    
    await call.message.edit_text(
        admin_text.ADD_GROUPS.format(accounts=accounts_str), 
        reply_markup=inline.cancel_button('groups')
    )
    await state.set_state(GroupsFSM.select_account_for_add)


@router.message(GroupsFSM.select_account_for_add)
async def select_account(msg: Message, state: FSMContext):
    account_name = msg.text
    session = await db_get_session(async_session, name=account_name)
    await state.update_data(session=session)

    if not session:
        await msg.answer(
            admin_text.ACCOUNT_NOT_FOUND.format(name=account_name),              
            reply_markup=inline.cancel_button('groups')
        )
        return

    async with TelethonClient(session.session_string) as client:
        folders = await get_folders(client)

    folders_str = "\n".join(f'{i+1}: <code>{f}</code>' for i, f in enumerate(folders))

    await msg.answer( 
        admin_text.ADD_FOLDRES.format(folders=folders_str), 
        reply_markup=inline.cancel_button('groups'))
    await state.set_state(GroupsFSM.add_groups)


@router.message(GroupsFSM.add_groups)
async def add_groups_from_folder(msg: Message, state: FSMContext):
    folders = msg.text.split('\n')

    state_data = await state.get_data()
    session = state_data['session']

    msg_info = await msg.answer(admin_text.ADD_GROUPS_WAITING)
    
    async with TelethonClient(session.session_string) as client:
        groups_data = await get_groups_from_folders(client, folders)

    groups = [(g[0].id, g[0].title, g[0].date, g[1].link) for g in groups_data]
    await db_create_groups(async_session, groups, session.id)

    await msg_info.edit_text(
        admin_text.ADD_GROUPS_SUCCESS,
        reply_markup=inline.to_keyboard('groups')
    )
    await state.clear()


