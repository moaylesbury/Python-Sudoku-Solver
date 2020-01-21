import numpy as np
from tkinter import *
from tkinter.ttk import *


def draw(array):
    print()
    count = 1
    for i in np.nditer(array):
        print(i, end=' ')
        if count % 3 == 0 and count % 9 != 0:
            print('##', end=' ')
        if count % 9 == 0:
            print(' ')
        if count == 27 or count == 27*2:
            print('#'*23)
        count += 1
    print()


def valid(x, y, n, board):
    if n not in range(1, 9):
        print("Error: n not between 1 and 9")
        return False
    elif n in board[:, x]:
        print("Error: n already in column")
        return False
    elif n in board[y, :]:
        print("Error: n already in row")
        return False
    elif y not in range(9):
        print("Error: coordinates out of bounds")
        return False
    elif x not in range(9):
        print("Error: coordinates out of bounds")
        return False
    elif 0 <= y <= 2:
        if 0 <= x <= 2:
            if n in board[0:3, 0:3]:
                print("Error: n already in sub-grid")
                return False
        if 3 <= x <= 5:
            if n in board[3:6, 0:3]:
                print("Error: n already in sub-grid")
                return False
        if 6 <= x <= 9:
            if n in board[6:9, 0:3]:
                print("Error: n already in sub-grid")
                return False
    elif 3 <= y <= 5:
        if 0 <= x <= 2:
            if n in board[0:3, 3:6]:
                print("Error: n already in sub-grid")
                return False
        if 3 <= x <= 5:
            if n in board[3:6, 3:6]:
                print("Error: n already in sub-grid")
                return False
        if 6 <= x <= 9:
            if n in board[6:9, 3:6]:
                print("Error: n already in sub-grid")
                return False
    elif 6 <= y <= 9:
        if 0 <= x <= 2:
            if n in board[0:3, 6:10]:
                print("Error: n already in sub-grid")
                return False
        if 3 <= x <= 5:
            if n in board[3:6, 6:10]:
                print("Error: n already in sub-grid")
                return False
        if 6 <= x <= 9:
            if n in board[6:9, 6:10]:
                print("Error: n already in sub-grid")
                return False
    else:
        return True


def complete(board):
    if 0 not in board:
        return True
    else:
        return False


def game():
    play = True
    board = np.zeros((9, 9), dtype=int)
    draw(board)

    while play:
        print("Enter \"xyn\" to change the number at (x,y) to n")
        inp = input()
        x = int(inp[0])
        y = int(inp[1])
        n = int(inp[2])
        if valid(x, y, n, board):
            board[y, x] = n
            draw(board)
        if complete(board):
            print("Sudoku complete!")
            play = False


game()
