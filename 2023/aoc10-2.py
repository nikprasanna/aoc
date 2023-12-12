from typing import Tuple, Dict, List, Set

FILENAME = "./aoc10.txt"

with open(FILENAME) as file:
    raw_data = [line.rstrip() for line in file]


class Point:
    x: int
    y: int

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f'[Point X:{self.x}, Y:{self.y}]'

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class Board:
    board_map: Dict[Point, str]
    starting_point: Point

    def __init__(self, raw_board: List[str]):
        self.board_map = {}
        self.board_width = 0
        self.board_height = 0

        y = 0
        for line in raw_board:
            x = 0
            for c in line:
                point = Point(x, y)
                self.board_map[point] = c
                if c == 'S':
                    self.starting_point = point
                x += 1
            if not self.board_width:
                self.board_width = x
            y += 1

        if not self.board_height:
            self.board_height = y


        print(self.board_map)
        print(f'{self.board_height} x {self.board_width}')
        area = self.get_calculated_area()
        print(area)

    def get_calculated_area(self) -> int:
        visited_nodes = self.get_visited_nodes()
        area_flag = False
        total_area = 0

        for y in range(self.board_height):
            for x in range(self.board_width):
                curr_point = Point(x, y)
                curr_val = self.board_map[Point(x, y)]
                # print(curr_point, curr_val)
                if curr_val in '7|FS' and curr_point in visited_nodes:
                    area_flag = not area_flag

                if area_flag and not curr_point in visited_nodes:
                    total_area += 1

        return total_area

    def get_visited_nodes(self) -> Set[Point]:
        prev_point = self.starting_point
        curr_point = self.get_pipes_connected_to_start()[0]
        curr_item = self.board_map[curr_point]
        step_count = 1
        visited_nodes = [curr_point]

        while curr_item != 'S':
            step_count += 1
            next_pos = self.get_next_neighbor(prev_point, curr_point)
            prev_point = curr_point
            curr_point = next_pos
            curr_item = self.board_map[curr_point]
            visited_nodes.append(curr_point)

        return set(visited_nodes)


    def get_pipes_connected_to_start(self) -> Tuple[Point]:
        if self.starting_point.y - 1 > 0:
            top = self.board_map[Point(self.starting_point.x, self.starting_point.y - 1)]
        else:
            top = '.'

        bottom = self.board_map[Point(self.starting_point.x, self.starting_point.y + 1)]

        if self.starting_point.x - 1 > 0:
            left = self.board_map[Point(self.starting_point.x - 1, self.starting_point.y)]
        else:
            left = '.'

        right = self.board_map[Point(self.starting_point.x + 1, self.starting_point.y)]

        valid_pipes = []
        if top == 'F' or top == '7' or top == '|':
            valid_pipes.append(Point(self.starting_point.x, self.starting_point.y - 1))

        if bottom == 'L' or bottom == 'J' or bottom == '|':
            valid_pipes.append(Point(self.starting_point.x, self.starting_point.y + 1))

        if left == '-' or left == 'F' or left == 'L':
            valid_pipes.append(Point(self.starting_point.x - 1, self.starting_point.y))

        if right == '-' or right == '7' or right == 'J':
            valid_pipes.append(Point(self.starting_point.x + 1, self.starting_point.y))

        return valid_pipes[0], valid_pipes[1]

    def point_difference(self, point_1: Point, point_2: Point) -> Point:
        return Point(x=(point_2.x - point_1.x), y=(point_2.y - point_1.y))

    def get_next_neighbor(self, from_point: Point, to_point: Point) -> Point:
        curr_pipe = self.board_map[to_point]
        point_difference = self.point_difference(from_point, to_point)

        if curr_pipe == '|':
            # If came from top, go to bottom
            if point_difference.y > 0:
                return Point(to_point.x, to_point.y+1)

            # If came from bottom, go to top
            if point_difference.y < 0:
                return Point(to_point.x, to_point.y-1)

        if curr_pipe == '-':
            # If came from left, go to right
            if point_difference.x > 0:
                return Point(to_point.x + 1, to_point.y)

            # If came from right, go to left
            if point_difference.x < 0:
                return Point(to_point.x - 1, to_point.y)

        if curr_pipe == 'L':
            # If it came from the top, go right
            if point_difference.y > 0:
                return Point(to_point.x + 1, to_point.y)

            # If it came from the right, go top
            if point_difference.x < 0:
                return Point(to_point.x, to_point.y - 1)

        if curr_pipe == 'J':
            # If it came from the left, go top
            if point_difference.x > 0:
                return Point(to_point.x, to_point.y - 1)

            # If it came from the top, go left
            if point_difference.y > 0:
                return Point(to_point.x - 1, to_point.y)

        if curr_pipe == '7':
            # If it came from the left, go down
            if point_difference.x > 0:
                return Point(to_point.x, to_point.y + 1)

            # If it came from below, go left
            if point_difference.y < 0:
                return Point(to_point.x - 1, to_point.y)

        if curr_pipe == 'F':
            # If it came from below, go right
            if point_difference.y < 0:
                return Point(to_point.x + 1, to_point.y)

            # If it came from the right, go down
            if point_difference.x < 0:
                return Point(to_point.x, to_point.y + 1)

board = Board(raw_data)
