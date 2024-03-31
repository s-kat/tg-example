from aiogram import Dispatcher

from src.app.rts.router import CoaRouter
from src.core.bot.manager import BotManager


class BotDispatcher:

    @staticmethod
    def create(bot_mng: BotManager):

        dispatcher = Dispatcher()

        dispatcher.include_router(router=CoaRouter.create(bot_mng=bot_mng))

        return dispatcher
