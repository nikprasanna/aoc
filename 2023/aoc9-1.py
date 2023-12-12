from typing import List

FILENAME = "./aoc9.txt"

with open(FILENAME) as file:
    raw_data = [line.rstrip() for line in file]

class Sequence:
    num_sequence: List[int]

    def __init__(self, initial_sequence: str):
        self.num_sequence = [int(x) for x in initial_sequence.split()]

        print(self.num_sequence)
        print('Next number:', self.get_next_number())

    def reduce_to_zero(self) -> List[List[int]]:
        iteration_list = []
        curr_sequence = self.num_sequence
        while any([x for x in curr_sequence]):
            iteration_list.append(curr_sequence)
            new_sequence = []
            for i in range(len(curr_sequence)):
                if i+1 < len(curr_sequence):
                    difference = curr_sequence[i+1] - curr_sequence[i]
                    new_sequence.append(difference)

            print(new_sequence)
            curr_sequence = new_sequence

        return iteration_list

    def get_next_number(self):
        iteration_list = self.reduce_to_zero()
        num_append = 0
        for l in iteration_list[::-1]:
            num_append += l[-1]

        return num_append


class SequenceParser:
    sequences: List[Sequence]

    def __init__(self, raw_value: List[str]):
        self.sequences = []
        for line in raw_value:
            self.sequences.append(Sequence(line))

    def get_total_number(self) -> int:
        total_number = 0
        for sequence in self.sequences:
            total_number += sequence.get_next_number()

        return total_number


parser = SequenceParser(raw_data)
print('Total number:', parser.get_total_number())