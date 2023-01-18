from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from .callback import main_menu, navigation
from loader import db

def create_basket_kb(id_user: int, my_basket: tuple):
    kb_goods = InlineKeyboardMarkup(row_width=2)
    btn_back = InlineKeyboardButton(text='Назад в главное меню', callback_data=main_menu.new(menu='back', item=''))
    btn_purchase = InlineKeyboardButton(text='Оформить заказ', callback_data=main_menu.new(menu='purchase', item=''))
    if len(my_basket) != 0:
        for i in range(len(my_basket)):
            id_order = str(my_basket[i][0])
            id_user = str(my_basket[i][1])
            id_goods = str(my_basket[i][2])
            goods = db.get_goods(id=id_goods)
            name_goods = goods[0][3]
            item_menu = f'Удалить {name_goods}'
            kb_goods.add(InlineKeyboardButton(text=item_menu,
                                              callback_data=navigation.new(
                                                  menu='remove', user_id=id_user,
                                                  goods_id=id_goods, item=id_order,
                                                  id=id_order)))
        kb_goods.add(btn_purchase, btn_back)
    else:
        kb_goods.add(btn_back)
    return kb_goods
