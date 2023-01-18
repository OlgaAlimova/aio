from aiogram.types import Message,InputFile, CallbackQuery, InputMediaPhoto
from aiogram.utils.markdown import hbold, hlink, hitalic, hunderline, hstrikethrough

from keyboards import kb_main_menu, main_menu
from loader import dp

@dp.callback_query_handler(main_menu.filter(menu='back'))
async def com_start(call: CallbackQuery):
    photo = InputFile('images/logo.png')
    name = call.message.chat.full_name
    current_chat_id = call.message.chat.id
    current_message_id = call.message.message_id
    caption = f'{hbold(name)},{hitalic("Добро пожаловать")} в {hstrikethrough("Центр развития человека")} ' \
              f'{hlink("Альфа-Омега Плюс")} !\n' \
              f'{hlink(url="https://t.me/Alimova_Olga", title="Служба поддержки")}'
    await dp.bot.edit_message_media(media=InputMediaPhoto(media=photo, caption=caption),
                                    chat_id=current_chat_id, message_id=current_message_id,
                                    reply_markup=kb_main_menu)

@dp.message_handler(commands=['start'])
async def com_start(message: Message):
    photo = InputFile('images/logo.png')
    name = message.from_user.full_name
    chat_id = message.chat.id
    await dp.bot.send_photo(chat_id=chat_id, photo=photo,
                            caption=f'{hbold(name)},{hitalic("Добро пожаловать")} в {hstrikethrough("Центр развития человека")} ' \
                                    f'{hlink("Альфа-Омега Плюс")} !\n' \
                                    f'{hlink(url="https://t.me/Alimova_Olga", title="Служба поддержки")}',
                                    reply_markup=kb_main_menu)
