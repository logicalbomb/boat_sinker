from random import randint

from sqlalchemy import func
from sqlalchemy.orm import Session

from . import models, schemas


def get_game(db: Session, game_id: int):
    return db.query(models.Game).filter(models.Game.id == game_id).first()

def get_random_game(db: Session):
    # TODO: bit of a hack relying upon autoincrementing PKs, fix this later
    max_id = db.query(func.max(models.Game.id)).scalar()
    min_id = db.query(func.min(models.Game.id)).scalar()
    return get_game(db=db, game_id=randint(min_id, max_id))

def create_game(db: Session, game: schemas.GameCreate):
    db_game = models.Game(**game.model_dump())
    db.add(db_game)
    db.commit()
    db.refresh(db_game)
    return db_game

