import functools
from typing import List, Tuple

FILENAME = "./aoc12.txt"

with open(FILENAME) as file:
    raw_data = [line.rstrip() for line in file]


GLOBAL_CACHE = {}
COPIES = 5

class SpringCondition:
    layout: str
    damaged_group: List[int]

    def __init__(self, raw_line: str):
        self.layout = raw_line.split()[0]
        self.layout = '?'.join([self.layout] * COPIES)

        self.layout += '.'
        self.damaged_group = [int(x) for x in raw_line.split()[1].split(',')] * COPIES

        self.layout = self.layout.replace('.', '0')
        self.layout = self.layout.replace('#', '1')

        # print(self.layout)
        # print(self.damaged_group)
        self.total = self.recursive_walk(tuple([c for c in self.layout]), tuple(self.damaged_group))
        print(f'{self.total} - {self.layout} - {self.damaged_group}')
        # self.check_all_strings()

    @functools.lru_cache(maxsize=None)
    def recursive_walk(self, curr_str: Tuple[str], remaining_group: Tuple[int], count: int = 0) -> int:
        if not curr_str:
            if not remaining_group:
                return 1    # Valid path found at the end
            return 0    # Not a valid path

        solution_count = 0
        updated_str = list(curr_str)

        # We only want to iterate through the two potential values if curr_str[0] is ?
        # Otherwise use curr_str[0]
        potential_update_vals = ["0", "1"] if updated_str[0] == "?" else updated_str[0]
        for update_val in potential_update_vals:
            if update_val == '1':
                # Damaged, continue to extend the count group (0->1->2, etc)
                solution_count += self.recursive_walk(tuple(updated_str[1:]), remaining_group, count + 1)
            else:
                if count > 0:
                    # We were creating a group, now we are ending the group (3->0)
                    # We need to check if the count is equal to the next value in the remaining group
                    # Then we found a solution and can remove it
                    if len(remaining_group) > 0:
                        next_num = list(remaining_group)[0]
                        if count == next_num:
                            solution_count += self.recursive_walk(tuple(updated_str[1:]), tuple(list(remaining_group[1:])), 0)

                    # otherwise it's done, continue with the next number
                else:
                    # We already weren't in a group so doesn't matter, continue walking
                    solution_count += self.recursive_walk(tuple(updated_str[1:]), remaining_group, 0)

        return solution_count

    def replace_question_marks(self, num: int, zero_count: int) -> str:
        binary_str = bin(num)[2:].zfill(zero_count)
        binary_cnt = 0
        from_str = list(self.layout)

        for c in range(len(from_str)):
            if from_str[c] == '?':
                from_str[c] = binary_str[binary_cnt]
                binary_cnt += 1

        return from_str

    def get_groupings(self, grouping_layout: List[str]) -> Tuple[int]:
        str_grouping_layout = ''.join(grouping_layout)
        if str_grouping_layout in GLOBAL_CACHE:
            return GLOBAL_CACHE[str_grouping_layout]

        groupings = []
        in_damaged_group = False
        damaged_count = 0
        for c in grouping_layout:
            if c == '1':
                damaged_count += 1
                if not in_damaged_group:
                    in_damaged_group = True

            elif c == '0' and in_damaged_group:
                in_damaged_group = False
                groupings.append(damaged_count)
                damaged_count = 0

        if in_damaged_group:
            groupings.append(damaged_count)

        GLOBAL_CACHE[str_grouping_layout] = tuple(groupings)

        return tuple(groupings)


    def check_all_strings(self) -> int:
        num_question_marks = self.layout.count('?')
        print(num_question_marks)
        matches = 0
        for i in range(2**num_question_marks):
            replaced_str = self.replace_question_marks(i, num_question_marks)
            grouping = self.get_groupings(replaced_str)
            if grouping == self.damaged_group:
                matches += 1
            # print(replaced_str, '->', self.get_groupings(replaced_str))
        print('Matches', matches)

        return matches


total = 0
for line in raw_data:
    spring = SpringCondition(line)
    total += spring.total

print('Total: ', total)
