import enum
import typing

import pydantic

from src.core.unit.coa.ds.model import CoaCity, CoaRegion
from src.core.unit.coa.state.status import GameStatus


class GameType(str, enum.Enum):

    COA_CITY: str = "COA_CITY"
    COA_REGION: str = "COA_REGION"
    BORDER_REGION: str = "BORDER_REGION"


class CoaGameCityState(pydantic.BaseModel):

    game_type: typing.Literal[GameType.COA_CITY] = GameType.COA_CITY
    chat_id: int
    expected_city: CoaCity
    attempts: int = 0
    status: GameStatus = GameStatus.STARTED


class CoaGameRegionState(pydantic.BaseModel):

    game_type: typing.Literal[GameType.COA_REGION] = GameType.COA_REGION
    chat_id: int
    expected_region: CoaRegion
    attempts: int = 0
    status: GameStatus = GameStatus.STARTED


class BorderGameRegionState(pydantic.BaseModel):
    game_type: typing.Literal[GameType.BORDER_REGION] = GameType.BORDER_REGION
    chat_id: int
    expected_region: CoaRegion
    attempts: int = 0
    status: GameStatus = GameStatus.STARTED


GameState = typing.Union[CoaGameCityState, CoaGameRegionState, BorderGameRegionState]


class CoaState(pydantic.BaseModel):

    games: dict[int, GameState] = {}
