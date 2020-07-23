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

## API Solution

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

## Algorithm Solution

The Boggle word finder algorithm utilizes a recursive function

``` python
    def calculate_points(word, board):
        board_2d_array = BoardManager.make_2d_board(board)
        print(board_2d_array)
        start_i = 0
        start_j = 0

        def is_out_of_bounds(i, j):
            if (
                i < 0
                or i > len(board_2d_array) - 1
                or j < 0
                or j > len(board_2d_array) - 1
            ):
                return True

        def check_board(board, start_position, word, word_index):
            print(word_index, start_position)
            print(board)
            i = start_position[0]
            j = start_position[1]
            word_index += 1
            word_found = False
            # Base Case - Word has been Found
            if word_index == len(word):
                board[i][j] = "-"
                print(word_index, word, board)
                return True

            # Check letter above
            next_i = i - 1
            next_j = j

            if not is_out_of_bounds(next_i, next_j):
                if (
                    word[word_index] == board[next_i][next_j]
                    or board[next_i][next_j] == "*"
                ) and board[next_i][next_j] != "-":
                    board[i][j] = "-"
                    return check_board(board, (next_i, next_j), word, word_index)

            # Check letter below
            next_i = i + 1
            next_j = j

            if not is_out_of_bounds(next_i, next_j):
                if (
                    board[next_i][next_j] == word[word_index]
                    or board[next_i][next_j] == "*"
                ) and board[next_i][next_j] != "-":
                    board[i][j] = "-"
                    return check_board(board, (next_i, next_j), word, word_index)

            # Check letter left
            next_i = i
            next_j = j - 1

            if not is_out_of_bounds(next_i, next_j):
                if (
                    word[word_index] == board[next_i][next_j]
                    or board[next_i][next_j] == "*"
                ) and board[next_i][next_j] != "-":
                    board[i][j] = "-"
                    return check_board(board, (next_i, next_j), word, word_index)

            # Check letter right
            next_i = i
            next_j = j + 1

            if not is_out_of_bounds(next_i, next_j):
                if (
                    word[word_index] == board[next_i][next_j]
                    or board[next_i][next_j] == "*"
                ) and board[next_i][next_j] != "-":
                    board[i][j] = "-"
                    return check_board(board, (next_i, next_j), word, word_index)

            # Check letter upper-right
            next_i = i - 1
            next_j = j + 1

            if not is_out_of_bounds(next_i, next_j):
                if (
                    word[word_index] == board[next_i][next_j]
                    or board[next_i][next_j] == "*"
                ) and board[next_i][next_j] != "-":
                    board[i][j] = "-"
                    return check_board(board, (next_i, next_j), word, word_index)

            # Check letter upper-left
            next_i = i - 1
            next_j = j - 1

            if not is_out_of_bounds(next_i, next_j):
                if (
                    word[word_index] == board[next_i][next_j]
                    or board[next_i][next_j] == "*"
                ) and board[next_i][next_j] != "-":
                    board[i][j] = "-"
                    return check_board(board, (next_i, next_j), word, word_index)

            # Check letter lower-right
            next_i = i + 1
            next_j = j + 1

            if not is_out_of_bounds(next_i, next_j):
                if (
                    word[word_index] == board[next_i][next_j]
                    or board[next_i][next_j] == "*"
                ) and board[next_i][next_j] != "-":
                    board[i][j] = "-"
                    return check_board(board, (next_i, next_j), word, word_index)

            # Check letter lower-left
            next_i = i + 1
            next_j = j - 1

            if not is_out_of_bounds(next_i, next_j):
                if (
                    word[word_index] == board[next_i][next_j]
                    or board[next_i][next_j] == "*"
                ) and board[next_i][next_j] != "-":
                    board[i][j] = "-"
                    return check_board(board, (next_i, next_j), word, word_index)

            # # If all cases fail, return false
            return False

        word_exists = False
        start_positions = []

        # Check if first letter exists in board first, use those as starting point
        for i in range(len(board_2d_array)):
            for j in range(len(board_2d_array[i])):
                if word[0] == board_2d_array[i][j] or board_2d_array[i][j] == "*":
                    start_positions.append((i, j))

        for start_position in start_positions:
            word_exists = check_board(board_2d_array, start_position, word, 0)
            if word_exists:
                break

        if word_exists:
            print("WORD FOUND")
            return len(word) # Score of word = length of word
        else:
            print("WORD NOT FOUND")
            return 0

```

Initialize:

index = 0

1. Get all starting locations that we can start the recursive algorithm and store it in a list.
2. The starting locations are determined when the first character of the input word matches the selected word on the boggle board.
3. For each start location, check its adjacent characters (8 directions).
4. If the adjacent character matches with the next character in the word (or is a '*' and is not '-'), "move" to that character, update the board by replacing the old position with a '-' such that the algorithm knows that that character was used.
5. Increase the index by 1
6. If index = length of input word, it means that the word can be found on the boggle board and we return True.