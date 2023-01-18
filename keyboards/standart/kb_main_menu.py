from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

kb_start = ReplyKeyboardMarkup(resize_keyboard=True)

btn_start = KeyboardButton(text='/start')

kb_start.add(btn_start)
