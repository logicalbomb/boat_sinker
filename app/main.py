from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

# TODO: Look into using alembic instead of quick and dirty tricks
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

templates = Jinja2Templates(directory="templates")


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/", response_model=schemas.Game)
def create_game(game: schemas.GameCreate, db: Session = Depends(get_db)):
    # TODO: maybe one day care about the uniqueness of the game
    # TODO: add advanced validation (game is playable, make finished optional and generated)
    return crud.create_game(db=db, game=game)

@app.get("/", response_class=HTMLResponse)
def play_game(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse("index.html", {"request": request, "game": crud.get_random_game(db=db)})

@app.get("/game_id}", response_model=schemas.Game)
def play_specific_game(game_id: int, db: Session = Depends(get_db)):
    #TODO: update this to use jinja templates and other "fun" FE stuff
    return crud.get_game(db=db, game_id=game_id)

