from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from .kb_cancel_fsm import btn_cancel

kb_g_type = ReplyKeyboardMarkup(resize_keyboard=True)

btn_beauty = KeyboardButton(text='beauty')
btn_youth = KeyboardButton(text='youth')
btn_health = KeyboardButton(text='health')
btn_abundance = KeyboardButton(text='abundance')
btn_destiny = KeyboardButton(text='destiny')

kb_g_type.add(btn_beauty, btn_youth)
kb_g_type.add(btn_health)
kb_g_type.add(btn_abundance, btn_destiny)
kb_g_type.add(btn_cancel)
