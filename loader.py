import os
import sqlite3

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from data_base.data_base import DataBase
from config import db_path

memory = MemoryStorage()

bot = Bot(os.getenv('TOKEN'), parse_mode='HTML')
dp = Dispatcher(bot, storage=memory)
db = DataBase(db_path=db_path)

async def on_startup(_):
    print('Бот запущен')
    try:
        db.create_table_goods()
        db.create_table_basket()
        db.create_table_purchase()
        print('Подключение к БД успешное!')
    except sqlite3.OperationalError:
        print('Ошибка подключения к БД')

async def on_shutdown(_):
    db.disconnect()

