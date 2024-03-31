import json

from pydantic import TypeAdapter

from src.core.unit.coa.state.model import CoaState, GameState
from src.settings.settings import Settings


class CoaStateStorage:

    state: CoaState

    def __init__(self, state: CoaState, settings: Settings):
        self.settings = settings
        self.state = state

    @classmethod
    def create(cls, settings: Settings):

        with open(settings.STATE_LOCATION, "r") as r_file:

            state = CoaState(**json.load(r_file))

        stg = cls(state=state, settings=settings)

        return stg

    def get_state(self, chat_id: int) -> GameState | None:

        return self.state.games.get(chat_id)

    def save_state(self, chat_id: int, state: GameState) -> None:

        self.state.games[chat_id] = state

        with open(self.settings.STATE_LOCATION, "w") as w_file:
            w_file.write(self.state.model_dump_json(by_alias=True))

    def delete_state(self, chat_id: int) -> None:

        self.state.games.pop(chat_id)

        with open(self.settings.STATE_LOCATION, "w") as w_file:
            w_file.write(self.state.model_dump_json(by_alias=True))
