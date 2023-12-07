from typing import List, Dict

FILENAME = "./aoc6.txt"

with open(FILENAME) as file:
    raw_data = [line.rstrip() for line in file]


class Race:
    time: int
    distance: int

    def __init__(self, time: int, distance: int):
        self.time = time
        self.distance = distance

class Races:
    times: List[Race]

    def __init__(self, raw_data: List[str]):
        self.times = []
        parsed_times = List[int]
        parsed_distances = List[int]
        for line in raw_data:
            if len(line.split('Time:')) > 1:
                parsed_times = [int(x) for x in line.split('Time:')[1].strip().split()]

            if len(line.split('Distance:')) > 1:
                parsed_distances = [int(x) for x in line.split('Distance:')[1].strip().split()]

        for i in range(len(parsed_times)):
            self.times.append(Race(time=parsed_times[i], distance=parsed_distances[i]))

    def generate_race_times(self, race: Race) -> Dict[int, int]:
        race_times_map = {}
        for i in range(race.time+1):
            remaining_time = race.time - i
            race_times_map[i] = remaining_time * i

        return race_times_map

    def get_winning_race_times(self, race: Race) -> List[int]:
        race_times_map = self.generate_race_times(race)
        winning_race_times = {key: val for key, val in race_times_map.items() if val > race.distance}

        return winning_race_times

    def get_winning_race_time_product(self) -> int:
        product_time = 1
        for race in self.times:
            winning_times_length = len(self.get_winning_race_times(race))
            print('*', winning_times_length)
            product_time *= winning_times_length

        return product_time



races = Races(raw_data)
# print(races.get_winning_race_times(races.times[0]))
print(races.get_winning_race_time_product())