from pickle import load, dump
from random import randint
from time import sleep


TO_FILL = 40

FILENAME = 'game.pkl'

SIZE = 9
SQUARE = 3

STOPWORD = 'pause'

EMPTY_BOARD = [0] * SIZE
for i in range(SIZE):
    EMPTY_BOARD[i] = [0] * SIZE


def is_line_valid(line):
    for i in range(SIZE):
        for j in range(i + 1, SIZE):
            if line[i] == 0 or line[j] == 0:
                continue
            if line[i] == line[j]:
                return False
    return True


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


def throw_error(text):
    print(f'ERROR: {text}')


def check_input_boundaries(row, column, number):
    if 0 <= row and row < SIZE and 0 <= column and column < SIZE and 0 < number and number <= SIZE:
        return True
    return False


class Board99:
    def __init__(self, numbers):
        self.numbers = numbers
        self.pickled = False

    def get_row_column_square(self, row, column):
        full_row = self.numbers[row]
        full_column = [self.numbers[i][column] for i in range(SIZE)]
        full_square = self.get_square33(row, column)
        return full_row, full_column, full_square

    def is_cell_valid(self, row, column):
        full_row, full_column, full_square = self.get_row_column_square(
            row, column)
        if is_line_valid(full_row) and is_line_valid(full_column) and is_line_valid(full_square):
            return True
        return False

    def get_square33(self, row, column):
        _, (x1, y1), (x2, y2) = determine_square(row, column)
        return [self.numbers[i][j]
                for i in range(x1, x2 + 1) for j in range(y1, y2+1)]

    def update_cell(self, row, column, new_number, validity_check=True):
        old_number = self.numbers[row][column]
        self.numbers[row][column] = new_number
        if validity_check:
            if self.is_cell_valid(row, column):
                return True
            self.numbers[row][column] = old_number
            return False

    def get_cell(self, row, column):
        return self.numbers[row][column]

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

    def to_string(self):
        print()
        for i in range(SIZE):
            line = ''
            for j in range(SIZE):
                line += f'{self.numbers[i][j]}|'
            print(f'|{line}')
        print()


class Session:
    def __init__(self, numbers=EMPTY_BOARD):
        self.board = Board99(numbers)

    def start_session(self):
        to_fill = int(input('just give me the number of cells to fill: '))
        # to_fill = TO_FILL
        self.generate_board(to_fill)
        self.board.to_string()

    def make_move(self, row, column, number):
        if not self.board.update_cell(row, column, number, validity_check=True):
            throw_error('not a valid number for this cell; the board didnt change: ')

    def import_from_pkl(self):
        try:
            with open(FILENAME, 'rb') as f:
                self.board = load(f)
        except FileNotFoundError:
            print('shit2')
            return -1

        with open(FILENAME, 'rb') as f:
            self.board = load(f)

    def export_to_pkl(self):
        with open(FILENAME, 'wb') as f:
            dump(self.board, f)

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
