from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from database import async_session
from database.crud.read import get_sessions as db_get_sessions
from bot.static.texts.admin import accounts as admin_text
from ...keyboards import inline
from ...filters.enums import CancelButton
from ...filters.callback_data import Menu, MenuButton


router = Router()


@router.callback_query(Menu.filter(F.button == MenuButton.ACCOUNTS))
async def accounts(call: CallbackQuery):
    sessions = await db_get_sessions(async_session)
    accounts_str = '\n'.join([f'{s.id}: <code>{s.name}</code>' for s in sessions])

    await call.message.edit_text(
        admin_text.MENU.format(accounts=accounts_str), 
        reply_markup=inline.accounts()
    )


@router.callback_query(F.data == CancelButton.ACCOUNTS)
async def cancel_action(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await accounts(call)





# @router.message(AdminSessionsFSM.upload_session)
# async def handle_upload_session(msg: Message, state: FSMContext):
#     await state.update_data(session_string=msg.text)

#     text = ('<b>👥 Сессии</b>\n\n'
#             'Отправьте прокси')
#     await msg.answer(text, reply_markup=inline_kb.to_cancel_button('sessions'))
#     await state.set_state(AdminSessionsFSM.add_proxy)
    

# @router.message(AdminSessionsFSM.add_proxy)
# async def handle_add_proxy(msg: Message, state: FSMContext):
#     proxy = format_proxy(msg.text)

#     if not proxy:
#         text = 'Не удалось добавить прокси.\nПроверьте корректность введенных данных.'
#         await msg.answer(text, reply_markup=inline_kb.to_cancel_button('sessions'))
#         return

#     await state.update_data(proxy=proxy)

#     text = ('<b>👥 Сессии</b>\n\n'
#             'Отправьте название сессии')
#     await msg.answer(text, reply_markup=inline_kb.to_cancel_button('sessions'))
#     await state.set_state(AdminSessionsFSM.add_name)                
    

# @router.message(AdminSessionsFSM.add_name)
# async def handle_add_name(msg: Message, state: FSMContext):
#     data = await state.get_data()
#     session_string = data['session_string']
#     proxy = data['proxy']
#     session_name = msg.text

#     await create_session(async_session, session_string, session_name, proxy)
#     await msg.answer('Успешно!', reply_markup=inline_kb.to_keyboard('sessions'))
#     await state.clear()


# @router.callback_query(AdminSessions.filter(F.button == AdminSessionsButton.DELETE_SESSION))
# async def delete_session(call: CallbackQuery):
#     sessions = await get_all_sessions(async_session)
#     if sessions:
#         sessions_ids = [session.id for session in sessions] 
#         await call.message.edit_text(
#             create_session_page(sessions, sessions_ids, f'<b>🗑 Выберите ID для удаления</b>\n\n', 0), 
#             reply_markup=inline_kb.sessions_ids_for_deletion(sessions_ids))
#     else:
#         text = (f'<b>🗑 Сессии не найдены</b>\n\n')
#         await call.message.edit_text(text, reply_markup=inline_kb.to_keyboard('sessions'))
        

# @router.callback_query(AdminDeletableSession.filter())
# async def handle_delete_session(call: CallbackQuery, callback_data: AdminDeletableSession):
#     session_id = callback_data.session_id
#     await db_delete_session(async_session, session_id)
    
#     await delete_session(call)


# @router.callback_query(AdminSessionDeletionPagination.filter())
# async def session_deletion_pagination(call: CallbackQuery, callback_data: dict):
#     page = callback_data.page
#     sessions = await get_all_sessions(async_session)
#     sessions_ids = [session.id for session in sessions] 
 
#     await call.message.edit_text(
#         create_session_page(sessions, sessions_ids, f'<b>🗑 Выберите ID для удаления</b>\n\n', page), 
#         reply_markup=inline_kb.sessions_ids_for_deletion(sessions_ids, page))


# @router.callback_query(AdminSessions.filter(F.button == AdminSessionsButton.UPDATE_PROXY))
# async def update_proxy(call: CallbackQuery):
#     sessions = await get_all_sessions(async_session)
#     if sessions:
#         sessions_ids = [session.id for session in sessions] 
#         await call.message.edit_text(
#             create_session_page(sessions, sessions_ids, f'<b>🌐 Выберите ID для обновления прокси</b>\n\n', 0), 
#             reply_markup=inline_kb.sessions_ids_for_update_proxy(sessions_ids))
#     else:
#         text = (f'<b>🌐 Сессии не найдены</b>\n\n')
#         await call.message.edit_text(text, reply_markup=inline_kb.to_keyboard('sessions'))


# @router.callback_query(AdminUpdateProxyPagination.filter())
# async def update_proxy_pagination(call: CallbackQuery, callback_data: dict):
#     page = callback_data.page
#     sessions = await get_all_sessions(async_session)
#     sessions_ids = [session.id for session in sessions] 
 
#     await call.message.edit_text(
#         create_session_page(sessions, sessions_ids, f'<b>🌐 Выберите ID для обновления прокси</b>\n\n', page), 
#         reply_markup=inline_kb.sessions_ids_for_update_proxy(sessions_ids))


# @router.callback_query(AdminUpdatableProxy.filter())
# async def proxy_entry_request(call: CallbackQuery, callback_data: AdminUpdatableProxy, state: FSMContext):
#     session_id = callback_data.session_id

#     text = ('<b>🌐 Прокси </b>\n\n'
#             'Отправьте новые прокси')
#     await call.message.edit_text(text, reply_markup=inline_kb.to_cancel_button('sessions'))

#     await state.update_data(session_id = session_id)
#     await state.set_state(AdminSessionsFSM.update_proxy) 


# @router.message(AdminSessionsFSM.update_proxy)
# async def handle_proxy_entry_request(msg: Message, state: FSMContext):
#     state_data = await state.get_data()
#     session_id = state_data['session_id']

#     proxy = format_proxy(msg.text)

#     if not proxy:
#         text = 'Не удалось добавить прокси.\nПроверьте корректность введенных данных.'
#         await msg.answer(text, reply_markup=inline_kb.to_cancel_button('sessions'))
#         return
    
#     await update_session_proxy(async_session, session_id, proxy) 
#     await msg.answer('Успешно!', reply_markup=inline_kb.to_keyboard('sessions'))
#     await state.clear()  


