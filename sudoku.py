import streamlit as st
import numpy as np
import time
import random

# Function to check if the move is possible/valid or not
def is_valid_move(board, row, col, num):
    # Check if the number already in the row
    if num in board[row, :]:
        return False
    # Check if the number already in the column
    if num in board[:, col]:
        return False
    
    subgrid_row = 3 * (row // 3)
    subgrid_col = 3 * (col // 3)
    # Check if the number in the 3x3 grid it's inserting in
    if num in board[subgrid_row:subgrid_row + 3, subgrid_col:subgrid_col + 3]:
        return False
    
    return True

# Function to solve the Sudoku
def solve_sudoku(board):
    empty_cell = find_empty_cell(board)
    if not empty_cell:
        return True
    
    row, col = empty_cell
    for num in range(1, 10):
        if is_valid_move(board, row, col, num):
            board[row, col] = num
            if solve_sudoku(board):
                return True
            board[row, col] = 0
    return False

# Function to find empty cell
def find_empty_cell(board):
    for row in range(9):
        for col in range(9):
            if board[row, col] == 0:
                return (row, col)
    return None

# Create random unsolved Sudoku board
def create_sudoku_board(difficulty):
    board = np.zeros((9, 9), dtype=int)
    solve_sudoku(board)

    if difficulty == "Easy":
        num_initial_cells = 30 
    elif difficulty == "Medium":
        num_initial_cells = 25
    elif difficulty == "Hard":
        num_initial_cells = 20
    else:
        raise ValueError("Invalid difficulty level")

    # Randomly remove cells to create the puzzle
    removed_cells = 81 - num_initial_cells
    for _ in range(removed_cells):
        row, col = random.randint(0, 8), random.randint(0, 8)
        while board[row, col] == 0:
            row, col = random.randint(0, 8), random.randint(0, 8)
        board[row, col] = 0

    return board

# Display board
def display_board(board):
    st.write(board)

# Function to display the instructions
def display_instructions():
    st.write("Welcome to Sudoku!")
    st.write("The goal of Sudoku is to fill in a 9x9 grid with digits so that each column, row, and 3x3 section contain the numbers between 1 to 9.")
    st.write("To play the game, you need to fill in the empty cells with numbers from 1 to 9.")
    st.write("Make sure that each row, column, and 3x3 subgrid contain each digit exactly once.")
    st.write("You can't change the initial numbers provided in the puzzle. Good luck!")

# Function to display completion message and time taken
def display_completion_message(start_time):
    st.write("Congratulations! You have completed the Sudoku Puzzle.")
    elapsed_time = time.time() - start_time
    st.write("Time taken:", "{:.2f} seconds".format(elapsed_time))

# Main function to run the game
def main():
    st.title("Sudoku Game")

    # Display instructions for beginners
    display_instructions()

    # Select difficulty level
    difficulty = st.selectbox("Select Difficulty Level:", ["Easy", "Medium", "Hard"])

    # Create a Sudoku board
    board = create_sudoku_board(difficulty)

    # Display the Sudoku board
    display_board(board)

    # Start timer
    start_time = time.time()

    # Solve Sudoku automatically when AI solve button is clicked 
    if st.button("AI Solve"):
        solve_sudoku(board)
        display_board(board)
        display_completion_message(start_time)

if __name__ == "__main__":
    main()
