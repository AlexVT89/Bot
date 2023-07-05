from aiogram import Bot
from aiogram.types import BotCommand



async def set_main_menu(bot: Bot):
    main_menu_commands = [
        BotCommand(command='/begin',
                   description='Начать поиск заново')]
        # BotCommand(command='/help',
        #            description='Описание работы с ботом'),]

    await bot.set_my_commands(main_menu_commands)