from aiogram.fsm.state import State, StatesGroup


class Accounts(StatesGroup):
    add_session_str = State()
    add_password = State()
    add_account_name = State()
    del_account = State()


class Groups(StatesGroup):
    select_account_for_add = State()
    select_account_for_del = State()
    add_groups = State()
    del_groups = State()


class Price(StatesGroup):
    edit_price = State()
    add_group_age = State()
    add_group_price = State()
    del_group_age = State()
