import secrets
import random
import string

class Board():
    id_counter = 0
    default_board = 'test_board.txt'

    def __init__(self, duration, random, board_string="", board_size=16):
        self.valid_characters = string.ascii_uppercase + "*"
        self.board_string = board_string

        if board_string is None:
            self.board_string = self.load_default_board()
        if random:
            self.board_string = self.random_board(board_size)

        self.board = self.format_board(self.board_string)
        self.id = self.get_id()
        self.token = self.generate_token()
        self.duration = duration

    def get_id(self):
        Board.id_counter += 1
        return Board.id_counter

    def format_board(self, board):
        board = board.upper()
        out = ""
        for i in range(len(board)):
            out += board[i]
            if i < len(board) - 1:
                out += ", "
        return out
        
    def generate_token(self):
        return secrets.token_hex(16)

    def get_json(self):
        out = {} 
        out['id'] = self.id
        out['token'] = self.token
        out['duration'] = self.duration
        out['board'] = self.board
        return out

    def random_board(self,board_size):
        out = ""
        for i in range(board_size):
            out += random.choice(string.ascii_letters)
        return out

    def load_default_board(self):
        with open(Board.default_board,"r") as f:
            data = f.read()
        return data
