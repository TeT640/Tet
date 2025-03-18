import numpy as np

colors = [
    (0, 0, 0),
    (120, 37, 179),
    (100, 179, 179),
    (80, 34, 22),
    (80, 134, 22),
    (180, 34, 22),
    (180, 34, 122),
]



class Figure:
    x = 0
    y = 0

    figures = [
        [[1, 5, 9, 13], [4, 5, 6, 7]],
        [[4, 5, 9, 10], [2, 6, 5, 9]],
        [[6, 7, 9, 10], [1, 5, 6, 10]],
        [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],
        [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],
        [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],
        [[1, 2, 5, 6]],
    ]

    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.type = type
        self.rotation = 0

    def image(self):
        return self.figures[self.type][self.rotation]

    def rotate(self, k):
        self.rotation = (self.rotation + k) % len(self.figures[self.type])


class Tetris:
    def __init__(self, height, width):
        self.level = 2
        self.score = 0
        self.state = "start"
        self.field = []
        self.height = 0
        self.width = 0
        self.x = 100
        self.y = 60
        self.zoom = 20
        self.figure = None
        self.reward=0

        self.height = height
        self.width = width
        self.field = []
        self.score = 0
        self.state = "start"
        for i in range(height):
            new_line = []
            for j in range(width):
                new_line.append(0)
            self.field.append(new_line)

    def new_figure(self, type):
        self.figure = Figure(3, 0, type)

    def intersects(self):
        intersection = False
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    if i + self.figure.y > self.height - 1 or \
                            j + self.figure.x > self.width - 1 or \
                            j + self.figure.x < 0 or \
                            self.field[i + self.figure.y][j + self.figure.x] > 0:
                        intersection = True
        return intersection

    def break_lines(self):
        lines = 0
        for i in range(1, self.height):
            zeros = 0
            for j in range(self.width):
                if self.field[i][j] == 0:
                    zeros += 1
            if zeros == 0:
                lines += 1
                for i1 in range(i, 1, -1):
                    for j in range(self.width):
                        self.field[i1][j] = self.field[i1 - 1][j]
        self.score += lines

    def go_space(self):
        while not self.intersects():
            self.figure.y += 1
        self.figure.y -= 1
        self.freeze()

    def go_down(self, ty):
        self.figure.y += 1
        if self.intersects():
            self.figure.y -= 1
            self.freeze()

    def freeze(self):
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    self.field[i + self.figure.y][j + self.figure.x] = 1
        self.break_lines()



    def go_side(self, dx):
        old_x = self.figure.x
        self.figure.x += dx
        if self.intersects():
            self.figure.x = old_x

    def rotate(self, k):
        old_rotation = self.figure.rotation
        self.figure.rotate(k)
        if self.intersects():
            self.figure.rotation = old_rotation
    def reset(self):
        '''Réinitialise le jeu et retourne l’état courant'''
        self.field = [[0] * self.width for _ in range(self.height)]  # Reset the board to empty
        self.game_over = False  # Reset game state
        self.new_figure(np.random.randint(len(Figure.figures)))  # Create a random figure
        self.score = 0  # Reset the score
        self.reward = 0
        return [0, 0, 0, 0]  # At the start, no cleared lines, no holes, no bumpiness, no height
    def play(self, x, rotation, render=False, render_delay=None):
        """
        Executes a move (position x and rotation) and returns (reward, game_over).
        """
        curr_score=self.score
        # Create a new figure if not present
        if not self.figure:
            return 0, True

        # Apply rotation
        self.figure.rotate(rotation)
        if self.intersects():
            #print("Game over: Rotation caused intersection")  # Debug print
            return -2, True  # Game over if rotation causes an intersection

        # Move the figure to the specified column
        self.go_side(x - self.figure.x)
        if self.intersects():
            #print("Game over: Movement caused intersection")  # Debug print
            return -2, True  # Game over if movement causes an intersection

        self.go_space()
        lines=self.score-curr_score


        reward=1 + (lines ** 2) * self.width
        self.reward += 1 + (lines ** 2) * self.width  # Reward formula
        #print(f"Lines cleared: {lines}, Reward: {self.reward}, Score: {self.score}")  # Debug print
        #print(self.field)
        # Start a new round with a new figure
        self.new_figure(np.random.randint(0, 7))

        # Check for game over
        if self.intersects():
            #print("Game over: New figure caused intersection")  # Debug print
            self.state = "gameover"
            return reward- 2, True  # Penalty for losing

        return reward, False
