# Python-Sudoku-Solver

A sudoku game created in **python** using the modules **tkinter** and **numpy**.

This was my first time using **tkinter**, so it was interesting exploring the module to create a GUI. **Numpy** was used to create a matrix representation of the sudoku board.

Aside from the grid, the interface consists of four buttons: **Solve, New Board, Reset Board, and Solve**.

The solve button makes use of the recursive **backtracking algorithm**, trying numbers 1-9. If the board cannot be solved then the algorithm goes back and tries different numbers until the board is solved.

In the future I would create a more sophisticated board generating algorithm, as the current one ends up with trends such as 1,2,3,4,5,6,7,8,9 in the first line and consecutive numbers appearing often. 
