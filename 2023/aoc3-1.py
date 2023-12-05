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
                if self.has_adjacent_symbol(start_end[0], start_end[1], row):
                    valid_sum += int(num)
                    print(int(num))

        return valid_sum

    def has_adjacent_symbol(self, start: int, end: int, row: int) -> bool:
        # print('Row:', row, 'Number map', self.number_map[row], 'Symbol map:', self.symbol_map[row])
        found = False
        symbol_row = self.symbol_map[row]

        # Check left
        if symbol_row.get(start-1):
            found = True

        # Check right
        if symbol_row.get(end):
            found = True

        # Check top
        if row-1 >= 0:
            symbol_row = self.symbol_map[row-1]
            for i in range(start-1, end+1):
                if symbol_row.get(i):
                    found = True

        # Check bottom
        if row+1 < len(self.symbol_map):
            symbol_row = self.symbol_map[row+1]
            for i in range(start-1, end+1):
                if symbol_row.get(i):
                    found = True

        return found

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
            if not c.isnumeric() and not c == '.':
                row_map[i] = c

        return row_map


# for row in raw_data:
#     print(row)
# print('---')

schematic = EngineSchematic(raw_data)
from pprint import pprint
print(schematic.number_map)
print(schematic.symbol_map)

print('Sum:', schematic.get_valid_sum())