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

    def __init__(self, parent, game):
        self.game = game
        self.parent = parent
        super().__init__(self, parent, game)
        self.master = master
        self.row, self.col = 0, 0
        self.__display()

    def __display(self):
        self.parent.title("Sudoku")
        self.pack(fill="BOTH", expand=1)
        self.canvas = tk.Canvas(self, width=40, height=40)\
            .pack(fill="BOTH", side="top")\
            .bind("<Button-1>", self.click)\
            .bind("<Key>", self.keypress)
        self.test_button = tk.Button(self, text="Test Button", command=print("test"))\
            .pack(fill="BOTH", side="bottom")
        self.quit = tk.Button(self, text="QUIT", fg="red", command=self.master.destroy)\
            .pack(fill="BOTH", side="bottom")


if __name__ == '__main__':
    game = Sudoku()
    root = tk.Tk()
    Interface(root, game)
    root.mainloop()
