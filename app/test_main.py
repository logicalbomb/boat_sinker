from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .database import Base
from .main import app, get_db


SQLALCHEMY_TEST_DB_URL = "sqlite://"

def override_get_db():
    try:
        test_engine = create_engine(SQLALCHEMY_TEST_DB_URL, connect_args={"check_same_thread": False})
        Base.metadata.create_all(bind=test_engine)
        TestSession = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
        yield TestSession()
    finally:
        test_engine.dispose()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


VALID_STARTING_BOARD = (
    "??????????"
    "?????????^"
    "~?????????"
    "??????????"
    "??????????"
    "??????????"
    "??????????"
    "??????????"
    "??????????"
    "??????????"
)

VALID_FINISHED_BOARD = (
    "o~o~~~~~~~"
    "~~~~~~~~~^"
    "~~^~~~~~~v"
    "o~v~~<#>~~"
    "~~~~~~~~~~"
    "^~~~~~~~~~"
    "#~~~~~~~~~"
    "v~<>~<##>~"
    "~~~~~~~~~~"
    "o~~~~~~~~~"
)

VALID_ROW_NUMS = "2125011701"

VALID_COL_NUMS = "6041022212"



def test_create_game():
    response = client.post(
        "/",
        json={
            "starting_board": VALID_STARTING_BOARD,
            "finished_board": VALID_FINISHED_BOARD,
            "row_nums": VALID_ROW_NUMS,
            "col_nums": VALID_COL_NUMS,
        },
    )
    #print("Response is:\n{}".format(response.json()))
    assert response.status_code == 200
    assert 'id' in response.json().keys()

def test_create_game_with_a_small_starting_board():
    response = client.post(
        "/",
        json={
            "starting_board": "?",
            "finished_board": VALID_FINISHED_BOARD,
            "row_nums": VALID_ROW_NUMS,
            "col_nums": VALID_COL_NUMS,
        },
    )
    #print("Response is:\n{}".format(response.json()))
    assert response.status_code == 422
    assert response.json()['detail'][0]['type'] == 'string_too_short'

def test_create_game_with_a_large_starting_board():
    response = client.post(
        "/",
        json={
            "starting_board": VALID_STARTING_BOARD + "?",
            "finished_board": VALID_FINISHED_BOARD,
            "row_nums": VALID_ROW_NUMS,
            "col_nums": VALID_COL_NUMS,
        },
    )
    #print("Response is:\n{}".format(response.json()))
    assert response.status_code == 422
    assert response.json()['detail'][0]['type'] == 'string_too_long'

def test_create_game_with_bad_char_in_starting_board():
    response = client.post(
        "/",
        json={
            "starting_board": VALID_STARTING_BOARD[:99] + "!",
            "finished_board": VALID_FINISHED_BOARD,
            "row_nums": VALID_ROW_NUMS,
            "col_nums": VALID_COL_NUMS
        }
    )
    assert response.status_code == 422
    assert response.json()['detail'][0]['type'] == 'string_pattern_mismatch'

def test_create_game_with_a_small_finished_board():
    response = client.post(
        "/",
        json={
            "starting_board": VALID_STARTING_BOARD,
            "finished_board": "~",
            "row_nums": VALID_ROW_NUMS,
            "col_nums": VALID_COL_NUMS,
        },
    )
    #print("Response is:\n{}".format(response.json()))
    assert response.status_code == 422
    assert response.json()['detail'][0]['type'] == 'string_too_short'

def test_create_game_with_a_large_finished_board():
    response = client.post(
        "/",
        json={
            "starting_board": VALID_STARTING_BOARD,
            "finished_board": VALID_FINISHED_BOARD + "~",
            "row_nums": VALID_ROW_NUMS,
            "col_nums": VALID_COL_NUMS,
        },
    )
    #print("Response is:\n{}".format(response.json()))
    assert response.status_code == 422
    assert response.json()['detail'][0]['type'] == 'string_too_long'

def test_create_game_with_bad_char_in_finished_board():
    response = client.post(
        "/",
        json={
            "starting_board": VALID_STARTING_BOARD,
            "finished_board": "?" + VALID_FINISHED_BOARD[:99],
            "row_nums": VALID_ROW_NUMS,
            "col_nums": VALID_COL_NUMS
        }
    )
    assert response.status_code == 422
    assert response.json()['detail'][0]['type'] == 'string_pattern_mismatch'

def test_create_game_with_small_row_nums():
    response = client.post(
        "/",
        json={
            "starting_board": VALID_STARTING_BOARD,
            "finished_board": VALID_FINISHED_BOARD,
            "row_nums": "0",
            "col_nums": VALID_COL_NUMS
        }
    )
    assert response.status_code == 422
    assert response.json()['detail'][0]['type'] == 'string_too_short'

def test_create_game_with_large_row_nums():
    response = client.post(
        "/",
        json={
            "starting_board": VALID_STARTING_BOARD,
            "finished_board": VALID_FINISHED_BOARD,
            "row_nums": VALID_ROW_NUMS + "0",
            "col_nums": VALID_COL_NUMS
        }
    )
    assert response.status_code == 422
    assert response.json()['detail'][0]['type'] == 'string_too_long'

def test_create_game_with_bad_char_in_row_nums():
    response = client.post(
        "/",
        json={
            "starting_board": VALID_STARTING_BOARD,
            "finished_board": VALID_FINISHED_BOARD,
            "row_nums": VALID_ROW_NUMS[:9] + "9",
            "col_nums": VALID_COL_NUMS
        }
    )
    assert response.status_code == 422
    assert response.json()['detail'][0]['type'] == 'string_pattern_mismatch'

def test_create_game_with_small_col_nums():
    response = client.post(
        "/",
        json={
            "starting_board": VALID_STARTING_BOARD,
            "finished_board": VALID_FINISHED_BOARD,
            "row_nums": VALID_ROW_NUMS,
            "col_nums": "8"
        }
    )
    assert response.status_code == 422
    assert response.json()['detail'][0]['type'] == 'string_too_short'

def test_create_game_with_large_col_nums():
    response = client.post(
        "/",
        json={
            "starting_board": VALID_STARTING_BOARD,
            "finished_board": VALID_FINISHED_BOARD,
            "row_nums": VALID_ROW_NUMS,
            "col_nums": VALID_COL_NUMS + "8"
        }
    )
    assert response.status_code == 422
    assert response.json()['detail'][0]['type'] == 'string_too_long'

def test_create_game_with_bad_char_in_col_nums():
    response = client.post(
        "/",
        json={
            "starting_board": VALID_STARTING_BOARD,
            "finished_board": VALID_FINISHED_BOARD,
            "row_nums": VALID_ROW_NUMS,
            "col_nums": "*" + VALID_COL_NUMS[:9]
        }
    )
    assert response.status_code == 422
    assert response.json()['detail'][0]['type'] == 'string_pattern_mismatch'

