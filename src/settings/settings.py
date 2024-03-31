import os

import pydantic
from aiogram.enums import ParseMode
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Settings object."""

    TG_TOKEN: str = ""

    PARSE_MODE: ParseMode = ParseMode.HTML

    ROOT_LOCATION: str = ""
    COA_CITIES_COLLECTION_LOCATION: str = "data/crest.json"
    COA_STATES_COLLECTION_LOCATION: str = "data/crest_states.json"
    STATE_LOCATION: str = "data/state.json"

    @pydantic.field_validator("ROOT_LOCATION")
    def set_root(sls, _ : str) -> str:
        root = os.path.abspath(__file__)

        for _ in range(3):
            root = os.path.dirname(root)

        return root

    @pydantic.field_validator("COA_CITIES_COLLECTION_LOCATION",
                              "COA_STATES_COLLECTION_LOCATION",)
    def get_absolute_path(cls, value : str, values: pydantic.ValidationInfo):

        return f"{values.data["ROOT_LOCATION"]}/{value}"
