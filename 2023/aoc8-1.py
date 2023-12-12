from typing import Dict, List

FILENAME = "./aoc8.txt"

with open(FILENAME) as file:
    raw_data = [line.rstrip() for line in file]


class Node:
    left: str
    right: str

    def __init__(self, left: str, right: str):
        self.left = left
        self.right = right

    def __repr__(self):
        return f'[Node: Left: {self.left}, Right: {self.right}]'

class NodeMap:
    node_map: Dict[str, Node]
    instruction_pattern: List[str]
    starting_node: str

    def __init__(self, raw_value: List[str]):
        self.instruction_pattern = None
        self.starting_node = None
        self.node_map = {}

        for line in raw_value:
            if not self.instruction_pattern:
                self.instruction_pattern = list(raw_value[0])
                print(self.instruction_pattern)
                print('---')
                continue

            if not line:
                continue

            key = line.split(' = ')[0].strip()
            left = line.split(' = ')[1].strip().split(',')[0].strip('(')
            right = line.split(' = ')[1].strip().split(', ')[1].strip(')')

            self.node_map[key] = Node(left, right)

            print(f'key={key}, left={left}, right={right}')

    def find_node(self, start: str, destination: str) -> int:
        instruction_count = 0
        curr_node = start
        curr_instruction = self.instruction_pattern[instruction_count]
        iteration_count = 0
        trigger = False
        while curr_node != destination or not trigger:
            trigger = True
            iteration_count += 1
            # print('Curr node:', curr_node, 'Curr instruction', curr_instruction, 'Instruction count', instruction_count)
            if curr_instruction == 'L':
                curr_node = self.node_map[curr_node].left
            else:
                curr_node = self.node_map[curr_node].right

            instruction_count = (instruction_count + 1) % len(self.instruction_pattern)
            curr_instruction = self.instruction_pattern[instruction_count]

        return iteration_count






node_map = NodeMap(raw_data)
iterations = node_map.find_node('ZZZ', 'ZZZ')
print('Iterations:', iterations)