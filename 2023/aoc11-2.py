from typing import List, Tuple, Dict, Set

FILENAME = "./aoc11.txt"
EXPANSION_COUNT = 1000000 - 1

with open(FILENAME) as file:
    raw_data = [line.rstrip() for line in file]

class Image:
    expanded_board: List[str]
    galaxy_positions: Set[Tuple[int]]

    def __init__(self, raw_board: List[str]):
        self.expanded_board = raw_board
        self.galaxy_positions = self.get_galaxy_positions()

        self.expand_rows = self.get_expand_rows(raw_board)
        self.expand_cols = self.get_expand_cols(raw_board)
        print('Empty rows', self.expand_rows)
        print('Empty cols', self.expand_cols)
        print('Path sum', self.get_path_sum())

    def get_path_sum(self) -> int:
        path_sum = 0
        eligible_pairs = set()
        for position in self.galaxy_positions:
            for sub_position in [x for x in self.galaxy_positions if x != position]:
                if not (sub_position, position) in eligible_pairs:
                    eligible_pairs.add((position, sub_position))

        # print('Eligible pairs', eligible_pairs)

        for eligible_pair in eligible_pairs:
            path_sum += self.get_distance(eligible_pair[0], eligible_pair[1])

        return path_sum

    def get_galaxy_positions(self) -> Set[Tuple[int]]:
        galaxy_positions = set()
        for row_pos in range(len(self.expanded_board)):
            row = self.expanded_board[row_pos]
            for col_pos in range(len(row)):
                c = row[col_pos]
                if c == '#':
                    galaxy_positions.add((row_pos, col_pos))

        return galaxy_positions

    def slice_column(self, l: List[str], col: int):
        slice = ''
        for val in l:
            slice += val[col]

        return slice

    def get_distance(self, point_1: Tuple[int], point_2: Tuple[int]) -> int:
        row_distance = point_1[0] - point_2[0]
        col_distance = point_1[1] - point_2[1]

        if row_distance <= 0:
            top_point = point_1[0]
        else:
            top_point = point_2[0]

        if col_distance <= 0:
            left_point = point_1[1]
        else:
            left_point = point_2[1]

        row_cross = sum([1 for x in range(top_point, top_point+abs(row_distance)) if x in self.expand_rows])
        col_cross = sum([1 for x in range(left_point, left_point+abs(col_distance)) if x in self.expand_cols])

        return abs(row_distance) + abs(col_distance) + EXPANSION_COUNT*row_cross + EXPANSION_COUNT*col_cross

    def get_expand_rows(self, raw_board: List[str]) -> Set[int]:
        expand_rows = set()
        row_cnt = 0
        for row in raw_board:
            if all([c == '.' for c in row]):
                expand_rows.add(row_cnt)
            row_cnt += 1

        return expand_rows

    def get_expand_cols(self, raw_board: List[str]) -> Set[int]:
        expand_cols = set()
        for i in range(len(raw_board[0])):
            col = self.slice_column(raw_board, i)
            if all([c == '.' for c in col]):
                expand_cols.add(i)

        return expand_cols


    def expand_board(self, raw_board: List[str]) -> List[str]:
        expand_rows = []
        curr_pos = 0
        new_row = ''
        for row in raw_board:
            if all([c == '.' for c in row]):
                if not new_row:
                    new_row = row
                expand_rows.append(curr_pos)
            curr_pos += 1

        expand_cols = []
        for i in range(len(raw_board[0])):
            col = self.slice_column(raw_board, i)
            if all([c == '.' for c in col]):
                expand_cols.append(i)

        # print(expand_cols)
        # print(expand_rows)

        expanded_board = raw_board
        while expand_rows:
            row = expand_rows.pop(0)
            expanded_board.insert(row, new_row)

            new_expand_rows = expand_rows
            temp_expand_rows = []

            while new_expand_rows:
                val = new_expand_rows.pop()
                if val > row:
                    val = val + 1

                temp_expand_rows.append(val)

            expand_rows = temp_expand_rows

        while expand_cols:
            col = expand_cols.pop(0)
            for i in range(len(expanded_board)):
                row = expanded_board[i]
                new_row = list(row)
                new_row.insert(col, '.')
                expanded_board[i] = ''.join(new_row)

            new_expand_cols = expand_cols
            temp_expand_cols = []

            while new_expand_cols:
                val = new_expand_cols.pop() + 1
                temp_expand_cols.append(val)

            expand_cols = temp_expand_cols


        for row in expanded_board:
            print(row)

        return expanded_board


# for row in raw_data:
#     print(row)

image = Image(raw_data)