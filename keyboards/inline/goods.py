from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from .callback import main_menu, navigation
from loader import db

def create_goods_menu(cur_id: int, item: str, goods_id: int):
    goods = db.get_goods(g_type=item)
    id_goods = goods[current_id][0]
    next_id = current_id + 1
    prev_id = current_id - 1
    product = db.get_goods(id=current_id)
    if current_id == 0:
        prev_id = len(goods) - 1
    elif current_id == len(goods) - 1:
        next_id = 0
    kb_goods = InlineKeyboardMarkup(row_width=1)

    btn_buy = InlineKeyboardButton(text='В корзину',
                                    callback_data=navigation.new(
                                        menu='basket', user_id='0',
                                        goods_id=goods_id, item=item,
                                        id=id_goods))
    btn_prev = InlineKeyboardButton(text='<<<',
                                   callback_data=navigation.new(
                                       menu='goods', user_id='0',
                                       goods_id='0', item=item,
                                       id=prev_id))
    btn_next = InlineKeyboardButton(text='>>>',
                                    callback_data=navigation.new(
                                        menu='goods', user_id='0',
                                        goods_id='0', item=item,
                                        id=next_id))
    btn_back = InlineKeyboardButton(text='Назад в главное меню',
                                    callback_data=main_menu.new(
                                        menu='back', item=''))

    kb_goods.row(btn_prev, btn_buy, btn_next)
    kb_goods.add(btn_back)
    return kb_goods
