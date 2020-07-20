import secrets
import random
import string

class BoardManager():

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
    def calculate_points(word):
        return 10
    
    @staticmethod
    def play_board(index, word):
        try:
            selected_board = BoardManager.active_boards[index]
            selected_board.add_points(BoardManager.calculate_points(word))
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
        self.id = self.assign_id()
        self.token = self.generate_token()
        self.duration = duration
        self.time_left = duration
        self.points = 0

    def assign_id(self):
        Board.id_counter += 1
        return Board.id_counter

    def get_id(self):
        return self.id

    def get_token(self):
        return self.token

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
        out['points'] = self.points
        out['time_left'] = self.time_left
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

    def add_points(self, points):
        self.points += points

    def update_time_left(self):
        self.time_left 