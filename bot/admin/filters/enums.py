from enum import Enum


class CancelButton(str, Enum):
    ACCOUNTS = 'accounts'
    GROUPS = 'groups'
    PRICE = 'price'
    EDIT_PRICE = 'edit price'
    ADD_PRICE = 'add price'


class MenuButton(str, Enum):
    MENU = 'menu'
    ACCOUNTS = 'accounts'
    GROUPS = 'groups'
    PRICE = 'price'


class AccountButton(str, Enum):
    ADD_ACCOUNT = 'add account'
    DEL_ACCOUNT = 'delete account'


class GroupButton(str, Enum):
    ADD_GROUPS = 'add groups'
    DEL_GROUPS = 'delete groups'


class PriceButton(str, Enum):
    EDIT_PRICE = 'edit price'
    ADD_PRICE = 'add price'
    DEL_PRICE = 'delete price'