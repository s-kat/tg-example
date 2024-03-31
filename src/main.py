import asyncio
import logging
import sys

import click

from src.app.app import App
from src.settings.settings import Settings

logger = logging.getLogger(__name__)


@click.group()
def cli() -> None:

    logging.basicConfig(level=logging.INFO, stream=sys.stdout)


@cli.command("run-bot")
def run() -> None:

    logger.info("Run app")
    settings = Settings()

    app = App.create(settings=settings)

    asyncio.run(app.run())


if __name__ == "__main__":
    cli()
