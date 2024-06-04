import streamlit as st
import numpy as np
import random
import time
import json

def is_valid(board, row=None, col=None, num=None):
    if row is not None and col is not None and num is not None:
        for i in range(9):
            if board[row][i] == num or board[i][col] == num:
                return False
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if board[start_row + i][start_col + j] == num:
                    return False
        return True
    else:
        for i in range(9):
            row_nums = [num for num in board[i] if num != 0]
            if len(row_nums) != len(set(row_nums)):
                return False
            col_nums = [board[j][i] for j in range(9) if board[j][i] != 0]
            if len(col_nums) != len(set(col_nums)):
                return False
        for i in range(0, 9, 3):
            for j in range(0, 9, 3):
                block = [board[x][y] for x in range(i, i+3) for y in range(j, j+3) if board[x][y] != 0]
                if len(block) != len(set(block)):
                    return False
        return True

def solve_sudoku(board):
    empty = find_empty(board)
    if not empty:
        return True
    row, col = empty
    for num in range(1, 10):
        if is_valid(board, row, col, num):
            board[row][col] = num
            if solve_sudoku(board):
                return True
            board[row][col] = 0
    return False

def find_empty(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return (i, j)
    return None

def generate_sudoku(difficulty='easy'):
    base = 3
    side = base * base

    def pattern(r, c):
        return (base * (r % base) + r // base + c) % side

    def shuffle(s):
        return random.sample(s, len(s))

    rBase = range(base)
    rows = [g * base + r for g in shuffle(rBase) for r in shuffle(rBase)]
    cols = [g * base + c for g in shuffle(rBase) for c in shuffle(rBase)]
    nums = shuffle(range(1, base * base + 1))

    board = [[nums[pattern(r, c)] for c in cols] for r in rows]

    squares = side * side
    if difficulty == 'easy':
        empties = squares * 3 // 10
    elif difficulty == 'medium':
        empties = squares * 4 // 10
    elif difficulty == 'hard':
        empties = squares * 5 // 10
    else:
        empties = squares * 3 // 10

    for p in random.sample(range(squares), empties):
        board[p // side][p % side] = 0

    return board

def display_board(board, editable=False):
    cell_style = """
    <style>
    .sudoku-cell {
        font-size: 18px;
        padding: 8px;
        border: 1px solid #000;
        text-align: center;
        width: 70px;
        height: 70px;
        box-sizing: border-box;
    }
    .sudoku-cell input {
        font-size: 18px;
        text-align: center;
        padding: 0;
        margin: 0;
        height: 100%;
        box-sizing: border-box;
    }
    .sudoku-row {
        display: flex;
    }
    .thick-border-left {
        border-left: 2px solid #000;
    }
    .thick-border-right {
        border-right: 2px solid #000;
    }
    .thick-border-top {
        border-top: 2px solid #000;
    }
    .thick-border-bottom {
        border-bottom: 2px solid #000;
    }
    </style>
    """
    st.write(cell_style, unsafe_allow_html=True)

    for i, row in enumerate(board):
        row_html = '<div class="sudoku-row">'
        for j, num in enumerate(row):
            border_classes = "sudoku-cell"
            if j % 3 == 2 and j != 8:
                border_classes += " thick-border-right"
            if i % 3 == 2 and i != 8:
                border_classes += " thick-border-bottom"
            if j % 3 == 0 and j != 0:
                border_classes += " thick-border-left"
            if i % 3 == 0 and i != 0:
                border_classes += " thick-border-top"

            if editable and num == 0:
                cell_html = f'<input type="number" class="{border_classes}" min="0" max="9" style="width:70px;height:70px;text-align:center;" key="{i},{j}">'
            else:
                if num != 0:
                    cell_html = f'<div class="{border_classes}">{num}</div>'
                else:
                    cell_html = f'<div class="{border_classes}">.</div>'
            row_html += cell_html
        row_html += '</div>'
        st.markdown(row_html, unsafe_allow_html=True)
def main():
    st.title("Sudoku Game with Streamlit")

    # Initialize session state variables
    if 'page' not in st.session_state:
        st.session_state.page = "Welcome"
    if 'board' not in st.session_state:
        st.session_state.board = None
    if 'solution' not in st.session_state:
        st.session_state.solution = None
    if 'start_time' not in st.session_state:
        st.session_state.start_time = None
    if 'moves' not in st.session_state:
        st.session_state.moves = []

    # Sidebar for navigation
    with st.sidebar:
        if st.button("Welcome"):
            st.session_state.page = "Welcome"
        if st.button("Instructions"):
            st.session_state.page = "Instructions"
        if st.button("Start Game"):
            st.session_state.page = "Start Game"

    # Welcome Page
    if st.session_state.page == "Welcome":
        st.header("Welcome to Sudoku!")
        st.write("""
        Sudoku is a logic-based, combinatorial number-placement puzzle. The objective is to fill a 9×9 grid with digits so that each column, each row, and each of the nine 3×3 subgrids that compose the grid contain all of the digits from 1 to 9.
        Enjoy solving Sudoku puzzles and enhance your problem-solving skills!
        """)

    # Instructions Page
    elif st.session_state.page == "Instructions":
        st.header("How to Play Sudoku")
        st.write("""
        1. Each row must contain the numbers from 1 to 9, without repetitions.
        2. Each column must contain the numbers from 1 to 9, without repetitions.
        3. Each of the nine 3x3 subgrids must contain the numbers from 1 to 9, without repetitions.
        4. Use logic and reasoning to fill in the missing numbers on the grid.
        5. Good luck and have fun!
        """)

    # Start Game Page
    elif st.session_state.page == "Start Game":
        with st.sidebar:
            difficulty = st.selectbox("Select Difficulty", ["easy", "medium", "hard"])
            if st.button("Generate Sudoku"):
                st.session_state.board = generate_sudoku(difficulty)
                st.session_state.solution = None
                st.session_state.start_time = time.time()
                st.session_state.moves = []

            if st.session_state.board is not None:
                if st.button("Solve Sudoku"):
                    st.session_state.solution = np.array(st.session_state.board)
                    solve_sudoku(st.session_state.solution)

                if st.button("Submit"):
                    board = st.session_state.board
                    if all(all(row) for row in board):
                        if is_valid(board):
                            st.success("Congratulations! You solved the Sudoku.")
                        else:
                            st.error("There are mistakes in your solution.")
                    else:
                        st.error("The board is not completely filled.")

                if st.button("Undo"):
                    if st.session_state.moves:
                        last_move = st.session_state.moves.pop()
                        st.session_state.board[last_move[0]][last_move[1]] = 0

                if st.button("Save Game"):
                    game_state = {
                        'board': st.session_state.board,
                        'start_time': st.session_state.start_time,
                        'moves': st.session_state.moves
                    }
                    st.download_button("Download Game", data=json.dumps(game_state), file_name="sudoku_game.json", mime="application/json")

                uploaded_file = st.file_uploader("Load Game", type=["json"])
                if uploaded_file:
                    game_state = json.load(uploaded_file)
                    st.session_state.board = game_state['board']
                    st.session_state.start_time = game_state['start_time']
                    st.session_state.moves = game_state['moves']

        if st.session_state.board is not None:
            st.write("<div style='margin: 0 auto; width: max-content;'>", unsafe_allow_html=True)
            display_board(st.session_state.board, editable=True)
            st.write("</div>", unsafe_allow_html=True)

            if st.session_state.solution is not None:
                st.write("Solved Sudoku Board:")
                st.write("<div style='margin: 0 auto; width: max-content;'>", unsafe_allow_html=True)
                display_board(st.session_state.solution)
                st.write("</div>", unsafe_allow_html=True)
        
        if st.session_state.start_time:
            elapsed_time = time.time() - st.session_state.start_time
            st.write(f"Elapsed Time: {elapsed_time:.2f} seconds")

if __name__ == "__main__":
    main()
