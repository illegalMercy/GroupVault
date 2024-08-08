from aiogram.filters.callback_data import CallbackData
from .enums import *


class Menu(CallbackData, prefix='menu'):
    button: MenuButton


class GroupSale(CallbackData, prefix='group_sale'):
    age: int
    price: float


class GroupOwnership(CallbackData, prefix='group_ownership'):
    buyer_id: int
    group_id: int
    session_id: int
