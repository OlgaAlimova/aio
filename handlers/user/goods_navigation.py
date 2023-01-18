from loader import dp, db
from aiogram.types import CallbackQuery, InputFile, InputMediaPhoto
from keyboards import navigation, create_goods_menu


@dp.callback_query_handler(navigation.filter(menu='goods'))
async def navi_goods(call: CallbackQuery):
    current_id = int(call.data.split(':')[-1])
    current_item = call.data.split(':')[-2]
    cur_product = db.get_goods(g_type=current_item)
    goods_id = int(cur_product[current_id][0])
    photo_path = str(cur_product[current_id][2])
    if photo_path.startswith('A'):
        photo = photo_path
    else:
        photo = InputFile(path_or_bytesio=photo_path)
    current_chat_id = call.message.chat.id
    current_message_id = call.message.message_id
    caption = f"{cur_product[current_id][3]}\n{cur_product[current_id][4]}\n\n" \
              f"Стоимость: {cur_product[current_id][6]}"
    await dp.bot.edit_message_media(media=InputMediaPhoto(media=photo, caption=caption),
                                    chat_id=current_chat_id, message_id=current_message_id,
                                    reply_markup=create_goods_menu(current_id, current_item, goods_id))

