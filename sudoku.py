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

def display_board(board):
    cell_style = """
    <style>
    .sudoku-cell {
        font-size: 18px;
        padding: 8px;
        border: 1px solid #000;
        text-align: center;
        width: 60px;
        height: 60px;
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
    .sudoku-cell.empty {
        background-color: #ADD8E6; /* Light blue */
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

            if num != 0:
                cell_html = f'<div class="{border_classes}">{num}</div>'
            else:
                cell_html = f'<div class="{border_classes} empty">.</div>'
            row_html += cell_html
        row_html += '</div>'
        st.markdown(row_html, unsafe_allow_html=True)

def main():
    st.title("Sudoku Game")

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
    if 'row_input' not in st.session_state:
        st.session_state.row_input = None
    if 'col_input' not in st.session_state:
        st.session_state.col_input = None
    if 'num_input' not in st.session_state:
        st.session_state.num_input = None


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
        st.header("Welcome to the World of Sudoku!")
        st.write("""
        <div style="text-align: center; margin-bottom: 20px;">
            <h3>We are thrilled to have you here, ready to explore the intriguing and intellectually stimulating world of Sudoku.</h3>
        </div>
        <p style="text-align: justify; font-size: 18px;">
            This timeless logic-based puzzle has captivated minds around the globe, offering not just a fun challenge but also a way to enhance cognitive abilities.
        </p>
        <h3 style="margin-top: 30px;">What is Sudoku?</h3>
        <p style="text-align: justify; font-size: 18px;">
            Sudoku, at its core, is a combinatorial number-placement puzzle. The objective is simple yet profoundly engaging: to fill a 9×9 grid with digits so that each column, each row, and each of the nine 3×3 subgrids contain all of the digits from 1 to 9 without repeating. This elegant simplicity is what makes Sudoku accessible to beginners and endlessly fascinating to seasoned enthusiasts.
        </p>
        <h3 style="margin-top: 30px;">Why Sudoku?</h3>
        <ul style="font-size: 18px;">
            <li><strong>Mental Gymnastics:</strong> Each puzzle hones your logical reasoning and strategic thinking.</li>
            <li><strong>Memory Boost:</strong> Regularly solving Sudoku helps improve your memory and recall abilities.</li>
            <li><strong>Stress Relief:</strong> The focused concentration required can be a wonderful way to unwind and relax.</li>
            <li><strong>Universal Appeal:</strong> Sudoku transcends age and cultural barriers, making it a perfect pastime for everyone.</li>
        </ul>
        <p style="text-align: justify; font-size: 18px;">
            Whether you're looking to sharpen your mind, relax, or simply enjoy a fulfilling hobby, Sudoku offers all of that and more. We invite you to dive into this world of numbers and logic, where each puzzle presents a unique challenge and an opportunity to learn and grow.
        </p>
        <div style="text-align: center; margin-top: 30px;">
            <h3>Happy puzzling, and welcome to the Sudoku community!</h3>
        </div>
        """, unsafe_allow_html=True)


    # Instructions Page
    if st.session_state.page == "Instructions":
        st.header("Getting Started with Sudoku: Instructions and Tips")
        st.write("""
        <div style="margin-bottom: 30px;">
            <h2>Understanding the Basics</h2>
            <p style="text-align: justify; font-size: 18px;">
                A standard Sudoku puzzle consists of a 9×9 grid divided into nine 3×3 subgrids. The goal is to fill each cell with a digit from 1 to 9. However, there are three critical rules to follow:
            </p>
            <ul style="font-size: 18px;">
                <li><strong>Row Rule:</strong> Each row must contain the digits from 1 to 9 without repetition.</li>
                <li><strong>Column Rule:</strong> Each column must contain the digits from 1 to 9 without repetition.</li>
                <li><strong>Subgrid Rule:</strong> Each of the nine 3×3 subgrids must also contain the digits from 1 to 9 without repetition.</li>
            </ul>
        </div>

        <div style="margin-bottom: 30px;">
            <h2>Steps to Solve a Sudoku Puzzle</h2>
            <ol style="font-size: 18px;">
                <li><strong>Scan for Obvious Numbers:</strong> Start by filling in numbers that are clearly obvious. For instance, if a row, column, or subgrid is missing only one number, fill it in first.</li>
                <li><strong>Cross-Hatching:</strong> Use a method called cross-hatching, where you check rows and columns within each 3×3 subgrid to identify where a number should go.</li>
                <li><strong>Pencil In Possibilities:</strong> If you're unsure about certain cells, lightly pencil in possible numbers. This helps keep track of potential solutions without committing to a number prematurely.</li>
                <li><strong>Use Logical Deduction:</strong> As you fill in more numbers, use the process of elimination to narrow down the possibilities for the remaining cells.</li>
            </ol>
        </div>

        <div style="margin-bottom: 30px;">
            <h2>Advanced Strategies</h2>
            <ul style="font-size: 18px;">
                <li><strong>Naked Pairs/Triples:</strong> If two or three cells in a row, column, or subgrid can only contain the same set of two or three numbers, these numbers can be eliminated from other cells in that row, column, or subgrid.</li>
                <li><strong>Hidden Pairs/Triples:</strong> Similar to naked pairs/triples, but these numbers are hidden among other possibilities in the cells.</li>
                <li><strong>X-Wing Technique:</strong> A more advanced strategy used to eliminate possible numbers by identifying patterns in rows and columns.</li>
            </ul>
        </div>

        <div style="margin-bottom: 30px;">
            <h2>Tips for Success</h2>
            <ul style="font-size: 18px;">
                <li><strong>Be Patient:</strong> Take your time to think through each move.</li>
                <li><strong>Practice Regularly:</strong> Like any skill, the more you practice, the better you become.</li>
                <li><strong>Start Simple:</strong> Begin with easier puzzles and gradually move to more difficult ones.</li>
                <li><strong>Stay Organized:</strong> Keep track of your steps to avoid confusion, especially when using pencil marks for possibilities.</li>
            </ul>
        </div>

        <div style="text-align: center; margin-top: 20px;">
            <h4>By following these instructions and tips, you'll soon find yourself more confident and skilled in solving Sudoku puzzles. Remember, every puzzle has a solution, and the journey to find it is where the real fun and satisfaction lie.</h4>
            <h3>Happy solving!</h3>
        </div>
        """, unsafe_allow_html=True)


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
            display_board(st.session_state.board)
            st.write("</div>", unsafe_allow_html=True)

            # Form to update cell values
            with st.form(key='update_form'):
                row = int(st.number_input("Row (1-9)", min_value=1, max_value=9, step=1))
                col = int(st.number_input("Column (1-9)", min_value=1, max_value=9, step=1))
                num = st.number_input("Number (1-9)", min_value=1, max_value=9, step=1)
                update_button = st.form_submit_button("Update Cell")
                
                if update_button:
                    # Check if row and col are within the valid range (0 to 8 for a 9x9 board)
                    if 0 <= row - 1 < 9 and 0 <= col - 1 < 9:
                        if is_valid(st.session_state.board, row - 1, col - 1, num):
                            if st.session_state.board[row - 1][col - 1] == 0:
                                st.session_state.board[row - 1][col - 1] = num
                                st.session_state.moves.append((row - 1, col - 1))
                                st.write("Successfully inputted!")
                            else:
                                st.error("Cell is not editable.")
                        else:
                            st.error("Invalid input. Number already exists in the row, column, or box.")



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
