from aiogram import Router
from aiogram.types import CallbackQuery
from bot.keyboards import inline
from database import async_session
from database.crud.read import get_session as db_get_session
from ..static.texts import user as user_text
from ..filters.callback_data import GroupOwnership
from ..client_api.telethon_client import TelethonClient
from ..client_api.functions import get_group_member, transfer_group_ownership, leave_group


router = Router()


@router.callback_query(GroupOwnership.filter())
async def group_ownership(call: CallbackQuery, callback_data: GroupOwnership):
    buyer_id = callback_data.buyer_id
    group_id = callback_data.group_id
    session_id = callback_data.session_id

    session = await db_get_session(async_session, session_id)
    
    async with TelethonClient(session.session_string) as client: 
        if not await get_group_member(client, buyer_id, group_id):
            await call.answer(user_text.NOT_MEMBER)
            return

        if not await transfer_group_ownership(client, session.password, buyer_id, group_id):
            await call.message.answer(text=user_text.TRANSFER_ERROR)
            return
        
        await leave_group(client, group_id)
    
    await call.message.edit_text(text=user_text.TRANSFER_SUCCESS, 
                                 reply_markup=inline.to_keyboard('group_sale'))

