from loader import dp, db
from aiogram.types import CallbackQuery, InputFile, InputMediaPhoto
from keyboards import main_menu, navigation #menu_data, navi_goods, create_goods_menu
# from data_base.SQLite import get_item, add_to_basket, set_count, get_basket, get_by_id
from keyboards import create_basket_kb

@dp.callback_query_handler(navigation.filter(menu='basket'))
async def add_to_basket(call: CallbackQuery):
    id_user = call.from_user.id
    id_goods = int(call.data.split(":")[-1])
    goods = dp.get_goods(id=id_goods)
    name_goods = goods[0][3]
    goods_quantity = db.get_goods(id=id_goods)[0][-2]
    if goods_quantity > 0:
        db.add_to_basket(id_user, id_goods)
        await call.answer(f'Товар {name_goods} добавлен в корзину')
    else:
        await call.answer(f'Извините, но товара {name_goods} нет в наличии', show_alert=True)


@dp.callback_query_handler(main_menu.filter(menu='basket'))
async def get_user_basket(call: CallbackQuery, user_basket: tuple):
    id_user = call.from_user.id
    current_message_id = call.message.message_id
    content_basket = 'Содержимое вашей корзины:\n'
    total = 0
    if len(user_basket) != 0:
        for i in range(len(user_basket)):
            id_goods = int(user_basket[i][-1])
            goods = db.get_goods(id=id_goods)[0]
            content_basket += f'{i+1}. {goods[3]}\n'
            total += float(goods[-1])
        content_basket += f'Общая сумма: {total} рублей'
    else:
        content_basket += 'Пусто'
    photo = InputFile('images/logo.png')
    await dp.bot.edit_message_media(media=InputMediaPhoto(media=photo, caption=content_basket),
                                    chat_id=id_user, message_id=current_message_id,
                                    reply_markup=create_basket_kb(id_user, user_basket))

@dp.callback_query_handler(navigation.filter(menu='remove'))
async def remove_from_basket(call: CallbackQuery, user_basket: tuple):
    id_goods = int(call.data.split(":")[-3])
    id_order = int(call.data.split(":")[-1])
    goods = db.get_goods(id-id_goods)
    name_goods = goods[0][3]
    await call.answer(f'Товар {name_goods} удален из корзины')
    db.remove_from_basket(id_order, id_goods)
    await get_user_basket(call, user_basket)
