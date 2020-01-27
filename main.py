import numpy as np
import tkinter as tk


class Sudoku:
    def __init__(self):
        self.board = np.zeros((9, 9), dtype=int)


def gridrange(x):
    return [0, 3] if 0 <= x <= 2 else [3, 6] if 3 <= x <= 5 else [6, 9] if 6 <= x <= 9 else [0, 0]


class Interface(tk.Frame, object):

    def __init__(self, game, master=None):
        super().__init__(master)
        self.col, self.row = 0, 0
        self.master = master
        self.game = game
        self.__display()
        self.pack()

    def __display(self):
        self.dimension = 512  # just called dimension as height = width in the square grid
        self.master.title("Sudoku")
        self.pack(fill="both", expand=1)

        self.canvas = tk.Canvas(self, width=self.dimension, height=self.dimension)
        self.canvas.pack(fill="both", side="top")

        quit_button = tk.Button(self, text="Quit", fg="red", command=self.master.destroy)
        quit_button.pack(fill="both", side="bottom")

        clear_button = tk.Button(self, text="Clear Board", command=self.clear)
        clear_button.pack(fill="both", side="bottom")

        solve_button = tk.Button(self, text="Solve", command=self.solving_algorithm)
        solve_button.pack(fill="both", side="bottom")

        self.__create_grid()

        self.canvas.bind("<Button-1>", self.__click)  # add a function for clicking
        self.canvas.bind("<Key>", self.__key_press)  # add a function for key pressing

    def __create_grid(self):
        # Defining constants
        self.increment = 50
        self.side_padding = (self.dimension - 9 * 50) // 2
        self.top_padding = 35

        self.right_edge = self.dimension - self.side_padding
        self.bottom_edge = 9 * 50 + self.top_padding

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
        xs = []
        ys = []

        # Clearing text
        self.canvas.delete("numbers")

        # Preparing coords
        for i in range(9):
            [xs.append(x) for x in [56 + self.increment * i for i in range(9)]]
        vy = [60 + self.increment * j for j in range(9)]
        for v in vy:
            for i in range(9):
                ys.append(v)

        # Drawing
        count = 0
        for row in self.game.board:
            for entry in row:
                self.canvas.create_text(xs[count], ys[count], text=entry, tags="numbers")
                count += 1

    def __click(self, event):
        # TODO: Check if game is over
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

    def __key_press(self, event):
        # TODO: Check if game is over
        if self.valid(int(event.char), self.row, self.col):
            self.game.board[self.col][self.row] = event.char
            self.draw()

    def clear(self):
        self.game.board = np.zeros((9, 9), dtype=int)
        self.draw()

    def valid(self, y, x, n):
        if n not in [1, 2, 3, 4, 5, 6, 7, 8, 9] or n in [r for r in self.game.board[:, x]] \
                or n in [c for c in self.game.board[y, :]]:
            return False

        rr, rc = gridrange(x), gridrange(y)
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

    def solving_algorithm(self):
        # Returns true if the algorithm is successful, false otherwise

        if self.finished():
            return True

        x, y = self.empty()

        for n in range(1, 10):
            if self.valid(x, y, n):
                self.game.board[x][y] = n
                self.draw()

                if self.solving_algorithm():
                    return True

                self.game.board[x][y] = 0
                self.draw()

        return False


if __name__ == '__main__':
    game = Sudoku()
    game.__init__()

    root = tk.Tk()
    Interface = Interface(game, root)
    root.mainloop()
