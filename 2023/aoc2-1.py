from typing import List, Dict

FILENAME = "./aoc2.txt"

with open(FILENAME) as file:
    raw_data = [line.rstrip() for line in file]


class Round:
    color_map: Dict[str, int]

    def __init__(self, raw_round: str):
        self.color_map = {}
        for color_count in raw_round.split(','):
            color = color_count.strip().split(' ')[1]
            count = color_count.strip().split(' ')[0]
            self.color_map[color] = int(count)


class Game:
    rounds: List[Round]
    game_number: int

    def __init__(self, raw_game: str):
        split_game = raw_game.split(':')
        self.game_number = int(split_game[0].split(' ')[1])

        self.rounds = []
        for raw_round in split_game[1].split(';'):
            round = Round(raw_round)
            self.rounds.append(round)

    def is_max_possible(self, max_dict: Dict[str, int]) -> bool:
        '''
        :param max_dict: {'blue': 14, 'red': 12, 'green': 13}
        :return:
        '''
        for round in self.rounds:
            for k, v in round.color_map.items():
                if max_dict[k] < v:
                    return False

        return True


max_possible = 0
for line in raw_data:
    game = Game(raw_game=line)
    # print(game.game_number)
    if game.is_max_possible({'blue': 14, 'red': 12, 'green': 13}):
        max_possible += game.game_number

print(max_possible)


