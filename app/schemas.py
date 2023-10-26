from typing_extensions import Annotated

from pydantic import BaseModel, Field, model_validator

# See test_main.py for examples of these data models
class GameBase(BaseModel):
    ##
    # A game board that is 10x10 and is encoded with the upper left being the character at index 0
    # and streaming horizontally until you get to the upper right at character index 9. This
    # continues with the next row starting with the character at index 10. It finally ends with
    # the lower right corner being the character at index 99.
    #
    # The characters in each space represent various items in the game:
    #   ~ The ocean
    #   o A ship that is singlespace-wide
    #   # The center of a multispace-wide ship that works vertically and horizontally, but not both
    #   < The left end of a horizontal, multispace-wide ship
    #   > The right end of a horizontal, multispace-wide ship
    #   ^ The top end of a vertical, multispace-wide ship
    #   v The bottom end of a vertical, multispace-wide ship
    #   ? An unknown space, it could be ocean or part of a ship
    ##
    starting_board: Annotated[str, Field(
        min_length=100,
        max_length=100,
        pattern='[~o#<>^v?]{100}',
        repr=True,
        frozen=True
    )]
    ##
    # The number of ship parts that would appear in the corresponding row. The character at index
    # 0 represents the top row and the character at index 9 represents the bottom row.
    ##
    row_nums: Annotated[str, Field(
        min_length=10,
        max_length=10,
        pattern='[0-8]{10}',
        repr=True,
        frozen=True
    )]
    ##
    # The number of ship parts that would appear in the corresponding column. The character at
    # index 0 represents the left row and the character at index 9 represents the right row.
    ##
    col_nums: Annotated[str, Field(
        min_length=10,
        max_length=10,
        pattern='[0-8]{10}',
        repr=True,
        frozen=True
    )]

class GameCreate(GameBase):
    ##
    # A game board that has all of the properties as the starting_board, with one major
    # exception. The finished board does not have any ? characters because it is solved.
    ##
    finished_board: Annotated[str, Field(
        min_length=100,
        max_length=100,
        pattern='[~o#<>^v]{100}',
        repr=True,
        frozen=True
    )]

    @model_validator(mode='after')
    def check_start_to_finish(self) -> 'GameCreate':
        # Make sure the starting_board matches the finished_board
        for i, c in enumerate(self.starting_board):
            if c == '?' or c == self.finished_board[i]: continue
            raise ValueError("Start cannot get to finish: {} -/> {} @ {}".format(c, self.finished_board[i], i))

        # TODO: make sure to walk through the steps to solve and produce a matching board

        return self

class Game(GameBase):
    ##
    # Database junk :-D
    ##
    id: int

