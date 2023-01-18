from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from .callback import main_menu


kb_main_menu = InlineKeyboardMarkup(row_width=2)

btn_beauty = InlineKeyboardButton(text='Красота', callback_data=main_menu.new(menu='main', item='beauty'))
btn_youth = InlineKeyboardButton(text='Молодость', callback_data=main_menu.new(menu='main', item='youth'))
btn_health = InlineKeyboardButton(text='Здоровье', callback_data=main_menu.new(menu='main', item='health'))
btn_abundance = InlineKeyboardButton(text='Изобилие', callback_data=main_menu.new(menu='main', item='abundance'))
btn_destiny = InlineKeyboardButton(text='Предназначение', callback_data=main_menu.new(menu='main', item='destiny'))

kb_main_menu.row(btn_beauty, btn_youth)
kb_main_menu.row(btn_abundance, btn_destiny)
kb_main_menu.row(btn_health)
