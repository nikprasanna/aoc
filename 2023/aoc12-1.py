from typing import List, Tuple

FILENAME = "./aoc12.txt"

with open(FILENAME) as file:
    raw_data = [line.rstrip() for line in file]


GLOBAL_CACHE = {}

class SpringCondition:
    layout: str
    damaged_group: List[int]

    def __init__(self, raw_line: str):
        self.layout = raw_line.split()[0]
        self.damaged_group = tuple([int(x) for x in raw_line.split()[1].split(',')])

        self.layout = self.layout.replace('.', '0')
        self.layout = self.layout.replace('#', '1')

        print(self.layout)
        print(self.damaged_group)
        # self.check_all_strings()

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
    total += spring.check_all_strings()

print('Total: ', total)
