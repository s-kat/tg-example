import io
import logging
import tempfile

import requests
from aiogram.types import BufferedInputFile, Message
from cairosvg import svg2png
from geopy.distance import geodesic

from src.core.stg.coa.ds.storage import CoaCollectionStorage
from src.core.stg.coa.state.storage import CoaStateStorage
from src.core.unit.coa.state.model import (
    BorderGameRegionState,
    CoaGameCityState,
    CoaGameRegionState,
    CoaState,
    GameState,
    GameType,
)
from src.settings.settings import Settings

logger = logging.getLogger(__name__)


class CoaController:

    def __init__(
        self,
        state_storage: CoaStateStorage,
        coa_storage: CoaCollectionStorage,
        settings: Settings,
    ):

        self.state_storage = state_storage
        self.coa_storage = coa_storage
        self.settings = settings

    @classmethod
    def create(cls, settings: Settings) -> "CoaController":

        collection_storage = CoaCollectionStorage.create(settings=settings)
        state_storage = CoaStateStorage.create(settings=settings)

        ctl = cls(
            state_storage=state_storage,
            coa_storage=collection_storage,
            settings=settings,
        )

        return ctl

    async def start_game(self, game_type: GameType, message: Message):

        if game_type == GameType.COA_CITY:
            await self.start_coa_game_cities(message=message)

        if game_type == GameType.COA_REGION:
            await self.start_coa_game_regions(message=message)

        if game_type == GameType.BORDER_REGION:
            await self.start_border_game_regions(message=message)

    @staticmethod
    async def download_image(image_url: str):

        logger.info(f"URL: {image_url}")
        headers = {"User-Agent": "GeoBot/0.1 (sergey.katkovskiy@mail.ru)"}
        image = requests.get(image_url, headers=headers)

        logger.info(f"IMAGE DOWNLOAD STATUS: {image.status_code}")

        content = image.content

        if not image_url.endswith(".svg"):
            return content

        with tempfile.NamedTemporaryFile() as tmp:
            svg2png(bytestring=content, write_to=tmp.name)

            content = tmp.read()

        return content

    async def start_coa_game_cities(self, message: Message):

        random_city = self.coa_storage.get_random_city()

        state = CoaGameCityState(
            chat_id=message.chat.id,
            expected_city=random_city,
        )

        self.state_storage.save_state(
            chat_id=message.chat.id,
            state=state,
        )

        await message.answer(text="Угадайте какому городу принадлежит данный герб.")

        image = await self.download_image(random_city.coa_url)
        await message.answer_photo(
            photo=BufferedInputFile(file=image, filename=random_city.coa_url)
        )

    async def start_coa_game_regions(self, message: Message):

        random_region = self.coa_storage.get_random_region()
        state = CoaGameRegionState(
            chat_id=message.chat.id, expected_region=random_region
        )

        self.state_storage.save_state(
            chat_id=message.chat.id,
            state=state,
        )

        await message.answer(text="Угадайте какому субъекту принадлежит данный герб.")
        image = await self.download_image(random_region.coa_url)
        await message.answer_photo(
            photo=BufferedInputFile(file=image, filename=random_region.coa_url)
        )

    async def start_border_game_regions(self, message: Message):

        random_region = self.coa_storage.get_random_region()
        state = BorderGameRegionState(
            chat_id=message.chat.id, expected_region=random_region
        )

        self.state_storage.save_state(
            chat_id=message.chat.id,
            state=state,
        )

        await message.answer(text="Угадайте какой субъект находится в данных границах.")

        image = await self.download_image(random_region.boards_img)
        await message.answer_photo(
            photo=BufferedInputFile(file=image, filename=random_region.boards_img)
        )

    async def play_game(self, message: Message):
        state = self.state_storage.get_state(chat_id=message.chat.id)

        if state is None:

            await message.answer(text="Для начала начните игру.")

            return

        if state.game_type == GameType.COA_CITY:
            await self.play_coa_game_cities(state=state, message=message)

        if state.game_type == GameType.COA_REGION:
            await self.play_coa_game_regions(state=state, message=message)

        if state.game_type == GameType.BORDER_REGION:
            await self.play_coa_game_regions(state=state, message=message)

    async def play_coa_game_cities(self, state: CoaGameCityState, message: Message):

        expected = state.expected_city
        possible_city = self.coa_storage.find_city(city_name=message.text)

        if possible_city is None:

            await message.answer(
                text="К сожалению, вы ошиблись. Попробуйте угадать снова."
            )

            return

        if possible_city.city_title == expected.city_title:

            await message.answer(text="Поздравляем! Вы угадали город.")

            await message.answer(text=expected.city_description)

            self.state_storage.delete_state(chat_id=message.chat.id)

            return

        distance = geodesic(expected.coordinates, possible_city.coordinates)

        await message.answer(
            text=f"К сожалению, вы ошиблись. Город находится в {distance} км от {possible_city.city_title}"
        )

    async def play_coa_game_regions(self, state: CoaGameRegionState, message: Message):

        expected = state.expected_region
        possible_region = self.coa_storage.find_region(region_name=message.text)

        if possible_region is None:

            await message.answer(
                text="К сожалению, вы ошиблись. Попробуйте угадать снова."
            )

            return

        if possible_region.region_title == expected.region_title:

            await message.answer(text="Поздравляем! Вы угадали субъект.")

            await message.answer(text=expected.state_description)

            self.state_storage.delete_state(chat_id=message.chat.id)

            return

        distance = geodesic(expected.coordinates, possible_region.coordinates)

        await message.answer(
            text=f"К сожалению, вы ошиблись. Субъект находится в {distance} км от {possible_region.region_title}"
        )
