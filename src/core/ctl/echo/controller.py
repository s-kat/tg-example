from aiogram.types import Message

from src.settings.settings import Settings


class EchoController:

    def __init__(self, settings: Settings):
        self.settings = settings

    @classmethod
    def create(cls, settings: Settings) -> "EchoController":

        ctl = cls(settings=settings)

        return ctl

    async def process_message(self, message: Message):
        try:
            # Send a copy of the received message
            await message.send_copy(chat_id=message.chat.id)
        except TypeError:
            # But not all the types is supported to be copied so need to handle it
            await message.answer("Nice try!")
