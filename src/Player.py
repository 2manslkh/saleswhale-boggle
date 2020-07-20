class Player():
    def __init__(self):
        self.points = 0

    def add_points(self,points):
        self.points += points

    def minus_points(self, points):
        self.points -= points

    def reset_points(self):
        self.points = 0
