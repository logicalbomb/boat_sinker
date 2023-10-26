from fastapi.testclient import TestClient

from .main import app

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