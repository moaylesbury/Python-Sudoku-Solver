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
        play = True

        draw(self.board)

        while play:
            print("Enter \"xyn\" to change the number at (x,y) to n")
            inp = input()
            x = int(inp[0])
            y = int(inp[1])
            n = int(inp[2])
            if self.valid(x, y, n):
                self.board[y, x] = n
                draw(self.board)
            if self.complete():
                print("Sudoku complete!")
                play = False


class Interface(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.__display()
        self.pack()


    def __display(self):
        self.dimension = 512  # just called dimension as height = width in the square grid
        self.master.title("Sudoku")
        self.pack(fill="both", expand=1)
        self.canvas = tk.Canvas(self, width=self.dimension, height=self.dimension)
        self.canvas.pack(fill="both", side="top")
        self.canvas.bind("<Button-1>", self.click)  # add a function for clicking
        self.canvas.bind("<Key>", self.key_press)  # add a function for key pressing

        # Buttons at the bottom

        self.quit = tk.Button(self, text="Quit", fg="red", command=self.master.destroy)
        self.quit.pack(fill="both", side="bottom")

        self.clear = tk.Button(self, text="Clear Board")
        self.clear.pack(fill="both", side="bottom")

        self.solve = tk.Button(self, text="Solve")
        self.solve.pack(fill="both", side="bottom")

        self.create_grid()

    def create_grid(self):
        # Defining constants
        increment = 50
        side_padding = (self.dimension - 9 * 50) // 2
        top_padding = 35

        right_edge = self.dimension - side_padding
        bottom_edge = 9 * 50 + top_padding

        self.canvas.create_line(side_padding, top_padding, side_padding, bottom_edge,  fill="blue")
        self.canvas.create_line(side_padding, top_padding, right_edge, top_padding, fill="blue")
        for i in range(1, 10):
            colour = "blue" if i % 3 == 0 else "gray"
            self.canvas.create_line(side_padding + i * increment, top_padding, side_padding + i * increment, bottom_edge, fill=colour)
            self.canvas.create_line(side_padding, top_padding + i * increment, right_edge, top_padding + i * increment, fill=colour)

    def click(self, event):
        print("click")

    def key_press(self, event):
        print("press")

if __name__ == '__main__':
    # game = Sudoku()
    root = tk.Tk()
    Interface = Interface(master=root)
    root.mainloop()
