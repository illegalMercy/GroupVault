from itertools import chain
from aiogram.utils.keyboard import InlineKeyboardBuilder
from ..filters.callback_data import *


def menu():
    kb = InlineKeyboardBuilder()

    kb.button(text='💬 Группы', callback_data=Menu(button=MenuButton.GROUPS))
    kb.button(text='👥 Аккаунты', callback_data=Menu(button=MenuButton.ACCOUNTS))
    kb.button(text='💵 Цена', callback_data=Menu(button=MenuButton.PRICE))
    
    kb.adjust(1)
    return kb.as_markup()


def accounts():
    kb = InlineKeyboardBuilder()

    kb.button(text = '📄 Добавить', callback_data=Account(button=AccountButton.ADD_ACCOUNT))
    kb.button(text = '🗑 Удалить', callback_data=Account(button=AccountButton.DEL_ACCOUNT))

    kb.button(text='« Назад', callback_data=Menu(button=MenuButton.MENU))
    kb.adjust(2,1)

    return kb.as_markup()


def groups():
    kb = InlineKeyboardBuilder()

    kb.button(text = '📄 Добавить', callback_data=Groups(button=GroupButton.ADD_GROUPS))
    kb.button(text = '🗑 Удалить', callback_data=Groups(button=GroupButton.DEL_GROUPS))

    kb.button(text='« Назад', callback_data=Menu(button=MenuButton.MENU))
    kb.adjust(2,1)

    return kb.as_markup()


def price():
    kb = InlineKeyboardBuilder()

    kb.button(text = '➕ Добавить', callback_data=Price(button=PriceButton.ADD_PRICE))
    kb.button(text = '✏️ Изменить', callback_data=Price(button=PriceButton.EDIT_PRICE))
    kb.button(text = '🗑 Удалить', callback_data=Price(button=PriceButton.DEL_PRICE))

    kb.button(text='« Назад', callback_data=Menu(button=MenuButton.MENU))
    kb.adjust(3,1)

    return kb.as_markup()


def group_age_for_price_editing(prices: dict):
    buttons_in_row = 3
    kb = InlineKeyboardBuilder()

    for age, price in prices.items():
        kb.button(text=f'{age} мес. | {int(price)} ₽', 
                    callback_data=EditPrice(age=age, price=price))

    fill_row(kb, buttons_in_row)
    kb.button(text='« Назад', callback_data=Menu(button=MenuButton.PRICE))

    kb.adjust(buttons_in_row)
    return kb.as_markup()


def cancel_button(button_type: str, text_button='Отмена'):
    kb = InlineKeyboardBuilder()

    if button_type == 'accounts':
        callback_data = CancelButton.ACCOUNTS
    elif button_type == 'groups':
        callback_data = CancelButton.GROUPS
    elif button_type == 'price':
        callback_data = CancelButton.PRICE
    elif button_type == 'edit_price':
        callback_data = CancelButton.EDIT_PRICE
    elif button_type == 'add_price':
        callback_data = CancelButton.ADD_PRICE
    else:
        raise ValueError("Invalid button_type."
                         "Expected 'accounts', 'groups', 'edit_price', 'price', 'add_price'")
    
    kb.button(text=text_button, callback_data=callback_data)
    kb.adjust(1)
    
    return kb.as_markup()


def to_keyboard(button_type, text_button='« Назад'):
    kb = InlineKeyboardBuilder()

    if button_type == 'accounts':
        callback_data = Menu(button=MenuButton.ACCOUNTS)
    elif button_type == 'groups':
        callback_data = Menu(button=MenuButton.GROUPS)
    elif button_type == 'price':
        callback_data = Menu(button=MenuButton.PRICE)
    elif button_type == 'edit_price':
        callback_data = Price(button=PriceButton.EDIT_PRICE)
    else:
        raise ValueError("Invalid button_type."
                         "Expected 'accounts', 'groups', 'price', 'edit_price'")
    
    kb.button(text=text_button, callback_data=callback_data)
    kb.adjust(1)

    return kb.as_markup()


def fill_row(kb: InlineKeyboardBuilder, buttons_per_row = 4):
    try:
        buttons = list(chain(*kb.export()))
        button_count = len(buttons) % buttons_per_row
    except IndexError:
        button_count = 0
        
    if button_count:
        for _ in range(buttons_per_row - button_count):
            kb.button(text='\t', callback_data='#keyboard-divider')