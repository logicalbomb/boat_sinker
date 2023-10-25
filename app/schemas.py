from pydantic import BaseModel


class GameBase(BaseModel):
    starting_board: str
    row_nums: str
    col_nums: str

class GameCreate(GameBase):
    finished_board: str

class Game(GameBase):
    id: int

