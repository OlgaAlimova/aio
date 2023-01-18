from aiogram import Dispatcher
from .mw_dbase import AddBasket

def setup(dp: Dispatcher):
    dp.middleware.setup(AddBasket())
