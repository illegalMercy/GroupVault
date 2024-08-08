from aiogram.filters.callback_data import CallbackData
from .enums import *


class Menu(CallbackData, prefix='admin_menu'):
    button: MenuButton


class Account(CallbackData, prefix='admin_account'):
    button: AccountButton


class Groups(CallbackData, prefix='admin_groups'):
    button: GroupButton


class Price(CallbackData, prefix='admin_price'):
    button: PriceButton


class EditPrice(CallbackData, prefix='admin_edit_price'):
    age: int
    price: float