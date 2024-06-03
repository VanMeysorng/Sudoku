import streamlit as st
import numpy as np
import time
import random

#function to check if the move is possible/valid or not
def is_valid_move(board, row, col, num):
    # check if the number already in the row
    if num in board[row, :]:
        return False
    # check if the number already in the column
    if num in board[:, col]:
        return False
    
    subgrid_row = 3 * (row // 3)
    subgrid_col = 3 * (col // 3)
    # check if the number in the 3x3 grid its inserting in
    if num in board[subgrid_row:subgrid_row_3, subgrid_col:subgrid_col + 3]:
        return False
    
    return True

#Fucntion solve

def solve_sudoku(board):
    empty_cell = find_empty_cell(board)
    if not empty_cell:
        return True
    
    row, col = empty_cell
    for num in range(1,10):
        if is_valid_move(board, row, col, num):
            board[row, col] = num
            if solve_sudoku(board):
                return True
            board[row, col] = 0
    return False

#Function find empty cell
def find_empty_cell(board):
    for row in range(9):
        for col in range(9):
            if board[row, col] == 0:
                return(row,col)
    return None

#create random unsolved sudoku board
def create_sudoku_board(difficulty):
    board = np.zeros((9, 9), dtype= int)
    solve_sudoku(board)

    if difficulty == "easy":
        num_initial_cells = 30 
    elif difficulty == "intermediate":
        num_initial_cells = 25
    elif difficulty == "hard":
        num_initial_cells = 20
    else:
        raise ValueError("Invalid difficulty level")

    #randomly remove cells to create the puzzle
    for _ in range(num_initial_cells):
        row, col = random.randint(0,8), random.randint(0, 8)
        while board[row, col] == 0:
            row, col = random.randint(0, 8), random.randint(0, 8)
        board[row, col] = 0

    return board

#display board
def display_board(board):
    st.write(board)