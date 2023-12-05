import sys
from collections import defaultdict
from enum import Enum
from typing import List, Dict, Tuple

FILENAME = "./aoc5.txt"

with open(FILENAME) as file:
    raw_data = [line.rstrip() for line in file]


TYPES = [
    'seed',
    'soil',
    'fertilizer',
    'water',
    'light',
    'temperature',
    'humidity',
    'location',
]


class Farm:
    seeds: List[int]
    type_graph: Dict[str, str]
    type_map: Dict[Tuple[str, str], Dict[int, int]]

    def __init__(self, raw_data: List[str]):
        self.seeds = []
        self.type_graph = {}
        self.type_map = {}

        self.populate_farm(raw_data)

    def get_destination_number(self, start_number: int, seed_range: int, source: str, destination: str) -> int:
        curr = source
        curr_number = start_number
        curr_ranges = [(start_number, start_number+seed_range)]

        while curr != destination:
            next = self.type_graph.get(curr)
            curr_map = self.type_map[(curr, next)]
            pending_new_ranges = []

            for r in curr_map:
                destination_range_start = r[0]
                source_range_start = r[1]
                range_length = r[2]

                # print('Processing interval ', source_range_start, 'to', source_range_start+range_length)

                # print('Split range', self.split_range(range(2, 95), range(18, 75)))
                # for curr_range in curr_ranges:
                #     print(curr_range)

                # get all ranges in curr_ranges
                all_ranges = curr_ranges.copy()
                for r in all_ranges:
                    if self.is_overlap(range(r[0], r[1]), range(source_range_start, source_range_start+range_length)):
                        print('Overlap', r[0], r[1], 'to', source_range_start, source_range_start+range_length)
                        r = range(max(source_range_start, r[0]),
                                  min(source_range_start + range_length, r[1]))
                        print('R', r)
                        print('Curr', curr_ranges)
                        pending_new = []
                        for curr_range in curr_ranges:
                            new_pending = self.split_range(range(curr_range[0], curr_range[1]), r)
                            if new_pending:
                                for new in new_pending:
                                    pending_new.append((new[0], new[1]))

                        curr_ranges = pending_new
                        print('New curr', curr_ranges)

                        new_range = range(r.start-source_range_start+destination_range_start, r.stop-source_range_start+destination_range_start)
                        print('New range', new_range)
                        pending_new_ranges.append((new_range.start, new_range.stop))
                        print('Pending new', pending_new_ranges)
                        print('Curr', curr_ranges)

            curr_ranges.extend(pending_new_ranges)
            print('Iteration complete', curr_ranges)

                # For each range:
                    # If there is an overlap between start_num and range with source_range and range_length
                    # Create new range of the overlap and add destination range value to new_ranges
                    # Delete overlapping range from curr_ranges

            curr = next

        print('*', curr_ranges)
        min_seed = sys.maxsize
        for rng in curr_ranges:
            if rng[0] < min_seed:
                min_seed = rng[0]
        print('Minseed', min_seed)
        return min_seed

    def is_overlap(self, range_1, range_2):
        return range_1.start < range_2.stop and range_2.start <= range_1.stop

    def split_range(self, curr, pending_delete):
        left_result = None
        right_result = None

        if curr.start < pending_delete.start and curr.stop >= pending_delete.start:
            left_result = range(curr.start, pending_delete.start)
        if curr.stop > pending_delete.stop and curr.start <= pending_delete.stop:
            right_result = range(pending_delete.stop, curr.stop)

        results = []
        if left_result:
            results.append((left_result.start, left_result.stop))
        if right_result:
            results.append((right_result.start, right_result.stop))

        return results or ([(curr.start, curr.stop)] if curr != pending_delete else None)

    def populate_farm(self, raw_data: List[str]):
        curr_source_type = ''
        curr_destination_type = ''

        for line in raw_data:
            if not line:
                continue

            if line.startswith('seeds: '):
                all_seeds = line.split(':')[1].strip()
                curr_seed = None
                for item in all_seeds.split():
                    if not curr_seed:
                        curr_seed = int(item)
                        continue

                    seed_range = int(item)
                    self.seeds.append((curr_seed, seed_range))
                    curr_seed = None

                continue

            if len(line.split('map:')) > 1:
                source = line.split('map:')[0].split('-to-')[0].strip()
                destination = line.split('map:')[0].split('-to-')[1].strip()

                curr_source_type = source
                curr_destination_type = destination
                self.type_graph[curr_source_type] = curr_destination_type
                self.type_map[(curr_source_type, curr_destination_type)] = []
            else:
                # Populate type map
                destination_range_start = int(line.split()[0])
                source_range_start = int(line.split()[1])
                range_length = int(line.split()[2])
                self.type_map[(curr_source_type, curr_destination_type)].append((destination_range_start, source_range_start, range_length))

                # print('*', destination_range_start, source_range_start, range_length)

        # print(raw_data)
        # print(self.seeds)
        # print(self.type_graph)
        # print(self.type_map)


farm = Farm(raw_data)
print(farm.seeds)
min_seed = sys.maxsize
for seed_range in farm.seeds:
    print('New range', seed_range)
    destination_number = farm.get_destination_number(seed_range[0], seed_range[1], 'seed', 'location')
    if destination_number < min_seed:
        min_seed = destination_number

print('Min minseed:', min_seed)


# class Farm:
#     seeds: List[int]
#     seed_to_soil_map: Dict[int, int]
#     soil_to_fertilizer_map: Dict[int, int]
#     fertilizer_to_water_map: Dict[int, int]
#     water_to_light_map: Dict[int, int]
#     light_to_temperature_map: Dict[int, int]
#     temperature_to_humidity_map: Dict[int, int]
#     humidity_to_location_map: Dict[int, int]
#
#     def __init__(self):
#         self.seeds = []
#         self.seed_to_soil_map = {}
#         self.soil_to_fertilizer_map = {}
#         self.fertilizer_to_water_map = {}
#         self.water_to_light_map = {}
#         self.light_to_temperature_map = {}
#         self.temperature_to_humidity_map = {}
#         self.humidity_to_location_map = {}
#
#     def populate_seeds(self, raw_value: str):
#         pass


# [(46, 55), (82, 84), (60, 61)]
# [(98, 99), (95, 97), (86, 90), (57, 60)]

# [46, 55], [57, 61], [82, 84], [86, 90], [95, 97], [98, 99]

# [46, 61], [82, 85], [86, 90], [94, 99]

# [(46, 55), (82, 84), (60, 61)]
# [(97, 99), (94, 97), (86, 90), (56, 60)]

# [(46, 56), (82, 85), (60, 61)]
# [(97, 99), (94, 97), (86, 90), (56, 60)]
