import secrets
import random
import string
import datetime

with open("dictionary.txt") as f:
    content = f.readlines()
content = [x.strip() for x in content]


class BoardManager:

    valid_words = content
    active_boards = {}

    @staticmethod
    def start_board(board):
        BoardManager.active_boards[board.get_id()] = board

    @staticmethod
    def end_board(_id):
        del BoardManager.active_boards[_id]

    @staticmethod
    def get_time_remaining():
        return 10000

    @staticmethod
    def make_2d_board(board):
        len_board = len(board)
        root_len_board = int(len_board ** 0.5)
        output = []
        if len_board == root_len_board ** 2:
            for i in range(root_len_board):
                out = list(board[i * root_len_board : (i + 1) * root_len_board])
                output.append(out)
        return output

    @staticmethod
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

            # Base Case - Word has been Found
            if word_index == len(word):
                board[i][j] = "-"
                print(word_index, word, board)
                return True
            
            # List of all possible moves in 8 directions
            possible_moves = [(i-1,j),(i+1,j),(i,j+1),(i,j-1),(i-1,j-1),(i-1,j+1),(i+1,j+1),(i+1,j-1)]
            
            # Loop through possible moves
            for k in range(len(possible_moves)):
              next_i = possible_moves[k][0]
              next_j = possible_moves[k][1]

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
                    print(start_positions)

        for start_position in start_positions:
            word_exists = check_board(board_2d_array, start_position, word, 0)
            if word_exists:
                break

        if word_exists:
            print("WORD FOUND")
            return len(word)
        else:
            print("WORD NOT FOUND")
            return 0

    @staticmethod
    def play_board(index, word):
        try:
            selected_board = BoardManager.active_boards[index]
            selected_board.add_points(
                BoardManager.calculate_points(word, selected_board.get_board_string())
            )
            selected_board.update_time_left()
            return selected_board
        except KeyError:
            return None

    @staticmethod
    def get_board(index):
        try:
            selected_board = BoardManager.active_boards[index]
            return selected_board
        except KeyError:
            return None


class Board:
    id_counter = 0
    # default_board = 'test_board.txt'

    def __init__(self, duration, random, board_string="", board_size=16):
        self.valid_characters = string.ascii_uppercase + "*"
        self.board_string = board_string

        # if board_string is None:
        #     self.board_string = self.load_default_board()
        if random:
            self.board_string = self.random_board(board_size)

        self.board = self.format_board(self.board_string)
        self.id = self.assign_id()
        self.token = self.generate_token()
        self.duration = duration
        self.time_left = duration
        self.points = 0
        self.start_time = datetime.datetime.now()

    def assign_id(self):
        Board.id_counter += 1
        return Board.id_counter

    def get_id(self):
        return self.id

    def get_token(self):
        return self.token

    def get_start_time(self):
        return self.start_time

    def format_board(self, board):
        board = board.upper()
        out = ""
        for i in range(len(board)):
            out += board[i]
            if i < len(board) - 1:
                out += ", "
        return out

    def get_duration(self):
        return self.duration

    def generate_token(self):
        # return secrets.token_hex(16)
        return "6679bd8553db4ccb0c62c6f9d775fcdc"

    def get_json(self):
        out = {}
        out["id"] = self.id
        out["token"] = self.token
        out["duration"] = self.duration
        out["board"] = self.board
        out["points"] = self.points
        out["time_left"] = self.time_left
        return out

    def random_board(self, board_size):
        out = ""
        for i in range(board_size):
            out += random.choice(string.ascii_letters)
        return out

    # def load_default_board(self):
    #     with open(Board.default_board,"r") as f:
    #         data = f.read()
    #     return data

    def add_points(self, points):
        self.points += points

    def update_time_left(self):
        self.time_left

    def get_board_string(self):
        return self.board_string
