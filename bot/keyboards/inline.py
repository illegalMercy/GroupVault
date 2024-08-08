from itertools import chain

from aiogram.utils.keyboard import InlineKeyboardBuilder
from ..filters.callback_data import *


def menu():
    kb = InlineKeyboardBuilder()

    kb.button(text='🛒  Купить', callback_data=Menu(button=MenuButton.GROUP_SALE))
    kb.button(text='☎️ Контакты', callback_data=Menu(button=MenuButton.CONTACTS))
    
    kb.adjust(1)
    return kb.as_markup()


def group_sale(months: list, prices: dict):
    buttons_in_row = 3
    kb = InlineKeyboardBuilder()

    for m in months:
        if not m in prices:
            continue
        
        price = prices[m]
        kb.button(text=f'{m} мес. | {int(price)} ₽', 
                    callback_data=GroupSale(age=m, price=price))

    fill_row(kb, buttons_in_row)
    kb.button(text='« Назад', callback_data=Menu(button=MenuButton.MENU))

    kb.adjust(buttons_in_row)
    return kb.as_markup()


def payment(url: str):
    kb = InlineKeyboardBuilder()

    kb.button(text='Оплатить', url=url)
    kb.button(text='« Назад', callback_data=Menu(button=MenuButton.GROUP_SALE))
    
    kb.adjust(1)
    return kb.as_markup()


def transfer_group_ownership(buyer_id: int, group_id: int, session_id: int):
    kb = InlineKeyboardBuilder()

    kb.button(text='✍️ Получить права', 
              callback_data=GroupOwnership(buyer_id=buyer_id, 
                                           group_id=group_id,
                                           session_id=session_id))
    kb.adjust(1)
    return kb.as_markup()



def to_keyboard(button_type: str, text_button: str ='« Назад'):
    kb = InlineKeyboardBuilder()

    if button_type == 'menu':
        callback_data = Menu(button=MenuButton.MENU)
    elif button_type == 'group_sale':
        callback_data = Menu(button=MenuButton.GROUP_SALE)
    else:
        raise ValueError("Invalid button_type. Expected 'menu', 'group_sale'")
    
    kb.button(text=text_button, callback_data=callback_data)
    kb.adjust(1)

    return kb.as_markup()


def fill_row(kb: InlineKeyboardBuilder, buttons_per_row: int = 4):
    try:
        buttons = list(chain(*kb.export()))
        button_count = len(buttons) % buttons_per_row
    except IndexError:
        button_count = 0
        
    if button_count:
        for _ in range(buttons_per_row - button_count):
            kb.button(text='\t', callback_data='#keyboard-divider')
