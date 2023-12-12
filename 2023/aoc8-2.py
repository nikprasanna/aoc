import math
from functools import reduce
from typing import Dict, List

FILENAME = "./aoc8.txt"

with open(FILENAME) as file:
    raw_data = [line.rstrip() for line in file]


def lcm(arr):
    l = reduce(lambda x, y: (x * y) // math.gcd(x, y), arr)
    return l


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

        curr_nodes = set()
        for key in self.node_map.keys():
            if key.endswith(start):
                curr_nodes.add(key)
        # print(curr_nodes)
        # curr_nodes.pop()
        # curr_nodes.pop()
        # curr_nodes.pop()
        # curr_nodes.pop()
        # curr_nodes.pop()
        # curr_nodes = ['QVZ']
        # print('Start:', curr_nodes)

        total_iteration_count = {}
        new_nodes = []
        for curr_node in curr_nodes:
            instruction_count = 0
            node = curr_node
            start_node = curr_node
            curr_instruction = self.instruction_pattern[instruction_count]
            iteration_count = 0
            while not node.endswith(destination):
                iteration_count += 1
                # print('Curr node:', curr_node, 'Curr instruction', curr_instruction, 'Instruction count', instruction_count)
                if curr_instruction == 'L':
                    node = self.node_map[node].left
                else:
                    node = self.node_map[node].right

                instruction_count = (instruction_count + 1) % len(self.instruction_pattern)
                curr_instruction = self.instruction_pattern[instruction_count]

            total_iteration_count[node] = iteration_count
            print('Iteration count:', start_node, node, iteration_count)
            new_nodes.append(node)

        # for curr_node in new_nodes:
        #     instruction_count = 0
        #     node = curr_node
        #     start_node = curr_node
        #     curr_instruction = self.instruction_pattern[instruction_count]
        #     iteration_count = 0
        #     trigger = False
        #     while not (node.endswith(destination) and trigger):
        #         trigger = True
        #         iteration_count += 1
        #         # print('Curr node:', curr_node, 'Curr instruction', curr_instruction, 'Instruction count', instruction_count)
        #         if curr_instruction == 'L':
        #             node = self.node_map[node].left
        #         else:
        #             node = self.node_map[node].right
        #
        #         instruction_count = (instruction_count + 1) % len(self.instruction_pattern)
        #         curr_instruction = self.instruction_pattern[instruction_count]
        #
        #     total_iteration_count[node] += iteration_count
        #     print('Iteration count:', start_node, node, iteration_count)

        # iteration_count = 0
        # while not all([curr_node.endswith(destination) for curr_node in curr_nodes]):
        #     # Iterate all start_nodes once
        #     new_nodes = set()
        #     curr_instruction = self.instruction_pattern[instruction_count]
        #     for curr_node in curr_nodes:
        #         if curr_instruction == 'L':
        #             new_nodes.add(self.node_map[curr_node].left)
        #         else:
        #             new_nodes.add(self.node_map[curr_node].right)
        #     curr_nodes = new_nodes
        #     # print(f'Instruction count: {instruction_count}')
        #     # print(f'Curr nodes: {curr_nodes}')
        #     instruction_count = (instruction_count + 1) % len(self.instruction_pattern)
        #     iteration_count += 1
        #
        # print(f'Final Instruction count: {instruction_count}')
        # print(f'Final Curr nodes: {curr_nodes}')

        lcm_iterations = lcm(total_iteration_count.values())

        return lcm_iterations

        # final_nodes = set()
        # for start_node in start_nodes:
        #     curr_node = start_node
        #     curr_instruction = self.instruction_pattern[instruction_count]
        #     iteration_count = 0
        #     while curr_node != destination:
        #         iteration_count += 1
        #         # print('Curr node:', curr_node, 'Curr instruction', curr_instruction, 'Instruction count', instruction_count)
        #         if curr_instruction == 'L':
        #             curr_node = self.node_map[curr_node].left
        #         else:
        #             curr_node = self.node_map[curr_node].right
        #
        #         instruction_count = (instruction_count + 1) % len(self.instruction_pattern)
        #         curr_instruction = self.instruction_pattern[instruction_count]
        #
        #     final_nodes.add(curr_node)

            # return iteration_count






node_map = NodeMap(raw_data)
iterations = node_map.find_node('A', 'Z')
print('Iterations:', iterations)