from flask import Flask, jsonify, request, Response
from jsonschema import validate, ValidationError # to validate post data
import json
import re
from Board import Board, BoardManager

app = Flask(__name__)
VALID_BOARD_LEN = 16

def load_default_board():
    with open(Board.default_board,"r") as f:
        data = f.read()
    return data

@app.route("/games",methods=["POST"])
def new_game():
    """
    Create a new Boggle game

    Parameters:
        duration (int): the time (in seconds) that specifies the duration of the game
        random (bool): if `true`, then the game will be generated with random
        board.  Otherwise, it will be generated based on input.
        board (string (16)): if `random` is not true, this will be used as the board
        for new game. If this is not present, new game will get the default board
        from `test_board.txt`

    Response Code:
        201: Success
        returns: 
        {
            "id": 1,
            "token": "9dda26ec7e476fb337cb158e7d31ac6c",
            "duration": 12345,
            "board": "A, C, E, D, L, U, G, *, E, *, H, T, G, A, F, K"
        }
        400: Error
    """
    # Schema for post data
    schema = {
        "type": "object",
        "properties": {
            "duration": {"type": "number", "minimum":1, 'maximum':2**31},
            "random": {"type": "boolean"},
            "board": {"type": "string"},
        },
        "required": ["duration", "random"],
    }

    post_data = request.json

    # Check if incoming POST data is valid
    try:
        validate(instance=post_data, schema=schema)
    except ValidationError as error:
    # Return to client the error
        return Response(str(error), status=400)
    try:
        board_string = post_data['board']
    except KeyError:
        board_string = load_default_board()
        print(board_string)

    random = post_data['random']
    duration = post_data['duration']

    # Insert Regex Expression Here
    invalid_characters = r"[^a-zA-Z\*]" # All non lowercase and uppercase alphabets + *
    board_string = re.sub(invalid_characters,"", board_string)
    print(board_string)

    # Check if length of board is correct
    if len(board_string) != VALID_BOARD_LEN and random is False:
        return Response(f"Invalid Board length! {board_string} ({len(board_string)} != {VALID_BOARD_LEN}) Calculated after removing invalid characters Regex: [^a-zA-Z\*]", status=400)
    
    # Instantiate a boggle board
    board = Board(duration, random, board_string, VALID_BOARD_LEN)
    BoardManager.start_board(board)

    print(board.get_json())
    # Return boggle board in json format with 201 Success Code
    return Response(json.dumps(board.get_json()),mimetype='application/json',status=201)


@app.route("/games/<id>",methods=["GET","PUT"])
def game(id):
    """
    PUT:
    Play a word in the existing boggle board

    Parameters:
        id (int) (required): The ID of the game
        token (string) (required): The token for authenticating the game
        word (string) (required): The word that can be used to play the game

    Responses:
        200: Success
        returns: 
        {
            "id": 1,
            "token": "9dda26ec7e476fb337cb158e7d31ac6c",
            "duration": 12345,
            "board": "A, C, E, D, L, U, G, *, E, *, H, T, G, A, F, K",
            "time_left": 10000,
            "points": 10
        }
        400: Error
    """
    
    schema = {
        "type": "object",
        "properties": {
            "token": {"type": "string"},
            "word": {"type": "string"},
        },
        "required": ["token", "word"],
    }

    # Get Arguments
    data = request.json
    # data = {}
    # data['board_id'] = request.args.get("id")
    # data['token'] = request.args.get("token")
    word = data['word'].upper()

    # Check if incoming POST data is valid
    try:
        validate(instance=data, schema=schema)
    except ValidationError as error:
    # Return to client the error
        return Response(str(error), status=400)

    # Check if board id exists
    board = BoardManager.play_board(int(id), word)
    if board is None:
        return Response("Board does not exist!", status=400)

    # Check if token is valid
    if board['token'] != data['token']:
        return Response("Invalid Token", status=401)

    # Check for invalid Characters
    invalid_characters = r"[^a-zA-Z]"
    if re.search(invalid_characters, data['word']) is not None:
        return Response("Invalid Character Detected!", status=400)

    return board


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
