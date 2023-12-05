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

    def get_destination_number(self, start_number: int, source: str, destination: str) -> int:
        curr = source
        curr_number = start_number

        while curr != destination:
            next = self.type_graph.get(curr)
            curr_map = self.type_map[(curr, next)]
            for r in curr_map:
                destination_range_start = r[0]
                source_range_start = r[1]
                range_length = r[2]

                # print('Processing', curr, next, ', currently', curr_number)
                # print('Map', curr_map)
                if source_range_start <= curr_number < source_range_start + range_length:
                    curr_number = destination_range_start + (curr_number - source_range_start)
                    break
                # print('Next number', curr_number)

            curr = next

        return curr_number


    def populate_farm(self, raw_data: List[str]):
        curr_source_type = ''
        curr_destination_type = ''

        for line in raw_data:
            if not line:
                continue

            if line.startswith('seeds: '):
                self.seeds = [int(x) for x in line.split(':')[1].strip().split()]
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

                print('*', destination_range_start, source_range_start, range_length)

        # print(raw_data)
        # print(self.seeds)
        # print(self.type_graph)
        # print(self.type_map)


farm = Farm(raw_data)
min_seed = sys.maxsize
for seed in farm.seeds:
    destination_number = farm.get_destination_number(seed, 'seed', 'location')
    print(destination_number)
    if destination_number < min_seed:
        min_seed = destination_number

print('Min:', min_seed)


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
