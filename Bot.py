import asyncio
import logging
import config
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher
import user_handlers
from menu_kb import set_main_menu
storage: MemoryStorage = MemoryStorage()

# Configure logging
logging.basicConfig(level=logging.INFO)
async def main():

    # Initialize bot and dispatcher
    bot: Bot = Bot(token=config.BOT_TOKEN, parse_mode='HTML')
    dp: Dispatcher = Dispatcher(storage=storage)
    await set_main_menu(bot)
    dp.include_router(user_handlers.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
    


if __name__ == '__main__':
    asyncio.run(main())