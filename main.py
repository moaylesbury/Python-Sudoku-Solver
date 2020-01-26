import numpy as np
import copy
import tkinter as tk

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

        self.quit = tk.Button(self, text="Quit", fg="red", command=self.master.destroy)
        self.quit.pack(fill="both", side="bottom")

        self.clear = tk.Button(self, text="Clear Board", command=self.clear)
        self.clear.pack(fill="both", side="bottom")

        self.solve = tk.Button(self, text="Solve", command=self.backtracking_algorithm)
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
        # TODO: Check if game is over
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

    def __key_press(self, event):
        # TODO: Check if game is over
        x = 0
        self.event = int(event.char)
        if self.valid(self.event):
            self.game.board[self.col][self.row] = event.char
            self.draw()

    def clear(self):
        self.game.board = np.zeros((9, 9), dtype=int)
        self.draw()

    def valid(self, v):
        print(v)
        # FutureWarning: elementwise comparison failed; returning scalar instead, but in the future will perform elementwise comparison
        #   if self.event in self.game.board[0:3, 0:3]:
        # Having problem with python and numpy clashes so cant use self.even in self.game.board...
        if v not in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
            return False
        if v in [r for r in self.game.board[:, self.row]]:
            print("Error: n already in column")
            return False
        if v in [c for c in self.game.board[self.col, :]]:
            print("Error: n already in row")
            return False
        rr, rc = gridrange(self.row), gridrange(self.col)
        if v in [i for i in np.reshape(self.game.board[rc[0]:rc[1], rr[0]:rr[1]], 9)]:
            print("Error: n already in sub-grid")
            return False
        return True

    def finished(self):
        for i in self.game.board:
            for j in i:
                if j == 0:
                    return False
        return True

    def backtracking_algorithm(self):
        original_board = np.reshape(copy.deepcopy(self.game.board), 81)
        print(original_board)
        board = np.reshape(self.game.board, 81)

        backtrack = True
        fail_count = 0
        count = 0
        attempts = []

        for i in range(len(board) - 70):
            attempts = []
            # 1.
            fail_count = 0
            for n in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
                if self.valid(n):
                    backtrack = False
                    board[i] = n
                    self.draw()
                    continue
                fail_count += 1
            if fail_count == 8:
                backtrack = True






            # 2.
            print("fail count", fail_count)
            print("backtrack?", backtrack)

            while backtrack:
                count += 1
                fail_count = 0
                attempts.append(board[i])
                for n in [j for j in range(1, 10) if j not in attempts]:
                    if self.valid(n):
                        backtrack = False
                        board[i-count] = n
                        self.draw()
                        continue
                    fail_count += 1
                if fail_count == 8:
                    backtrack = True



    """
    # Pseudo code for backtracking
    
    # 1. 
    loop row:
        loop entries in row:
            try numbers 1-9:
                if none are valid then backtrack    
                
    # 2.
    while backtracking:
        try numbers 1-9 but not the current one:
            if valid stop backtracking
    
    """



if __name__ == '__main__':
    game = Sudoku()
    game.__init__()

    root = tk.Tk()
    Interface = Interface(game, root)
    root.mainloop()
