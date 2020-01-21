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
    if n not in range(1, 9) or n in board[:, x] or n in board[y, :] or y not in range(9) or x not in range(9):
        print("input invalid")
        return False
    else:
        return True
# check the subgrid
  

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
