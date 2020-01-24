import numpy as np
import tkinter as tk


#  from tkinter import *
# from tkinter.ttk import *


def draw(board):
    print()
    count = 1
    for i in np.nditer(board):
        print(i, end=' ')
        if count % 3 == 0 and count % 9 != 0:
            print('##', end=' ')
        if count % 9 == 0:
            print(' ')
        if count == 27 or count == 27 * 2:
            print('#' * 23)
        count += 1
    print()


class Sudoku:
    def __init__(self):
        self.board = np.zeros((9, 9), dtype=int)
        self.game()

    def valid(self, x, y, n):
        if n not in range(1, 9):
            print("Error: n not between 1 and 9")
            return False
        if n in self.board[:, x]:
            print("Error: n already in column")
            return False
        if n in self.board[y, :]:
            print("Error: n already in row")
            return False
        if y not in range(9):
            print("Error: coordinates out of bounds")
            return False
        if x not in range(9):
            print("Error: coordinates out of bounds")
            return False
        if 0 <= y <= 2:
            if 0 <= x <= 2:
                if n in self.board[0:3, 0:3]:
                    print("Error: n already in sub-grid")
                    return False
            if 3 <= x <= 5:
                if n in self.board[3:6, 0:3]:
                    print("Error: n already in sub-grid")
                    return False
            if 6 <= x <= 9:
                if n in self.board[6:9, 0:3]:
                    print("Error: n already in sub-grid")
                    return False
        if 3 <= y <= 5:
            if 0 <= x <= 2:
                if n in self.board[0:3, 3:6]:
                    print("Error: n already in sub-grid")
                    return False
            if 3 <= x <= 5:
                if n in self.board[3:6, 3:6]:
                    print("Error: n already in sub-grid")
                    return False
            if 6 <= x <= 9:
                if n in self.board[6:9, 3:6]:
                    print("Error: n already in sub-grid")
                    return False
        if 6 <= y <= 9:
            if 0 <= x <= 2:
                if n in self.board[0:3, 6:10]:
                    print("Error: n already in sub-grid")
                    return False
            if 3 <= x <= 5:
                if n in self.board[3:6, 6:10]:
                    print("Error: n already in sub-grid")
                    return False
            if 6 <= x <= 9:
                if n in self.board[6:9, 6:10]:
                    print("Error: n already in sub-grid")
                    return False
        return True

    def complete(self):
        if 0 not in self.board:
            return True
        else:
            return False

    def game(self):
        play = False

        #draw(self.board)

        while play:
            print("Enter \"xyn\" to change the number at (x,y) to n")
            inp = input()
            x = int(inp[0])
            y = int(inp[1])
            n = int(inp[2])
            if self.valid(x, y, n):
                self.board[y, x] = n
                #draw(self.board)
            if self.complete():
                print("Sudoku complete!")
                play = False


class Interface(tk.Frame, object):

    def __init__(self, game, master=None):
        super().__init__(master)
        self.col = 0
        self.row = 0
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
        #self.canvas.bind("<Button-1>", self.__click)  # add a function for clicking
        #self.canvas.bind("<Key>", lambda evt: self.__key_press)  # add a function for key pressing

        # Buttons at the bottom

        self.quit = tk.Button(self, text="Quit", fg="red", command=self.master.destroy)
        self.quit.pack(fill="both", side="bottom")

        self.clear = tk.Button(self, text="Clear Board")
        self.clear.pack(fill="both", side="bottom")

        self.solve = tk.Button(self, text="Solve")
        self.solve.pack(fill="both", side="bottom")

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
        x, y = 56, 60
        xs = []
        ys = []

        self.canvas.delete("numbers")

        # x coords
        vx = [56 + self.increment * i for i in range(9)]
        for i in range(9):
            for v in vx:
                xs.append(v)
        #print(xs)
        # y coords
        vy = [60 + self.increment * j for j in range(9)]
        for v in vy:
            for i in range(9):
                ys.append(v)
        # drawing
        count = 0
        for k in self.game.board:
            for l in k:
                self.canvas.create_text(xs[count], ys[count], text=l, tags="numbers")
                count += 1

    def __click(self, event):
        # Only continue if game is not over, check that. if it is done return
        """
        If game over
            return
        """
        # Check x and y are in play area
        # if self.side_padding <= event.x <= self.right_edge and self.top_padding <= event.y <= self.bottom_edge:
        # print("In play")

        self.canvas.delete("selected")
        self.yaxis = [self.top_padding + 50 * i for i in range(10)]
        self.xaxis = [self.side_padding + 50 * i for i in range(10)]
        self.x0, x1, self.y0, y1 = 0, 0, 0, 0
        x, y = event.x, event.y
        self.canvas.focus_set()
        for i in range(len(self.xaxis) - 1):
            if self.xaxis[i] <= x <= self.xaxis[i + 1]:
                self.row = i
                self.x0 = self.xaxis[i]
                x1 = self.xaxis[i + 1]
            if self.yaxis[i] <= y <= self.yaxis[i + 1]:
                self.col = i
                self.y0 = self.yaxis[i]
                y1 = self.yaxis[i + 1]
        self.canvas.create_rectangle(self.x0, self.y0, x1, y1, outline="red", tags="selected")
        print(self.row, self.col)
        # print(event.x, event.y)

    def __key_press(self, event):
        print("test")
        print(event.char)
        x = 0
        ## if game not over add according to sudoku rules
        if event.char in "123456789":
            self.game.board[self.col][self.row] = event.char
            self.draw()



if __name__ == '__main__':
    game = Sudoku()
    game.__init__()

    root = tk.Tk()
    Interface = Interface(game, root)
    root.mainloop()
