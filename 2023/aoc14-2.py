from collections import defaultdict
from typing import Set, Tuple, Dict, List

FILENAME = "./aoc14.txt"

with open(FILENAME) as file:
    raw_data = [line.rstrip() for line in file]


class Board:
    board: Dict[Tuple[int], str]
    original_rock_position_set: Set[Tuple[int]]
    hash_position_set: Set[Tuple[int]]

    hashes_by_column_dict: Dict[int, Set[Tuple[int]]]
    hashes_by_row_dict: Dict[int, Set[Tuple]]
    row_length: int
    col_length: int

    def __init__(self, raw_board: List[str]):
        self.initialize_board(raw_board)

    def initialize_board(self, raw_board: List[str]) -> None:
        row = 0
        self.original_rock_position_set = set()
        self.hash_position_set = set()
        self.hashes_by_column_dict = defaultdict(set)
        self.hashes_by_row_dict = defaultdict(set)
        self.board = {}
        for line in raw_board:
            col = 0
            for c in line:
                self.board[(row, col)] = c
                if c == 'O':
                    self.original_rock_position_set.add((row, col))

                if c == '#':
                    self.hash_position_set.add((row, col))
                    self.hashes_by_column_dict[col].add(row)
                    self.hashes_by_row_dict[row].add(col)

                col += 1

            row += 1

        self.row_length = row
        self.col_length = col

        # print(self.original_rock_position_set)
        # print(self.hash_position_set)
        # print(self.hashes_by_row_dict)
        # print(self.hashes_by_column_dict)

        NUM_CYCLES = 1000000000
        seen_boards = []
        for i in range(NUM_CYCLES):
            # self.print_board()
            self.tilt_north()
            # print(self.board)
            self.tilt_west()
            # print(self.board)
            self.tilt_south()
            # print(self.board)
            self.tilt_east()
            # print(self.board)
            rock_positions = self.get_rock_positions()
            if rock_positions in seen_boards:
                first_seen_pos = seen_boards.index(rock_positions)
                cycle_count = i - first_seen_pos

                remaining = (NUM_CYCLES - i - 1) % cycle_count
                for cnt in range(remaining):
                    self.tilt_north()
                    self.tilt_west()
                    self.tilt_south()
                    self.tilt_east()
                    # print('temp', self.get_score())

                print('Matching board')
                self.print_board()
                print('Cycle found', i, 'Cycle count', cycle_count, 'Processed', remaining)
                break
            seen_boards.append(rock_positions)


    def push_to_top(self, pos: Tuple[Set]) -> Tuple:
        new_pos = (pos[0] - 1, pos[1])
        if new_pos[0] < 0 or self.board[new_pos] == '#' or self.board[new_pos] == 'O':
            return pos

        while new_pos[0] != 0:
            if self.board[new_pos] == '#' or self.board[new_pos] == 'O':
                return new_pos[0] + 1, new_pos[1]

            new_pos = (new_pos[0] - 1, new_pos[1])

        if self.board[new_pos] == '#' or self.board[new_pos] == 'O':
            return new_pos[0] + 1, new_pos[1]

        return new_pos

    def push_to_bottom(self, pos: Tuple[Set]) -> Tuple:
        new_pos = (pos[0] + 1, pos[1])
        if new_pos[0] > self.row_length-1 or self.board[new_pos] == '#' or self.board[new_pos] == 'O':
            return pos

        while new_pos[0] < self.row_length-1:
            if self.board[new_pos] == '#' or self.board[new_pos] == 'O':
                return new_pos[0] - 1, new_pos[1]

            new_pos = (new_pos[0] + 1, new_pos[1])

        if self.board[new_pos] == '#' or self.board[new_pos] == 'O':
            return new_pos[0] - 1, new_pos[1]

        return new_pos

    def push_to_west(self, pos: Tuple[Set]) -> Tuple:
        new_pos = (pos[0], pos[1] - 1)
        if new_pos[1] < 0 or self.board[new_pos] == '#' or self.board[new_pos] == 'O':
            return pos

        while new_pos[1] != 0:
            if self.board[new_pos] == '#' or self.board[new_pos] == 'O':
                return new_pos[0], new_pos[1] + 1

            new_pos = (new_pos[0], new_pos[1] - 1)

        if self.board[new_pos] == '#' or self.board[new_pos] == 'O':
            return new_pos[0], new_pos[1] + 1

        return new_pos

    def push_to_east(self, pos: Tuple[Set]) -> Tuple:
        new_pos = (pos[0], pos[1] + 1)
        if new_pos[1] > self.row_length-1 or self.board[new_pos] == '#' or self.board[new_pos] == 'O':
            return pos

        while new_pos[1] < self.col_length-1:
            if self.board[new_pos] == '#' or self.board[new_pos] == 'O':
                return new_pos[0], new_pos[1] - 1

            new_pos = (new_pos[0], new_pos[1] + 1)

        if self.board[new_pos] == '#' or self.board[new_pos] == 'O':
            return new_pos[0], new_pos[1] - 1

        return new_pos

    def tilt_north(self):
        for r in range(self.row_length):
            for c in range(self.col_length):
                rock_pos = (r, c)
                if self.board[rock_pos] == 'O':
                    new_pos = self.push_to_top(rock_pos)
                    self.board[rock_pos] = '.'
                    self.board[new_pos] = 'O'


    def tilt_south(self):
        for r in range(self.row_length-1, -1, -1):
            for c in range(self.col_length):
                rock_pos = (r, c)
                if self.board[rock_pos] == 'O':
                    new_pos = self.push_to_bottom(rock_pos)
                    self.board[rock_pos] = '.'
                    self.board[new_pos] = 'O'


    def tilt_west(self):
        for r in range(self.row_length):
            for c in range(self.col_length):
                rock_pos = (r, c)
                if self.board[rock_pos] == 'O':
                    new_pos = self.push_to_west(rock_pos)
                    self.board[rock_pos] = '.'
                    self.board[new_pos] = 'O'


    def tilt_east(self):
        for r in range(self.row_length):
            for c in range(self.col_length-1, -1, -1):
                rock_pos = (r, c)
                if self.board[rock_pos] == 'O':
                    new_pos = self.push_to_east(rock_pos)
                    self.board[rock_pos] = '.'
                    self.board[new_pos] = 'O'


    def get_rock_positions(self) -> Set[Tuple[int]]:
        rock_set = set()
        for r in range(self.row_length):
            for c in range(self.col_length):
                rock_pos = (r, c)
                if self.board[rock_pos] == 'O':
                    rock_set.add(rock_pos)

        return rock_set

    def print_board(self):
        for r in range(self.row_length):
            s = ''
            for c in range(self.col_length):
                s += self.board[(r, c)]
            print(s)

    def get_score(self) -> int:
        score = 0
        for r in range(self.row_length):
            for c in range(self.col_length):
                rock_pos = (r, c)
                if self.board[rock_pos] == 'O':
                    score += self.row_length - r
                    print(f'{rock_pos} Score: {self.row_length - r}, Total: {score}')

        return score



board = Board(raw_data)
print('Score', board.get_score())