import sqlite3

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from loader import dp, db
from aiogram.types import Message
from keyboards import kb_g_type, kb_cancel_fsm
from config import admins

class NewGoodsItem(StatesGroup):
    name = State()
    desc = State()
    g_type = State()
    photo = State()
    quantity = State()
    price = State()

@dp.message_handler(commands=['add'], state=None)
async def add_catch(message: Message, admin: bool, state: FSMContext):
    if admin:
        await message.answer(text='Введите название товара', reply_markup=kb_cancel_fsm)
        await NewGoodsItem.name.set()
    else:
        await message.answer('Извините, у вас нет доступа к этой команде')

@dp.message_handler(state=NewGoodsItem.name)
async def name_catch(message: Message, state: FSMContext):
    await state.update_data({'name': message.text})
    await message.answer(text='Введите описание товара', reply_markup=kb_cancel_fsm)
    await NewGoodsItem.next()

@dp.message_handler(state=NewGoodsItem.desc)
async def desc_catch(message: Message, state: FSMContext):
    if message.text in ['beauty', 'youth', 'health', 'abundance', 'destiny']:
        await state.update_data({'desc': message.text})
        await message.answer('Введите тип товара', reply_markup=kb_g_type)
        await NewGoodsItem.next()
    else:
        await message.answer('Выберите категорию из списка', reply_markup=kb_g_type)

@dp.message_handler(content_types='photo', state=NewGoodsItem.photo)
async def photo_catch(message: Message, state: FSMContext):
    await state.update_data({'image': message.photo[0].file_id})
    await message.answer('Введите количество товара', reply_markup=kb_cancel_fsm)
    await NewGoodsItem.next()

@dp.message_handler(state=NewGoodsItem.quantity)
async def quantity_catch(message: Message, state: FSMContext):
    await state.update_data({'quantity': message.text})
    await message.answer('Введите цену товара', reply_markup=kb_cancel_fsm)
    await NewGoodsItem.next()

@dp.message_handler(state=NewGoodsItem.price)
async def price_catch(message: Message, state: FSMContext):
    await state.update_data({'price': message.text})
    data = await state.get_data()
    try:
        db.add_goods(data)
        await message.answer(f'Товар {data.get("name")} добавлен!')
    except sqlite3.OperationalError:
        await message.answer(f'Ошибка! добавления товара!'
                             f'Проверьте правильность вводимых данных')
    await state.reset_data()
    await state.finish()


