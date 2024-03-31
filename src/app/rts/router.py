import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold

from src.core.bot.manager import BotManager
from src.core.unit.coa.state.model import GameType


class CoaRouter:

    name: str = "coa_router"

    @staticmethod
    def create(bot_mng: BotManager) -> Router:

        router = Router(name=CoaRouter.name)

        @router.message(CommandStart())
        async def start_handler(message: types.Message) -> None:
            """
            This handler receives messages with `/start` command
            """

            await message.answer(
                f"Добро пожаловать, {hbold(message.from_user.full_name)}!"
            )

        @router.message(Command("start_coa_cities_game"))
        async def game_start_coa_cities_handler(message: types.Message) -> None:
            """
            This handler receives messages with `/start` command
            """
            coa_ctl = await bot_mng.get_coa_controller()

            await coa_ctl.start_game(
                game_type=GameType.COA_CITY,
                message=message,
            )

        @router.message(Command("start_coa_regions_game"))
        async def game_start_coa_regions_handler(message: types.Message) -> None:
            """
            This handler receives messages with `/start` command
            """
            coa_ctl = await bot_mng.get_coa_controller()

            await coa_ctl.start_game(
                game_type=GameType.COA_REGION,
                message=message,
            )

        @router.message(Command("start_border_regions_game"))
        async def game_start_border_regions_handler(message: types.Message) -> None:
            """
            This handler receives messages with `/start` command
            """
            coa_ctl = await bot_mng.get_coa_controller()

            await coa_ctl.start_game(
                game_type=GameType.BORDER_REGION,
                message=message,
            )

        @router.message()
        async def echo_handler(message: types.Message) -> None:
            """
            Handler will forward receive a message back to the sender

            By default, message handler will handle all message types (like a text, photo, sticker etc.)
            """

            coa_ctl = await bot_mng.get_coa_controller()

            await coa_ctl.play_game(message=message)

        return router
