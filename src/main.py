from flask import Flask, jsonify, request, Response
from jsonschema import validate, ValidationError # to validate post data
import json
import re
from Board import Board, BoardManager
import datetime

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
        return {'message':str(error)}, 400
    try:
        board_string = post_data['board']
    except KeyError:
        board_string = load_default_board()
        # print(board_string)

    random = post_data['random']
    duration = post_data['duration']

    # Insert Regex Expression Here
    invalid_characters = r"[^a-zA-Z\*]" # All non lowercase and uppercase alphabets + *
    board_string = re.sub(invalid_characters,"", board_string)
    # print(board_string)

    # Check if length of board is correct
    if len(board_string) != VALID_BOARD_LEN and random is False:
        return json.dumps({'message': f"Invalid Board length! {board_string} ({len(board_string)} != {VALID_BOARD_LEN}) Calculated after removing invalid characters Regex: [^a-zA-Z\*]"}), 400
    
    # Instantiate a boggle board
    board = Board(duration, random, board_string, VALID_BOARD_LEN)
    BoardManager.start_board(board)
    
    output = board.get_json()
    del output['points']
    del output['time_left']

    # Return boggle board in json format with 201 Success Code
    print(output)
    return json.dumps(output), 201


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

    if request.method == "PUT":
        # data = {}
        # data['board_id'] = request.args.get("id")
        # data['token'] = request.args.get("token")
        word = data['word'].upper()

        # Check if incoming POST data is valid
        try:
            validate(instance=data, schema=schema)
        except ValidationError as error:
        # Return to client the error
            return json.dumps({'message': str(error)}), 400

        # Check if board id exists
        board = BoardManager.get_board(int(id))
        if board is None:
            return json.dumps({'message':"Board does not exist!"}), 404

        # Check if token is valid
        if board.get_token() != data['token']:
            return json.dumps({'message':"Invalid Token"}), 401

        # Check if game expired
        if (datetime.datetime.now() - board.get_start_time()).total_seconds() > board.get_duration():
            return json.dumps({'message':"Game Expired!"}), 400

        # Check for invalid Characters
        invalid_characters = r"[^a-zA-Z]"
        if re.search(invalid_characters, data['word']) is not None:
            return json.dumps({'message':"Invalid Character Detected!"}), 400

        # Check if word is valid
        if word.lower() not in BoardManager.valid_words:
            return json.dumps({'message':"Invalid Word"}), 401

        # Play word
        BoardManager.play_board(int(id), word)
        output = board.get_json()

        return json.dumps(output), 200

    elif request.method == "GET":
        board = BoardManager.get_board(int(id))
        if board is None:
            return {'message':"Board does not exist!"}, 404
        output = board.get_json()
        return json.dumps(output), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000,threaded=False)
