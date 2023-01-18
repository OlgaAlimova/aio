import os

from aiogram.types import Message, PreCheckoutQuery, SuccessfulPayment, ShippingOption, ShippingQuery, LabeledPrice
from aiogram.types import CallbackQuery, InputFile, InputMediaPhoto, ContentType

from keyboards import main_menu, navigation
from loader import dp, db
from config import admins

EXPRESS_SHIPPING_OPTION = ShippingOption(id='express', title='СДЭК')
EXPRESS_SHIPPING_OPTION.add(LabeledPrice(label='Упаковка', amount=39000))
EXPRESS_SHIPPING_OPTION.add(LabeledPrice(label='Доставка', amount=56000))

PR_SHIPPING_OPTION = ShippingOption(id='pr', title='Почта России')
PR_SHIPPING_OPTION.add(LabeledPrice('Упаковка', 12000))
PR_SHIPPING_OPTION.add(LabeledPrice(label='Доставка', amount=45000))

PICKUP_SHIPPING_OPTION = ShippingOption(id='pickup', title='В Краснодаре')
PICKUP_SHIPPING_OPTION.add(LabeledPrice(label='Самовызов', amount=000))

@dp.callback_query_handler(main_menu.filter(menu='purchase'))
async def purchase(call: CallbackQuery, user_basket: tuple):
    id_user = call.message.chat.id
    prices = []
    for i, item in enumerate(user_basket):
        goods = db.get_goods(id=user_basket[i][-1])
        name_goods = goods[0][3]
        price = int(goods[0][-1])
        prices.append(LabeledPrice(label=f'{name_goods}', amount=price*100))
    await dp.bot.send_invoice(chat_id=id_user,
                              title='Оплата покупки!',
                              description='Подтвердите покупку товаров',
                              provider_token=os.getenv('P_TOKEN'),
                              currency='RUB',
                              is_flexible=True,
                              prices=prices,
                              need_name=True,
                              need_email=True,
                              need_phone_number=True,
                              payload=f'{call.message.chat.id}',
                              start_parameter='purchase')

@dp.shipping_query_handler()
async def shipping_options(shipping_query: ShippingQuery):
    shipping_options = [EXPRESS_SHIPPING_OPTION, PR_SHIPPING_OPTION, PICKUP_SHIPPING_OPTION]
    await dp.bot.answer_shipping_query(shipping_query.id, ok=True,
                                       shipping_options=shipping_options)

@dp.pre_checkout_query_handler()
async def process_pre_checkout_query(pre_checkout_query: PreCheckoutQuery):
    await dp.bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def process_pay(message: Message):
    if message.successful_payment.invoice_payload == f'{message.from_user.id}':
        await message.answer(text='Спасибо за покупку!\nСкоро с вами свяжется менеджер для уточнения деталей!')
        shipping = str(message.successful_payment.shipping_option_id)
        order = dict(message.successful_payment.order_info)
        id_user = int(message.from_user.id)
        db.add_purchase(id_user=id_user, order=order, shipping=shipping)
        db.clear_basket(id_user=id_user)
        for admin in admins:
            await dp.bot.send_message(chat_id=admin, text='У вас куплен товар. Проверьте БД')
