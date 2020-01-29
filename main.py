import numpy as np
import tkinter as tk
from random import randint


class Board:
    def __init__(self):
        self.board = np.zeros((9, 9), dtype=int)


def grid_range(x):
    return [0, 3] if 0 <= x <= 2 else [3, 6] if 3 <= x <= 5 else [6, 9] if 6 <= x <= 9 else [0, 0]


class Interface(tk.Frame, object):

    def __init__(self, game, master=None):
        super().__init__(master)
        self.col, self.row = 0, 0
        self.master = master
        self.game = game
        self.original_board, self.solved = np.zeros((9, 9), dtype=int), np.zeros((9, 9), dtype=int)

        self.dimension = 512  # just called dimension as height = width in the square grid
        self.increment = 50
        self.side_padding = (self.dimension - 9 * 50) // 2
        self.top_padding = 35

        self.right_edge = self.dimension - self.side_padding
        self.bottom_edge = 9 * 50 + self.top_padding

        self.xs, self.ys = [], []
        for i in range(9):
            [self.xs.append(x) for x in [56 + self.increment * i for i in range(9)]]
        vy = [60 + self.increment * j for j in range(9)]
        for v in vy:
            for i in range(9):
                self.ys.append(v)

        self.__display()
        self.new_board()
        self.pack()

    def __display(self):

        self.master.title("Sudoku")
        self.pack(fill="both", expand=1)

        self.canvas = tk.Canvas(self, width=self.dimension, height=self.dimension, highlightthickness=0)
        self.canvas.pack(fill="both", side="top")

        quit_button = tk.Button(self, text="Quit", fg="red", command=self.master.destroy)
        quit_button.pack(fill="both", side="bottom")

        reset_button = tk.Button(self, text="Reset", command=self.reset_board)
        reset_button.pack(fill="both", side="bottom")

        new_button = tk.Button(self, text="New Sudoku", command=self.new_board)
        new_button.pack(fill="both", side="bottom")

        solve_button = tk.Button(self, text="Solve", command=self.solve)
        solve_button.pack(fill="both", side="bottom")

        self.__create_grid()

        self.canvas.bind("<Button-1>", self.__click)  # add a function for clicking
        self.canvas.bind("<Key>", self.key_press)  # add a function for key pressing

    def new_board(self):
        self.game.board = np.zeros((9, 9), dtype=int)
        self.solving_algorithm()
        self.solved = np.copy(self.game.board)
        remove = randint(36, 46)
        while remove != 0:
            x, y = randint(0, 8), randint(0, 8)
            if self.game.board[x][y] != 0:
                self.game.board[x][y] = 0
                remove -= 1
        self.original_board = np.copy(self.game.board)
        self.draw()

    def reset_board(self):
        self.game.board = self.original_board
        self.draw()

    def __create_grid(self):
        # Defining constants
        self.canvas.create_line(self.side_padding, self.top_padding, self.side_padding, self.bottom_edge, fill="blue")
        self.canvas.create_line(self.side_padding, self.top_padding, self.right_edge, self.top_padding, fill="blue")
        for i in range(1, 10):
            colour = "blue" if i % 3 == 0 else "gray"
            self.canvas.create_line(self.side_padding + i * self.increment, self.top_padding,
                                    self.side_padding + i * self.increment, self.bottom_edge, fill=colour)
            self.canvas.create_line(self.side_padding, self.top_padding + i * self.increment, self.right_edge,
                                    self.top_padding + i * self.increment, fill=colour)
        self.draw()

    def draw(self):
        # Clearing text
        self.canvas.delete("numbers")
        print(self.solved)
        # Drawing
        count = 0
        for x in range(9):
            for y in range(9):
                if not self.finished():
                    if self.original_board[x][y] == 0:
                        self.canvas.create_text(self.xs[count], self.ys[count], text=self.game.board[x][y],
                                                tags="numbers", fill="black")
                    else:
                        self.canvas.create_text(self.xs[count], self.ys[count], text=self.original_board[x][y],
                                                tags="numbers", fill="blue")
                else:
                    self.canvas.create_text(self.xs[count], self.ys[count], text=self.game.board[x][y],
                                            tags="numbers", fill="green")
                count += 1

    def __click(self, event):

        if self.finished():
            self.draw()
            return

        self.canvas.delete("selected")
        yaxis = [self.top_padding + 50 * i for i in range(10)]
        xaxis = [self.side_padding + 50 * i for i in range(10)]
        x0, x1, y0, y1 = 0, 0, 0, 0
        x, y = event.x, event.y
        self.canvas.focus_set()
        for i in range(len(xaxis) - 1):
            if xaxis[i] <= x <= xaxis[i + 1]:
                self.row = i
                x0 = xaxis[i]
                x1 = xaxis[i + 1]
            if yaxis[i] <= y <= yaxis[i + 1]:
                self.col = i
                y0 = yaxis[i]
                y1 = yaxis[i + 1]
        self.canvas.create_rectangle(x0, y0, x1, y1, outline="red", tags="selected")

    def key_press(self, event):

        if self.finished():
            self.draw()
            return

        if self.valid(self.row, self.col, int(event.char)):
            self.game.board[self.col][self.row] = event.char
            self.draw()

    def valid(self, x, y, n):
        if n not in [1, 2, 3, 4, 5, 6, 7, 8, 9] or n in [r for r in self.game.board[:, x]] \
                or n in [c for c in self.game.board[y, :]]:
            return False

        rr, rc = grid_range(x), grid_range(y)

        if n in [i for i in np.reshape(self.game.board[rc[0]:rc[1], rr[0]:rr[1]], 9)]:
            return False

        return True

    def finished(self):
        return False if 0 in np.reshape(self.game.board, 81) else True

    def empty(self):
        for x in range(9):
            for y in range(9):
                if self.game.board[x][y] == 0:
                    return x, y

    def solve(self):
        self.game.board = self.solved
        self.draw()

    def solving_algorithm(self):
        # Returns true if the algorithm is successful, false otherwise
        if self.finished():
            return True

        x, y = self.empty()

        for n in range(1, 10):

            if self.valid(y, x, n):
                self.game.board[x][y] = n

                if self.solving_algorithm():
                    return True

                self.game.board[x][y] = 0

        return False


if __name__ == '__main__':
    Game = Board()
    Game.__init__()

    root = tk.Tk()
    Interface = Interface(Game, root)
    root.mainloop()
