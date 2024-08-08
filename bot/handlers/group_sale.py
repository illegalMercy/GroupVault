import json
from datetime import datetime
from collections import defaultdict

from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery
from config import config
from yoomoney.quickpay import Quickpay
from database import async_session
from database.crud.update import update_group_buyer as db_update_group_buyer
from database.crud.read import (get_free_groups as db_get_free_groups,
                                get_prices as db_get_prices)
from ..keyboards import inline
from ..static.texts import user as user_text
from ..utils.utils import calculate_month_delta
from ..filters.callback_data import GroupSale, Menu, MenuButton


router = Router()


@router.callback_query(Menu.filter(F.button == MenuButton.GROUP_SALE))
async def group_sale(call: CallbackQuery):
    groups = await db_get_free_groups(async_session)
    prices = await db_get_prices(async_session)

    current_date = datetime.now()
    sorted_groups_by_month = defaultdict(list)

    for group in groups:
        month_delta = calculate_month_delta(group.created_at, current_date)
        sorted_groups_by_month[month_delta].append(group)

    only_months = sorted(sorted_groups_by_month.keys(), reverse=True)
    price_dict = {price.age: price.price for price in prices}

    groups_str = '\n'.join(
        f'{month} мес. - <b>{len(sorted_groups_by_month[month])}</b> шт.'
        for month in sorted(sorted_groups_by_month, reverse=True)
        if month in price_dict
    )

    await call.message.edit_text(
        user_text.GROUP_MENU.format(groups=groups_str),
        reply_markup=inline.group_sale(only_months, price_dict)
    )


@router.callback_query(GroupSale.filter())
async def send_invoice(call: CallbackQuery, callback_data: GroupSale):
    payment_data = {
        'user_id': call.from_user.id,
        'group_age': callback_data.age
    }
    quickpay = Quickpay(
        receiver=config.yoomoney_wallet_id.get_secret_value(),
        quickpay_form='shop',
        targets='Chat Sales Bot',
        paymentType='SB',
        sum=callback_data.price,
        label=json.dumps(payment_data)
    )
    await quickpay.request()

    await call.message.edit_text(
        user_text.INVOICE.format(price=int(callback_data.price), age=callback_data.age),
        reply_markup=inline.payment(str(quickpay.redirected_url))
    )

async def successful_payment(bot: Bot, request_data: dict):
    payment_data = json.loads(request_data['label'])

    user_id = payment_data.get('user_id')
    group_age = payment_data.get('group_age')

    current_date = datetime.now()
    groups = await db_get_free_groups(async_session)
    buyer_group = next(
        (group for group in groups
            if group_age == calculate_month_delta(group.created_at, current_date)),
        None
    )
    await db_update_group_buyer(async_session, user_id, buyer_group.id)

    text = user_text.SUCCESS_PAYMENT.format(
        group_name=buyer_group.name,
        group_created_at=buyer_group.created_at.strftime("%d.%m.%Y"),
        group_link=buyer_group.link
    )

    await bot.send_message(
        user_id, text, disable_web_page_preview=True,
        reply_markup=inline.transfer_group_ownership(
            user_id,
            buyer_group.id,
            buyer_group.session_id
        )
    )
