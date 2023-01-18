from loader import dp, db
from aiogram.types import CallbackQuery, InputFile, InputMediaPhoto
from keyboards import main_menu, create_goods_menu


@dp.callback_query_handler(main_menu.filter(menu='main'))
async def shirts(call: CallbackQuery):
    current_id = 0
    current_item = call.data.split(':')[-1]
    cur_product = db.get_goods(g_type=current_item)
    photo = InputFile(path_or_bytesio=cur_product[current_id][2])
    # name = call.message.from_user.full_name
    current_chat_id = call.message.chat.id
    current_message_id = call.message.message_id
    caption = f"{cur_product[current_id][3]}\n{cur_product[current_id][4]}\n\n" \
              f"Стоимость: {cur_product[current_id][6]}"
    await dp.bot.edit_message_media(media=InputMediaPhoto(media=photo, caption=caption),
                                    chat_id=current_chat_id, message_id=current_message_id,
                                    reply_markup=create_goods_menu(current_id, current_item, 0))
