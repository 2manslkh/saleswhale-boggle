# Boggle API

Lim Keng Hin

## Requirements

Python 3.7 and above

## Setup

Install the prerequisite packages

`$ pip install -r requirements.txt`

Run flask

`$ cd src`

`$ python main.py`

The server should be running on `localhost:5000`

## Solution

There are 2 main endpoints for this API, `games` and `games/<id>`.

- `games` endpoint
  - Only accepts POST request, otherwise return with 405 code
  - Checks if the required params are included using `jsonschema`

  ``` python
  schema = {
    "type": "object",
      "properties": {
        "duration": {"type": "number", "minimum":1, 'maximum':2**31},
        "random": {"type": "boolean"},
        "board": {"type": "string"},
      },
    "required": ["duration", "random"],
  }
  ```

  - Returns 400 response if invalid POST data
  - Check if input board is valid (has 16 alphabet characters after removing special characters)
  - Check if duration is > 0 and < 2**32
  - Post data is passed into a `Board` instance
  - If random is enabled, randomize 16 letters including '*' and set it as the board
  - If random is disabled and board is absent, use the default board
    - Read test_board.txt using open() function
  - `Board` instance is added to `BoardManager` which keeps track of all active `Board` instances (extra: to keep track of multiple games)
  - Call Board.get_json() to prepare output json
  - use del methods to remove unnecessary json keys.
  - use json.dumps() to dump json into a string format
  - Return json string with 201 Response Code

- `games/<id>` [PUT] endpoint
  - Formulate schema for valid json input using `jsonschema`

  ``` python
  schema = {
    "type": "object",
      "properties": {
        "token": {"type": "string"},
        "word": {"type": "string"},
      },
    "required": ["token", "word"],
  }
  ```
  - Validate input json
  - Apply .upper() function to input word string (extra: to make word matching for algorithm easier)
  - Check if board id exists
    - Return 404 board not found otherwise
  - Check if token is valid
    - Return 401 not authorized otherwise
  - Check if game has expired using (datetime.now - board.startime) > board.duration
    - Return 400 status otherwise
  - Check if any invalid character is included (extra: saves some time)
  - Check if any invalid word is included
    - Return 400 status otherwise
  - Play the input word into the board
  - Calculate points based on length of input word
  - Update and save points to board
  - Return current status of board

- `games/<id>` [GET] endpoint
  - Validate input id if id exists in existing games.
    - If not valid, return 404 status
  - Return board status