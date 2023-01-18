from aiogram.utils.callback_data import CallbackData

main_menu = CallbackData('Main menu', 'menu', 'item')

navigation = CallbackData('Navigation', 'menu', 'user_id', 'goods_id', 'item', 'id')

remove_list = CallbackData('Remove List', 'menu')
