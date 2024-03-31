from src.core.ctl.coa.controller import CoaController
from src.core.ctl.echo.controller import EchoController
from src.settings.settings import Settings


class BotManager:

    def __init__(self, settings: Settings):

        self.settings = settings

    @classmethod
    def create(cls, settings: Settings) -> "BotManager":

        bot = cls(settings=settings)

        return bot

    async def get_echo_controller(self) -> EchoController:

        echo_ctl = EchoController.create(settings=self.settings)

        return echo_ctl

    async def get_coa_controller(self) -> CoaController:

        coa_ctl = CoaController.create(settings=self.settings)

        return coa_ctl
