from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.middlewares import BaseMiddleware

from loader import dp, db
from config import admins

class AddBasket(BaseMiddleware):
    async def on_process_message(self, message: Message, data: dict):
        data['user_basket'] = db.get_basket(id_user=message.from_user.id)
        for admin in admins:
            if message.from_user.id == admin:
                data['admin'] = True
                break
        else:
            data['admin'] = False

    async def on_process_callback_query(self, call: CallbackQuery, data: dict):
        data['user_basket'] = db.get_basket(id_user=call.message.chat.id)
        for admin in admins:
            if call.message.from_user.id == admin:
                data['admin'] = True
                break
        else:
            data['admin'] = False