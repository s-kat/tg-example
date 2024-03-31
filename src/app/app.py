import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand

from src.app.dispatcher.dispatcher import BotDispatcher
from src.core.bot.manager import BotManager
from src.settings.settings import Settings


class App:

    def __init__(self, bot: Bot, dispatcher: Dispatcher, settings: Settings):

        self.bot = bot
        self.dispatcher = dispatcher
        self.settings = settings

    @classmethod
    def create(cls, settings: Settings) -> "App":

        bot_mng = BotManager.create(settings=settings)

        bot = Bot(settings.TG_TOKEN, parse_mode=settings.PARSE_MODE)

        bot_ds = BotDispatcher.create(bot_mng=bot_mng)

        app = cls(bot=bot, dispatcher=bot_ds, settings=settings)

        return app

    async def run(self):

        logging.basicConfig(level=logging.INFO, stream=sys.stdout)

        commands_dict: dict[str, str] = {
            "/start_coa_cities_game": "Начать угадывать населенный пункт по гербу",
            "/start_coa_regions_game": "Начать угадвать субъект по гербу",
            "/start_border_regions_game": "Начать угадывать субъект по границам",
        }

        main_menu_commands = [
            BotCommand(command=command, description=description)
            for command, description in commands_dict.items()
        ]

        await self.bot.set_my_commands(main_menu_commands)

        await self.dispatcher.start_polling(self.bot)
