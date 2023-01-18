from aiogram.utils import executor
from handlers import dp
from loader import on_startup, on_shutdown
import middlevare

if __name__ == '__main__':
    middlevare.setup(dp)
    executor.start_polling(dispatcher=dp, skip_updates=True, on_startup=on_startup,
                           on_shutdown=on_shutdown)
