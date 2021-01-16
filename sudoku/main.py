from pickle import load, dump
from random import randint


FILENAME = 'game.pkl'

SIZE = 9
SQUARE = 3
EMPTY_LINE = [0] * SIZE
EMPTY_BOARD = [EMPTY_LINE for i in range(SIZE)]


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


class Board99:
    def __init__(self, numbers):
        self.numbers = numbers
        self.pickled = False

    def get_row_column_square(self, row, column):
        full_row = self.numbers[row]
        full_column = [self.numbers[i][column] for i in range(SIZE)]
        full_square = self.get_square33(row, column)
        return full_row, full_column, full_square

    def is_sell_valid(self, row, column):
        full_row, full_column, full_square = self.get_row_column_square(row, column)
        if is_line_valid(full_row) and is_line_valid(full_column) and is_line_valid(full_square):
            return True
        return False

    def get_square33(self, row, column):
        _, (x1, y1), (x2, y2) = determine_square(row, column)
        return [self.numbers[i][j]
                for i in range(x1, x2 + 1) for j in range(y1, y2+1)]

    def update_sell(self, row, column, new_number):
        old_numbers = self.numbers
        self.numbers[row][column] = new_number
        if self.is_sell_valid(row, column):
            return True
        self.numbers = old_numbers
        return False

    def get_sell(self, row, column):
        return self.numbers[row][column]

    def find_possible_sell_answers(self, row, column):
        cur_value = self.get_sell(row, column)
        if cur_value != 0:
            return cur_value
        full_row, full_column, full_square = self.get_row_column_square(row, column)
        possible_values = []
        for num in range(1, SIZE+1):
            if num not in full_row and num not in full_column and num not in full_square:
                possible_values.append(num)
        return possible_values if len(possible_values) > 0 else 0


    def toString(self):
        print()
        for i in range(SIZE):
            line = ''
            for j in range(SIZE):
                line += f'{self.numbers[i][j]}|'
            print(f'|{line}')
        print()

    def set_pickled(self, state):
        self.pickled = state


class Session:
    def __init__(self, numbers=EMPTY_BOARD):
        self.board = Board99(numbers)

    def export_from_pkl(self):
        if self.board.pickled == False:
            return -1
        with open(FILENAME, 'rb') as f:
            self.board = load(f)
        self.board.set_pickled(False)

    def import_to_pkl(self):
        self.board.set_pickled(True)
        with open(FILENAME, 'wb') as f:
            dump(self.board, f)

    def update_sell(self, row, column, number):
        pass

    def generate_board(self, to_fill=0):
        if to_fill == 0:
            return

        while to_fill > 0:
            row, column = randint(0, SIZE-1)
            if self.board.get_sell(row, column) != 0:
                to_fill += 1
            else:
                to_fill -= 1
                possible_values = self.board.find_possible_sell_answers(row, column)
                if possible_values == 0:
                    return -1
                else:
                    self.board.update_sell(possible_values[randint(0, len(possible_values)-1)])
    
