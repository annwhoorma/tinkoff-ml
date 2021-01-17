from pickle import load, dump
from random import randint
from time import sleep


# name of the file in which the game will be stored when a user pauses it
FILENAME = 'game.pkl'

# size of the board
SIZE = 9
SQUARE = 3

# a word to save the game and resume later
STOPWORD = 'pause'

# create an empty board
EMPTY_BOARD = [0] * SIZE
for i in range(SIZE):
    EMPTY_BOARD[i] = [0] * SIZE

# returns yes if line of length SIZE is valid (3x3 square can be represented as a line)


def is_line_valid(line):
    for i in range(SIZE):
        for j in range(i + 1, SIZE):
            if line[i] == 0 or line[j] == 0:
                continue
            if line[i] == line[j]:
                return False
    return True

# the only function that was left with "magic numbers" :c
# returns the index and the coordinates of the 3x3 square (upper left and bottom right)


def determine_square(r, c):
    if (0 <= r <= 2):
        if (0 <= c <= 2):
            return 0, (0, 0), (2, 2)
        if (3 <= c <= 5):
            return 1, (0, 3), (2, 5)
        if (6 <= c <= 8):
            return 2, (0, 6), (2, 8)
    if (3 <= r <= 5):
        if (0 <= c <= 2):
            return 3, (3, 0), (5, 2)
        if (3 <= c <= 5):
            return 4, (3, 3), (5, 5)
        if (6 <= c <= 8):
            return 5, (3, 6), (5, 8)
    if (6 <= r <= 8):
        if (0 <= c <= 2):
            return 6, (6, 0), (8, 2)
        if (3 <= c <= 5):
            return 7, (6, 3), (8, 5)
        if (6 <= c <= 8):
            return 8, (6, 6), (8, 8)
    else:
        return -1

# throws an error with given text


def throw_error(text):
    print(f'ERROR: {text}')

# checks if the user input is valid


def check_input_boundaries(row, column, number):
    if 0 <= row and row < SIZE and 0 <= column and column < SIZE and 0 < number and number <= SIZE:
        return True
    return False


class Board99:
    def __init__(self, numbers):
        self.numbers = numbers

    # returns row, column and square to which the given cell belongs
    def get_row_column_square(self, row, column):
        full_row = self.numbers[row]
        full_column = [self.numbers[i][column] for i in range(SIZE)]
        full_square = self.get_square33(row, column)
        return full_row, full_column, full_square

    # decides if the cell is valid
    def is_cell_valid(self, row, column):
        full_row, full_column, full_square = self.get_row_column_square(
            row, column)
        if is_line_valid(full_row) and is_line_valid(full_column) and is_line_valid(full_square):
            return True
        return False

    # represents the square, to which the cell belongs, as a list
    def get_square33(self, row, column):
        _, (x1, y1), (x2, y2) = determine_square(row, column)
        return [self.numbers[i][j]
                for i in range(x1, x2 + 1) for j in range(y1, y2+1)]

    # updates the cell if the new_number is valid, validity checker can be disabled
    def update_cell(self, row, column, new_number, validity_check=True):
        old_number = self.numbers[row][column]
        self.numbers[row][column] = new_number
        if validity_check:
            if self.is_cell_valid(row, column):
                return True
            self.numbers[row][column] = old_number
            return False

    # returns the number in the cell
    def get_cell(self, row, column):
        return self.numbers[row][column]

    # returns a list of possible numbers that can be in the cell
    # returns 0 if there are no possible numbers for this cell
    def find_possible_cell_answers(self, row, column):
        cur_value = self.get_cell(row, column)
        if cur_value != 0:
            return cur_value
        full_row, full_column, full_square = self.get_row_column_square(
            row, column)
        possible_values = []
        for num in range(1, SIZE+1):
            if num not in full_row and num not in full_column and num not in full_square:
                possible_values.append(num)
        return possible_values if len(possible_values) > 0 else 0

    # prints the board
    def to_string(self):
        print()
        for i in range(SIZE):
            line = ''
            for j in range(SIZE):
                line += f'{self.numbers[i][j]}|'
            print(f'|{line}')
        print()

    # finds the first empty cell
    def find_unfilled_cell(self):
        for i in range(0, SIZE):
            for j in range(0, SIZE):
                if self.numbers[i][j] == 0:
                    # return the first empty cell
                    return i, j
        # no empty cells found
        return -1, -1

    # backtracking algorithm to solve sudoku
    def solve(self):
        # find one empty cell
        row, column = self.find_unfilled_cell()
        if row == -1 and column == -1:
            # if no empty cells found, the game is solved
            return True

        for number in (1, SIZE + 1):
            # try each possible number
            # save the number that was in this cell before
            old_number = self.get_cell(row, column)
            # if this cell can hold the new number:
            if(self.update_cell(row, column, number)):
                # print the move and the new board
                print(f'move: row-{row} column-{column} number-{number}')
                self.to_string()
                if self.solve():
                    # continue this branch of solving until False is returned or the game is over
                    return True
                else:
                    # update this cell to its old number and continue iterating
                    self.update_cell(row, column, old_number,
                                     validity_check=False)
        # if all possible numbers were tried and the solution wasn't found then return False
        return False


