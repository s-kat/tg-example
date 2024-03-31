import enum


class GameStatus(str, enum.Enum):

    STARTED: str = "STARTED"
    FINISHED: str = "FINISHED"
    FAILED: str = "FAILED"
