from typing import List, Tuple, Dict

FILENAME = "./aoc3.txt"

with open(FILENAME) as file:
    raw_data = [line.rstrip() for line in file]


class EngineSchematic:
    rows: List[str]
    number_map: List[Dict[Tuple, str]]
    symbol_map: List[Dict[int, str]]

    def __init__(self, rows: List[str]):
        self.rows = rows
        self.number_map = []
        self.symbol_map = []

        for curr_row_index in range(len(rows)):
            self.number_map.append(self.populate_number_map(rows[curr_row_index]))

        for curr_row_index in range(len(rows)):
            self.symbol_map.append(self.populate_symbol_map(rows[curr_row_index]))

    def get_valid_sum(self) -> int:
        valid_sum = 0
        for row in range(len(self.number_map)):
            number_row = self.number_map[row]
            for start_end, num in number_row.items():
                if self.has_adjacent_gear(start_end[0], start_end[1], row):
                    valid_sum += int(num)
                    print(int(num))

        return valid_sum

    def build_gear_map(self) -> Dict[Tuple, List[int]]:
        gear_map = {}
        for symbol_row_index in range(len(self.symbol_map)):
            symbol_row = self.symbol_map[symbol_row_index]
            for pos in symbol_row.keys():
                gear_map[(symbol_row_index, pos)] = []

        for row, col in gear_map:
            gear_map[(row, col)] = self.get_adjacent_numbers(row, col)

        return gear_map

    def get_gear_ratio(self) -> int:
        gear_map = self.build_gear_map()
        ratio_sum = 0
        for pos, nums in gear_map.items():
            if len(nums) == 2:
                ratio_sum += int(nums[0]) * int(nums[1])

        return ratio_sum

    def get_adjacent_numbers(self, row: int, col: int) -> List[int]:
        number_row = self.number_map[row]
        adjacent_numbers = []

        # Check left
        for num_pos, num_val in number_row.items():
            if num_pos[0] <= col-1 < num_pos[1]:
                adjacent_numbers.append(num_val)

        # Check right
        for num_pos, num_val in number_row.items():
            if num_pos[0] <= col+1 < num_pos[1]:
                adjacent_numbers.append(num_val)

        # Check top
        if row-1 >= 0:
            number_row = self.number_map[row-1]
            for num_pos, num_val in number_row.items():
                if num_pos[0]-1 <= col < num_pos[1]+1:
                    adjacent_numbers.append(num_val)

        # Check bottom
        if row+1 < len(self.number_map):
            number_row = self.number_map[row+1]
            for num_pos, num_val in number_row.items():
                if num_pos[0]-1 <= col < num_pos[1]+1:
                    adjacent_numbers.append(num_val)

        return adjacent_numbers

    def populate_number_map(self, row: str) -> Dict[Tuple, int]:
        curr_num = ''
        start_index = -1
        row_map = {}

        for i in range(len(row)):
            c = row[i]
            if c.isnumeric():
                curr_num += c
                if start_index == -1:
                    start_index = i
            else:
                if curr_num:
                    row_map[(start_index, i)] = curr_num

                curr_num = ''
                start_index = -1

        if curr_num:
            row_map[(start_index, i+1)] = curr_num

        return row_map

    def populate_symbol_map(self, row: str):
        row_map = {}

        for i in range(len(row)):
            c = row[i]
            if c == '*':
                row_map[i] = c

        return row_map


# for row in raw_data:
#     print(row)
# print('---')

schematic = EngineSchematic(raw_data)
from pprint import pprint
# print(schematic.number_map)
# print(schematic.symbol_map)

print(schematic.get_gear_ratio())
# print('Sum:', schematic.build_gear_map())