# a class to represent the user's session
class Session:
    def __init__(self, numbers=EMPTY_BOARD):
        self.board = Board99(numbers)

    # start the session: generate a new board with a given number of filled cells
    def start_session(self):
        to_fill = int(input('just give me the number of cells to fill: '))
        self.generate_board(to_fill)
        self.board.to_string()

    # make a move and give an error if it's not possible
    def make_move(self, row, column, number):
        if not self.board.update_cell(row, column, number, validity_check=True):
            throw_error(
                'not a valid number for this cell; the board didnt change: ')

    # import from .pkl file if possible
    def import_from_pkl(self):
        try:
            with open(FILENAME, 'rb') as f:
                self.board = load(f)
        except FileNotFoundError:
            print('shit2')
            return -1

        with open(FILENAME, 'rb') as f:
            self.board = load(f)

    # export to .pkl file
    def export_to_pkl(self):
        with open(FILENAME, 'wb') as f:
            dump(self.board, f)

    # generate a board with valid numbers, leaves the board empty by default
    def generate_board(self, to_fill=0):
        if to_fill == 0:
            return

        while to_fill > 0:
            row, column = randint(0, SIZE-1), randint(0, SIZE-1)
            if self.board.get_cell(row, column) != 0:
                continue
            else:
                to_fill -= 1
                possible_values = self.board.find_possible_cell_answers(
                    row, column)
                if possible_values == 0:
                    return -1
                else:
                    self.board.update_cell(row, column, possible_values[randint(
                        0, len(possible_values)-1)], validity_check=False)
        print('the board has been generated :)')


def main():
    session = Session()
    print("""for each move, type: <row> <column> <number>. each of them is a number between 1 and 9 \nif you want to take a break, type 'pause' and the game will stop until you decide to resume it later""")

    answer = input("\noh wait, do you have a game to resume? [y/n] ")
    if answer == 'y':
        if session.import_from_pkl() == -1:
            print('nope, you have no game to resume, you may start a new one')

        print('cool, you may continue :) just to remind you where you were: ')
        session.board.to_string()
    elif answer == 'n':
        print('okay, starting a new one')
        session.start_session()
        session.generate_board()
    else:
        throw_error('wrong answer, come back later')
        return

    print('now, start typing in your moves')
    while(True):
        inp = input("your move: ")
        if inp == STOPWORD:
            session.export_to_pkl()
            print('yup, saved it :) resume the game whenever you want')
            break
        row, column, number = inp.split(' ')
        row, column, number = int(row), int(column), int(number)
        row, column = row - 1, column - 1
        if check_input_boundaries(row, column, number):
            session.make_move(row, column, number)
            session.board.to_string()


main()
