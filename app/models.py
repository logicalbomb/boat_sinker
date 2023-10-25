from sqlalchemy import Column, Integer, String

from .database import Base

class Game(Base):
    __tablename__ = "games"

    # TODO: Come back and add more rigorous schema (like string lengths)
    id = Column(Integer, primary_key=True, index=True)
    starting_board = Column(String)
    finished_board = Column(String)
    # TODO: keep things simple with string for now, could be arrays of ints in the future?
    row_nums = Column(String)
    col_nums = Column(String)

